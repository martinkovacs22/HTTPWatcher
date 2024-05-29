import subprocess
import re
from scapy.all import *
from PortClass import Port

class PortManager:
    def __init__(self):
        # Futtatja a netstat parancsot és meghívja a findstr LISTENING szűrőt
        output = subprocess.check_output("netstat -an | findstr LISTENING", shell=True)

        # Dekódolja a kimenetet a UTF-8 kódolásra
        output_text = output.decode("utf-8")

        # Kinyeri a portok számait a kimenetből
        ports = re.findall(r":(\d+)", output_text)

        # Létrehoz egy üres halmazt (set)
        self.ports = set()

        # Hozzáadja a portokat a halmazhoz
        for port in ports:
            print(port)
            self.ports.add(Port(port))

    def packet_callback(self, packet):
        if packet.haslayer(TCP):  # Csak a TCP csomagokat figyeljük meg
            tcp_layer = packet[TCP]
            if tcp_layer.dport in {int(port.portNum) for port in self.ports} or tcp_layer.sport in {int(port.portNum) for port in self.ports}:
                if packet.haslayer(Raw):
                    load = packet[Raw].load.decode('utf-8', errors='ignore')
                    if 'HTTP' in load:
                        print("HTTP Data Detected:")
                        print("Source IP:", packet[IP].src)
                        print("Destination IP:", packet[IP].dst)
                        print("Source Port:", tcp_layer.sport)
                        print("Destination Port:", tcp_layer.dport)
                        print("HTTP Data:")
                        print(load)
                        print("-" * 50)

                        # Split the HTTP data to separate headers and body
                        headers, body = self.split_headers_body(load)
                        if headers:
                            print("HTTP Headers:")
                            print(headers)
                        if body:
                            print("HTTP Body:")
                            print(body)
                        print("=" * 50)

    def split_headers_body(self, http_data):
        # HTTP adat szétválasztása fejlécekre és törzsre
        parts = http_data.split("\r\n\r\n", 1)
        headers = parts[0] if len(parts) > 0 else ""
        body = parts[1] if len(parts) > 1 else ""
        return headers, body

    def start(self):
        sniff(filter='tcp', prn=self.packet_callback, store=0)

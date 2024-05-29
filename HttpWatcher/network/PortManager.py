import subprocess
import re
import sys
from scapy.all import *
from PortClass import Port

sys.path.append('dataController')  # Ellenőrizd, hogy ez a helyes útvonal
from dataController.JsonLogger import JsonLogger
class PortManager:
    def __init__(self):


        # Példányosítsuk a JsonLogger-t a megfelelő elérési úttal
        self.json_logger = JsonLogger()
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


                        headers, body = self.split_headers_body(load)

                        # Create a dictionary to store the HTTP data
                        http_entry = {
                            "source_ip": packet[IP].src,
                            "destination_ip": packet[IP].dst,
                            "source_port": tcp_layer.sport,
                            "destination_port": tcp_layer.dport,
                            "headers": headers,
                            "body": body
                        }
                        # Log the HTTP entry using JsonLogger
                        self.json_logger.log_http_data(http_entry)
    def split_headers_body(self, http_data):
        # HTTP adat szétválasztása fejlécekre és törzsre
        parts = http_data.split("\r\n\r\n", 1)
        headers = parts[0] if len(parts) > 0 else ""
        body = parts[1] if len(parts) > 1 else ""
        return headers, body

    def start(self):
        sniff(filter='tcp', prn=self.packet_callback, store=0)

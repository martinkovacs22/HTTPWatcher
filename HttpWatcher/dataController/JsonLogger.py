import json
import os
class JsonLogger:
    def __init__(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        json_file_path = os.path.join(current_dir, 'datas.json')
        self.output_file = json_file_path
        self.http_data = []
        self.save_to_json()

    def log_http_data(self, http_entry):
        self.http_data.append(http_entry)
        self.save_to_json()

    def save_to_json(self):
        print("File ")
        print(self.output_file)
        with open(self.output_file, 'w') as f:
            json.dump(self.http_data, f, indent=4)
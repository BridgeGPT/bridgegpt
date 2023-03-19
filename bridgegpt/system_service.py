import subprocess
import json


class SystemService:
    def __init__(self):
        self.next_id = 1

    def is_valid_json(self, payload):
        try:
            obj = json.loads(payload)
            return isinstance(obj, dict) and "action" in obj and "id" in obj and "from" in obj
        except ValueError:
            return False

    def execute_command(self, command_id, command):
        try:
            # Execute the command using subprocess.check_output
            output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, executable="/bin/bash").decode().strip()
            response = {"id": command_id, "response": output, "from": "BridgeGPT"}
        except subprocess.CalledProcessError as e:
            response = {"id": command_id, "error": e.output.decode().strip(), "from": "BridgeGPT"}
        return json.dumps(response)

    def process_json(self, json_string):
        try:
            payload = json.loads(json_string)
            if "action" in payload and "id" in payload:
                command_id = payload["id"]
                command = payload["action"]
                return self.execute_command(command_id, command)
            else:
                return json.dumps({"error": "Invalid JSON payload.", "from": "BridgeGPT"})
        except json.JSONDecodeError:
            return json.dumps({"error": "Invalid JSON payload.", "from": "BridgeGPT"})

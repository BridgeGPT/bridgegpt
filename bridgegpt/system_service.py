import subprocess
import json


class SystemService:
    def __init__(self):
        self.next_id = 1

    def is_valid_json(self, payload):
        try:
            obj = json.loads(payload)
            return isinstance(obj, dict) and "action" in obj and "id" in obj
        except ValueError:
            return False

    def execute_command(self, command_id, command):
        # Check if command uses pipes
        if "|" in command:
            # Split the command by pipes
            commands = command.split("|")
            # Execute the commands using subprocess.PIPE to redirect output
            # from one command to the input of the next command
            process = None
            for cmd in commands:
                cmd = cmd.strip()
                if process is None:
                    process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE, executable="/bin/bash")
                else:
                    process = subprocess.Popen(cmd.split(), stdin=process.stdout, stdout=subprocess.PIPE, executable="/bin/bash")
            output, _ = process.communicate()
            response = {"id": command_id, "response": output.decode().strip()}
            return json.dumps(response)
        else:
            try:
                # Execute the command using subprocess.check_output
                output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, executable="/bin/bash").decode().strip()
                response = {"id": command_id, "response": output}
            except subprocess.CalledProcessError as e:
                response = {"id": command_id, "error": e.output.decode().strip()}
            return json.dumps(response)

    def process_json(self, json_string):
        try:
            payload = json.loads(json_string)
            if "action" in payload and "id" in payload:
                command_id = payload["id"]
                command = payload["action"]
                return self.execute_command(command_id, command)
            else:
                return json.dumps({"error": "Invalid JSON payload."})
        except json.JSONDecodeError:
            return json.dumps({"error": "Invalid JSON payload."})

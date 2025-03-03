from netmiko import ConnectHandler
import yaml

# Load device configuration from YAML file
def load_devices(file_path="devices.yaml"):
    with open(file_path, "r") as file:
        return yaml.safe_load(file)

# Function to connect and run commands on a device
def connect_and_execute(device, commands):
    try:
        print(f"\nConnecting to {device['host']}...")
        connection = ConnectHandler(**device)

        output = ""
        for command in commands:
            output += f"\nExecuting: {command}\n"
            output += connection.send_command(command) + "\n"

        connection.disconnect()
        return output

    except Exception as e:
        return f"Error connecting to {device['host']}: {str(e)}"

# Main execution
if __name__ == "__main__":
    devices = load_devices()  # Load devices from YAML file
    commands = ["show ip interface brief", "show version"]  # Commands to execute

    for device in devices:
        result = connect_and_execute(device, commands)
        print(result)

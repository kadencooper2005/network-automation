import os
import yaml
import logging
from datetime import datetime
from netmiko import ConnectHandler, NetmikoAuthenticationException, NetmikoTimeoutException

# Setup logging
log_filename = f"logs/network_automation_{datetime.now().strftime('%Y-%m-%d')}.log"
os.makedirs("logs", exist_ok=True)
logging.basicConfig(filename=log_filename, level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Load device configurations
def load_yaml(file_path):
    with open(file_path, "r") as file:
        return yaml.safe_load(file)

# Backup configurations
def save_backup(device_name, config):
    os.makedirs("backup", exist_ok=True)
    filename = f"backup/{device_name}_config_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    with open(filename, "w") as file:
        file.write(config)
    logging.info(f"Backup saved: {filename}")

# Connect to device and execute commands
def connect_and_execute(device, show_commands, config_commands):
    try:
        logging.info(f"Connecting to {device['host']} ({device['device_type']})")
        print(f"\n[+] Connecting to {device['host']} ({device['device_type']})...")

        connection = ConnectHandler(**device)

        # Retrieve device configuration
        print("[+] Running show commands...")
        output = "\n".join([connection.send_command(cmd) for cmd in show_commands])
        save_backup(device['host'], output)

        # Apply bulk configuration changes
        print("[+] Applying configuration changes...")
        if config_commands:
            connection.send_config_set(config_commands)
            logging.info(f"Configuration changes applied to {device['host']}")

        connection.disconnect()
        logging.info(f"Disconnected from {device['host']}")
        print(f"[+] Disconnected from {device['host']}\n")

    except (NetmikoAuthenticationException, NetmikoTimeoutException) as e:
        logging.error(f"Connection failed for {device['host']}: {str(e)}")
        print(f"[-] Error connecting to {device['host']}")

# Main execution
if __name__ == "__main__":
    devices = load_yaml("devices.yaml")
    commands = load_yaml("commands.yaml")

    for device in devices:
        connect_and_execute(device, commands["show_commands"], commands["config_commands"])

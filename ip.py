import subprocess
import re
import random

class IPChangerCLI:
    def __init__(self):
        self.eth_interface_name = self.detect_eth_interface_name()
        self.current_ip = self.get_current_ip()

    def detect_eth_interface_name(self):
        # Run ifconfig command to get network interface names and IP addresses
        output = subprocess.check_output(["ifconfig"]).decode()

        # Use regular expression to extract Ethernet interface name
        eth_regex = r"en\w+"
        eth_interface_name = re.search(eth_regex, output)

        # Return Ethernet interface name
        return eth_interface_name.group()

    def get_current_ip(self):
        # Run ifconfig command to get network interface names and IP addresses
        output = subprocess.check_output(["ifconfig"]).decode()

        # Use regular expression to extract current IP address
        ip_regex = r"inet \d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}"
        ip_address = re.search(ip_regex, output)

        # Return current IP address
        return ip_address.group().split()[1]

    def change_ip(self):
        # Generate random IP address
        new_ip = "192.168." + str(random.randint(1, 255)) + "." + str(random.randint(1, 255))

        # Bring Ethernet interface down
        subprocess.run(["ifconfig", self.eth_interface_name, "down"])

        # Change IP address
        subprocess.run(["ifconfig", self.eth_interface_name, new_ip])

        # Bring Ethernet interface back up
        subprocess.run(["ifconfig", self.eth_interface_name, "up"])

        # Update current IP address
        self.current_ip = self.get_current_ip()

    def print_current_ip(self):
        print("Current IP address:", self.current_ip)

    def run(self):
        try:
            print("Detected Ethernet interface:", self.eth_interface_name)
            self.print_current_ip()
            self.change_ip()
            self.print_current_ip()
        except Exception as e:
            print("Error:", e)

if __name__ == "__main__":
    ip_changer = IPChangerCLI()
    ip_changer.run()


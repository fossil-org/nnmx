import subprocess
import platform

def list_known_wifis():
    """Lists all known (saved) Wi-Fi networks."""
    if platform.system() == "Windows":
        result = subprocess.run(["netsh", "wlan", "show", "profiles"], capture_output=True, text=True)
        return [line.split(':')[1].strip() for line in result.stdout.split('\n') if "All User Profile" in line]
    elif platform.system() == "Linux":
        result = subprocess.run(["nmcli", "connection", "show"], capture_output=True, text=True)
        return [line.split()[0] for line in result.stdout.split('\n')[1:] if line]
    else:
        raise NotImplementedError("Unsupported OS")

def scan_wifis():
    """Scans and lists available Wi-Fi networks."""
    if platform.system() == "Windows":
        subprocess.run(["netsh", "wlan", "refresh"], capture_output=True, text=True)  # Refresh Wi-Fi list
        result = subprocess.run(["netsh", "wlan", "show", "networks"], capture_output=True, text=True)
        return [line.split(':')[1].strip() for line in result.stdout.split('\n') if "SSID" in line]
    elif platform.system() == "Linux":
        result = subprocess.run(["nmcli", "-t", "-f", "ssid", "dev", "wifi"], capture_output=True, text=True)
        ssids = result.stdout.split("\n")
        return list(filter(None, ssids))  # Remove empty lines
    else:
        raise NotImplementedError("Unsupported OS")

def connect_to_wifi(ssid, password):
    """Connects to a Wi-Fi network on Windows or Linux."""
    system = platform.system()

    if system == "Windows":
        command = f'netsh wlan connect name="{ssid}" ssid="{ssid}"'
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if "completed successfully" in result.stdout:
            print(f"Connected to {ssid} successfully.")
            return True
        else:
            print(f"Failed to connect to {ssid}.\nError: {result.stdout}")
            return False

    elif system == "Linux":
        # Check if the network is already saved
        check_command = f"nmcli connection show '{ssid}'"
        check_result = subprocess.run(check_command, shell=True, capture_output=True, text=True)

        if "no such connection" in check_result.stderr.lower():
            print(f"Network {ssid} is not saved. Adding it now...")
            add_command = f"nmcli dev wifi connect '{ssid}' password '{password}'"
        else:
            print(f"Connecting to saved network {ssid}...")
            add_command = f"nmcli connection up '{ssid}'"

        result = subprocess.run(add_command, shell=True, capture_output=True, text=True)

        if "successfully activated" in result.stdout.lower():
            print(f"Connected to {ssid} successfully.")
            return True
        else:
            print(f"Failed to connect to {ssid}.\nError: {result.stderr}")
            return False

    else:
        print("Unsupported OS.")
        return False

def disconnect_wifi():
    """Disconnects from the current Wi-Fi network."""
    if platform.system() == "Windows":
        subprocess.run(["netsh", "wlan", "disconnect"], capture_output=True, text=True)
    elif platform.system() == "Linux":
        subprocess.run(["nmcli", "radio", "wifi", "off"], capture_output=True, text=True)
    else:
        raise NotImplementedError("Unsupported OS")

def check_wifi_password(ssid):
    """Checks the saved password of a known Wi-Fi network (Windows only)."""
    if platform.system() == "Windows":
        result = subprocess.run(["netsh", "wlan", "show", "profile", ssid, "key=clear"], capture_output=True, text=True)
        for line in result.stdout.split('\n'):
            if "Key Content" in line:
                return line.split(':')[1].strip()
        return "Password not found or not stored."
    elif platform.system() == "Linux":
        try:
            password_cmd = f"nmcli -s -g 802-11-wireless-security.psk connection show '{ssid}'"
            password = subprocess.check_output(password_cmd, shell=True, text=True).strip()
            return password
        except subprocess.CalledProcessError:
            print(f"Error: No saved network found for SSID '{ssid}'.")
    else:
        raise NotImplementedError("Unsupported OS")

if __name__ == "__main__":
    print("Known Wi-Fi networks:", list_known_wifis())
    print("Available Wi-Fi networks:", scan_wifis())
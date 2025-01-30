import requests
import json
import os  # Import the os module for directory handling


def generatewireguardconf(address: str, privkey: str, dns: str, pubkey: str, allowedip: str, endpoint: str, output: str):
    # Format the WireGuard configuration file content
    file_content = f"""[Interface]
Address = {address}
PrivateKey = {privkey}
DNS = {dns}

[Peer]
PublicKey = {pubkey}
AllowedIPs = {allowedip}
Endpoint = {endpoint}
"""
    
    # Extract the hostname part without the port and domain
    hostname_without_port = endpoint.split(":")[0]
    hostname_part = hostname_without_port.split(".")[0]
    
    # Create the output directory if it doesn't exist
    os.makedirs(output, exist_ok=True)
    
    # Generate the full file path
    filename = f"{hostname_part}nordvpnwireguard.conf"
    full_path = os.path.join(output, filename)
    
    # Write the configuration to the file
    with open(full_path, "w") as f:
        f.write(file_content)


def checktechnology(technologies):
    for t in technologies:
        if t["identifier"] == "wireguard_udp":
            return t["metadata"][0]["value"]
    return False


def downloadnord(url: str, privkey: str, allowedip: str, addr: str, outputdir: str):
    response = requests.get(url)
    data = json.loads(response.content.decode("utf-8"))
    
    for server in data:
        wg_public_key = checktechnology(server["technologies"])
        if not wg_public_key:
            continue  # Skip servers without WireGuard support
        
        # Generate configuration for this server
        generatewireguardconf(
            addr, privkey, server["station"],
            wg_public_key, allowedip,
            f"{server['hostname']}:51820",  # Endpoint with port
            outputdir
        )


if __name__ == '__main__':
    with open('config.json') as config_file:
        config = json.load(config_file)
        downloadnord(
            config["url"] + config["limit"],
            config["privatekey"],
            config["allowedip"],
            config["adress"],
            config["outputdir"]
        )

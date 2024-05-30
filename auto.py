import socket
import json
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm

def check_port(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)
    result = sock.connect_ex((host, port))
    sock.close()
    return port if result == 0 else None

def port_scan(host, start_port, end_port):
    open_ports = []
    total_ports = end_port - start_port + 1

    with ThreadPoolExecutor(max_workers=100) as executor:
        futures = [executor.submit(check_port, host, port) for port in range(start_port, end_port + 1)]
        for future in tqdm(futures, desc="Scanning ports", unit="port"):
            port = future.result()
            if port:
                open_ports.append(port)
    return open_ports

if __name__ == "__main__":

    with open('setting.json', 'r') as file:
        data = json.load(file)

    target_ip = data['scan']['targetIp'] # Replace with the target host
    print(f'The target IP is: {target_ip}')

    start_port = data['scan']['startPort']
    end_port = data['scan']['endPort']

    open_ports = port_scan(target_ip, start_port, end_port)
    if open_ports:
        print(f"Open ports: {open_ports}")
    else:
        print("No open ports found.")
import requests
import ssl
import socket
import json

def check_ssl(url):
    try:
        response = requests.get(url, verify=False)
        
        if response.status_code == 200:
            hostname = url.split("//")[-1].split("/")[0]
            context = ssl.create_default_context()
            try:
                with socket.create_connection((hostname, 443)) as sock:
                    with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                        cert = ssock.getpeercert()
                        tls_version = ssock.version()
                        cipher_suite = ssock.cipher()

                if tls_version < 'TLSv1.2':
                    return "취약 : The site is using an insecure TLS version."

                with open('vuln_ssl_cipher.txt', 'r') as file:
                    vuln_ciphers = file.read().splitlines()
                
                if cipher_suite[0] in vuln_ciphers:
                    return f"취약 : The site is using a vulnerable cipher suite: {cipher_suite[0]}"

                return (f"The site uses a valid SSL/TLS certificate. "
                        f"Certificate info: {cert}, "
                        f"TLS version: {tls_version}, "
                        f"Cipher suite: {cipher_suite}")
            except ConnectionRefusedError:
                return "취약 : The target computer is not using port 443. SSL/TLS certificate is not present."
            except socket.gaierror:
                return "Failed to resolve hostname. Please check the URL and your network connection."
            except ssl.SSLCertVerificationError as e:
                if "CERTIFICATE_VERIFY_FAILED" in str(e):
                    if "certificate has expired" in str(e):
                        return "취약 : SSL certificate has expired"
                    return f"취약 : SSL certificate verification failed : {e}"
            return f"SSL certificate verification error: {e}"
        else:
            return f"Status code: {response.status_code}"
    except requests.exceptions.SSLError as e:
        return f"SSL certificate error: {e}"
    except requests.exceptions.RequestException as e:
        return f"An error occurred: {e}"
    
if __name__ == "__main__":
    with open('setting.json', 'r') as file:
        data = json.load(file)

    target_url = data['check_ssl']['targetUrl'] # Replace with the target host
    print(f'The targetUrl is: {target_url}')

    result = check_ssl(target_url)
    print(result)
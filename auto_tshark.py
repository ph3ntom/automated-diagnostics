import subprocess
import json

def capture_packets(interface, packet_count, output_file):
    """
    tshark를 사용하여 패킷을 캡처하고 파일에 저장하는 함수
    """
    command = ['tshark', '-i', interface, '-c', str(packet_count), '-w', output_file]
    try:
        subprocess.run(command, check=True)
        print(f"Captured {packet_count} packets on {interface} and saved to {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while capturing packets: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def apply_filter(input_file, filter_expression, output_file):
    """
    tshark를 사용하여 필터링된 패킷을 새로운 파일에 저장하는 함수
    """
    command = ['tshark', '-r', input_file, '-Y', filter_expression, '-w', output_file]
    subprocess.run(command, check=True)
    print(f"Applied filter '{filter_expression}' on {input_file} and saved to {output_file}")

def extract_info_from_filtered_file(filtered_file, fields):
    """
    필터링된 파일에서 특정 필드를 추출하는 함수
    """
    command = ['tshark', '-r', filtered_file, '-T', 'fields']
    for field in fields:
        command.extend(['-e', field])
    result = subprocess.run(command, capture_output=True, text=True, check=True)
    print(f"Extracted fields {fields} from {filtered_file}")
    return result.stdout

def print_original_packets(input_file):
    """
    원본 패킷 데이터를 텍스트 형식으로 출력하는 함수
    """
    command = ['tshark', '-r', input_file]
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True, encoding='utf-8', errors='ignore')
        print(f"Original packets from {input_file}:\n{result.stdout}")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while reading packets: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":

    with open('setting.json', 'r') as file:
            data = json.load(file)
    interface = data['tshark']['interface']
    size = data['tshark']['size']
    save = f"./information_exposure/{data['service_name']}_tshark.pcap"
    # 예제 사용법
    capture_packets(interface , size, save)
    #filtered_file = f"./information_exposure/{data['service_name']}_f_tshark.pcap"
    # apply_filter(save, 'tcp.port == 80', filtered_file)
    # fields = ['frame.number', 'ip.src', 'ip.dst', 'http.request', 'http.response.code', 'http.content_type']
    # info = extract_info_from_filtered_file(filtered_file, fields)
    # print(info)

    print_original_packets(save)

 
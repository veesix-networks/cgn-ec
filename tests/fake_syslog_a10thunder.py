import random
import socket
from time import sleep


# Function to generate a random IP address
def random_ip():
    return ".".join(str(random.randint(0, 255)) for _ in range(4))


# Function to generate a random port number
def random_port():
    return random.randint(1024, 65535)  # Exclude well-known ports


# Function to generate a random syslog message
def generate_syslog_message_session_mapping():
    # A VRF 0 6 INT 10.0.0.1:57938 EXT 100.64.0.1:28475 DST 185.165.123.206:443 DIR OUT
    event = random.choice(["C", "D", "U"])  # Event can be "A" or "D"
    protocol = random.choice(["TCP", "UDP"])  # TCP (6) or UDP (17)
    src_ip = "100.64.23.122"
    src_port = random_port()
    x_ip = "194.15.97.34"  # Example external IP (fixed for now)
    x_port = random_port()
    dst_ip = random_ip()
    dst_port = 443

    # Construct the syslog message
    syslog_message = (
        f"test NAT-{protocol}-{event}: {src_ip}:{src_port}<->"
        f"{dst_ip}:{dst_port},{x_ip}:{x_port}<-->{dst_ip}:{dst_port}"
    )
    return syslog_message


def generate_syslog_message_port_mapping():
    # A VRF 0 6 INT 10.0.0.1:57938 EXT 100.64.0.1:28475
    event = random.choice(["C", "D", "U"])  # Event can be "A" or "D"
    protocol = random.choice(["TCP", "UDP"])  # TCP (6) or UDP (17)
    src_ip = "100.64.23.122"
    src_port = random_port()
    x_ip = "194.15.97.34"  # Example external IP (fixed for now)
    x_port = random_port()

    # Construct the syslog message
    syslog_message = f"test NAT-{protocol}-{event}: {src_ip}:{src_port}<-->{x_ip}:{x_port} to 8.8.8.8:53"
    return syslog_message


# Function to send a syslog message to a server via UDP
def send_syslog_message(message, syslog_server_ip, syslog_server_port=514):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(message.encode(), (syslog_server_ip, syslog_server_port))
    sock.close()


# Main function to generate and send syslog messages
def main():
    syslog_server_ip = "localhost"  # Replace with the IP of your syslog server
    syslog_server_port = 1514  # Default UDP port for syslog

    for _ in range(10):  # Generate and send 10 random syslog messages
        # message1 = generate_syslog_message_address_mapping()
        message2 = generate_syslog_message_session_mapping()
        message3 = generate_syslog_message_port_mapping()
        # message4 = generate_syslog_message_port_block_mapping()

        # messages = [message1, message2, message3, message4]
        messages = [message2, message3]
        for message in messages:
            print(f"Sending messages: {message}")
            send_syslog_message(message, syslog_server_ip, syslog_server_port)
            sleep(0.1)


if __name__ == "__main__":
    main()

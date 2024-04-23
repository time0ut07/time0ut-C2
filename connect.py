import socket

def send_heartbeat(client_socket):
    try:
        client_socket.send(b"Heartbeat")
    except socket.error:
        print("Error sending heartbeat")
        return False
    return True

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.connect(("127.0.0.1", 1337))
    print("Successfully connected to C2")
except socket.error:
    print("Something went wrong")

while True:
    try:
        data = s.recv(4096)
        if not data:
            print("Connection closed by the server.")
            break

        if data == b"Request_Heartbeat":
            send_heartbeat(s)
            
    except socket.error as e:
        print(f"Error receiving data: {e}")
        break

s.close()

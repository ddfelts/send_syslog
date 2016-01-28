import os
import socket
import argparse

version = 0.5

p = argparse.ArgumentParser(__file__,
                                 description="A syslog message generator")

p.add_argument("--server",
                    "-s",
                    required=True,
                    help="Syslog server or Receiver IP address")

p.add_argument("--port",
                    "-p",
                    type=int,
                    default=514,
                    help="Destination syslog port")

p.add_argument("--log",
                    "-l",
                    required=True,
                    help="Log filename or directory of files. May be compressed.")


def file_or_dir():
    if os.path.isdir(args.log):
        filelist = os.listdir(args.log)
        return (filelist)
        
        
def send_logs():
    count = 0
    
    with open(args.log, 'r') as openlog:
        for log in openlog:
            dlog = log.encode()
            s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.connect((args.server,args.port))
            s.sendall(dlog)
            count += 1
            print (count)
            s.shutdown(socket.SHUT_RDWR)
            s.close()
            
if __name__ == "__main__":
    args = p.parse_args()
    print("Main Function")
    file_or_dir();
    send_logs();
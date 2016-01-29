import os
import socket
import zipfile
import argparse
import glob

version = 0.7

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

def send_logs():
    tlogcount = 0 
    for logfile in glob.glob(args.log):
        s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.connect((args.server,args.port))
    
        with open(logfile, 'r') as openlog:
            logcount = 0
            for log in openlog:
                dlog = log.encode()
                s.sendall(dlog)
                logcount += 1
                tlogcount += 1
            s.close()
            print ("File: ", logfile, "Logs Sent: ", logcount)
    print ("Total Logs Sent: ", tlogcount)
            
if __name__ == "__main__":
    args = p.parse_args()
    send_logs();
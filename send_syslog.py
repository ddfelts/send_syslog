#!/usr/bin/env python

import os
import socket
import zipfile
import gzip
import argparse
import datetime
import tempfile
import shutil
import errno
from glob import glob

version = 1.0

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

p.add_argument("--file",
                    "-f",
                    required=True,
                    help="Name(s) of log files. (log.txt, *.log, log*.zip")


def open_socket(server, port):
    '''Open TCP socket using supplied server IP and port. Returns socket.'''
    s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        s.connect((server,port))
    except socket.error as e:
        if s:
            s.close()
        print ("Could not open socket to", server, port)
        print (e)
    return s
 
def check_zip(file):
    '''If zip, unzips file into temp directory. Returns path.'''
    if zipfile.is_zipfile(file):
        path = os.path.dirname(os.path.realpath(file))
        tmpdir = tempfile.mkdtemp(dir=path)
        with zipfile.ZipFile(file, 'r') as zfile:
            filecount = len(zfile.infolist())
            if filecount > 1:
                print ("Only one file per zip is supported.\nSkipping:", file)
                try:
                    shutil.rmtree(tmpdir)
                except:
                    print ("Error: Temp directory not deleted:", tmpdir)
                return 
            else:
                tmpfile = ''.join(zfile.namelist())
                zfile.extractall(tmpdir)
                logfile = os.path.join(tmpdir, tmpfile)
                return logfile
    else:
        return file

def send_log(logfile):
    '''Iterates lines from log file to an open socket. Returns lines sent'''
    with open(logfile, 'r') as openlog:
        logcount = 0
        for log in openlog:
            s.sendall(log.encode())
            logcount += 1
    return logcount

            
if __name__ == "__main__":
    args = p.parse_args()
    s = open_socket(args.server, args.port)
    total = 0
    for file in glob(args.file): 
        logfile = check_zip(file)
        if logfile:
            logcount = send_log(logfile)
            if (os.path.dirname(logfile)):
                deldir = (os.path.dirname(logfile))
                try:
                    shutil.rmtree(deldir)
                except:
                    print ("Error: Temp directory not deleted:", tmpdir)
            print ("Sent", logcount, "logs from", logfile)
            total += logcount
    s.close
    print ("Sent", total, "logs total.")
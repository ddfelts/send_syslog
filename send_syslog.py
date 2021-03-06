#!/usr/bin/env python
"""

Send lines from text files to destination via syslog

"""

import argparse
import gzip
import logging
import os
import socket
import sys
from glob import glob
from binaryornot.check import is_binary

__author__ = "Andy Walden"
__version__ = "Beta4"
__status__ = "Development"


class Args:
 
    def __init__(self, args):
        self.log_levels = ["quiet", "error", "warning", "info", "debug"]
        self.formatter_class = argparse.RawDescriptionHelpFormatter
           
        self.parser = argparse.ArgumentParser(formatter_class=self.formatter_class, 
                                              description="Send files to syslog")
        self.args = args
        
        
        self.parser.add_argument("-s", "--server",
                                 required=True,
                                 help="Syslog server or Receiver IP address")
 
        self.parser.add_argument("-f", "--file",
                                 required=True,
                                 help="Logs to send. Can be files (messages, \
                                 *.log) or directory with logs. Warning: \
                                 directory will be recursed and send every \
                                 text file found.")
 
        self.parser.add_argument("-p", "--port", 
                                 type=int, 
                                 default=514,
                                 help="Destination syslog port. Default: 514")

        self.parser.add_argument("-z", "--zip", 
                                 action="store_true",
                                 help="Send logs in gz files. \
                                 Default: disabled")

        self.parser.add_argument("-v", "--version", 
                                 action="version",
                                 version="%(prog)s {}".format(__version__))

        self.parser.add_argument("-l", "--level", 
                                 default="info", dest="level",
                                 choices=self.log_levels,
                                 help="Logging output level. Default: info")

        
        self.pargs = self.parser.parse_args()
          
 
    def get_args(self):
        return self.pargs
 

def config_logging(level):
    """Configure logging parameters"""

    # No logs are set to critical so it effectively disables logging.
    if level == "quiet":
        level = "CRITICAL"

    logging.basicConfig(level=level.upper(),
                        format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                        datefmt='%m-%d %H:%M',
                        filename='send_syslog.log',
                        filemode='w')

    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(levelname)-8s %(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)


def open_socket(server, port):
    """Open TCP socket using supplied server IP and port. Returns socket or
       None on failure"""

    logging.debug("Function: open_socket: %s: %s", server, port)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        sock.connect((server, port))

    except:
        raise

    return sock


def walk_dir(dirname):
    """Yields all file objects recursively"""

    logging.debug("Function: walk_dir: %s", dirname)
    for root, dirs, files in os.walk(dirname):
        logging.debug("Walking path: %s%s%s", root, dirs, files)
        for filename in files:
            logging.debug("**Returning new file**: %s", filename)
            yield os.path.join(root, filename)


def send_to_syslog(filename, sock, zflag):
    """Wraps individual syslog functions. Returns linecount"""

    linecount = 0
    logging.debug("Function: send_to_syslog %s, send_zip=%s", filename, zflag)


    if os.stat(filename).st_size > 0:
        if is_binary(filename):
            if zflag:
                if filename.lower().endswith(".zip"):
                    linecount = 0
                    logging.info("Skipped zip: %s",
                                 os.path.basename(filename))

                elif filename.lower().endswith(".gz"):
                    logging.info("Sending file: %s",
                                 os.path.basename(filename))
                    linecount = send_gzip_to_syslog(filename, sock)
                    logging.info("Sent    file: %s: Lines: %s",
                                 os.path.basename(filename), linecount)

            else:
                linecount = 0
                logging.debug("Skipped binary file: %s", filename)
        else:
            logging.info("Sending file: %s", os.path.basename(filename))
            linecount = send_text_to_syslog(filename, sock)
            logging.info("Sent    file: %s: Lines: %s",
                         os.path.basename(filename), linecount)
    else:
        linecount = 0
        logging.info("Skipped empty file: %s", os.path.basename(filename))

    return linecount


def send_gzip_to_syslog(filename, sock):
    """Iterates lines from file to open socket object. Returns lines sent"""

    linecount = 0
    logging.debug("Function: send_gzip_to_syslog: %s", filename)
    with gzip.open(filename, 'rb') as zopenfile:
        for line in zopenfile:
            sock.sendall(line)
            linecount += 1

    return linecount


def send_text_to_syslog(filename, sock):
    """Iterates lines from file to open socket object. Returns lines sent"""

    linecount = 0
    logging.debug("Function: send_text_to_syslog: %s", filename)
    try:
        with open(filename, 'rt') as openfile:
            for line in openfile:
                try:
                    sock.sendall(line.encode())
                    linecount += 1
                except OSError:
                    logging.exception("Server failed to respond. Please \
                                 check connectivity.")
                    sys.exit()
    except UnicodeDecodeError:
        logging.error("Aborting: %s: Invalid characters at line %s",
                      filename, linecount)
    except:
        raise

    return linecount


def main():
    """Main function"""

    linecount = 0
    linetotal = 0
    
    args = Args(sys.argv)
    pargs = args.get_args()
    
    config_logging(pargs.level)
    logging.debug("****************%s INITIALIZED******************", __name__)

    # Optimistically opening socket
    sock = open_socket(pargs.server, pargs.port)
    if not sock:
        logging.error("Could not connect to server.\n"
                      "Server: %s:%s", args.server, args.port)
        sys.exit()
    else:
        logging.debug("Socket established to %s on port %s", 
                      pargs.server, pargs.port)
    
    argnames = glob(pargs.file)
    if not argnames:
        logging.info("Unable to access given directory or file: %s", pargs.file)
        sys.exit()
     
    # Process files
    for argname in argnames:
        name = os.path.realpath(argname)
                        
        if os.path.isdir(name):
            logging.debug("Searching directory %s", name)
            for filename in walk_dir(name):
                logging.debug("Found file: %s, checking", filename)
                linecount = send_to_syslog(filename, sock, pargs.zip)
                linetotal += linecount
        else:
            linecount = send_to_syslog(name, sock, pargs.zip)
            linetotal += linecount

        logging.info("Total lines Sent: %s", linetotal)
        logging.shutdown()

if __name__ == "__main__":
    try:
        main()
    
    except KeyboardInterrupt:
        logging.error("Halting: Control-C Detected")
        sys.exit()

<snippet>
  <content>
 ## Send_Syslog

send_syslog is a script to send (ideally) RFC5424 formatted logs to a syslog server or SIEM. The deceptively simple premise can assist with a number of use cases:

 * Manual log transport - common on "specialized" networks
 * Testing parsers, rules
 * Forensic repopulation - Tune and re-import

## Installation

Linux / Mac / from script requires binaryornot module.

pip install binaryornot

Pre-compiled with pyinstaller for Windows.

## Usage

Usage:

  -s SERVER,    --server SERVER 	Syslog server or Receiver IP address

  -f FILE,      --file FILE         Logs to send. Can be files (messages, *.log) or
                                    directory with logs. Warning: directory will be
                                    recursed and send every text file found.

optional arguments:
  -h,		--help		show this help message and exit

  -p PORT,	--port PORT Destination syslog port. Default: 514

  -z,		--zip		Send logs in gz files. Default: disabled

  -v,		--version   Show version number and exit

  -l, 		--level		Logging output level. Default: info





## Examples:

Mininum:

send_syslog -s x.x.x.x -f messages.log

Wildcards:

send_syslog -s x.x.x.x -f *.log

Directory - automatically recurses:

send_syslog -s x.x.x.x -f /var/log

Process gzip:

send_syslog -s x.x.x.x -f log.gz -z

Directory + Process all gzip's:

send_syslog -s x.x.x.x -f /var/log -z

Output:

Default is info level.


- Debugging:

  send_syslog -s x.x.x.x -f /var/log -z -l debug

- No output:

  send_syslog -s x.x.x.x -f /var/log -z -l quiet


## Credits

Andy Walden -
Andy.Walden @ intel dot com

## License

MIT License

></content>
  <tabTrigger>readme</tabTrigger>
</snippet>

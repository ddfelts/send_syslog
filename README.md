<snippet>
  <content>
## Send_Syslog

send_syslog is a script to send (ideally) RFC5424 formatted logs to a syslog server or SIEM. The deceptively simple premise can assist with a number of use cases:

 * Manual log transport - common on "specialized" networks
 * Testing parsers, rules
 * Forensic repopulation - Tune and re-import

## Installation

Tested with Python 2.7 and 3.4.

Requires binaryornot module for script.

pip install binaryornot

Pre-compiled with pyinstaller for Windows - nothing required but the .exe

## Usage

```Usage:

  -s SERVER,    --server SERVER 	Syslog server or Receiver IP address

  -f FILE,      --file FILE         Logs to send. Can be files (messages, *.log) or
                                    directory with logs. Warning: directory will be
                                    recursed and send every text file found.

optional arguments:
  -h,		--help		show this help message and exit

  -p PORT,	--port PORT Destination syslog port. Default: 514

  -z,		--zip		Send logs in gz files. Default: disabled

  -v,		--version   Show version number and exit

  -l, 		--level		Logging output level. Default: info```

```



## Examples:

Mininum:

```send_syslog -s x.x.x.x -f messages.log```

Wildcards:

```send_syslog -s x.x.x.x -f *.log```

Directory - automatically recurses:

```send_syslog -s x.x.x.x -f /var/log```

Process gzip:

```send_syslog -s x.x.x.x -f log.gz -z```

Directory + Process all gzip's:

```send_syslog -s x.x.x.x -f /var/log -z```

Output:

Default is info level.


- Debugging:

  ```send_syslog -s x.x.x.x -f /var/log -z -l debug```

- No output:

  ```send_syslog -s x.x.x.x -f /var/log -z -l quiet```


## Caveats

There isn't any verification that a "log" is actually a log. This will send
most any text file including your source code respository and your collection
of chewbacca ASCII art so do take care where you point it. /var/log is generally
safe.

## License

The MIT License (MIT)

Copyright (c) [year] [fullname]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

></content>

</snippet>

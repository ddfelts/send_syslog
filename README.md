# send_syslog

send_syslog is a dead simple Python script to send a RFC5424 formatted logs
to a syslog server or SIEM. It can read in a file or group of files (wildcards 
supported) and handle zipped files. 

* Uses TCP
* No rate limiting
* No log formatting or manipulation

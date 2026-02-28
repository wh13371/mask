# mask.py

## A log file hash/mask utility

Parses log files/directories/STDIN, redacts (hash/mask) specific content to output files, based on regexes in a regex.txt file.

## Example input Log File (i.e "log.log")
    
    2025-11-19 08:11:46 - INFO - Started HTTP server
    2025-11-19 08:15:07 - DEBUG - User:'clint.eastwood' successfully logged-in from IP:192.168.1.22
    2025-11-19 08:15:07 - DEBUG - User:'clint.eastwood' DNIS=9999 ANI=1234
    2025-11-19 08:22:58 - WARNING - Disk usage exceeded 90%

## Example Regex input file (default="regex.txt")

    .*User:'(.*)'
    .*DNIS=(.*).ANI=(.*)
    .*IP:(.*)

## Example output file ("log.log_2026-02-28 12:00:39.309499.OUT")

    2025-11-19 08:11:46 - INFO - Started HTTP server
    2025-11-19 08:15:07 - DEBUG - User:'55502a99bc7e6869e2e20f2cfe6f2df7' successfully logged-in from IP:46888c135058fbc76e318d665a8d030d
    2025-11-19 08:15:07 - DEBUG - User:'55502a99bc7e6869e2e20f2cfe6f2df7' DNIS=b97fad7d9df377cd722796cb8892bb2e ANI=f346a8dd3905996459ddd8edec7de68d
    2025-11-19 08:22:58 - WARNING - Disk usage exceeded 90%


## Usage examples:
  
Process all files in the /home/fizz/tmp directory.
  
By default, use the "regex.txt" for pattern matching.

Output files will be created in the same directory as the input files.
  
    ./mask.py /home/fizz/tmp/*

Process all files in the /home/fizz/tmp directory.
  
By default, use the "regex.txt" for pattern matching.

Output files will be created in the /home/fizz/out directory.

    ./mask.py /home/fizz/tmp/* --output /home/fizz/out/

Process all '.log' files in the /home/fizz/tmp/ directory.
  
Use "myregexes.txt" for pattern matching.

Output files will be created in the same directory as the input files.

    ./mask.py /home/fizz/tmp/*.log -r myregexes.txt

Set the output "map file" to "mymap.txt"

    ./mask.py /home/fizz/tmp/*.log /home/fizz/tmp/*.log --mapfile mymap.txt -V

Set the output file(s) suffix to ".HASH"

    ./mask.py /home/fizz/tmp/*.log /home/fizz/tmp/*.txt -s .HASH

Process 2 files, 'sip.log' and 'log.log' from the /tmp directory and all files in the 'logs' directory with max "verbosity=3" mode using -VVV

    ./mask.py /home/fizz/tmp/log.log /home/fizz/tmp/sip.log /home/fizz/logs/* -VVV

Get utility version

    ./mask.py -v

Quiet output mode with "-q"

    ./mask.py /home/fizz/tmp/*.log /home/fizz/tmp/*.log -q

Process 'log.txt' based on STDIN

    cat log.txt | ./mask.py

    cat log.txt | ./mask.py -V

    cat log.txt | ./mask.py -VVV -o /home/fizz/out/

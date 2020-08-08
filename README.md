# mask.py

## A log file hash/mask utility

Parses log file(s) as an [input], hash(s) or mask(s) specific content, based on Regex's in an input [regex file], to [output] file(s).

# Example Input Log File (i.e "log.log")
    
    some text to ignore
    ANI		'9876'
    ignore this also
            DNIS	'9702'
    Target 'fizz' @ '10.20.30.40' - keep this
    middle
    some text to ignore
        ANI		'9876'
    ignore this also
            DNIS	'9702'
    Target 'flo' @ '40.30.20.10' - keep this
    end
    

# Regex Input File (default="regex.txt")

    \tANI\t\t'(\d+)'
    \t\tDNIS\t'(\d+)'
    Target '(.*)' @ '(\S+)'


# Hash Example Output Log File ("log.log.#.2020-08-02 17:00:39.309499")

    some text to ignore
        ANI		'ac807d6248ed4a68197c817e8fd1f4a5'
    ignore this also
            DNIS	'ee0d294a65beacb211878a54dd6d3e3f'
    Target 'f458fa957e0d3c2dd9b146253d35769a' @ '219b3ba5488949170a89560ad1824293' - keep this
    middle
    some text to ignore
        ANI		'ac807d6248ed4a68197c817e8fd1f4a5'
    ignore this also
            DNIS	'ee0d294a65beacb211878a54dd6d3e3f'
    Target '88e27b75d1e505030453fdfb07049600' @ 'b4cf215a6c91fdafe45f8e30e2e75e84' - keep this
    end

# Mask Example Output Log File ("log.log.#.2020-08-02 17:01:51.131909")

    some text to ignore
        ANI		'<<<REDACTED>>>'
    ignore this also
            DNIS	'<<<REDACTED>>>'
    Target '<<<REDACTED>>>' @ '<<<REDACTED>>>' - keep this
    middle
    some text to ignore
        ANI		'<<<REDACTED>>>'
    ignore this also
            DNIS	'<<<REDACTED>>>'
    Target '<<<REDACTED>>>' @ '<<<REDACTED>>>' - keep this
    end

# Usage Examples:
  
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

#! /usr/bin/env python
import fileinput, argparse, re, hashlib, json, os, sys, time, datetime
from pprint import pprint

args = argparse.ArgumentParser(usage='%(prog)s FILE(s) [-ormqsvV --mapfile]', description='python log file hash/mask utility')

def parse_cmd_args(): # overkill on the args for my education
 global args
 args.add_argument('FILES', nargs='*', help='log FILE(s) or PATH or STDIN to hash/mask')
 args.add_argument('-o', '--output', dest="OUTPUT_DIR", help='output directory') # --output /home/fizz/out/
 args.add_argument("-r", dest="REGEX_FILE", default='regex.txt', help="regex pattern input file")
 args.add_argument('-m', '--mask', action='store_true', dest="MASK_NOT_HASH", help='mask with <<<REDACT>>> not hash redaction')
 args.add_argument('-s', '--suffix', dest="OUTPUT_SUFFIX", default=".#." + str(datetime.datetime.now()), help='output file suffix')
 args.add_argument('--mapfile', dest="MAP_FILE", default="map.txt", help='output map file')
 args.add_argument('-v', '--version', action='version', version='%(prog)s 46664')
 group = args.add_mutually_exclusive_group() # either -q or -V but not both
 group.add_argument('-V', dest="DEBUG", action='count', default=0, help="++ the verbosity output") # -V or -VV or -VVV
 group.add_argument('-q', '--quiet', action='store_true', dest="QUIET", default=False, help="no output")
 args = args.parse_args()
 if args.DEBUG >= 1:
   for arg in vars(args): print (arg, getattr(args, arg))
 return args

def load_regexes_from_file():
    # read in the [regex file] containing the list of 'Regex's'
    needles = [line.rstrip() for line in open(args.REGEX_FILE)]
    if args.DEBUG >= 1: print(needles)
    patterns = re.compile('|'.join(needles))
    return patterns

def run():
    regexes = load_regexes_from_file()
     
    map = {}
    if args.DEBUG >= 1: print(args.FILES)
    
    # read each 'line' from each 'file' passed in [args.FILES] or [STDIN]
    for line in fileinput.input(files=args.FILES if len(args.FILES) > 0 else ('-', )): 
        
        # if first 'line' of [input file], initialise the corresponding [output file]
        if fileinput.isfirstline():
            if args.DEBUG == 2: print("Processing file:", fileinput.filename())
            if args.OUTPUT_DIR:
                # i.e. [--output /home/fizz/output/] or [-o /home/fizz/output/]
                fout = open(args.OUTPUT_DIR + os.path.basename(fileinput.filename()) + args.OUTPUT_SUFFIX,'w')
            else:
                # same dir as input file if no -o/--output provided
                fout = open(fileinput.filename() + args.OUTPUT_SUFFIX,'w')
        
        line = line.rstrip()

        # REPR, useful for debugging on the input log 'line'
        if args.DEBUG > 1: print(f'{line!r}') # -VV

        # find matches on the current log 'line'
        for matches in re.finditer(regexes, line): 
            # useful debug details of the Regex matches for this log 'line'
            if args.DEBUG > 2: print(matches.groups(0)) # -VVV

            # loop through the Match Objects for matches
            for match in matches.groups(): 

                if (match):
                    if args.MASK_NOT_HASH: 
                        line = re.sub(match, '<<<REDACTED>>>', line) # mask 'value' with "<<<REDACTED>>>"
                    else:
                        if match not in map:
                            # 'MD5' (for a shorter hash) a 'SHA256' of the matched 'value'
                            md5_of_sha256 = hashlib.md5(hashlib.sha256(match.encode()).hexdigest().encode('utf-8')).hexdigest()
                            line = re.sub(match, md5_of_sha256, line)
                            map[match] = md5_of_sha256
                        else:
                            if args.DEBUG >= 2: print(f"[{match}] already mapped to [{map[match]}]")
                            line = re.sub(match, map[match], line)
       
        if not args.QUIET: print(line)
        # write 'line' (either untouched or hashed/masked) to [output file]
        fout.write(line +'\n')
               
    if map: 
        # when done, write hash/values to [args.MAP_FILE] for correlation
        write_hash_map_to_file(map)

def write_hash_map_to_file(hashmap):
    with open(args.MAP_FILE,'w') as fout_map:
        pprint(hashmap,stream=fout_map)
    if args.DEBUG >= 1: print(json.dumps(hashmap, indent=4))

if __name__ == '__main__':
 parse_cmd_args()

 start_time = time.time()
 
 run()
 
 end_time = time.time()
 runTime = end_time - start_time
 print(f'{runTime=:.3f}')


"""
Usage Examples:
./mask.py /home/fizz/tmp/*
./mask.py /home/fizz/tmp/* --output /home/fizz/out/
./mask.py /home/fizz/tmp/*.log
./mask.py /home/fizz/tmp/*.log /home/fizz/tmp/*.txt
./mask.py /home/fizz/tmp/*.log /home/fizz/tmp/*.txt -m
./mask.py /home/fizz/tmp/*.log /home/fizz/tmp/*.txt -m -r regex.txt
./mask.py /home/fizz/tmp/*.log /home/fizz/tmp/*.txt --mapfile mymap.txt -V
./mask.py /home/fizz/tmp/*.log /home/fizz/tmp/*.txt -s .HASH
./mask.py /home/fizz/tmp/*.log /home/fizz/tmp/*.txt -VV
./mask.py /home/fizz/tmp/log.log /home/fizz/tmp/log.txt /home/fizz/logs/* -VVV
./mask.py -v
./mask.py /home/fizz/tmp/*.log /home/fizz/tmp/*.txt -q
cat log.txt | ./mask.py
cat log.txt | ./mask.py -V
cat log.txt | ./mask.py -VVV -o /home/fizz/out/

Perf: processes a 50MB file, with 127 chars per line, 409599 lines, 4 regex matches per line in ~3 minutes, with a 70MB output file.
"""
#################################################
# © Copyright 2014 Hyojoon Kim
# All Rights Reserved 
# 
# email: deepwater82@gmail.com
#################################################

import os
from optparse import OptionParser
import python_api
import plot_lib
import sys
import pickle

def plot_the_data(the_map, output_dir, filename, title):
    key_list = the_map.keys()
    key_list.sort()

    num_tests = len(the_map[key_list[0]])
    ymap = {}
   
    for i in range(num_tests):
        xa = []
        ya = []
        for nflows in key_list:
            if len(the_map[nflows]) > (i):
                ts_val = the_map[nflows][i]
            else:
                ts_val = 0
            ya.append(ts_val/1000000000.0)
            if len(xa) != len(key_list):
                xa.append(nflows)
        ymap[i] = ya

    plot_lib.plot_multiline(xa, ymap, output_dir, filename, title)
#    plot_lib.plot_distribution(xa, ymap, output_dir, filename, title)

    return   

def main():

    desc = ( 'Plotting data' )
    usage = ( '%prog [options]\n'
                          '(type %prog -h for details)' )
    op = OptionParser( description=desc, usage=usage )

    # Options
    op.add_option( '--inputfile', '-i', action="store", \
                   dest="input_file", help = "Pickled data")
    
    op.add_option( '--outputdir', '-o', action="store", \
                   dest="output_dir", help = "Directory to store plots")

    # Parsing and processing
    options, args = op.parse_args()
    args_check = sys.argv[1:]
    if len(args_check) != 4:
        print 'Something wrong with paramenters. Please check.'
        print op.print_help()
        sys.exit(1)

    # Check and add slash to directory if not there.
    output_dir = python_api.check_directory_and_add_slash(options.output_dir)
    title = ''
    filename = ''

    # Check file, open, read
    if os.path.isfile(options.input_file) is True:
        fd = open(options.input_file, 'r')
        the_map = pickle.load(fd)
        fd.close()
        filename = os.path.basename(options.input_file)

        if (filename == 'flowmod_delay_map.p'):
            title = 'Flow modification delay'
        elif (filename == 'groupmod_delay_map.p'):
            title = 'Group modification delay'
        elif (filename == 'flowadd_delay_map.p'):
            title = 'Flow addition delay'
        elif (filename == 'groupadd_delay_map.p'):
            title = 'Group addition delay'
        else:
            print 'What mode is this? Using default title'
            title = 'Group addition delay'

    # Plot
    plot_the_data(the_map, output_dir, filename.rstrip('.p'), title)


######        
if __name__ == '__main__':
    main()

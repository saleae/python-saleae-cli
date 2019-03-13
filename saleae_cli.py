# -*- coding: utf-8 -*-
import os
import saleae
import argparse


parser = argparse.ArgumentParser(description='Saleae Command Line Interface Capture Utility', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('--capture-count', type=int, default=1, metavar='COUNT', help='Number of captures to repeat')
parser.add_argument('--capture-duration', type=float, default=1.0, metavar='SECONDS', help='Duration of each capture in seconds')
parser.add_argument('--save-captures', metavar='PATH', help='Saves each capture to the specified directory')
parser.add_argument('--export-data', metavar='PATH', help='Exports the raw capture to the sepcified directory')
parser.add_argument('--export-analyzers', metavar='PATH', help='Exports each analyzer to the specified directory')
parser.add_argument('--ip', metavar='IP', default='localhost', help='IP address to connect to')
parser.add_argument('--port', metavar='PORT', default=10429, help='Port to connect to')

args = parser.parse_args()

s = saleae.Saleae(args.ip, args.port)

for x in range(args.capture_count):
    #set capture duration
    s.set_capture_seconds(args.capture_duration)
    #start capture. Only save to disk if the --save-captures option was specified.
    if args.save_captures is not None:
        file_name = '{0}.logicdata'.format(x)
        save_directory = os.path.abspath(args.save_captures)
        if not os.path.exists(save_directory):
            os.makedirs(save_directory)
        save_path = os.path.join(save_directory, file_name)
        print('Starting capture and saving to ' + save_path)
        s.capture_to_file(save_path)
    else:
        #currently, the python library doesn't provide a CAPTURE command that blocks until an ACK is received
        s._cmd('CAPTURE')

    #raw export
    if args.export_data is not None:
        file_name = '{0}.csv'.format(x)
        save_directory = os.path.abspath(args.export_data)
        if not os.path.exists(save_directory):
            os.makedirs(save_directory)
        save_path = os.path.join(save_directory, file_name)
        print('Exporting data to ' + save_path)
        s.export_data2(save_path)

    #analyzer export
    if args.export_analyzers is not None:
        analyzers = s.get_analyzers()
        if analyzers.count == 0:
            print('Warning: analyzer export path was specified, but no analyzers are present in the capture')
        for analyzer in analyzers:
            file_name = '{0}_{1}.csv'.format(x, analyzer[0])
            save_directory = os.path.abspath(args.export_analyzers)
            if not os.path.exists(save_directory):
                os.makedirs(save_directory)
            save_path = os.path.join(save_directory, file_name)
            print('Exporting analyzer ' + analyzer[0] + ' to ' + save_path)
            s.export_analyzer(analyzer[1], save_path)

import os
import saleae
import argparse

def validate_path( path, argument_name ):
    if path != None:
        if os.path.isdir(path) == False:
            print('the specified ' + argument_name + ' directory does not exist or is invalid')
            print('you specified: ' + path)
            quit()

parser = argparse.ArgumentParser(description='Saleae Command Line Interface Capture Utility')
parser.add_argument('--capture-count', required=True, type=int, metavar='COUNT', help='number of captures to repeat')
parser.add_argument('--capture-duration', required=True, type=float, metavar='SECONDS', help='duration of each capture in seconds')
parser.add_argument('--save-captures', metavar='PATH', help='if specified, saves each capture to the specified directory')
parser.add_argument('--export-data', metavar='PATH', help='if specified, exports the raw capture to the sepcified directory')
parser.add_argument('--export-analyzers', metavar='PATH', help='if specified, exports each analyzer to the specified directory')
parser.add_argument('--ip', metavar='IP', default='localhost', help='optional, IP address to connect to. Default localhost')
parser.add_argument('--port', metavar='PORT', default=10429, type=int, help='optional, Port to connect to. Default 10429')
parser.add_argument('--exit', action='store_true', help='optional, use to close the Logic software once complete')

args = parser.parse_args()

validate_path(args.save_captures, '--save-captures')
validate_path(args.export_data, '--export-data')
validate_path(args.export_analyzers, '--export-analyzers')


s = saleae.Saleae(args.ip, args.port)

for x in range(args.capture_count):
    #set capture duration
    s.set_capture_seconds(args.capture_duration)
    #start capture. Only save to disk if the --save-captures option was specified.
    if args.save_captures != None:
        file_name = '{0}.logicdata'.format(x)
        save_path = os.path.join(args.save_captures, file_name)
        print('starting capture and saving to ' + save_path)
        s.capture_to_file(save_path)
    else:
        #currently, the python library doesn't provide a CAPTURE command that blocks until an ACK is received
        s._cmd('CAPTURE')

    #raw export
    if args.export_data != None:
        file_name = '{0}.csv'.format(x)
        save_path = os.path.join(args.export_data, file_name)
        print('exporting data to ' + save_path)
        s.export_data2(save_path)

    #analyzer export
    if args.export_analyzers != None:
        analyzers = s.get_analyzers()
        if analyzers.count == 0:
            print('Warning: analyzer export path was specified, but no analyzers are present in the capture')
        for analyzer in analyzers:
            file_name = '{0}_{1}.csv'.format(x, analyzer[0])
            save_path = os.path.join(args.export_analyzers, file_name)
            print('exporting analyzer ' + analyzer[0] + ' to ' + save_path)
            s.export_analyzer(analyzer[1], save_path)
        
if args.exit is True:
    print('closing Logic software')
    try:
        s.exit()
    except:
        # ignore errors from exit command, since it will raise due to socket disconnect.
        pass
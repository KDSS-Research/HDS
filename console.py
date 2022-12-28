import hsf
import argparse
import os
print('Welcome to HSF Console! (C) KDSS-Research 2022\nIm not responsible for any actions with that program!\n')

parser = argparse.ArgumentParser(description='Videos to images')
parser.add_argument('mode', type=str, help='Mode of work (d - download from file, b - brew file)')
parser.add_argument('urlfile', type=str, help='URL or File')
parser.add_argument(
    '--bsf',
    type=str,
    default='brewed.hsf',
    help='How save file? (for brew)'
)
args = parser.parse_args()
if args.mode == 'd':
    if os.path.exists(args.urlfile):
        hsf_c = hsf.hsf_downloader(args.urlfile)
        hsf_c.download()
    else:
        print('File not found!')
elif args.mode == 'b':
    if args.urlfile[:4] == 'http':
        if args.bsf != 'brewed.hsf':
            hsf_c = hsf.hsf_brew(args.urlfile,filename=args.bsf)
            hsf_c.brew()
        else:
            hsf_c = hsf.hsf_brew(args.urlfile)
            hsf_c.brew()
    else:
        print('Not URL!')
else:
    print('Unknown mode!')
    exit()
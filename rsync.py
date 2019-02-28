import argparse
import os
from stat import *
from os import path
from os import chmod
parser = argparse.ArgumentParser(prog='rsync')
parser.add_argument('filename1',type=str)
parser.add_argument('filename2',type=str)
args = parser.parse_args()
path1 = path.abspath(args.filename1)
path2 = path.abspath(args.filename2)
perm_info = oct(os.stat(path1).st_mode)
if path.isdir(path1):
    print('skipping directory ' + args.filename1)
else:
    if path.isdir(path2):
        file1 = open(args.filename1,'r')
        file2 = open(path.abspath(path2) + '/' + args.filename1, 'w+')
        chmod(path.abspath(path2) + '/' + args.filename1, perm_info)
        f = file1.read()
        file2.write(f)
        file1.close()
        file2.close()
    else:
        file1 = open(args.filename1,'r')
        file2 = open(args.filename2, 'w')
        chmod(path2, perm_info)
        f = file1.read()
        file2.write(f)
        file1.close()
        file2.close()

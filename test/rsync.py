#!/usr/bin/env python3
import argparse
from os import path, chmod, stat, utime, symlink, link, readlink, lstat
from stat import *


""" Global variables """
parser = argparse.ArgumentParser(prog='rsync')
parser.add_argument('filename1', type=str)
parser.add_argument('filename2', type=str)
args = parser.parse_args()
path_source = path.basename(args.filename1)
path_dest = path.abspath(args.filename2)


"""    Copy from file source to file destination    """


def copy_file(path_source, path_dest):
    if path.isdir(path_source):         # filesource is a directory
        print('skipping directory ' + path_source)
    else:
        if path.isdir(path_dest):      # filedest is a directory
            file1 = open(path_source, 'r')
            file2 = open(path_dest + '/' + path_source, 'w+')
            f = file1.read()
            file2.write(f)
        else:                       # both files are files
            file1 = open(path_source, 'r')
            file2 = open(path_dest, 'w')
            f = file1.read()
            file2.write(f)
    file1.close()
    file2.close()


"""    Sync the permissions and time  """


def sync_perm_time(path_source, path_dest):
    perm_info = stat(path_source).st_mode
    chmod(path_dest, perm_info)
    if path.islink(path_source):
        time_info = (lstat(path_source).st_atime, lstat(path_source).st_mtime)
        utime(path_dest, time_info, follow_symlinks = False)
    else:
        time_info = (stat(path_source).st_atime, stat(path_source).st_mtime)
        utime(path_dest, time_info)


"""   Copy symlink and hardlink  """


def copy_symlink(path_source, path_dest):
    link_origin = readlink(path_source)
    if path.isdir(path_dest):
        symlink(link_origin, path_dest + '/' + path_source)
        raise TypeError('Broken symlink')
    else:
        symlink(link_origin, path_dest)


def copy_hardlink(path_source, path_dest):
    if path.isdir(path_dest):
        link(path_source, path_dest + '/' + path_source)
    else:
        link(path_source, path_dest)


"""   Rsync function   """


def rsync(path_source, path_dest):
    if path.islink(path_source):
        copy_symlink(path_source, path_dest)
    elif stat(path_source).st_nlink >= 2:
        copy_hardlink(path_source, path_dest)
    else:
        copy_file(path_source, path_dest)
    if path.isdir(path_dest):
        path_dest = path_dest + '/' + path_source
    sync_perm_time(path_source, path_dest)


rsync(path_source, path_dest)

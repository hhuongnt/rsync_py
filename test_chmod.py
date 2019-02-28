import os
from stat import *
from os import path
path1 = path.abspath('/tmp/guest-v9r6ek/nhuong/test/file1')
path2 = path.abspath('/tmp/guest-v9r6ek/nhuong/test/test2')
perm_info = oct(os.stat(path1).st_mode)
print (perm_info)

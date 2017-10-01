import os
import glob
from shutil import copy

directories = glob.glob('./american-ash-*')

for directory in directories:
        for filename in os.listdir(directory):
                print filename
                path = os.path.join('./',directory)
                if (filename == '0.png'):
                        print 'Renamed H for ', directory
                        copy(os.path.join(path,filename),  os.path.join(path, 'H.png'))
                if (filename == '45.png'):
                        print 'Renamed P for ', directory
                        copy(os.path.join(path,filename),  os.path.join(path, 'P.png'))
                if (filename == '90.png'):
                        print 'Renamed V for ', directory
                        copy(os.path.join(path,filename),  os.path.join(path, 'V.png'))
                if (filename == '135.png'):
                        print 'Renamed M for ', directory
                        copy(os.path.join(path,filename),  os.path.join(path, 'M.png'))

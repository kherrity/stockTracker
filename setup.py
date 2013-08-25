import os
from distutils.core import setup
import py2exe

def get_pytz_zoneinfo_files():
    zoneinfo_files = []
    zoneinfo_dir = r'C:\Python27\Lib\site-packages\pytz\zoneinfo'
    for dirpath, subdirs, filenames in os.walk(zoneinfo_dir):
        subdir = os.path.basename(dirpath)
        if subdir != 'zoneinfo':
            subdir = 'zoneinfo' + os.path.sep + subdir
        for filename in filenames:
            f1 = os.path.join(dirpath, filename)
            if os.path.isfile(f1): # skip directories
                f2 = subdir, [f1]
                zoneinfo_files.append(f2)
    return zoneinfo_files

all_data_files = []
all_data_files.extend(get_pytz_zoneinfo_files())

def main():
    setup(
        console = ['st_gui.py'],
        options = {
            'py2exe': {
                'packages':['pytz'],
                }
            },
        data_files = all_data_files,
        )

if __name__ == "__main__":
    main()

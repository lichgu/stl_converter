# Created by lcg at 21.07.22

import os
from pathlib import Path

from bin2ascii import bin2ascii
from ascii2bin import ascii2bin

root_dir = Path(os.path.dirname(__file__))
in_dir = os.path.join(root_dir, 'data/samples')
out_dir = os.path.join(root_dir, 'data/converted')


if __name__ == '__main__':
    bin2ascii(os.path.join(in_dir, 'part1_bin.stl'),
              os.path.join(out_dir, 'part1_ascii_converted.stl'))
    ascii2bin(os.path.join(in_dir, 'part1_ascii.stl'),
              os.path.join(out_dir, 'part1_bin_converted.stl'))


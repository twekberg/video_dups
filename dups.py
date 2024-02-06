#!/usr/bin/env python
"""
"""

# Note: a video can be converted to a thumbnail. This is useful because VisiPics can
# be used to detect duplicates. A sample command is:
#
# magick convert 'input.mpg[5]' -resize 400x400 thumbnail.jpg

import argparse
from pathlib import Path
import sys
import subprocess

#TODO:
# One iteration is coded. Testing is needed.


def build_parser():
    """
    Collect command line arguments.
    """
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('-i', '--input_directory_base',
                        default='F:/N/O/SPELLSNO/IMAGES/xxxbunker/EDITED',
                        help='The name of the directory containing'
                        ' video clips.'
                        ' Default: %(default)s.')
    parser.add_argument('-s', '--sub_directory',
                        default='BELOW',
                        help='Subdirectory under input_directory_base containing'
                        ' video clips.'
                        ' Default: %(default)s.')
    parser.add_argument('-o', '--output_directory_base',
                        default='F:/N/O/SPELLSNO/IMAGES/xxxbunker/EDITED/CLIPS',
                        help='Input directory. '
                        ' Default: %(default)s.')
    parser.add_argument('-f', '--frame', type=int,
                        default=5,
                        help='Frame number to use as thumbnail. '
                        ' Default: %(default)s.')
    return parser


def exec_one(prog, args):
    """
    Run program with args. Returns stdout, throw exception when status != 0.
    """
    result = subprocess.run([prog] + args,
                            stdout = subprocess.PIPE,
                            text=True,
                            stderr = subprocess.STDOUT)
    return result.stdout


def path_dos2unix(path):
    """
    Convert a Path object to Unix format as a string.
    """
    return str(path).replace('\\', '/')


def main(args):
    """
    Starting point.
    """
    output_directory = Path(args.output_directory_base) / args.sub_directory
    if not output_directory.is_dir():
        if output_directory.exists():
            print('Output directory already exists but is not a directory. {output_directory=}')
            exit(1)
        output_directory.mkdir(mode=0o755, parents=True, exist_ok=True)
    input_directory = Path(args.input_directory_base) / args.sub_directory
    if not output_directory.is_dir():
        print(f"Input directory already doesn't exist. {input_directory=}")
        exit(1)

    for file in input_directory.glob('*.mpg'):
        clip_filename = output_directory / (file.stem + '.jpg')
        if clip_filename.exists():
            # The clip already exists.
            continue
        stdout = exec_one('magick', ['convert', f'{path_dos2unix(file)}[{args.frame}]',
                                     path_dos2unix(clip_filename)])


if __name__ == '__main__':
    sys.exit(main(build_parser().parse_args()))

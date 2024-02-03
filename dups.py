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
    parser.add_argument('-i', '--input_directory',
                        default='F:/N/O/SPELLSNO/IMAGES/xxxbunker/EDITED/BELOW',
                        help='The name of the directory containing'
                        ' video clips.'
                        ' Default: %(default)s.')
    parser.add_argument('-o', '--output_directory',
                        default='F:/N/O/SPELLSNO/IMAGES/xxxbunker/EDITED/CLIPS/BELOW',
                        help='Input directory. '
                        ' Default: %(default)s.')
    return parser


def exec_one(prog, args):
    """
    Run program with args. Returns stdout, throw exception when status != 0.
    """
    #result = subprocess.Popen(["./ffprobe", filename],
    print([prog] + args)
    result = subprocess.run([prog] + args,
                            stdout = subprocess.PIPE,
                            text=True,
                            stderr = subprocess.STDOUT)
    return result.stdout


def path_dos2unix(path):
    return str(path).replace('\\', '/')

def main(args):
    """
    Starting point.
    """
    output_directory = Path(args.output_directory)
    if not output_directory.is_dir():
        if output_directory.exists():
            print('Output directory already exists but is not a directory. {output_directory=}')
            exit(1)
        output_directory.mkdir(mode=0o755, parents=True, exist_ok=True)
    input_directory = Path(args.input_directory)
    if not output_directory.is_dir():
        print(f"Input directory already doesn't exist. {input_directory=}")
        exit(1)

    for file in input_directory.glob('*.mpg'):
        print(file)
        clip_filename = path_dos2unix(output_directory / (file.stem + '.jpg'))
        stdout = exec_one('magick', ['convert', f'{path_dos2unix(file)}[5]', str(clip_filename)])
        print(f'{stdout}')
        exit(0)


if __name__ == '__main__':
    sys.exit(main(build_parser().parse_args()))

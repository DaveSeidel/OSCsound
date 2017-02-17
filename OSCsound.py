#
# OSCsound - Version 0.2
# Author: Steven Yi, Dave Seidel
#
# Script for rapid live Csound application development with OSC
#
# Licensed under LGPL. Please view LICENSE for more information.
#

import argparse
import sys

from CsoundProxy import CsoundProxy
from OSCServerProxy import OSCServerProxy


def process_args():
    parser = argparse.ArgumentParser(prog='OSCsound',
                                     description='OSCsound - version 0.2-ds')

    parser.add_argument("csd_file", help="Csound CSD file")
    parser.add_argument("-p", "--port", help="server port (default 7110)",
                        type=int, default=7110)

    return parser.parse_args()


def main():
    args = process_args()

    with CsoundProxy(args.csd_file) as csound:
        with OSCServerProxy(csound, args.port) as osc:
            osc.run()

    return 0


if __name__ == '__main__':
    sys.exit(main())

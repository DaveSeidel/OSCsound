import argparse
from os.path import dirname, abspath
import sys

sys.path.insert(0, dirname(dirname(abspath(__file__))))
from CsoundProxy import CsoundProxy
from OSCServerProxy import OSCServerProxy, OSCCallback


class MyOSCServerProxy(OSCServerProxy):
    def __init__(self, csound_proxy, port):
        self._handlers = [
            OSCCallback(address="/greg", callback=self._greg_handler)
        ]

        super(MyOSCServerProxy, self).__init__(csound_proxy, port, handlers=self._handlers)

    def _greg_handler(self, path, tags, args, source):
        print "osc greg: %s %s %s %s" % (path, tags, str(args), source)
        if not args:
            print "Error: /greg must have at least one value"
            return
        print "greg args: %s" % (args)


def process_args():
    parser = argparse.ArgumentParser(prog='OSCsoundExt',
                                     description='OSCSound extension test')

    parser.add_argument("csd_file", help="Csound CSD file")
    parser.add_argument("-p", "--port", help="server port (default 7110)",
                        type=int, default=7110)

    return parser.parse_args()


def main():
    args = process_args()

    with CsoundProxy(args.csd_file) as csound:
        with MyOSCServerProxy(csound, args.port) as osc:
            osc.run()

    return 0


if __name__ == '__main__':
    sys.exit(main())

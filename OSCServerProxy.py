from collections import namedtuple
import sys
from time import sleep
import traceback
import types

from OSC import OSCServer


OSCCallback = namedtuple("OSCCallback", "address callback")


class OSCServerProxy(object):
    """An OSC server wrapper that works in conjunction with a CsoundProxy
    instance, for use in a 'with' scope.
    """

    def __init__(self, csound_proxy, port, handlers=[]):
        """Args:
            csound_proxy: a Csound instance
            port: port OSCServer will listen on
        """
        print "osc, port=%s" % (port)
        self._cs = csound_proxy.cs
        self._pt = csound_proxy.pt
        self._port = port
        self._handlers = handlers
        self._run = True

    def __enter__(self):
        """Sets up the OSC server

        Returns:
            : this instance
        """

        print "osc enter"
        self._server = OSCServer(("localhost", self._port))

        self._server.timeout = 0
        self._server.handle_timeout = types.MethodType(OSCServerProxy._handle_timeout, self._server)

        self._server.addMsgHandler("/sco", self._handle_score)
        self._server.addMsgHandler("/cc", self._handle_cc)
        self._server.addMsgHandler("/quit", self._quit_callback)
        self._server.addMsgHandler("default", self._default_callback)

        for handler in self._handlers:
            if not isinstance(handler, OSCCallback):
                print "Error: rejecting callback '', wrong type" % str(handler)
            self._server.addMsgHandler(handler.address, handler.callback)

        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Shuts down the OSC server"""

        print "osc exit"
        if exc_type is not None:
            print exc_type, exc_value, traceback

        self._server.close()

    def run(self):
        """This is the server loop, exits on termination."""

        print "osc run"
        while self._run is True:
            sleep(1)
            self._server.timed_out = False
            while not self._server.timed_out:
                self._server.handle_request()

    ## handlers/callbacks

    @staticmethod
    def _handle_timeout(server):
        server.timed_out = True

    def _handle_score(self, path, tags, args, source):
        if len(args) == 0:
            print "Error: /score must have one arg: scoreText"
            return

        score = args[0]
        print "osc score: \"%s\"" % (score)
        self._pt.inputMessage(score)

    def _handle_cc(self, path, tags, args, source):
        print "osc cc: %s %s %s" % (path, tags, str(args))
        if len(args) != 2:
            print "Error: /cc must have two args: channelName floatValue"
            return

        channel_name = args[0]
        float_value = args[1]
        print "cc args: %s %s" % (channel_name, float_value)
        self._cs.setControlChannel(channel_name, float_value)

    def _default_callback(self, path, tags, args, source):
        try:
            print "osc default_callback: %s %s %s" % (path, tags, str(args))
            if path.startswith("/cc/"):
                channel_name = path[4:]
                float_value = args[0]
                print "args: %s %s" % (channel_name, float_value)
                self._cs.setControlChannel(channel_name, float_value)
            else:
                print "ignoring message"
        except Exception as e:
            print e.message
            traceback.print_exc(file=sys.stdout)

    def _quit_callback(self, path, tags, args, source):
        print "osc quit"
        self._run = False

from time import sleep
import types

from OSC import OSCServer

class OSCServerProxy():
    def __init__(self, csound_proxy, port):
        print "osc, port=%s" % (port)
        self._csound = csound_proxy.csound
        self._csPerfThread = csound_proxy.csPerfThread
        self._port = port
        self._run = True

    def __enter__(self):
        print "osc enter"
        self._server = OSCServer(("localhost", self._port))

        self._server.timeout = 0
        self._server.handle_timeout = types.MethodType(OSCServerProxy._handle_timeout, self._server)

        self._server.addMsgHandler("/sco", self._handle_score)
        self._server.addMsgHandler("/cc", self._handle_cc)
        self._server.addMsgHandler("/quit", self._quit_callback)
        self._server.addMsgHandler("default", self._default_callback)

        return self

    def __exit__(self, exc_type, exc_value, traceback):
        print "osc exit"
        if exc_type is not None:
            print exc_type, exc_value, traceback

        self._server.close()

    def run(self):
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
        self._csPerfThread.InputMessage(score)

    def _handle_cc(self, path, tags, args, source):
        print "osc cc: %s" % (str(args))
        if len(args) != 2:
            print "Error: /cc must have two args: channelName floatValue"
            return

        channel_name = args[0]
        float_value = args[1]
        print "cc args: %s %s" % (channel_name, float_value)
        self._csound.SetChannel(channel_name, float_value)

    def _default_callback(self, path, tags, args, source):
        print "osc default_callback: %s %a" % (path, str(args))
        if path.startswith("/cc/"):
            channel_name = path[4:]
            float_value = args[0]
            print "args: %s %s" % (channel_name, float_value)
            self._csound.SetChannel(channel_name, float_value)
        else:
            print "ignoring message:", path, tags, args

    def _quit_callback(self, path, tags, args, source):
        print "osc quit"
        self._run = False

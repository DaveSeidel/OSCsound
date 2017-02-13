from csnd6 import Csound, CsoundPerformanceThread, csoundInitialize

class CsoundProxy(object):
    def __init__(self, csd_file):
        print "csound: csd_file=%s" % (csd_file)
        self._csd_file = csd_file
        self._csound = None
        self._csPerfThread = None

        csoundInitialize(3)

    @property
    def csound(self):
        return self._csound

    @property
    def csPerfThread(self):
        return self._csPerfThread

    def __enter__(self):
        print "csound enter"
        self._csound = Csound()
        self._csound.SetOption("-odac")
        self._csound.Compile(self._csd_file)
        self._csound.Start()

        self._csPerfThread = CsoundPerformanceThread(self._csound)
        self._csPerfThread.Play()

        return self

    def __exit__(self, exc_type, exc_value, traceback):
        print "csound exit"
        if exc_type is not None:
            print exc_type, exc_value, traceback

        self._csPerfThread.Stop()
        self._csPerfThread.Join()
        self._csound.Stop()

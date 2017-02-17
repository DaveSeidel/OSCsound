from csnd6 import Csound, CsoundPerformanceThread, csoundInitialize

class CsoundProxy(object):
    """A Csound instance wrapper for use in a 'with' scope.

    >>> with CsoundProxy(csd_file) as csound_proxy:
    >>>     # csound_proxy.csound is the Csound instance
    >>>     # csound_proxy.csPerfThread is the CsoundPerformaceThread instance
    >>>     do_stuff(csound_proxy)
    """

    DEFAULT_OPTIONS = ["-odac", "-m7"]

    def __init__(self, csd_file, options=DEFAULT_OPTIONS):
        """Args:
            csd_file: name of CSD file to run
            options: list of Csound command-line options (optional, defaults to CsoundProxy.DEFAULT_OPTIONS)
        """
        print "csound: csd_file=%s options=%s" % (csd_file, options)
        self._csd_file = csd_file
        self._options = options
        self._csound = None
        self._csPerfThread = None

    @property
    def csound(self):
        """the underlying Csound instance"""
        return self._csound

    @property
    def csPerfThread(self):
        """the CsoundPerformanceThread instance"""
        return self._csPerfThread

    def __enter__(self):
        """Starts up the Csound/CsoundPerformanceThread instances

        Returns:
            this proxy instance
        """
        print "csound enter"

        csoundInitialize(3)

        self._csound = Csound()
        map(self._csound.SetOption, self._options)
        self._csound.Compile(self._csd_file)
        self._csound.Start()

        self._csPerfThread = CsoundPerformanceThread(self._csound)
        self._csPerfThread.Play()

        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Shuts down Csound"""
        print "csound exit"
        if exc_type is not None:
            print exc_type, exc_value, traceback

        self._csPerfThread.Stop()
        self._csPerfThread.Join()
        self._csound.Stop()

import ctcsound

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
        self._cs = None
        self._pt = None

    @property
    def cs(self):
        """the underlying Csound instance"""
        return self._cs

    @property
    def pt(self):
        """the CsoundPerformanceThread instance"""
        return self._pt

    def __enter__(self):
        """Starts up the Csound/CsoundPerformanceThread instances

        Returns:
            this proxy instance
        """
        print "csound enter"

        self._cs = ctcsound.Csound()
        map(self._cs.setOption, self._options)
        self._cs.compileCsd(self._csd_file)
        self._cs.start()

        self._pt = ctcsound.CsoundPerformanceThread(self._cs.csound())
        self._pt.play()

        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Shuts down Csound"""
        print "csound exit"
        if exc_type is not None:
            print exc_type, exc_value, traceback

        self._pt.stop()
        self._pt.join()
        self._cs.stop()

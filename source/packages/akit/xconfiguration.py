__author__ = "Myron Walker"
__copyright__ = "Copyright 2020, Myron W Walker"
__credits__ = []
__version__ = "1.0.0"
__maintainer__ = "Myron Walker"
__email__ = "myron.walker@gmail.com"
__status__ = "Development" # Prototype, Development or Production
__license__ = "MIT"

class DiagnosticLabel:
    PRERUN_DIAGNOSTIC = "prerun-diagnostic"
    POSTRUN_DIAGNOSTIC = "postrun-diagnostic"

class RuntimeConfigPaths:
    DIAGNOSTIC_PRERUN = "/configuration/diagnostics/prerun-diagnostic"
    DIAGNOSTIC_POSTRUN = "/configuration/diagnostics/postrun-diagnostic"

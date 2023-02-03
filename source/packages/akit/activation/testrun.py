
import os

from akit.exceptions import AKitSemanticError
from akit.environment.variables import ActivationProfile, AKIT_VARIABLES, JOB_TYPES

__activation_profile__ = ActivationProfile.TestRun

# Guard against attemps to activate more than one, activation profile.
if AKIT_VARIABLES.AKIT_ACTIVATION_PROFILE is not None:
    errmsg = "An attempt was made to activate multiple environment activation profiles. profile={}".format(
        AKIT_VARIABLES.AKIT_ACTIVATION_PROFILE
    )
    raise AKitSemanticError(errmsg)

AKIT_VARIABLES.AKIT_ACTIVATION_PROFILE = ActivationProfile.TestRun

AKIT_VARIABLES.AKIT_JOBTYPE = JOB_TYPES.TESTRUN

os.environ["AKIT_JOBTYPE"] = AKIT_VARIABLES.AKIT_JOBTYPE

import akit.activation.base

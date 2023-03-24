
from akit.xfeature import FeatureTag

class SingleBoardComputer(FeatureTag):
    "Features for single board computers"

    class Processor(FeatureTag):
        """Features of the processor"""

        class DualCore(FeatureTag):
            """The processor is dual core"""

    class Video(FeatureTag):
        """Video Interfaces"""

        class HDMI(FeatureTag):
            """HDMI Capabilities"""

            class Micro(FeatureTag):
                """Has a Micro HDMI port"""
            class Standard(FeatureTag):
                """Has standard HDMI capabilities"""

from akit.interop.landscaping.landscapedevice import LandscapeDevice

class RaspberryPi (LandscapeDevice):

    FEATURE_TAGS = [
        SingleBoardComputer.Processor.DualCore,
        SingleBoardComputer.Video.HDMI.Micro
    ]


from akit.testing.constraints import Constraints

class MicroHDMIConstraint(Constraints):
    def __init__(self):
        super().__init__(required_features=[
                SingleBoardComputer.Video.HDMI.Micro
            ])
    
    def setup(self):
        return
    
    def teardown(self):
        return
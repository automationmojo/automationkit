"""
.. module:: templates
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Package marking the folder that contains html and other renderable
               content templates.

.. moduleauthor:: Myron Walker <myron.walker@gmail.com>
"""

__author__ = "Myron Walker"
__copyright__ = "Copyright 2020, Myron W Walker"
__credits__ = []
__version__ = "1.0.0"
__maintainer__ = "Myron Walker"
__email__ = "myron.walker@gmail.com"
__status__ = "Development" # Prototype, Development or Production
__license__ = "MIT"

import os

from akit.exceptions import AKitRuntimeError

DIR_TEMPLATES = os.path.dirname(os.path.abspath(__file__))

DIR_TAB_TEMPLATES = os.path.join(DIR_TEMPLATES, "tabs")

TABS_TEMPLATE_IMAGES = os.path.join(DIR_TAB_TEMPLATES, "tab-images.html")
TABS_TEMPLATE_SOUNDS = os.path.join(DIR_TAB_TEMPLATES, "tab-sounds.html")

class SummaryTemplateNames:
    Html = "html-template"
    Script = "script-template"
    Style = "style-template"


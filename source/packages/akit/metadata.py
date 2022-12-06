"""
.. module:: metadata
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Module that contains decorators that can be utilized to attach metadata to automation
               tasks, tests, scopes, and integrations.

.. moduleauthor:: Myron Walker <myron.walker@gmail.com>
"""

# pylint: disable=too-few-public-methods

__author__ = "Myron Walker"
__copyright__ = "Copyright 2020, Myron W Walker"
__credits__ = []
__version__ = "1.0.0"
__maintainer__ = "Myron Walker"
__email__ = "myron.walker@gmail.com"
__status__ = "Development" # Prototype, Development or Production
__license__ = "MIT"

class Category:
    """
        The 'Category' decorator allows test engineers to associate categories with individual test
        cases or collections of tests.
    """

    def __init__(self, *categories):
        if len(categories) == 0:
            raise ValueError("The 'Category' decorator requires at least one category arguement.")
        self._categories = categories
        return

    def __call__(self, obj_to_decorate):
        if not hasattr(obj_to_decorate, "_metadata_"):
            obj_to_decorate._metadata_ = {}
        if "categories" in obj_to_decorate._metadata_:
            obj_to_decorate._metadata_["categories"].extend(self._categories)
        else:
            obj_to_decorate._metadata_["categories"] = self._categories
        return obj_to_decorate

class Keywords:
    """
        The 'Keywords' decorator allows test engineers to associate keywords with individual test
        cases or collections of tests.
    """

    def __init__(self, *keywords):
        if len(keywords) == 0:
            raise ValueError("The 'Keyword' decorator requires at least one keyword arguement.")
        self._keywords = keywords
        return

    def __call__(self, obj_to_decorate):
        if not hasattr(obj_to_decorate, "_metadata_"):
            obj_to_decorate._metadata_ = {}
        if "keywords" in obj_to_decorate._metadata_:
            obj_to_decorate._metadata_["keywords"].extend(self._keywords)
        else:
            obj_to_decorate._metadata_["keywords"] = self._keywords
        return obj_to_decorate

class Priority:
    """
        The 'Priority' decorator allows test engineers to associate a test priority with
        individual test cases or collections of tests.
    """

    def __init__(self, priority):
        self._priority = priority
        return

    def __call__(self, obj_to_decorate):
        if not hasattr(obj_to_decorate, "_metadata_"):
            obj_to_decorate._metadata_ = {}
        if "priority" in obj_to_decorate._metadata_:
            obj_to_decorate._metadata_["priority"].extend(self._priority)
        else:
            obj_to_decorate._metadata_["priority"] = self._priority
        return obj_to_decorate

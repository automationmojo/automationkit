
from typing import List, Optional, Tuple, Type, Union

import os
import re

from akit.exceptions import AKitReaderError, AKitSemanticError

class RegExPattern:
    """
        The :class:`RegExPattern` object provides a way to combine a regular expression
        pattern with additional characteristic data that describe how the pattern should be
        used by the :class:`RegExReader` to match and process text content.
    """
    def __init__(self, pattern: Union[str, re.Pattern], *, match_type: str=None, destination: str=None,
                 required: bool=False, repeats: bool=False, strict: Optional[bool]=None, consume: bool=False):

        if match_type is not None and destination is None:
            errmsg = "RegExPattern: If 'match_type' is specified then you must provide a 'destination' parameter."
            raise AKitSemanticError(errmsg)

        if repeats and match_type is None:
            errmsg = "RegExPattern: If 'repeats=True', you must specify an 'match_type' parameter."
            raise AKitSemanticError(errmsg)

        self.pattern = pattern
        if isinstance(pattern, str):
            self.pattern = re.compile(pattern)
        self.match_type = match_type
        self.destination = destination
        self.required = required
        self.repeats = repeats
        self.strict = strict
        self.consume = consume
        return

    def __repr__(self) -> str:
        pattern_repr = 'RegExPattern(%r, match_type=%r, destination=%r, required=%r, repeats=%r, strict=%r)' % (
            self.pattern, self.match_type, self.destination, self.required, self.repeats, self.strict
        )
        return pattern_repr

    def __str__(self) -> str:
        pattern_str = 'pattern=%r match_type=%r destination=%r required=%r repeats=%r strict=%r' % (
            self.pattern, self.match_type, self.destination, self.required, self.repeats, self.strict
        )
        return pattern_str

class RegExMultiPattern:
    """
        The :class:`RegExMultiPattern` object provides a way to combine list regular expression
        patterns with a set of additional characteristic data that describe how the patterns should
        be used by the :class:`RegExReader` to match list of lines from text content.
    """
    def __init__(self, patterns: List[Union[str, re.Pattern]], *, match_type: str=None, destination: str=None,
                 required: bool=False, repeats: bool=False, strict: Optional[bool]=None, consume: bool=False):

        if match_type is not None and destination is None:
            errmsg = "RegExPattern: If 'match_type' is specified then you must provide a 'destination' parameter."
            raise AKitSemanticError(errmsg)
        
        self.destination = destination
        self.patterns = None

        if len(self.patterns) == 0:
            errmsg = "The RegExMultiPattern object requires at least one pattern to be passed."
            raise AKitSemanticError(errmsg)
        else:
            self.patterns = [p if isinstance(p, re.Pattern) else re.compile(p) for p in patterns]

        self.match_type = match_type
        self.required = required
        self.repeats = repeats
        self.strict = strict
        self.consume = consume
        return

    def __repr__(self) -> str:
        pattern_repr = 'RegExPattern(%r, match_type=%r, destination=%r, required=%r, repeats=%r, strict=%r)' % (
            self.patterns, self.match_type, self.destination, self.required, self.repeats, self.strict
        )
        return pattern_repr

    def __str__(self) -> str:
        pattern_str = 'patterns=%r match_type=%r destination=%r required=%r repeats=%r strict=%r' % (
            self.patterns, self.match_type, self.destination, self.required, self.repeats, self.strict
        )
        return pattern_str

class RegExReader:
    """
        The :class:`RegExReader` is a class that makes it easy to create text content
        parsers.
        
        The user of this class will inherit from the class and override the
        `EXPECTED_LINES` class variable and the `_process_matches` method to capture
        value matches.
        
        I The user might also want to override the `_register_pattern_match_bugs`
        method in order to integrate with custom enterprise but filing functionality
        for filing bugs for pattern match misses.
    """

    EXPECTED_LINES: List[Union[RegExPattern, RegExMultiPattern]] = None
    READ_ONLY_PATTERN = False
    CONSUME_WHITESPACE = True

    def __init__(self, content:Union[List, str], strict=False):
        self._content = content

        if isinstance(content, str):
            self._content = content.splitlines(keepends=False)

        self._strict = strict

        self._pattern_misses = []
        self._pattern_skips = []

        self._reader_code_start = 0

        self._process_content()
        return

    def _get_preview_line(self, content_queue):

        preview_line = None

        for nxt_line in content_queue:
            if self.CONSUME_WHITESPACE and nxt_line.strip() == "":
                continue
            preview_line = nxt_line

        return preview_line

    def _process_content(self):

        pattern_queue = [p for p in self.EXPECTED_LINES]
        content_queue = [cl for cl in self._content]

        if len(pattern_queue) == 0:
            errmsg = "The 'EXPECTED_LINES' list must be a list with at least one 'RegExPattern' or 'RegExMultiPattern' object."
            raise AKitSemanticError(errmsg)

        current_pattern = None
        current_line = None
        strict = None

        while len(content_queue) > 0:

            current_line = content_queue.pop(0)
            if self.CONSUME_WHITESPACE:
                while current_line.strip() == "" and len(content_queue) > 0:
                    current_line = content_queue.pop(0)

            if current_line is None:
                break

            # If pattern was set to None then we either found a match and
            # the pattern that was matched was not a repeating patter or
            # it was a repeating pattern but the repeating condition was
            # terminated due to mis-match or match for a following pattern.
            if current_pattern is None:
                if len(pattern_queue) == 0:
                    break

                current_pattern = pattern_queue.pop(0)

                strict = self._strict
                if current_pattern.strict is not None:
                    strict = current_pattern.strict

            matches = None
            if isinstance(current_pattern, RegExPattern):

                matches = self._process_pattern_simple(current_pattern, current_line, strict)
                if matches is not None:
                    if not current_pattern.consume:
                        if current_pattern.match_type is None:
                            self._process_name_based_match(current_pattern, matches)
                        else:
                            self._process_match_type_based_match(current_pattern, matches)

            elif isinstance(current_pattern, RegExMultiPattern):

                matches = self._process_pattern_multimatch(current_pattern, content_queue, strict)
                if matches is not None:
                    if not current_pattern.consume:
                        if current_pattern.match_type is None:
                            self._process_name_based_match(current_pattern, matches)
                        else:
                            self._process_match_type_based_match(current_pattern, matches)

            else:
                errmsg = "The 'EXPECTED_LINES' list must be a list of 'RegExPattern' or 'RegExMultiPattern' objects."
                raise AKitSemanticError(errmsg)

            if matches is not None:
                if not current_pattern.repeats:
                    current_pattern = None

                elif len(pattern_queue) > 0 and len(content_queue) > 0:
                    # If we are processing a repeating pattern, we need to see if the next
                    # pattern is going to match and result in a termination of the current
                    # repeating pattern.

                    preview_pattern = pattern_queue[0]
                    preview_line = self._get_preview_line(content_queue)

                    if preview_line is not None:
                        # Perform a preview operation, if the next pattern is a match for the
                        # next line then clear the current pattern
                        pmobj = None
                        if isinstance(preview_pattern, RegExPattern):
                            pmobj = preview_pattern.pattern.match(preview_line)
                        elif isinstance(preview_pattern, RegExMultiPattern):
                            pmobj = preview_pattern.patterns[0].match(preview_line)
                        if pmobj is not None:
                            current_pattern = None
                    else:
                        current_pattern = None

        if len(self._pattern_misses) > 0 or len(pattern_queue) > 0:
            # We shouldn't have pattern misses, if we have a miss, let the
            # reader register bugs.
            self._pattern_misses.extend(pattern_queue)
            self._register_pattern_match_bugs()

        return

    def _process_match_type_based_match(self, pattern: RegExPattern, matches: dict):

        destname = pattern.destination if not self.READ_ONLY_PATTERN else "_" + self.READ_ONLY_PATTERN

        pitem = pattern.match_type(**matches)
        if pattern.repeats:
            getattr(self, destname).append(pitem)
        else:
            setattr(self, destname, pitem)

        return

    def _process_name_based_match(self, pattern: RegExPattern, matches: dict):

        for mname, mval in matches.items():
            destname = mname if not self.READ_ONLY_PATTERN else "_" + mname
            setattr(self, destname, mval)

        return

    def _process_pattern_multimatch(self, multi_pattern: RegExMultiPattern, current_line: str, content_queue: str, strict: bool):

        match_complete = False
        current_matches = {}

        exp_pattern_list = [p for p in multi_pattern.patterns]

        cqindex = 0
        cqlen = len(content_queue)

        while len(exp_pattern_list) > 0:

            current_pattern = exp_pattern_list.pop(0)
            mobj = current_pattern.match(current_line)
            if mobj is not None:
                current_matches.update(mobj.groupdict())
            else:
                match_complete = False
                break

            if cqindex < cqlen:
                current_line = content_queue[cqindex]
                if self.CONSUME_WHITESPACE and current_line.strip() == "":
                    while current_line.strip() == "" and cqindex < (cqlen - 1):
                        cqindex += 1
                        current_line = content_queue[cqindex]
            else:
                break

            cqindex += 1

        matches = None

        if match_complete:
            matches = current_matches
            
            # If we did find a match, we need to consume the rest of the lines from the
            # queue that we used to make the match
            while cqindex > 0 and len(content_queue) > 0:
                content_queue.pop(0)
                cqindex -= 1

        elif not match_complete and strict:
            append_line_count = len(multi_pattern.patterns) - 1

            errmsg_lines = [
                "Failed to match content line with a strict pattern match.",
                "REGEX: %r" % multi_pattern.patterns,
                "LINES:",
                "    {}".format(current_line)
            ]

            for nxtindex, nxtline in enumerate(content_queue):
                if nxtindex >= append_line_count:
                    break
                errmsg_lines.append("    {}".format(nxtline))

            errmsg = os.linesep(errmsg_lines)
            raise AKitReaderError(errmsg)
        else:
            self._pattern_misses.append(multi_pattern)

        return matches

    def _process_pattern_simple(self, regex_pattern: RegExPattern, current_line: str, strict: bool):

        matches = None

        mobj = regex_pattern.pattern.match(current_line)
        if mobj is not None:
            if not regex_pattern.consume:
                matches = mobj.groupdict()
            else:
                matches = {}
        elif strict:
            errmsg_lines = [
                "Failed to match content line with a strict pattern match.",
                "REGEX: %r" % regex_pattern.pattern,
                "LINE: %r" % current_line 
            ]
            errmsg = os.linesep(errmsg_lines)
            raise AKitReaderError(errmsg)
        else:
            self._pattern_misses.append(regex_pattern)

        return matches

    def _register_pattern_match_bugs(self):

        return
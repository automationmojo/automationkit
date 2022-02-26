
from typing import List, Optional, Tuple, Union

import os
import re

from akit.exceptions import AKitReaderError, AKitSemanticError

class RegExPattern:
    """
        The :class::`RegExPattern` object provides a way to combine a regular expression
        pattern with additional characteristic data that describe how the pattern should be
        used by the :class::`RegExReader` to match and process text content.
    """
    def __init__(self, pattern: Union[str, re.Pattern], *, exclass: str=None, required: bool=False,
                 repeats: bool=False, strict: Optional[bool]=None):
        self.pattern = pattern
        if isinstance(pattern, str):
            self.pattern = re.compile(pattern)
        self.exclass = exclass
        self.required = required
        self.repeats = repeats
        self.strict = strict
        return

    def __repr__(self) -> str:
        pattern_repr = 'RegExPattern(%r, exclass=%r, required=%r, repeats=%r, strict=%r)' % (
            self.pattern, self.exclass, self.required, self.repeats, self.strict
        )
        return pattern_repr

    def __str__(self) -> str:
        pattern_str = 'expr=%r exclass=%r required=%r repeats=%r strict=%r' % (
            self.pattern, self.exclass, self.required, self.repeats, self.strict
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

    EXPECTED_LINES: List[RegExPattern] = None

    def __init__(self, content:Union[List, str], strict=False, consume_whitespace_lines=True):
        self._content = content

        if isinstance(content, str):
            self._content = content.splitlines(keepends=False)

        self._strict = strict
        self._consume_whitespace_lines = consume_whitespace_lines

        self._pattern_misses = []
        self._pattern_skips = []

        self._reader_code_start = 0

        self._process_content()
        return

    def _process_content(self):

        pattern_queue = [p for p in self.EXPECTED_LINES]
        content_queue = [cl for cl in self._content]

        while len(pattern_queue) > 0:

            if len(content_queue) == 0:
                break

            repeats = False
            nxtpattern: RegExPattern = pattern_queue.pop(0)
            strict = self._strict
            if nxtpattern.strict is not None:
                strict = nxtpattern.strict

            if not isinstance(nxtpattern, RegExPattern):
                errmsg = "The 'EXPECTED_LINES' list must be a list of 'RegExReader' objects."
                raise AKitSemanticError(errmsg)

            found_at = []
            consumed_lines = []
            for nxtidx, nxtline in enumerate(content_queue):
                if self._consume_whitespace_lines and nxtline.strip() == "":
                    consumed_lines.append(nxtidx)
                    continue

                mobj = nxtpattern.pattern.match(nxtline)
                if mobj is not None:
                    found_at.append(nxtidx)
                    match_lookup = mobj.groupdict()
                    self._process_matches(nxtpattern, match_lookup)
                    if not repeats:
                        break

            if len(found_at) == 0:
                if nxtpattern.required:
                    if strict:
                        errmsg_lines = [
                            "There was a required regex match error attempting to process content.",
                            "REGEX: {}".format(str(nxtpattern)),
                            "CONTENT:"
                        ]
                        errmsg_lines.extend(self._content)
                        errmsg = os.linesep.join(errmsg_lines)
                        raise AKitReaderError(errmsg)
                    else:
                        self._pattern_misses.append(nxtpattern)
                else:
                    self._pattern_skips.append(nxtpattern)
            elif len(consumed_lines) > 0:
                # We have to pop out our consumed lines from highest to lowest
                # index so we don't modify the indexing of other lines we want
                # to pop when we pop a line.
                consumed_lines.extend(found_at)
                consumed_lines.sort()
                consumed_lines.reverse()
                for lidx in consumed_lines:
                    content_queue.pop(lidx)
            else:
                # We have to pop out our found_at lines from highest to lowest
                # index so we don't modify the indexing of other lines we want
                # to pop when we pop a line.
                found_at.sort()
                found_at.reverse()
                for fidx in found_at:
                    content_queue.pop(fidx)

        if len(self._pattern_misses) > 0 or len(pattern_queue) > 0:
            # We shouldn't have pattern misses, if we have a miss, let the
            # reader register bugs.
            self._pattern_misses.extend(pattern_queue)
            self._register_pattern_match_bugs()

        return

    def _process_matches(self, pattern: RegExPattern, matches: dict):
        return

    def _register_pattern_match_bugs(self):
        return
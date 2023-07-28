# -*- coding: utf-8 -*-

"""
The MIT License (MIT)

Copyright (c) 2022-present mccoderpy

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""

from __future__ import annotations

from typing import (
    TYPE_CHECKING,
    Union,
    Optional,
    Hashable,
    Sequence,
    Dict,
    Any,
    TypeVar
)


if TYPE_CHECKING:
    from _typeshed import SupportsWrite
    from regex import Match


import json
import colorama
import multidict
# We need to use regex instead of the builtin re module because the build-in one doesn't support recursive patterns
from regex import Pattern, compile as _re_compile
import collections.abc

from pprint import saferepr

__all__ = (
    'highlight_values',
    'color_dict',
    'color_dumps',
    'cprint'
)

colorama.init()
FORE = colorama.Fore
BACK = colorama.Back
RESET = FORE.RESET + BACK.RESET

DICT_TYPE = (
    dict,
    multidict.CIMultiDict,
    multidict.CIMultiDictProxy,
    multidict.MultiDict,
    multidict.MultiMapping,
    multidict.MultiDictProxy,
    multidict.MutableMultiMapping,
    collections.abc.Mapping,
    collections.abc.MappingView,
    collections.abc.MutableMapping,
)

T = TypeVar('T', bound=Union[Dict[Hashable, Any], str, Sequence, Any])
T_STR = TypeVar('T_STR', bound=str)
NoneType = type(None)

DOUBLE_QUOTE_REGEX = _re_compile(r'(?<!\\)"', cache_pattern=True)
REP_LIST_WITH_PARENTHESES_REGEX = _re_compile(
    r'(?!\x1b\[\d)\[(?P<before>\s*)__rep_list_with_(?P<p_start>[^,]), (?P<p_end>[^,])__,?\s*(?P<after>(?>\x1b\[|[^\][]|(?R))*+)\]',
    cache_pattern=True
)  # This one took me literally one day to get it work like it should :)


def highlight_values(
        target: T_STR,
        to_highlight: Union[str, bytes, Pattern, Sequence[Union[str, bytes, Pattern]]],
        foreground_color: Union[FORE, BACK] = FORE.LIGHTRED_EX,
        background_color: Union[FORE, BACK] = BACK.LIGHTYELLOW_EX,
        reset_color: Union[FORE, BACK] = BACK.RESET + FORE.RESET,
        *,
        highlight_groups: Sequence[str] = []
) -> T_STR:
    if not isinstance(to_highlight, Sequence):
        to_highlight = [to_highlight]
    for index, pattern in enumerate(to_highlight):
        if isinstance(pattern, Pattern):
            try:
                group = highlight_groups[index]
            except IndexError:
                group = 0
            target = pattern.sub(fr'{foreground_color}{background_color}\g<{group}>{reset_color}', target)
        else:
            target = target.replace(pattern, f'{foreground_color}{background_color}{pattern}{reset_color}')
    return target


def color_dict(
        obj: T,
        *,
        highlight: Sequence[Union[str, Pattern]] = None,
        highlight_groups: Sequence[str] = [],
        key_color: Union[FORE, BACK] = FORE.LIGHTRED_EX,
        bool_color: Union[FORE, BACK] = FORE.LIGHTBLUE_EX,
        int_color: Union[FORE, BACK] = FORE.BLUE,
        str_color: Union[FORE, BACK] = FORE.YELLOW,
        highlight_color_fg: Union[FORE, BACK] = FORE.LIGHTRED_EX,
        highlight_color_bg: Union[FORE, BACK] = BACK.LIGHTYELLOW_EX,
        __is_key: bool = False
) -> T:
    if not isinstance(obj, (list, tuple, set, *DICT_TYPE)):
        if isinstance(obj, (bool, NoneType)):
            c_type = bool_color
            obj = f'{bool_color}{obj}{RESET}'
        elif isinstance(obj, (int, float)):
            c_type = int_color
            obj = f'{int_color}{obj}{RESET}'
        elif isinstance(obj, str):
            c_type = str_color
            if not __is_key:
                obj = f'{str_color}\'{obj}\'{RESET}'
            else:
                obj = f'{key_color}{obj}{RESET}'
        else:
            c_type = FORE.RESET
            obj = f'{str_color}{obj if type(obj).__module__ != "builtins" else saferepr(obj)}{c_type}'
        if highlight:
            obj = highlight_values(
                obj,
                highlight,
                foreground_color=highlight_color_fg,
                background_color=highlight_color_bg,
                reset_color=c_type,
                highlight_groups=highlight_groups
            )
        return obj
    else:
        if isinstance(obj, (list, tuple, set)):
            after_dump_instruction = None
            obj_type = type(obj)
            if obj_type in (tuple, set):
                # So we can cast it to show as the original type after dumping, terrible solution, but it works for now
                after_dump_instruction = f'__rep_list_with_{"(, )" if obj_type is tuple else "{, }"}__'
            to_return = [
                    color_dict(
                        value,
                        key_color=key_color,
                        bool_color=bool_color,
                        int_color=int_color,
                        str_color=str_color,
                        highlight_color_bg=highlight_color_bg,
                        highlight_color_fg=highlight_color_fg,
                        highlight=highlight,
                        highlight_groups=highlight_groups
                    ) for value in obj
                ]
            if after_dump_instruction:
                to_return = [after_dump_instruction, *to_return]
            return to_return
        elif isinstance(obj, DICT_TYPE):
            return {
                color_dict(
                    k,
                    key_color=key_color,
                    bool_color=bool_color,
                    int_color=int_color,
                    str_color=str_color,
                    highlight_color_bg=highlight_color_bg,
                    highlight_color_fg=highlight_color_fg,
                    highlight=highlight,
                    highlight_groups=highlight_groups,
                    __is_key=True
                ): color_dict(
                    v,
                    key_color=key_color,
                    bool_color=bool_color,
                    int_color=int_color,
                    str_color=str_color,
                    highlight_color_bg=highlight_color_bg,
                    highlight_color_fg=highlight_color_fg,
                    highlight=highlight,
                    highlight_groups=highlight_groups
                )
                for k, v in obj.items()
            }


def color_dumps(
        obj: T,
        highlight: Sequence[Union[str, Pattern]] = None,
        highlight_groups: Sequence[str] = [],
        key_color: Union[FORE, BACK] = FORE.LIGHTRED_EX,
        bool_color: Union[FORE, BACK] = FORE.LIGHTBLUE_EX,
        int_color: Union[FORE, BACK] = FORE.BLUE,
        str_color: Union[FORE, BACK] = FORE.YELLOW,
        highlight_color_fg: Union[FORE, BACK] = FORE.LIGHTRED_EX,
        highlight_color_bg: Union[FORE, BACK] = BACK.LIGHTYELLOW_EX,
        **kwargs
) -> str:
    result = color_dict(
        obj=obj,
        highlight=highlight,
        highlight_groups=highlight_groups,
        key_color=key_color,
        bool_color=bool_color,
        int_color=int_color,
        str_color=str_color,
        highlight_color_fg=highlight_color_fg,
        highlight_color_bg=highlight_color_bg,
    )
    try:
        as_str = json.dumps(
            result,
            separators=(', ', f'{FORE.RED}:{FORE.RESET} '),
            **kwargs
        )
        as_str = DOUBLE_QUOTE_REGEX.sub("", as_str)
        as_str = as_str.replace('\\u001b', '\033')
        if '__rep_list_with_' in as_str:  # save some time if there is no need to performe the regex
            for match in REP_LIST_WITH_PARENTHESES_REGEX.finditer(as_str, overlapped=True):
                match: Match[str]
                as_str = as_str.replace(
                    match.group(),  # type: ignore
                    f'{match["p_start"]}{match["before"]}{match["after"]}{match["p_end"]}'
                )

    except Exception as exc:
        print(exc)
        return str(result)
    else:
        return as_str


def cprint(
        *values: object,
        highlight: Sequence[Union[str, Pattern]] = None,
        highlight_groups: Sequence[str] = [],
        key_color: Union[FORE, BACK] = FORE.LIGHTRED_EX,
        bool_color: Union[FORE, BACK] = FORE.LIGHTBLUE_EX,
        int_color: Union[FORE, BACK] = FORE.BLUE,
        str_color: Union[FORE, BACK] = FORE.YELLOW,
        highlight_color_fg: Union[FORE, BACK] = FORE.LIGHTRED_EX,
        highlight_color_bg: Union[FORE, BACK] = BACK.LIGHTYELLOW_EX,
        sep: Optional[str] = ' ',
        end: Optional[str] = '\n',
        file: SupportsWrite[str] = None,
        flush: bool = False,
        indent: int = 4,
        **kwargs

) -> None:
    print(
        sep.join(
            [
                color_dumps(
                    value,
                    highlight=highlight,
                    highlight_groups=highlight_groups,
                    key_color=key_color,
                    bool_color=bool_color,
                    int_color=int_color,
                    str_color=str_color,
                    highlight_color_fg=highlight_color_fg,
                    highlight_color_bg=highlight_color_bg,
                    indent=indent,
                    **kwargs
                ) for value in values
            ]
        ),
        end=end,
        file=file,
        flush=flush
    )

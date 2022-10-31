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
    Pattern,
    Dict,
    Any,
    TypeVar
)

if TYPE_CHECKING:
    from _typeshed import SupportsWrite

import json
import colorama
import multidict
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
        if isinstance(obj, DICT_TYPE):
            colored_obj = dict()
            for key, value in obj.items():
                colored_obj[
                    color_dict(
                        key,
                        key_color=key_color,
                        bool_color=bool_color,
                        int_color=int_color,
                        str_color=str_color,
                        highlight_color_bg=highlight_color_bg,
                        highlight_color_fg=highlight_color_fg,
                        highlight=highlight,
                        highlight_groups=highlight_groups,
                        __is_key=True
                    )
                ] = color_dict(
                        value,
                        key_color=key_color,
                        bool_color=bool_color,
                        int_color=int_color,
                        str_color=str_color,
                        highlight_color_bg=highlight_color_bg,
                        highlight_color_fg=highlight_color_fg,
                        highlight=highlight,
                        highlight_groups=highlight_groups
                    )
        else:
            colored_obj = type(obj)()
            for value in obj:
                if isinstance(colored_obj, (list, tuple)):
                    colored_obj.__iadd__([
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
                        )
                    ])
                elif isinstance(obj, DICT_TYPE):
                    new_value = {}
                    for k, v in value.items():
                        new_value[
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
                            )
                        ] = color_dict(
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
                    colored_obj.append(new_value)
                else:
                    colored_obj.append(
                        color_dict(
                            value,
                            key_color=key_color,
                            bool_color=bool_color,
                            int_color=int_color,
                            highlight_color_bg=highlight_color_bg,
                            highlight_color_fg=highlight_color_fg,
                            str_color=str_color,
                            highlight=highlight,
                            highlight_groups=highlight_groups
                        )
                    )
        return colored_obj


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
            ensure_ascii=False,
            **kwargs
        )
    except Exception as exc:
        print(exc)
        return str(result)
    else:
        return as_str.replace('\\u001b', '\033').replace('"', '')


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

# -*- coding: utf-8 -*-

"""
A simple package to pretty-print lists dicts, tuples, etc. with color and highlight

The MIT License (MIT)

Copyright (c) 2021-present mccoderpy

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

import sys
import json
from . import *
from os import PathLike


def exit_with_help():
    sys.exit(
        "Usage:\n\n"
        "<python> -m color_pprint [--ansi/-a] [--discord/-d] [--file/-f <FILE_TO_WRITE_TO>] <[value/PATH_TO_READ_FROM,]>\n\n"
        "Example: \"py -m color_pprint --file ./test.json --discord '{\"hello\": \"world\", \"something\": 1234}'\""
    )


def open_file(path: PathLike):
    return open(path, "a+", encoding='utf-8')


if __name__ == '__main__':
    args: list[str | PathLike] = sys.argv[1:]
    if not args or '--help' in args:
        print('A simple package to pretty-print lists dicts, tuples, etc. with color and highlight - (c) 2022-present mccoderpy')
        exit_with_help()

    values = []
    mode = 'default'
    file = sys.stdout
    kwargs = {}

    for i, option in enumerate(args):
        if option.startswith('-'):
            o = option.strip('-').lower()
            if o in ('a', 'ansi'):
                mode = 'ansi'
            elif o in ('f', 'file'):
                try:
                    file_name = args.pop(i+1)
                except IndexError:
                    print('Missing file name after --file parameter')
                    exit_with_help()
                else:
                    try:
                        file = open_file(file_name)
                    except OSError as exc:
                        print(f'Failed to open file "{file_name}" due to {exc.__class__.__name__}:\n')
                        raise exc from None
            elif o in ('d', 'discord'):
                kwargs.update(
                    key_color="\u001B[31m",
                    str_color="\u001B[33m"
                )
            else:
                print(f'Invalid option "{option}"')
                exit_with_help()
        else:
            values.append(option)

    if not len(values):
        exit_with_help()

    if mode == 'ansi':
        for index, input_or_path in enumerate(values):
            try:
                with open(input_or_path) as fp:
                    value = json.load(fp)
            except FileNotFoundError as exc:
                print(f'Failed to parse input value at position {index} due to FileNotFoundError:\n')
                raise exc from None
            except OSError as origin_exc:
                if origin_exc.strerror.startswith('Invalid argument'):  # expect it is not a valid path here
                    try:
                        value = json.loads(input_or_path)
                    except json.JSONDecodeError as exc:
                        print(f'Failed to parse input value at position {index} due to JSONDecodeError:\n')
                        raise exc from None
                else:  # Some other error occurred - re-raise
                    print(f'Failed to parse input value at position {index} due to {origin_exc.__class__.__name__}:\n')
                    raise origin_exc from None

            print(color_dict(value, **kwargs), file=file)
    else:
        for index, input_or_path in enumerate(values):
            try:
                with open(input_or_path) as fp:
                    value = json.load(fp)
            except FileNotFoundError as exc:
                print(f'Failed to parse input value at position {index} due to FileNotFoundError:\n')
                raise exc from None
            except OSError as origin_exc:
                if origin_exc.strerror.startswith('Invalid argument'):  # expect it is not a valid path here
                    try:
                        value = json.loads(input_or_path)
                    except json.JSONDecodeError as exc:
                        print(f'Failed to parse input value at position {index} due to JSONDecodeError:\n')
                        raise exc from None
                else:  # Some other error occurred - re-raise
                    print(f'Failed to parse input value at position {index} due to {origin_exc.__class__.__name__}:\n')
                    raise origin_exc from None

            cprint(value, file=file, ensure_ascii=False, **kwargs)

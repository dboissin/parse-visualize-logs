#!/usr/bin/python
# -*- coding: utf-8 -*-

from distutils.core import setup, Extension

def main():
    setup(
        name = "parse",
        version = "1.0",
        ext_modules = [Extension("parse", ["bind.c", "parse.c", "ranges.c"])]
    )

if __name__ == "__main__":
    main()

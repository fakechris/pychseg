#!/usr/bin/env python

"""
setup.py file for SWIG example
"""

from distutils.core import setup, Extension

pydarts_module = Extension('_pydarts',
                           sources=['pydarts_wrap.cxx'],
                           )

setup (name = 'pydarts',
       version = '0.1',
       author      = "SWIG Docs",
       description = """Simple swig example from docs""",
       ext_modules = [pydarts_module],
       py_modules = ["pydarts"],
       )


from __future__ import absolute_import, division, print_function, unicode_literals

from importlib import import_module

# From echomesh/code/python/echomesh/util/Importer.py

def import_function(classpath):
    parts = classpath.split('.')
    function = parts.pop()

    return getattr(import_module('.'.join(parts)), function)

def import_symbol(classpath):
    try:
        return import_module(classpath)
    except ImportError:
        return import_function(classpath)

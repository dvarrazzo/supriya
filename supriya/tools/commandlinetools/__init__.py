# -*- encoding: utf-8 -*-

"""
Tools for Supriya's project maintenance scripts.
"""

from abjad.tools import systemtools

systemtools.ImportManager.import_structured_package(
    __path__[0],
    globals(),
    )

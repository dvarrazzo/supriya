# -*- encoding: utf-8 -*-
from supriya.tools import systemlib

systemlib.ImportManager.import_structured_package(
    __path__[0],
    globals(),
    )
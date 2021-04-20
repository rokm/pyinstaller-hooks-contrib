# ------------------------------------------------------------------
# Copyright (c) 2021 PyInstaller Development Team.
#
# This file is distributed under the terms of the GNU General Public
# License (version 2.0 or later).
#
# The full license is available in LICENSE.GPL.txt, distributed with
# this software.
#
# SPDX-License-Identifier: GPL-2.0-or-later
# ------------------------------------------------------------------

import sys
import pathlib

from PyInstaller.utils.hooks import exec_statement
from PyInstaller.utils.hooks import logger


def pre_find_module_path(hook_api):
    # Check if OpenCV is compiled from source, in which case cv2 is not
    # a binary module, but a loader package that eventually replaces the
    # reference to itself with a forward to the module stored in the
    # cv2/python-3.x subfolder. So import cv2 in a subprocess, and
    # retrieve its path...
    cv2_file = None
    out = exec_statement("""
        import cv2
        print('\\n$_pyi:' + cv2.__file__ + '*')
        """)
    for line in out.split():
        if line.startswith("$_pyi:") and line.endswith("*"):
            cv2_file = pathlib.Path(line[6:-1])
            break

    # Check if module file's parent directory is cv2/python-3.x
    python_3x = "python-{}.{}".format(*sys.version_info[:2])  # python-3.x
    compiled_from_source = cv2_file is not None and \
        cv2_file.parent.name == python_3x and \
        cv2_file.parent.parent.name == "cv2"
    if not compiled_from_source:
        return

    # Completely override the search path to avoid picking up any traces
    # of the cv2 loader package.
    cv2_search_path = str(cv2_file.parent)
    logger.info("cv2: overriding search path for cv2 module to %r to bypass "
                "the loader package", cv2_search_path)
    hook_api.search_dirs = [cv2_search_path]

# ------------------------------------------------------------------
# Copyright (c) 2020 PyInstaller Development Team.
#
# This file is distributed under the terms of the GNU General Public
# License (version 2.0 or later).
#
# The full license is available in LICENSE, distributed with
# this software.
#
# SPDX-License-Identifier: GPL-2.0-or-later
# ------------------------------------------------------------------

import sys

from PyInstaller import compat

__version__ = '2025.7'
__maintainer__ = 'Legorooj, bwoodsend'
__uri__ = 'https://github.com/pyinstaller/pyinstaller-hooks-contrib'


def get_hook_dirs():
    import os
    hooks_dir = os.path.dirname(__file__)
    return [
        # Required because standard hooks are in sub-directory instead of the top-level hooks directory.
        os.path.join(hooks_dir, 'stdhooks'),
        # pre_* and run-time hooks
        hooks_dir,
    ]


# Several packages for which provide hooks are involved in deep dependency chains when various optional dependencies are
# installed in the environment, and their analysis typically requires recursion limit that exceeds the default 1000.
# Therefore, automatically raise the recursion limit to at least 5000. This alleviates the need to do so on per-hook
# basis.
if (compat.is_win or compat.is_cygwin) and not compat.is_py311:
    # The recursion limit test in PyInstaller repository seems to be crashing python interpreter under Windows and
    # Cygwin with python < 3.11 when recursion limit is raised to 5000. In fact, with python 3.8, the crash seems
    # to occur if recursion limit is set above 2097. So for combinations of affected platforms and python versions,
    # use more conservative value for the new recursion limit.
    new_recursion_limit = 2100
else:
    new_recursion_limit = 5000
if sys.getrecursionlimit() < new_recursion_limit:
    sys.setrecursionlimit(new_recursion_limit)

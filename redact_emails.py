# =========================================================
# MIT license.
#
# (c) 2025 Aportio Developments Ltd.
# =========================================================

"""
Tool to pre-process bulk import files into JSON
"""

import json
from typing import Optional
import uuid

from import_handlers import (
    VALID_FIELDS,
    import_spreadsheet,
    import_pst,
)




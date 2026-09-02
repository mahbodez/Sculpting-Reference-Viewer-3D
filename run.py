#!/usr/bin/env python
"""Launch the viewer straight from a source checkout, without installing."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from refview.application import main  # noqa: E402

if __name__ == "__main__":
    main()

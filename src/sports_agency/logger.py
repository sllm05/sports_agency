"""
Project Work & Runtime Logger (`src/sports_agency/logger.py`)

Enforces Project Rule #2:
- Maintains `work.log` (chronological record of all engineering/system tasks and live executions).
"""

from __future__ import annotations

import logging
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
WORK_LOG_PATH = PROJECT_ROOT / "work.log"

logger = logging.getLogger("sports_agency")
if not logger.handlers:
    logger.setLevel(logging.INFO)
    file_handler = logging.FileHandler(WORK_LOG_PATH, encoding="utf-8")
    formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)


def log_work_event(category: str, detail: str) -> None:
    """Appends a structured work or runtime event to `work.log`."""
    logger.info(f"[{category}] {detail}")

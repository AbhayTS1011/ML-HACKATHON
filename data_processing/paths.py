"""Shared path settings for the processing and feature engineering stages.

Both stages read and write the shared artifacts folder, so they can use the same outputs.
Override with environment variables:
  PATHSNAP_DATA       folder that contains train/ and student_test/   (default: <split root>/../Student folder)
  PATHSNAP_ARTIFACTS  shared artifacts folder                          (default: <split root>/artifacts)
"""
import os
from pathlib import Path

SPLIT_ROOT = Path(__file__).resolve().parents[1]
ARTIFACTS = Path(os.environ.get("PATHSNAP_ARTIFACTS", SPLIT_ROOT.parent / "artifacts"))
DATA_ROOT = Path(os.environ.get("PATHSNAP_DATA", SPLIT_ROOT.parent.parent / "Student folder"))


def ART(sub: str = "") -> str:
    """Path inside the shared artifacts folder (parent folders are created)."""
    p = ARTIFACTS / sub
    p.parent.mkdir(parents=True, exist_ok=True)
    return str(p)


def DATA(partition: str) -> str:
    """Path of a dataset partition folder, e.g. DATA("train")."""
    return str(DATA_ROOT / partition)

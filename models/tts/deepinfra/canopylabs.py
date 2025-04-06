"""Canopylabs model."""

from enum import Enum


ORPHEUS_3B: str = "canopylabs/orpheus-3b-0.1-ft"


class OrpheusVoices(Enum):
    """Orpheus voices."""

    TARA = "tara"
    LEAH = "leah"
    JESS = "jess"
    LEO = "leo"
    DAN = "dan"
    MIA = "mia"
    ZAC = "zac"

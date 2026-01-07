import os
import sys

def resource_path(relative_path: str) -> str:
    """
    Returns a correct resource path for both PyInstaller EXE and dev mode.
    """
    if hasattr(sys, '_MEIPASS'):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

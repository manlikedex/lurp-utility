import os
import shutil

def folder_size(path):
    total = 0
    for root, dirs, files in os.walk(path, topdown=True):
        for f in files:
            try:
                total += os.path.getsize(os.path.join(root, f))
            except:
                pass
    return total

def get_storage_analysis():
    """Return a dict of estimated space reclaimable across FiveM, GTA, Temp."""
    paths = {
        "FiveM Cache": r"%localappdata%\FiveM\FiveM.app\data\cache",
        "FiveM Logs": r"%localappdata%\FiveM\FiveM.app\logs",
        "Shader Cache": r"%localappdata%\Rockstar Games\GTA V\Shaders",
        "Windows Temp": r"%temp%",
    }

    result = {}

    for label, p in paths.items():
        p = os.path.expandvars(p)
        if os.path.exists(p):
            result[label] = folder_size(p)
        else:
            result[label] = 0

    result["Total"] = sum(result.values())
    return result

import os
import shutil


# -------------------------------
#  Helper: Safe delete folder
# -------------------------------
def safe_delete(path):
    """
    Deletes a folder safely.
    """
    try:
        if os.path.exists(path):
            shutil.rmtree(path, ignore_errors=True)
    except Exception as e:
        print(f"Failed to delete {path}: {e}")


# -------------------------------
#  CLEANING FUNCTIONS
# -------------------------------
def clear_fivem_cache():
    """
    Clears FiveM's main cache.
    """
    cache_paths = [
        r"%localappdata%\FiveM\FiveM.app\data\cache",
        r"%localappdata%\FiveM\FiveM.app\data\nui-storage",
        r"%localappdata%\FiveM\FiveM.app\data\server-cache",
    ]

    for p in cache_paths:
        safe_delete(os.path.expandvars(p))


def clear_fivem_logs():
    """
    Clears FiveM logs, crashes, and dumps.
    """
    paths = [
        r"%localappdata%\FiveM\FiveM.app\logs",
        r"%localappdata%\FiveM\FiveM.app\crashes",
        r"%localappdata%\FiveM\FiveM.app\crash-reports",
    ]

    for p in paths:
        safe_delete(os.path.expandvars(p))


def clear_temp_files():
    """
    Clears Windows temp folder.
    """
    temp = os.path.expandvars(r"%temp%")
    safe_delete(temp)
    os.makedirs(temp, exist_ok=True)


def clear_gta_shader_cache():
    """
    Clears GTA V shader cache folder.
    """
    shader = os.path.expandvars(r"%localappdata%\Rockstar Games\GTA V\Shaders")
    safe_delete(shader)
    os.makedirs(shader, exist_ok=True)

import os
import socket
import shutil
import subprocess
import requests


def folder_exists(path):
    return os.path.exists(os.path.expandvars(path))


def get_folder_size(path):
    try:
        total = 0
        for root, _, files in os.walk(os.path.expandvars(path)):
            for f in files:
                fp = os.path.join(root, f)
                total += os.path.getsize(fp)
        return total
    except:
        return 0


def run_all_checks():
    """
    Runs all diagnostics and returns a result dictionary.
    Each item: { 'status': bool, 'message': str }
    """

    results = {}

    # --------------------------------
    # 1. FiveM Folder Check
    # --------------------------------
    fivem_path = r"%localappdata%\FiveM\FiveM.app"
    exists = folder_exists(fivem_path)

    results["FiveM Installation"] = {
        "status": exists,
        "message": "FiveM installation folder located." if exists else
                   "FiveM folder not found. Please ensure FiveM is installed."
    }

    # --------------------------------
    # 2. GTA Shader Cache Check
    # --------------------------------
    shader_path = r"%localappdata%\Rockstar Games\GTA V\Shaders"
    shader_exists = folder_exists(shader_path)

    shader_size = get_folder_size(shader_path) if shader_exists else 0
    shader_large = shader_size > (300 * 1024 * 1024)  # 300MB threshold

    if shader_exists and not shader_large:
        s_msg = "Shader cache healthy."
    elif shader_exists and shader_large:
        s_msg = f"Shader cache too large ({shader_size/1024/1024:.1f} MB). Cleaning recommended."
    else:
        s_msg = "Shader folder missing. GTA V may not be installed correctly."

    results["GTA Shader Cache"] = {
        "status": shader_exists and not shader_large,
        "message": s_msg
    }

    # --------------------------------
    # 3. Windows Temp Folder Size
    # --------------------------------
    temp_path = r"%temp%"
    temp_size = get_folder_size(temp_path)
    temp_large = temp_size > (500 * 1024 * 1024)  # 500MB

    results["Windows Temp Folder"] = {
        "status": not temp_large,
        "message": (
            f"Temp folder size OK ({temp_size/1024/1024:.1f} MB)."
            if not temp_large else
            f"Temp folder very large ({temp_size/1024/1024:.1f} MB). Cleaning recommended."
        )
    }

    # --------------------------------
    # 4. DNS Resolution Check
    # --------------------------------
    try:
        socket.gethostbyname("google.com")
        dns_ok = True
        dns_msg = "DNS resolution working normally."
    except:
        dns_ok = False
        dns_msg = "DNS resolution failed. Try using Flush DNS in Tools."

    results["DNS Resolution"] = {
        "status": dns_ok,
        "message": dns_msg
    }

    # --------------------------------
    # 5. Internet Connectivity
    # --------------------------------
    try:
        requests.get("https://google.com", timeout=3)
        net_ok = True
        net_msg = "Internet connection looks good."
    except:
        net_ok = False
        net_msg = "Cannot reach the internet. Check your network."

    results["Internet Connectivity"] = {
        "status": net_ok,
        "message": net_msg
    }

    # --------------------------------
    # 6. Disk Space
    # --------------------------------
    try:
        total, used, free = shutil.disk_usage("C:\\")
        low = free < (10 * 1024 * 1024 * 1024)  # < 10GB
        results["Disk Space (C:)"] = {
            "status": not low,
            "message": (
                f"Free space OK ({free/1024/1024/1024:.1f} GB free)."
                if not low else
                f"Low disk space ({free/1024/1024/1024:.1f} GB free). Clean-up recommended."
            )
        }
    except:
        results["Disk Space (C:)"] = {
            "status": False,
            "message": "Unable to check disk space."
        }

    # --------------------------------
    # 7. FiveM Crash Logs
    # --------------------------------
    logs_path = r"%localappdata%\FiveM\FiveM.app\crashes"
    logs_exist = folder_exists(logs_path)

    log_files = 0
    if logs_exist:
        try:
            log_files = len(os.listdir(os.path.expandvars(logs_path)))
        except:
            pass

    too_many_logs = log_files > 20

    results["FiveM Crash Logs"] = {
        "status": not too_many_logs,
        "message": (
            f"Crash log count OK ({log_files} files)."
            if not too_many_logs else
            f"High number of crash logs ({log_files}). Consider clearing them."
        )
    }

    return results

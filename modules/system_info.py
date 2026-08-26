import platform
import socket
import shutil

from modules.logger import log_info, log_error


def show_system_info():
    try:
        print("\n" + "=" * 45)
        print("          SYSTEM INFORMATION")
        print("=" * 45)

        print(f"Hostname:         {socket.gethostname()}")
        print(f"Operating System: {platform.system()} {platform.release()}")
        print(f"Architecture:     {platform.machine()}")
        print(f"Python Version:   {platform.python_version()}")

        total, used, free = shutil.disk_usage("/")

        print("\nDisk Information:")
        print(f"Total:            {total // (1024**3)} GB")
        print(f"Used:             {used // (1024**3)} GB")
        print(f"Free:             {free // (1024**3)} GB")

        print("=" * 45)

        log_info("System information retrieved successfully.")

    except Exception as e:
        print(f"\nError retrieving system information: {e}")
        log_error(f"System information error: {e}")
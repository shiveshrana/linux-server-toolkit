import subprocess
import time

import psutil

from modules.logger import log_info, log_warning, log_error


def show_status(name, value, warning_threshold=80):
    if value >= warning_threshold:
        status = "WARNING"
        log_warning(f"{name} is high: {value}%")
    else:
        status = "OK"

    print(f"{name:<20}: {value}% [{status}]")


def check_failed_services():
    try:
        result = subprocess.run(
            ["systemctl", "--failed", "--no-legend"],
            capture_output=True,
            text=True,
            timeout=10
        )

        if result.returncode != 0:
            print("\nUnable to check failed services.")
            log_error("systemctl --failed returned an error.")
            return

        failed_services = result.stdout.strip()

        if failed_services:
            print("\nFailed Services:")
            print(failed_services)
            log_warning("One or more failed services detected.")
        else:
            print("\nFailed Services     : None [OK]")
            log_info("No failed services detected.")

    except FileNotFoundError:
        print("\nsystemctl is not available.")
        log_error("systemctl command not found.")

    except subprocess.TimeoutExpired:
        print("\nService check timed out.")
        log_error("systemctl service check timed out.")

    except Exception as e:
        print(f"\nError checking services: {e}")
        log_error(f"Failed service check error: {e}")


def run_health_check():
    try:
        print("\n" + "=" * 45)
        print("             SERVER HEALTH CHECK")
        print("=" * 45)

        cpu_usage = psutil.cpu_percent(interval=1)
        show_status("CPU Usage", cpu_usage)

        memory = psutil.virtual_memory()
        show_status("RAM Usage", memory.percent)

        disk = psutil.disk_usage("/")
        show_status("Disk Usage", disk.percent)

        boot_time = psutil.boot_time()
        uptime_seconds = int(time.time() - boot_time)

        hours = uptime_seconds // 3600
        minutes = (uptime_seconds % 3600) // 60

        print(f"System Uptime       : {hours}h {minutes}m")

        check_failed_services()

        print("=" * 45)

        log_info("Health check completed successfully.")

    except Exception as e:
        print(f"\nHealth check failed: {e}")
        log_error(f"Health check error: {e}")
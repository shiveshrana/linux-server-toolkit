import os
import time
import platform
import socket
import subprocess

import psutil

from modules.logger import log_info, log_warning, log_error


REPORT_DIR = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "..",
        "reports"
    )
)


def get_failed_services():
    try:
        result = subprocess.run(
            ["systemctl", "--failed", "--no-legend"],
            capture_output=True,
            text=True,
            timeout=10
        )

        if result.returncode != 0:
            log_error("Failed to retrieve systemd services.")
            return None

        return result.stdout.strip()

    except Exception as e:
        log_error(f"Failed service check error: {e}")
        return None


def generate_report():
    try:
        os.makedirs(REPORT_DIR, exist_ok=True)

        hostname = socket.gethostname()
        operating_system = f"{platform.system()} {platform.release()}"

        cpu = psutil.cpu_percent(interval=1)
        ram = psutil.virtual_memory().percent
        disk = psutil.disk_usage("/").percent

        boot_time = psutil.boot_time()
        uptime_seconds = int(time.time() - boot_time)

        hours = uptime_seconds // 3600
        minutes = (uptime_seconds % 3600) // 60

        failed_services = get_failed_services()

        problems = []

        if cpu >= 80:
            problems.append("High CPU usage")

        if ram >= 80:
            problems.append("High RAM usage")

        if disk >= 80:
            problems.append("High disk usage")

        if failed_services is None:
            problems.append("Unable to check services")
        elif failed_services:
            problems.append("Failed systemd services detected")

        if problems:
            overall_status = "WARNING"
        else:
            overall_status = "PASS"

        timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")

        report_file = os.path.join(
            REPORT_DIR,
            f"health_report_{timestamp}.txt"
        )

        with open(report_file, "w") as report:
            report.write("=" * 55 + "\n")
            report.write("       LINUX SERVER HEALTH REPORT\n")
            report.write("=" * 55 + "\n\n")

            report.write(f"Hostname:          {hostname}\n")
            report.write(f"Operating System:  {operating_system}\n")
            report.write(f"CPU Usage:         {cpu}%\n")
            report.write(f"RAM Usage:         {ram}%\n")
            report.write(f"Disk Usage:        {disk}%\n")
            report.write(f"System Uptime:     {hours}h {minutes}m\n")
            report.write(f"Overall Status:    {overall_status}\n\n")

            report.write("-" * 55 + "\n")
            report.write("FAILED SERVICES\n")
            report.write("-" * 55 + "\n")

            if failed_services:
                report.write(failed_services + "\n")
            else:
                report.write("None\n")

            report.write("\n" + "-" * 55 + "\n")
            report.write("ISSUES DETECTED\n")
            report.write("-" * 55 + "\n")

            if problems:
                for problem in problems:
                    report.write(f"- {problem}\n")
            else:
                report.write("No issues detected.\n")

            report.write("\n" + "=" * 55 + "\n")

        print("\n" + "=" * 55)
        print("          FULL SERVER CHECK")
        print("=" * 55)

        print(f"Hostname:        {hostname}")
        print(f"Operating System:{operating_system}")
        print(f"CPU Usage:       {cpu}%")
        print(f"RAM Usage:       {ram}%")
        print(f"Disk Usage:      {disk}%")
        print(f"Uptime:          {hours}h {minutes}m")

        if failed_services:
            print("Failed Services: WARNING")
        else:
            print("Failed Services: OK")

        print(f"\nOverall Status:  {overall_status}")
        print(f"\nReport saved to:")
        print(report_file)

        print("=" * 55)

        if overall_status == "PASS":
            log_info("Full server check completed: PASS")
        else:
            log_warning(
                f"Full server check completed with issues: {problems}"
            )

    except PermissionError:
        print("\nPermission denied while creating the report.")
        log_error("Permission denied while creating health report.")

    except OSError as e:
        print(f"\nFile system error: {e}")
        log_error(f"Health report file system error: {e}")

    except Exception as e:
        print(f"\nFull server check failed: {e}")
        log_error(f"Full server check error: {e}")
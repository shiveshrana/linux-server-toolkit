import os
import shutil
import platform

from modules.logger import log_info, log_error


REQUIRED_COMMANDS = [
    "bash",
    "sudo",
    "systemctl",
]


def check_operating_system():
    """Check whether the toolkit is running on Linux."""

    if platform.system() != "Linux":
        print("ERROR: This toolkit requires Linux.")
        log_error(
            f"Unsupported operating system: {platform.system()}"
        )
        return False

    return True


def check_commands():
    """Check whether required Linux commands are available."""

    missing_commands = []

    for command in REQUIRED_COMMANDS:
        if shutil.which(command) is None:
            missing_commands.append(command)

    if missing_commands:
        print("\nMissing required commands:")

        for command in missing_commands:
            print(f"  - {command}")

        log_error(
            f"Missing required commands: {', '.join(missing_commands)}"
        )

        return False

    return True


def check_directories():
    """Ensure required project directories exist."""

    directories = [
        "logs",
        "reports",
    ]

    try:
        project_root = os.path.abspath(
            os.path.join(
                os.path.dirname(__file__),
                ".."
            )
        )

        for directory in directories:
            path = os.path.join(project_root, directory)
            os.makedirs(path, exist_ok=True)

        return True

    except OSError as e:
        print(f"\nUnable to create required directories: {e}")
        log_error(f"Directory setup failed: {e}")
        return False


def run_environment_check():
    """Run all environment checks."""

    print("\n" + "=" * 50)
    print("             ENVIRONMENT CHECK")
    print("=" * 50)

    checks_passed = True

    print("\n[1] Operating System")
    if check_operating_system():
        print("    Linux detected [OK]")
    else:
        checks_passed = False

    print("\n[2] Required Commands")

    if check_commands():
        print("    Required commands available [OK]")
    else:
        checks_passed = False

    print("\n[3] Project Directories")

    if check_directories():
        print("    Required directories available [OK]")
    else:
        checks_passed = False

    print("\n" + "-" * 50)

    if checks_passed:
        print("Environment Check: PASS")
        log_info("Environment check passed.")
    else:
        print("Environment Check: FAIL")
        log_error("Environment check failed.")

    print("=" * 50)

    return checks_passed
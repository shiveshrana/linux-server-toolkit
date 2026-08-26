import os
import shutil

from modules.logger import log_info, log_warning, log_error


def is_root():
    """Check whether the current process is running as root."""

    try:
        return os.geteuid() == 0

    except AttributeError:
        log_error("Unable to determine root privileges.")
        return False

    except Exception as e:
        log_error(f"Root privilege check failed: {e}")
        return False


def has_sudo():
    """Check whether sudo is available."""

    try:
        if shutil.which("sudo") is None:
            log_error("sudo command not found.")
            return False

        return True

    except Exception as e:
        log_error(f"sudo check failed: {e}")
        return False


def require_sudo():
    """Verify that sudo is available before privileged operations."""

    if is_root():
        return True

    if not has_sudo():
        print("\nERROR: sudo is not available.")
        print("This operation requires administrator privileges.")

        log_error("Privileged operation requested without sudo.")
        return False

    return True


def confirm_action(message):
    """Require explicit confirmation for dangerous operations."""

    try:
        print("\n" + "!" * 60)
        print("WARNING")
        print("!" * 60)
        print(message)
        print("!" * 60)

        confirmation = input(
            "\nType 'YES' to continue: "
        ).strip()

        if confirmation == "YES":
            log_warning(
                f"User confirmed dangerous action: {message}"
            )
            return True

        print("\nOperation cancelled.")

        log_info(
            f"User cancelled action: {message}"
        )

        return False

    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.")
        log_info("Dangerous operation cancelled using Ctrl+C.")
        return False

    except EOFError:
        print("\nInput stream closed.")
        log_error("Input stream closed during confirmation.")
        return False

    except Exception as e:
        print(f"\nConfirmation error: {e}")
        log_error(f"Confirmation error: {e}")
        return False
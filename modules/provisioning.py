import os
import subprocess

from modules.logger import log_info, log_error
from modules.security import confirm_action, require_sudo


def provision_server():
    """Run the Linux server provisioning script."""

    print("\n" + "=" * 45)
    print("          SERVER PROVISIONING")
    print("=" * 45)

    # Check sudo privileges
    if not require_sudo():
        return

    # Confirm before making system changes
    if not confirm_action(
        "Server provisioning will update system packages "
        "and install required software."
    ):
        return

    # Locate provisioning script
    script_path = os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            "..",
            "scripts",
            "provision.sh"
        )
    )

    # Check whether script exists
    if not os.path.isfile(script_path):
        print("\nERROR: Provisioning script was not found.")

        log_error(
            f"Provisioning script missing: {script_path}"
        )

        return

    print("\nStarting server provisioning...\n")

    try:
        result = subprocess.run(
            ["bash", script_path],
            text=True
        )

        if result.returncode == 0:

            print(
                "\nServer provisioning completed successfully."
            )

            log_info(
                "Server provisioning completed successfully."
            )

        else:

            print(
                "\nServer provisioning failed."
            )

            log_error(
                f"Provisioning script failed with "
                f"exit code {result.returncode}"
            )

    except FileNotFoundError:

        print("\nERROR: Bash was not found.")

        log_error(
            "Bash command not found."
        )

    except PermissionError:

        print("\nERROR: Permission denied.")

        log_error(
            "Permission denied while running provisioning."
        )

    except subprocess.TimeoutExpired:

        print("\nERROR: Provisioning timed out.")

        log_error(
            "Provisioning process timed out."
        )

    except KeyboardInterrupt:

        print("\n\nProvisioning interrupted by user.")

        log_info(
            "Provisioning interrupted by user."
        )

    except Exception as e:

        print(
            f"\nUnexpected provisioning error: {e}"
        )

        log_error(
            f"Provisioning error: {e}"
        )
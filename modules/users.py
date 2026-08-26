import subprocess

from modules.logger import log_info, log_error
from modules.security import confirm_action, require_sudo


def run_command(command):
    try:
        result = subprocess.run(
            command,
            timeout=30
        )

        if result.returncode == 0:
            print("\nOperation completed successfully.")
            log_info(f"Command succeeded: {' '.join(command)}")
        else:
            print("\nOperation failed.")
            log_error(f"Command failed: {' '.join(command)}")

    except subprocess.TimeoutExpired:
        print("\nOperation timed out.")
        log_error(f"Command timed out: {' '.join(command)}")

    except FileNotFoundError:
        print("\nRequired command was not found.")
        log_error(f"Command not found: {' '.join(command)}")

    except PermissionError:
        print("\nPermission denied.")
        log_error(f"Permission denied: {' '.join(command)}")

    except Exception as e:
        print(f"\nError: {e}")
        log_error(f"User management command error: {e}")


def validate_username(username):
    if not username:
        print("\nUsername cannot be empty.")
        return False

    if not username.replace("-", "").replace("_", "").isalnum():
        print("\nInvalid username.")
        return False

    return True


def list_users():
    try:
        print("\nNormal Users:\n")

        with open("/etc/passwd", "r") as file:
            for line in file:
                parts = line.split(":")

                if len(parts) < 3:
                    continue

                username = parts[0]
                uid = int(parts[2])

                if uid >= 1000:
                    print(username)

        log_info("User list retrieved successfully.")

    except PermissionError:
        print("\nPermission denied.")
        log_error("Permission denied while reading /etc/passwd.")

    except FileNotFoundError:
        print("\n/etc/passwd was not found.")
        log_error("/etc/passwd was not found.")

    except ValueError as e:
        print(f"\nInvalid user data: {e}")
        log_error(f"Invalid /etc/passwd data: {e}")

    except Exception as e:
        print(f"\nError: {e}")
        log_error(f"User listing error: {e}")


def create_user():
    username = input("Enter new username: ").strip()

    if not validate_username(username):
        return

    if not require_sudo():
        return

    if not confirm_action(
        f"This will create a new Linux user '{username}'."
    ):
        return

    run_command([
        "sudo",
        "useradd",
        "-m",
        username
    ])


def delete_user():
    username = input("Enter username to delete: ").strip()

    if not validate_username(username):
        return

    if not require_sudo():
        return

    if not confirm_action(
        f"This will permanently delete user '{username}' "
        "and their home directory."
    ):
        return

    run_command([
        "sudo",
        "userdel",
        "-r",
        username
    ])


def add_user_to_group():
    username = input("Enter username: ").strip()
    group = input("Enter group name: ").strip()

    if not validate_username(username):
        return

    if not validate_username(group):
        return

    if not require_sudo():
        return

    if not confirm_action(
        f"This will add user '{username}' to group '{group}'."
    ):
        return

    run_command([
        "sudo",
        "usermod",
        "-aG",
        group,
        username
    ])


def user_info():
    username = input("Enter username: ").strip()

    if not validate_username(username):
        return

    run_command([
        "id",
        username
    ])


def user_management():
    while True:
        try:
            print("\n" + "=" * 45)
            print("           USER MANAGEMENT")
            print("=" * 45)

            print("1. List Users")
            print("2. Create User")
            print("3. Delete User")
            print("4. Add User to Group")
            print("5. Check User Information")
            print("0. Back to Main Menu")

            choice = input("\nEnter your choice: ").strip()

            if choice == "1":
                list_users()

            elif choice == "2":
                create_user()

            elif choice == "3":
                delete_user()

            elif choice == "4":
                add_user_to_group()

            elif choice == "5":
                user_info()

            elif choice == "0":
                break

            else:
                print("\nInvalid choice.")
                log_error(f"Invalid user management choice: {choice}")

            if choice != "0":
                input("\nPress Enter to continue...")

        except KeyboardInterrupt:
            print("\n\nReturning to main menu.")
            log_info("User management interrupted by user.")
            break

        except Exception as e:
            print(f"\nUnexpected error: {e}")
            log_error(f"User management error: {e}")
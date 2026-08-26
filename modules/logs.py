import os

from modules.logger import log_error


LOG_DIR = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "..",
        "logs"
    )
)


def get_log_files():
    try:
        if not os.path.exists(LOG_DIR):
            os.makedirs(LOG_DIR)

        return [
            file for file in os.listdir(LOG_DIR)
            if file.endswith(".log")
        ]

    except OSError as e:
        print(f"\nUnable to access log directory: {e}")
        log_error(f"Log directory error: {e}")
        return []


def view_log():
    log_files = get_log_files()

    if not log_files:
        print("\nNo log files found.")
        return

    print("\nAvailable Log Files:")
    print("-" * 30)

    for index, file in enumerate(log_files, start=1):
        print(f"{index}. {file}")

    print("0. Back")

    try:
        choice = input("\nSelect log file: ").strip()

        if choice == "0":
            return

        if not choice.isdigit():
            print("\nInvalid choice.")
            return

        index = int(choice) - 1

        if index < 0 or index >= len(log_files):
            print("\nInvalid log selection.")
            return

        log_path = os.path.join(LOG_DIR, log_files[index])

        print("\n" + "=" * 60)
        print(f"                    {log_files[index]}")
        print("=" * 60)

        with open(log_path, "r") as file:
            content = file.read()

        if content:
            print(content)
        else:
            print("Log file is empty.")

        print("=" * 60)

    except PermissionError:
        print("\nPermission denied while reading the log.")
        log_error("Permission denied while reading log file.")

    except OSError as e:
        print(f"\nUnable to read log file: {e}")
        log_error(f"Log reading error: {e}")

    except Exception as e:
        print(f"\nUnexpected error: {e}")
        log_error(f"Unexpected log viewer error: {e}")


def log_management():
    while True:
        try:
            print("\n" + "=" * 45)
            print("              LOG VIEWER")
            print("=" * 45)

            print("1. View Log File")
            print("0. Back to Main Menu")

            choice = input("\nEnter your choice: ").strip()

            if choice == "1":
                view_log()
                input("\nPress Enter to continue...")

            elif choice == "0":
                break

            else:
                print("\nInvalid choice.")

        except KeyboardInterrupt:
            print("\n\nReturning to main menu.")
            break

        except Exception as e:
            print(f"\nUnexpected error: {e}")
            log_error(f"Log management error: {e}")
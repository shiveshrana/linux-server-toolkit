import subprocess

from modules.logger import log_info, log_error


def run_service_command(command):
    try:
        result = subprocess.run(
            command,
            text=True,
            timeout=30
        )

        if result.returncode == 0:
            print("\nOperation completed successfully.")
            log_info(f"Service command succeeded: {' '.join(command)}")
        else:
            print("\nOperation failed.")
            log_error(f"Service command failed: {' '.join(command)}")

    except subprocess.TimeoutExpired:
        print("\nOperation timed out.")
        log_error(f"Service command timed out: {' '.join(command)}")

    except FileNotFoundError:
        print("\nsystemctl was not found.")
        log_error("systemctl command not found.")

    except Exception as e:
        print(f"\nError: {e}")
        log_error(f"Service command error: {e}")


def get_service_name():
    service = input("Enter service name: ").strip()

    if not service:
        print("\nService name cannot be empty.")
        return None

    if not service.replace("-", "").replace("_", "").isalnum():
        print("\nInvalid service name.")
        return None

    return service


def list_failed_services():
    run_service_command([
        "systemctl",
        "--failed"
    ])


def service_status():
    service = get_service_name()

    if service:
        run_service_command([
            "systemctl",
            "status",
            service,
            "--no-pager"
        ])


def start_service():
    service = get_service_name()

    if service:
        run_service_command([
            "sudo",
            "systemctl",
            "start",
            service
        ])


def stop_service():
    service = get_service_name()

    if service:
        run_service_command([
            "sudo",
            "systemctl",
            "stop",
            service
        ])


def restart_service():
    service = get_service_name()

    if service:
        run_service_command([
            "sudo",
            "systemctl",
            "restart",
            service
        ])


def enable_service():
    service = get_service_name()

    if service:
        run_service_command([
            "sudo",
            "systemctl",
            "enable",
            service
        ])


def service_management():
    while True:
        try:
            print("\n" + "=" * 45)
            print("         SERVICE MANAGEMENT")
            print("=" * 45)

            print("1. List Failed Services")
            print("2. Check Service Status")
            print("3. Start Service")
            print("4. Stop Service")
            print("5. Restart Service")
            print("6. Enable Service")
            print("0. Back to Main Menu")

            choice = input("\nEnter your choice: ").strip()

            if choice == "1":
                list_failed_services()

            elif choice == "2":
                service_status()

            elif choice == "3":
                start_service()

            elif choice == "4":
                stop_service()

            elif choice == "5":
                restart_service()

            elif choice == "6":
                enable_service()

            elif choice == "0":
                break

            else:
                print("\nInvalid choice.")

            if choice != "0":
                input("\nPress Enter to continue...")

        except KeyboardInterrupt:
            print("\n\nReturning to main menu.")
            break

        except Exception as e:
            print(f"\nUnexpected error: {e}")
            log_error(f"Service management error: {e}")
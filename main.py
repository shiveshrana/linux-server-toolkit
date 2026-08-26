#!/usr/bin/env python3

import platform

from modules.logger import log_info, log_warning, log_error
from modules.environment import run_environment_check
from modules.system_info import show_system_info
from modules.health_check import run_health_check
from modules.services import service_management
from modules.users import user_management
from modules.provisioning import provision_server
from modules.logs import log_management
from modules.full_check import generate_report
from modules.constants import (
    SUCCESS,
    GENERAL_ERROR,
    DEPENDENCY_ERROR,
    INTERRUPTED,
)


def clear_screen():
    try:
        print("\033[H\033[J", end="")
    except Exception as e:
        log_error(f"Failed to clear screen: {e}")


def show_menu():
    print("=" * 50)
    print("       AUTOMATED LINUX SERVER TOOLKIT")
    print("=" * 50)

    print("1.  System Information")
    print("2.  Run Health Check")
    print("3.  Service Management")
    print("4.  User Management")
    print("5.  Provision Server")
    print("6.  View Logs")
    print("7.  Run Full Server Check")
    print("0.  Exit")

    print("=" * 50)


def main():

    try:
        print("\nRunning environment check...\n")

        if not run_environment_check():
            print("\nEnvironment check failed.")
            print("Fix the reported issues before starting the toolkit.")
            return 4

        log_info("Environment check passed.")
        log_info("Linux Server Toolkit started.")

        while True:

            clear_screen()
            show_menu()

            try:
                choice = input("\nEnter your choice: ").strip()

            except EOFError:
                print("\nInput stream closed.")
                log_warning("Input stream closed.")
                return 1

            if choice == "1":
                show_system_info()

            elif choice == "2":
                run_health_check()

            elif choice == "3":
                service_management()

            elif choice == "4":
                user_management()

            elif choice == "5":
                provision_server()

            elif choice == "6":
                log_management()

            elif choice == "7":
                generate_report()

            elif choice == "0":
                print("\nExiting Linux Server Toolkit...")
                log_info("Linux Server Toolkit stopped.")
                return 0

            else:
                print("\nInvalid choice.")
                log_warning(f"Invalid menu choice: {choice}")

            try:
                input("\nPress Enter to continue...")

            except EOFError:
                print("\nInput stream closed.")
                return 1

    except KeyboardInterrupt:
        print("\n\nToolkit interrupted by user.")
        log_info("Toolkit interrupted by user.")
        return 130

    except Exception as e:
        print(f"\nUnexpected application error: {e}")
        log_error(f"Unexpected application error: {e}")
        return 1


if __name__ == "__main__":
    exit(main())
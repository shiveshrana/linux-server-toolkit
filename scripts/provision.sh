#!/bin/bash

set -u

# ==========================================
# Linux Server Provisioning Script
# ==========================================

SUCCESS=0
GENERAL_ERROR=1
PERMISSION_ERROR=3
DEPENDENCY_ERROR=4

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
LOG_DIR="$PROJECT_DIR/logs"
LOG_FILE="$LOG_DIR/provision.log"

PACKAGES=(
    curl
    wget
    git
    vim
    htop
    net-tools
)

# ------------------------------------------
# Logging
# ------------------------------------------

mkdir -p "$LOG_DIR"

log() {
    local level="$1"
    local message="$2"

    echo "$(date '+%Y-%m-%d %H:%M:%S') | $level | $message" \
        | tee -a "$LOG_FILE"
}

# ------------------------------------------
# Error handler
# ------------------------------------------

error_exit() {
    local message="$1"
    local code="$2"

    log "ERROR" "$message"
    echo
    echo "Provisioning failed."
    echo "Exit code: $code"

    exit "$code"
}

# ------------------------------------------
# Check Linux
# ------------------------------------------

check_os() {

    if [[ "$(uname -s)" != "Linux" ]]; then
        error_exit \
            "Unsupported operating system. Linux is required." \
            "$DEPENDENCY_ERROR"
    fi

    log "INFO" "Linux operating system detected."
}

# ------------------------------------------
# Check sudo
# ------------------------------------------

check_sudo() {

    if ! command -v sudo >/dev/null 2>&1; then
        error_exit \
            "sudo is not installed." \
            "$DEPENDENCY_ERROR"
    fi

    if ! sudo -n true 2>/dev/null; then

        echo
        echo "This operation requires sudo privileges."
        echo "You may be asked for your password."
        echo

        if ! sudo -v; then
            error_exit \
                "Unable to obtain sudo privileges." \
                "$PERMISSION_ERROR"
        fi
    fi

    log "INFO" "Sudo privileges verified."
}

# ------------------------------------------
# Check apt
# ------------------------------------------

check_package_manager() {

    if ! command -v apt >/dev/null 2>&1; then
        error_exit \
            "APT package manager was not found." \
            "$DEPENDENCY_ERROR"
    fi

    log "INFO" "APT package manager detected."
}

# ------------------------------------------
# Update packages
# ------------------------------------------

update_system() {

    log "INFO" "Updating package repositories..."

    if ! sudo apt update >> "$LOG_FILE" 2>&1; then
        error_exit \
            "Failed to update package repositories." \
            "$GENERAL_ERROR"
    fi

    log "INFO" "Package repositories updated successfully."
}

# ------------------------------------------
# Upgrade system
# ------------------------------------------

upgrade_system() {

    log "INFO" "Upgrading installed packages..."

    if ! sudo apt upgrade -y >> "$LOG_FILE" 2>&1; then
        error_exit \
            "Failed to upgrade installed packages." \
            "$GENERAL_ERROR"
    fi

    log "INFO" "System upgrade completed successfully."
}

# ------------------------------------------
# Install packages
# ------------------------------------------

install_packages() {

    log "INFO" "Installing required packages..."

    for package in "${PACKAGES[@]}"; do

        echo "Installing: $package"

        if ! sudo apt install -y "$package" >> "$LOG_FILE" 2>&1; then

            log "ERROR" \
                "Failed to install package: $package"

            error_exit \
                "Package installation failed: $package" \
                "$GENERAL_ERROR"
        fi

        log "INFO" \
            "Package installed successfully: $package"
    done
}

# ------------------------------------------
# Main
# ------------------------------------------

main() {

    echo "=========================================="
    echo "     LINUX SERVER PROVISIONING"
    echo "=========================================="

    log "INFO" "Provisioning started."

    check_os
    check_sudo
    check_package_manager

    update_system
    upgrade_system
    install_packages

    echo
    echo "=========================================="
    echo " Provisioning completed successfully!"
    echo "=========================================="

    log "INFO" "Provisioning completed successfully."

    exit "$SUCCESS"
}

main
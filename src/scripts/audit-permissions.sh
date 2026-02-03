#!/usr/bin/env bash
#
# Permission Audit and Reporting Script for Meza
#
# Usage:
#   audit-permissions.sh [directory]
#   audit-permissions.sh --all|-a|all
#   audit-permissions.sh (interactive menu)
#
# This script only reports. It does not make any changes, or have any side-effects.
#
# CAUTION: Using 'ALL' may not be suitable for a large wiki farm due to inclusion of
# all database, web and upload files. Try individual menu options first before going "All IN"

set -euo pipefail

# Color output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
BOLD='\033[1m'
NC='\033[0m' # No Color

# Predefined Meza directories
MEZA_DIRS=(
    "/opt/meza"
    "/opt/conf-meza"
    "/opt/data-meza/backups"
    "/opt/data-meza/cache"
    "/opt/data-meza/elasticsearch"
    "/opt/data-meza/logs"
    "/opt/data-meza/mariadb"
    "/opt/data-meza/mw-temp"
    "/opt/data-meza/tmp"
    "/opt/data-meza/uploads"
    "/opt/.deploy-meza"
    "/opt/htdocs"
)

print_header() {
    echo -e "\n${BOLD}${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${BOLD}${BLUE}$1${NC}"
    echo -e "${BOLD}${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}\n"
}

print_section() {
    echo -e "\n${BOLD}${YELLOW}▸ $1${NC}"
    echo -e "${YELLOW}$([[ -n "${2:-}" ]] && echo "$2" || echo "$(printf '─%.0s' {1..60})")${NC}"
}

audit_directory() {
    local dir="$1"

    if [[ ! -d "$dir" ]]; then
        echo -e "${RED}ERROR: Directory does not exist: $dir${NC}" >&2
        return 0  # Return success so loop continues
    fi

    if [[ ! -r "$dir" ]]; then
        echo -e "${RED}ERROR: Directory not readable: $dir${NC}" >&2
        return 0  # Return success so loop continues
    fi

    print_header "Permission Audit Report: $dir"

    # Get total count
    print_section "Summary Statistics"
    local total_items
    total_items=$(find "$dir" 2>/dev/null | wc -l)
    echo -e "Total items (files + directories): ${BOLD}$total_items${NC}"

    # Owner distribution
    print_section "Ownership by USER"
    find "$dir" -printf "%u\n" 2>/dev/null | sort | uniq -c | sort -rn | \
        awk '{printf "  %6s items  %-20s", $1, $2; if ($1>0) printf " (%.1f%%)", ($1/'$total_items')*100; print ""}'

    # Group distribution
    print_section "Ownership by GROUP"
    find "$dir" -printf "%g\n" 2>/dev/null | sort | uniq -c | sort -rn | \
        awk '{printf "  %6s items  %-20s", $1, $2; if ($1>0) printf " (%.1f%%)", ($1/'$total_items')*100; print ""}'

    # Disk usage
    print_section "Disk Usage by Top-Level Directories/Files"
    if [[ -n "$(find "$dir" -maxdepth 1 -mindepth 1 2>/dev/null)" ]]; then
        du -sh "$dir"/* 2>/dev/null | sort -rh | head -20 | \
            awk '{printf "  %8s  %s\n", $1, $2}'
    else
        echo "  (empty or no subdirectories)"
    fi

    # File counts per subdirectory
    print_section "File Count per Top-Level Directory"
    if [[ -n "$(find "$dir" -maxdepth 1 -mindepth 1 -type d 2>/dev/null)" ]]; then
        (
            cd "$dir" 2>/dev/null || return
            find . -maxdepth 1 -type d 2>/dev/null | sort | while read -r subdir; do
                local file_count
                file_count=$(find "$subdir" -type f 2>/dev/null | wc -l)
                printf "  %-50s %6s files\n" "$subdir" "$file_count"
            done
        )
    else
        echo "  (no subdirectories)"
    fi

    # Top-level directory permissions sorted by ownership
    print_section "Top-Level Directories - Sorted by Ownership"
    if [[ -n "$(find "$dir" -maxdepth 1 -mindepth 1 -type d 2>/dev/null)" ]]; then
        find "$dir" -maxdepth 1 -type d -printf "%M %u:%g %p\n" 2>/dev/null | \
            LC_ALL=C sort --key=2,2 | \
            awk '{printf "  %-12s %-25s %s\n", $1, $2, $3}'
    fi

    # Top-level directory permissions sorted by name
    print_section "Top-Level Directories - Sorted by Name"
    if [[ -n "$(find "$dir" -maxdepth 1 -mindepth 1 -type d 2>/dev/null)" ]]; then
        find "$dir" -maxdepth 1 -type d -printf "%M %u:%g %p\n" 2>/dev/null | \
            LC_ALL=C sort --key=3 | \
            awk '{printf "  %-12s %-25s %s\n", $1, $2, $3}'
    fi

    # Sample of files with permissions (first 20)
    print_section "Sample Files (first 20)" "showing permissions, ownership, path"
    find "$dir" -type f -printf "%M %u:%g %p\n" 2>/dev/null | head -20 | \
        awk '{printf "  %-12s %-25s %s\n", $1, $2, $3}'

    echo ""
}

show_menu() {
    print_header "Meza Permission Audit - Directory Selection"

    echo -e "${BOLD}Select a directory to audit:${NC}\n"

    local i=1
    for dir in "${MEZA_DIRS[@]}"; do
        local exists=""
        [[ -d "$dir" ]] && exists="${GREEN}✓${NC}" || exists="${RED}✗${NC}"
        printf "  %2d) ${exists} %s\n" "$i" "$dir"
        ((i++))
    done

    echo -e "\n  ${BOLD}a)${NC} Audit ALL directories"
    echo -e "  ${BOLD}q)${NC} Quit\n"

    read -rp "Enter selection [1-${#MEZA_DIRS[@]}], a, or q: " choice

    case "$choice" in
        [1-9]|1[0-2])
            local index=$((choice - 1))
            if [[ $index -lt ${#MEZA_DIRS[@]} ]]; then
                audit_directory "${MEZA_DIRS[$index]}"
            else
                echo -e "${RED}Invalid selection${NC}"
                return 1
            fi
            ;;
        a|A)
            for dir in "${MEZA_DIRS[@]}"; do
                if [[ -d "$dir" ]]; then
                    audit_directory "$dir" || true
                else
                    echo -e "${YELLOW}Skipping non-existent directory: $dir${NC}\n"
                fi
            done
            ;;
        q|Q)
            echo "Exiting."
            exit 0
            ;;
        *)
            echo -e "${RED}Invalid selection${NC}"
            return 1
            ;;
    esac
}

# Main logic
if [[ $# -eq 0 ]]; then
    # No arguments - show interactive menu
    show_menu
elif [[ "$1" == "all" || "$1" == "-a" || "$1" == "--all" ]]; then
    # Audit all predefined directories
    for dir in "${MEZA_DIRS[@]}"; do
        if [[ -d "$dir" ]]; then
            audit_directory "$dir" || true
        else
            echo -e "${YELLOW}Skipping non-existent directory: $dir${NC}\n"
        fi
    done
elif [[ "$1" == "-h" || "$1" == "--help" ]]; then
    cat <<EOF
${BOLD}Meza Permission Audit Script${NC}

${BOLD}Usage:${NC}
  $0 [directory]          Audit specific directory
  $0 --all|-a|all         Audit all Meza directories
  $0                      Interactive menu selection
  $0 --help|-h            Show this help

${BOLD}Predefined Meza Directories:${NC}
EOF
    for dir in "${MEZA_DIRS[@]}"; do
        echo "  - $dir"
    done
    echo ""
else
    # Audit specified directory
    audit_directory "$1"
fi

#!/bin/bash
#
# Meza Linting Script - Run appropriate linters on files
# Usage: ./lint-files.sh [-v|--verbose] [file1] [file2] ... or ./lint-files.sh (for all files)
# Note: quickly fix files with trailing whitespace using: sed -i 's/[[:space:]]\+$//' <filename>
#

set -e

# Global verbose flag
VERBOSE=false

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    if [ "$VERBOSE" = true ]; then
        echo -e "${BLUE}[LINT]${NC} $1"
    fi
}

# Always-visible output functions
print_info() {
    echo -e "${BLUE}[LINT]${NC} $1"
}

print_success() {
    if [ "$VERBOSE" = true ]; then
        echo -e "${GREEN}[SUCCESS]${NC} $1"
    fi
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

# Change to project root
cd "$PROJECT_ROOT"

# Activate virtual environment if it exists
VENV_PATH="$PROJECT_ROOT/.venv"
if [ -d "$VENV_PATH" ] && [ -f "$VENV_PATH/bin/activate" ]; then
    print_status "Activating virtual environment: $VENV_PATH"
    # shellcheck source=/dev/null
    source "$VENV_PATH/bin/activate"
    # Add venv bin to PATH
    export PATH="$VENV_PATH/bin:$PATH"
else
    print_warning "Virtual environment not found at $VENV_PATH"
    print_status "Using system-wide Python packages"
fi

# Export Ansible configuration and roles path for ansible-lint
export ANSIBLE_CONFIG="$PROJECT_ROOT/config/ansible.cfg"
export ANSIBLE_ROLES_PATH="$PROJECT_ROOT/src/roles"

# Check if linting tools are available
check_tools() {
    local missing_tools=()
    local install_cmd=""

    # Determine installation method based on environment
    if [ -n "$VIRTUAL_ENV" ] || [ -d "$PROJECT_ROOT/.venv" ]; then
        install_cmd="pip install ansible-lint yamllint"
    else
        install_cmd="pip install --user ansible-lint yamllint"
    fi

    if ! command -v ansible-lint >/dev/null 2>&1; then
        missing_tools+=("ansible-lint")
    fi

    if ! command -v yamllint >/dev/null 2>&1; then
        missing_tools+=("yamllint")
    fi

    if [ ${#missing_tools[@]} -gt 0 ]; then
        print_warning "Missing linting tools: ${missing_tools[*]}"
        print_status "Install with: $install_cmd"
        return 1
    fi

    return 0
}

# Function to lint YAML files
lint_yaml() {
    local file="$1"
    print_status "Linting YAML file: $file"

    if yamllint "$file"; then
        print_success "YAML lint passed: $file"
        return 0
    else
        print_error "YAML lint failed: $file"
        return 1
    fi
}

# Function to lint Ansible files
lint_ansible() {
    local file="$1"
    print_status "Linting Ansible file: $file"

    # Use ansible-lint with project config
    if ansible-lint "$file"; then
        print_success "Ansible lint passed: $file"
        return 0
    else
        print_error "Ansible lint failed: $file"
        return 1
    fi
}

# Function to build directory exclusion pattern from .gitignore
build_exclusion_pattern() {
    local base_dirs="\.venv|vendor|\.cache|\.git|tests/docker|collections|node_modules"

    # Try to read additional patterns from .gitignore
    if [ -f "$PROJECT_ROOT/.gitignore" ]; then
        while IFS= read -r line; do
            # Skip comments and empty lines
            [[ "$line" =~ ^#.*$ ]] && continue
            [[ -z "$line" ]] && continue

            # Handle directory patterns (ending with /)
            if [[ "$line" =~ /$ ]]; then
                # Remove trailing slash and escape dots
                local dir="${line%/}"
                dir="${dir//./\\.}"
                base_dirs="${base_dirs}|${dir}"
            fi
        done < "$PROJECT_ROOT/.gitignore"
    fi

    echo "$base_dirs"
}

# Function to determine file type and run appropriate linter
lint_file() {
    local file="$1"
    local exit_code=0

    # Build exclusion pattern once per script run (cached via static variable pattern)
    if [ -z "$EXCLUSION_PATTERN" ]; then
        EXCLUSION_PATTERN="^($(build_exclusion_pattern))/"
    fi

    # Skip files in excluded directories
    if [[ "$file" =~ $EXCLUSION_PATTERN ]]; then
        print_status "Skipping excluded directory: $file"
        return 0
    fi

    # Skip binary and image files
    local binary_pattern="\.(svg|png|jpg|jpeg|gif|ico|pdf|zip|tar|gz|bz2)$"
    if [[ "$file" =~ $binary_pattern ]]; then
        print_status "Skipping binary/image file: $file"
        return 0
    fi

    # Check if file exists
    if [ ! -f "$file" ]; then
        print_warning "File not found: $file"
        return 0
    fi

    # Determine file type and lint accordingly
    case "$file" in
        *.yml|*.yaml)
            # Check if it's an Ansible file
            if [[ "$file" =~ ^src/playbooks/ ]] || [[ "$file" =~ ^src/roles/.*/tasks/ ]] || [[ "$file" =~ ^src/roles/.*/handlers/ ]] || [[ "$file" =~ ^src/roles/.*/vars/ ]] || [[ "$file" =~ ^src/roles/.*/defaults/ ]]; then
                lint_ansible "$file" || exit_code=1
            else
                lint_yaml "$file" || exit_code=1
            fi
            ;;
        *.py)
            print_status "Python linting not configured for: $file"
            ;;
        *)
            print_status "No linter configured for: $file"
            ;;
    esac

    return $exit_code
}

# Main function
main() {
    local files=()
    local exit_code=0

    # Parse command line arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            -v|--verbose)
                VERBOSE=true
                shift
                ;;
            -h|--help)
                echo "Usage: $0 [-v|--verbose] [FILES...]"
                echo ""
                echo "Options:"
                echo "  -v, --verbose    Show detailed progress and success messages"
                echo "  -h, --help       Show this help message"
                echo ""
                echo "By default, only warnings and errors are shown."
                exit 0
                ;;
            -*)
                echo "Unknown option: $1" >&2
                exit 1
                ;;
            *)
                files+=("$1")
                shift
                ;;
        esac
    done

    print_info "Starting Meza file linting..."

    # Check if tools are available
    if ! check_tools; then
        exit 1
    fi

    # If no files specified, find all relevant files
    if [ ${#files[@]} -eq 0 ]; then
        print_status "No files specified, finding all YAML files..."
        # Find all YAML files, excluding certain directories
        mapfile -t files < <(find . -name "*.yml" -o -name "*.yaml" | grep -v -E "^\./(\.venv|vendor|\.cache|tests/docker|collections)" | sort)
    fi

    print_info "Found ${#files[@]} files to lint"

    # Lint each file
    local failed_files=()
    for file in "${files[@]}"; do
        if ! lint_file "$file"; then
            failed_files+=("$file")
            exit_code=1
        fi
    done

    # Summary
    echo
    print_info "Linting complete!"

    if [ $exit_code -eq 0 ]; then
        echo -e "${GREEN}[SUCCESS]${NC} All ${#files[@]} files passed linting checks!"
    else
        echo -e "${GREEN}[SUCCESS]${NC} $((${#files[@]} - ${#failed_files[@]}))/${#files[@]} files passed"
        print_error "Linting failed for ${#failed_files[@]} files:"
        for file in "${failed_files[@]}"; do
            echo "  - $file"
        done
    fi

    return $exit_code
}

# Run main function with all arguments
main "$@"

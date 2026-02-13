#!/usr/bin/env bash
# filepath: /home/greg/src/meza/src/scripts/generate-playbook-graphs.sh
"""
Generate ansible-playbook-grapher visualizations for all Meza playbooks.

Requirements:
    pip install ansible-playbook-grapher

Usage:
    cd ~/src/meza/src/playbooks
    ../scripts/generate-playbook-graphs.sh [--with-tasks]

    Or from anywhere:
    /home/greg/src/meza/src/scripts/generate-playbook-graphs.sh [--with-tasks]

Options:
    --with-tasks    Include individual role tasks in the graph
"""

set -euo pipefail

# Parse command line arguments
INCLUDE_TASKS=false
if [[ $# -gt 0 ]] && [[ "$1" == "--with-tasks" ]]; then
    INCLUDE_TASKS=true
    echo "Including role tasks in graphs"
    echo ""
fi

# Determine project root and playbooks directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"
PLAYBOOKS_DIR="${PROJECT_ROOT}/src/playbooks"
ANSIBLE_CONFIG="${PROJECT_ROOT}/config/ansible.cfg"

# Change to playbooks directory
cd "${PLAYBOOKS_DIR}" || exit 1

echo "Generating playbook graphs in: ${PLAYBOOKS_DIR}"
echo "Using Ansible config: ${ANSIBLE_CONFIG}"
echo ""

# Loop through all .yml files
for playbook in *.yml; do
    # Skip if no files match (empty directory)
    [[ -e "${playbook}" ]] || continue

    # Extract base name without extension for title
    base_name="${playbook%.yml}"

    # Convert filename to human-readable title
    # Example: site.yml -> Meza site playbook
    #          setup-meza-user.yml -> Meza setup meza user playbook
    title="Meza ${base_name//-/ } playbook"
    output_file="${base_name}"

    # Add "with tasks" to title and filename suffix if including tasks
    if [[ "${INCLUDE_TASKS}" == "true" ]]; then
        title="${title} with tasks"
        output_file="${base_name}-w-tasks"
    fi

    echo "Processing: ${playbook}"
    echo "  Title: ${title}"
    echo "  Output: ${output_file}.svg"

    # Build ansible-playbook-grapher command
    grapher_cmd=(
        ansible-playbook-grapher
        --open-protocol-handler vscode
        --collapsible-nodes
        --title "${title}"
        --output-filename "${output_file}"
    )

    # Add --include-role-tasks if requested
    if [[ "${INCLUDE_TASKS}" == "true" ]]; then
        grapher_cmd+=(--include-role-tasks)
    fi

    grapher_cmd+=(-vvv "${playbook}")

    # Run ansible-playbook-grapher
    ANSIBLE_CONFIG="${ANSIBLE_CONFIG}" "${grapher_cmd[@]}"

    echo "  ✓ Generated graph for ${playbook}"
    echo ""
done

echo "All playbook graphs generated successfully!"
echo "SVG files created in: ${PLAYBOOKS_DIR}"
echo "Open in VS Code, your browser, any SVG viewer, or upload to wiki pages!"

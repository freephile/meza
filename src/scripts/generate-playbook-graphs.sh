#!/usr/bin/env bash
# filepath: /home/greg/src/meza/src/scripts/generate-playbook-graphs.sh
"""
Generate ansible-playbook-grapher visualizations for all Meza playbooks.

Requirements:
    pip install ansible-playbook-grapher

Usage:
    cd ~/src/meza/src/playbooks
    ../scripts/generate-playbook-graphs.sh

    Or from anywhere:
    /home/greg/src/meza/src/scripts/generate-playbook-graphs.sh
"""

set -euo pipefail

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
    
    echo "Processing: ${playbook}"
    echo "  Title: ${title}"
    
    # Run ansible-playbook-grapher
    ANSIBLE_CONFIG="${ANSIBLE_CONFIG}" \
        ansible-playbook-grapher \
        --open-protocol-handler vscode \
        --collapsible-nodes \
        --title "${title}" \
        -vvv \
        "${playbook}"
    
    echo "  ✓ Generated graph for ${playbook}"
    echo ""
done

echo "All playbook graphs generated successfully!"
echo "SVG files created in: ${PLAYBOOKS_DIR}"
echo "Open in VS Code, your browser, any SVG viewer, or upload to wiki pages!"
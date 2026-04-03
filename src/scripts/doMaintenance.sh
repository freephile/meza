#!/bin/bash

# This script runs a specified MediaWiki maintenance script across all wikis
# located in the /opt/htdocs/wikis directory. It logs the output and summarizes
# the results at the end.
# Ensure this script has execute permissions: chmod +x doMaintenance.sh
# Usage: ./doMaintenance.sh
# Adjust the MAINTENANCE_SCRIPT variable to change which script to run.
# https://www.mediawiki.org/wiki/Manual:Maintenance_scripts/List_of_scripts

# This is just a simple example script prior to implementing a more robust Ansible-based maintenance system.
# See .github/prompts/plan-mezaMaintenanceRefactor.prompt.md for the plan for that refactor.

WIKIS_DIR="/opt/htdocs/wikis"
MEDIAWIKI_DIR="/opt/htdocs/mediawiki"
MAINTENANCE_SCRIPT="showSiteStats"
LOG_FILE="/opt/data-meza/logs/maintenance_$(date +%Y%m%d_%H%M%S).log"

echo "Starting maintenance run at $(date)" | tee "$LOG_FILE"
echo "Log file: $LOG_FILE" | tee -a "$LOG_FILE"

successful=0
failed=0

for wiki_path in "$WIKIS_DIR"/*; do
    if [ -d "$wiki_path" ]; then
        wiki_name=$(basename "$wiki_path")
        
        echo "Processing wiki: $wiki_name" | tee -a "$LOG_FILE"
        
        # Determine command based on MediaWiki version
        if [ -f "$MEDIAWIKI_DIR/maintenance/run" ]; then
            # REL1_40+ - Use maintenance/run
            COMMAND=("$MEDIAWIKI_DIR/maintenance/run" "$MAINTENANCE_SCRIPT")
        else
            # REL1_39 - Use legacy direct script call
            COMMAND=(php "$MEDIAWIKI_DIR/maintenance/$MAINTENANCE_SCRIPT.php")
        fi
        
        if WIKI="$wiki_name" "${COMMAND[@]}" 2>&1 | tee -a "$LOG_FILE"; then
            echo "✓ Success: $wiki_name" | tee -a "$LOG_FILE"
            ((successful++))
        else
            echo "✗ Failed: $wiki_name" | tee -a "$LOG_FILE"
            ((failed++))
        fi
        
        echo "----------------------------------------" | tee -a "$LOG_FILE"
    fi
done

echo "Summary: $successful successful, $failed failed" | tee -a "$LOG_FILE"
echo "Finished at $(date)" | tee -a "$LOG_FILE"
#!/bin/bash
# Meza Release Automation Helper
# This script provides easy shortcuts for triggering release documentation workflows

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check if gh CLI is available
if ! command -v gh &> /dev/null; then
    echo -e "${RED}Error: GitHub CLI (gh) is not installed.${NC}"
    echo "Install it from: https://cli.github.com/"
    exit 1
fi

# Check if we're in a git repository
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    echo -e "${RED}Error: Not in a git repository${NC}"
    exit 1
fi

show_usage() {
    cat << EOF
${BLUE}Meza Release Automation Helper${NC}

${YELLOW}Usage:${NC}
  $0 <command> [options]

${YELLOW}Commands:${NC}
  ${GREEN}auto${NC}           Trigger automatic release notes update
  ${GREEN}force${NC}          Force update release notes (even if no changes)
  ${GREEN}range${NC}          Generate release notes for specific commit range
  ${GREEN}tag${NC}            Generate release notes for specific tag
  ${GREEN}status${NC}         Show status of recent workflow runs
  ${GREEN}help${NC}           Show this help message

${YELLOW}Examples:${NC}
  # Force update current release notes
  $0 force

  # Generate notes from last tag to HEAD
  $0 range v1.2.0 HEAD

  # Generate notes for specific tag
  $0 tag v1.3.0

  # Check workflow status
  $0 status

EOF
}

get_latest_tag() {
    git describe --tags --abbrev=0 2>/dev/null || echo ""
}

validate_ref() {
    local ref="$1"
    if ! git rev-parse --verify "$ref" &>/dev/null; then
        echo -e "${RED}Error: Invalid git reference: $ref${NC}"
        return 1
    fi
}

trigger_auto() {
    echo -e "${BLUE}Triggering automatic release notes update...${NC}"
    gh workflow run "Advanced Release Management" --field force_update=true
    echo -e "${GREEN}✅ Workflow triggered successfully${NC}"
    echo "Check status with: $0 status"
}

trigger_force() {
    echo -e "${BLUE}Force triggering release notes update...${NC}"
    gh workflow run "Advanced Release Management" --field force_update=true
    echo -e "${GREEN}✅ Force update workflow triggered${NC}"
    echo "Check status with: $0 status"
}

trigger_range() {
    local start_ref="${1:-}"
    local end_ref="${2:-HEAD}"
    
    if [[ -z "$start_ref" ]]; then
        echo -e "${RED}Error: Start reference required${NC}"
        echo "Usage: $0 range <start_ref> [end_ref]"
        echo "Example: $0 range v1.2.0 HEAD"
        return 1
    fi
    
    echo -e "${BLUE}Validating references...${NC}"
    validate_ref "$start_ref" || return 1
    validate_ref "$end_ref" || return 1
    
    # Check if range has commits
    local commit_count
    commit_count=$(git rev-list --count "$start_ref..$end_ref" 2>/dev/null || echo "0")
    
    echo -e "${BLUE}Generating release notes for range:${NC}"
    echo "  Start: $start_ref"
    echo "  End: $end_ref" 
    echo "  Commits: $commit_count"
    
    if [[ "$commit_count" -eq "0" ]]; then
        echo -e "${YELLOW}Warning: No commits found in range${NC}"
        read -p "Continue anyway? (y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "Cancelled"
            return 0
        fi
    fi
    
    gh workflow run "Manual Release Notes Generator" \
        --field start_ref="$start_ref" \
        --field end_ref="$end_ref" \
        --field update_changelog=true
    
    echo -e "${GREEN}✅ Range workflow triggered successfully${NC}"
    echo "Check status with: $0 status"
}

trigger_tag() {
    local tag="${1:-}"
    
    if [[ -z "$tag" ]]; then
        echo -e "${RED}Error: Tag required${NC}"
        echo "Usage: $0 tag <tag_name>"
        echo "Example: $0 tag v1.3.0"
        return 1
    fi
    
    echo -e "${BLUE}Validating tag...${NC}"
    validate_ref "$tag" || return 1
    
    # Find previous tag for range
    local prev_tag
    prev_tag=$(git describe --tags --abbrev=0 --exclude="$tag" 2>/dev/null || echo "")
    
    echo -e "${BLUE}Generating release notes for tag: ${tag}${NC}"
    if [[ -n "$prev_tag" ]]; then
        echo "  Previous tag: $prev_tag"
        local commit_count
        commit_count=$(git rev-list --count "$prev_tag..$tag" 2>/dev/null || echo "0")
        echo "  Commits: $commit_count"
    fi
    
    gh workflow run "Advanced Release Management" \
        --field version_tag="$tag"
    
    echo -e "${GREEN}✅ Tag workflow triggered successfully${NC}"
    echo "Check status with: $0 status"
}

show_status() {
    echo -e "${BLUE}Recent workflow runs:${NC}"
    echo
    
    # Show recent runs for each workflow
    local workflows=("release-notes.yml" "advanced-release-management.yml" "manual-release-notes.yml")
    
    for workflow in "${workflows[@]}"; do
        echo -e "${YELLOW}${workflow}:${NC}"
        gh run list --workflow="$workflow" --limit=3 --json="displayTitle,status,conclusion,createdAt,url" \
            --template='{{range .}}  {{.displayTitle}} - {{.status}} {{if .conclusion}}({{.conclusion}}){{end}} - {{timeago .createdAt}} - {{.url}}
{{end}}' 2>/dev/null || echo "  No recent runs"
        echo
    done
}

main() {
    local command="${1:-help}"
    
    case "$command" in
        "auto")
            trigger_auto
            ;;
        "force")  
            trigger_force
            ;;
        "range")
            shift
            trigger_range "$@"
            ;;
        "tag")
            shift
            trigger_tag "$@"
            ;;
        "status")
            show_status
            ;;
        "help"|"-h"|"--help")
            show_usage
            ;;
        *)
            echo -e "${RED}Error: Unknown command '$command'${NC}"
            echo
            show_usage
            exit 1
            ;;
    esac
}

# Only run main if script is executed directly (not sourced)
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi
#!/bin/sh

## Check for uncommitted changes in git-managed extensions and skins

for d in /opt/htdocs/mediawiki/ /opt/htdocs/mediawiki/extensions/*/ /opt/htdocs/mediawiki/skins/*/; do
  [ -d "$d/.git" ] || continue
  status=$(git -C "$d" status --short --untracked-files=no)
  name="${d%/}"; name="${name##*/}"
  if [ -n "$status" ]; then
    dirty=1
    echo "=== $name ==="
    echo "$status"
  fi
done

[ -z "$dirty" ] && echo "No changes found in any git managed directory (core, extensions or skins)."

echo "To check for changes in composer-managed extensions/skins, run 'composer status --verbose --working-dir=/opt/htdocs/mediawiki'"

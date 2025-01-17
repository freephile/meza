#! /bin/sh
#
# Unite us. Unite the wikis.


# must be root or sudoer
if [ "$(whoami)" != "root" ]; then
	echo "Try running this script with sudo: \"sudo bash unite-the-wikis.sh\""
	exit 1
fi


# If /usr/local/bin is not in PATH then add it
# Ref enterprisemediawiki/meza#68 "Run install.sh with non-root user"
if [[ $PATH != *"/usr/local/bin"* ]]; then
	PATH="/usr/local/bin:$PATH"
fi


#
# For now this script is not called within the same shell as install.sh
# and thus it needs to know how to get to the config.sh script on it's own
#
source "/opt/.deploy-meza/config.sh" # FIXME assumes installed in /opt


# prompt for wikis to merge
while [ -z "$wikis" ]
do
echo -e "Enter comma-separated list of wikis to merge and hit [ENTER]: "
read wikis
done

# for new wiki id
while [ -z "$wiki_id" ]
do
echo -e "Enter the ID of the new wiki you're creating and hit [ENTER]: "
read wiki_id
done

# FIXME assumes installed in /opt
if [ -d "/opt/.deploy-meza/public/wikis/$wiki_id" ]; then

	if [ "$skip_confirm_merge" != "y" ]; then
		echo
		echo
		echo -e "Are you sure you want to import into $wiki_id? Type \"y\" and hit [ENTER]: "
		read confirm_merge

		# Confirm you want to import into this existing wiki
		if [ "$confirm_merge" != "y" ]; then
			echo
			echo "User does not want to merge into $wiki_id"
			exit 1
		fi
	fi

else

	# new wiki name
	while [ -z "$wiki_name" ]
	do
		echo -e "Enter the name of the new wiki and hit [ENTER]: "
		read wiki_name
	done

	meza create wiki-promptless "$1" "$wiki_id" "$wiki_name"

fi


echo -e "\nBefore doing anything, run a cleanup..."
WIKI="$wiki_id" php "$m_scripts/uniteTheWikis.php" --cleanup


echo -e "\nSetting up merge"
WIKI="$wiki_id" php "$m_scripts/uniteTheWikis.php" "--mergedwiki=$wiki_id" "--sourcewikis=$wikis"


# Each pass of this loop checks to see how many imports are remaining
# This is broken out this way because PHP CLI has a memory leak (I think), and
# letting bash control repeated calls to the script gets around this.
while [[ `WIKI="$wiki_id" php "$m_scripts/uniteTheWikis.php" --imports-remaining` != "0" ]]; do
	echo -e "\n\n*********************\nANOTHER ROUND\n******************\n"
	echo "Clean out hoards of temp files"
	find /tmp -name "importupload*" -print0 | xargs -0 rm -f
	echo "run uniteTheWikis.php again"
	WIKI="$wiki_id" php "$m_scripts/uniteTheWikis.php"
done;

# for wiki in $(echo $wikis | sed "s/,/ /g")
# do
# 	for dir in 0 1 2 3 4 5 6 7 8 9 a b c d e f
# 	do
# 		echo "Importing from $m_uploads_dir/$wiki/$dir"
# 		WIKI="$wiki_id" "$m_mediawiki/maintenance/run importImages" --search-recursively "$m_uploads_dir/$wiki/$dir"
# 	done
# done

# Seemed to be a memory leak in rebuildall.php. Breaking it up into its
# component scripts to limit impact.
# WIKI="$wiki_id" "$m_mediawiki/maintenance/run rebuildall"


# FIXME: Is this even necessary with elasticsearch?
echo "Beginning rebuildtextindex.php script"
WIKI="$wiki_id" "$m_mediawiki/maintenance/run rebuildtextindex"

echo "Beginning rebuildrecentchanges.php script"
WIKI="$wiki_id" "$m_mediawiki/maintenance/run rebuildrecentchanges"

# num_pages=$(WIKI="$wiki_id" "$m_mediawiki/maintenance/run showSiteStats.php" | grep "Total pages" | sed 's/[^0-9]*//g')
num_pages=$(mysql -s -r -e"USE wiki_$wiki_id; SELECT page_id FROM page ORDER BY page_id DESC LIMIT 1;" | sed -n "1p")
end_id=0
delta=2000

echo "Beginning refreshLinks.php script"
echo "  Total pages = $num_pages"
echo "  Doing it in $delta-page chunks to avoid memory leak"

while [ "$end_id" -lt "$num_pages" ]; do
	start_id=$(($end_id + 1))
	end_id=$(($end_id + $delta))
	echo "Running refreshLinks.php from $start_id to $end_id"
	WIKI="$wiki_id" "$m_mediawiki/maintenance/run refreshLinks" --e "$end_id" -- "$start_id"
done

start_id=$(($end_id + 1))
echo "Running final refreshLinks.php in case there are more pages beyond num_pages, beyond $start_id"
WIKI="$wiki_id" "$m_mediawiki/maintenance/run refreshLinks" "$start_id"

# Merge watchlists
echo -e "\nMerging watchlists..."
WIKI="$wiki_id" php "$m_scripts/uniteTheWikis.php" --merge-watchlists

# Don't clean up merge table until rebuild all and images are imported. That
# way if this needs to stop and restart it won't try to reimport.
echo -e "\nCleaning up..."
WIKI="$wiki_id" php "$m_scripts/uniteTheWikis.php" --cleanup

echo -e "\nCOMPLETE!"

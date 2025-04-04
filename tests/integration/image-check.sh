#!/bin/sh
#
# Test if an image exists on a wiki
# This script expects two arguments:
# 1. The wiki ID
# 2. The title of the image to check
# e.g. if you have an image at https://localhost/demo/File:Logo-mc.png
# you would run this script with "demo" and "Logo-mc.png" as arguments


# -e: kill script if anything fails
# -u: don't allow undefined variables
# -x: debug mode; print executed commands
set -eux

origin="http://127.0.0.1:8080"
wiki_id="$1"
image_title="$2"
expected_code="200"


# Check if title of "Test image" exists
api_url_base="$origin/$wiki_id/api.php"
api_url_image="$api_url_base?action=query&titles=File:$image_title&prop=imageinfo&iiprop=sha1|url&format=json"
curl --insecure -L "$api_url_image" | jq '.query.pages[].title'

# Get image url according to database (via API)
# We could also get the sha1 hash and check the file system 
img_url=$( curl --insecure -L "$api_url_image" | jq --raw-output '.query.pages[].imageinfo[0].url' --exit-status )
# remove protocol, numeric domain and trailing slash
img_url=$( echo $img_url | sed 's/https:\/\/[[:digit:]]\+\.[[:digit:]]\+\.[[:digit:]]\+\.[[:digit:]]\+\///' )
# remove protocol, 'localhost' domain and trailing slash
img_url=$( echo $img_url | sed 's/https:\/\/localhost\///' )
# set URL to the internal URL
img_url="http://127.0.0.1:8080/$img_url"

# Retrieve image
curl --write-out %{http_code} --silent --output /dev/null "$img_url" \
	| grep -q "$expected_code" \
	&& (echo 'Image test: pass' && exit 0) \
	|| (echo 'Image test: fail' && exit 1)


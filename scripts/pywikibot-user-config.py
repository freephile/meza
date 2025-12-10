# PyWikibot Configuration for Freephile Wiki
# Save this as user-config.py in your pywikibot directory
# pylint: skip-file
# flake8: noqa
# This file uses PyWikibot's configuration format which defines variables dynamically

# The family of your wiki
family = 'freephile'

# The wiki language code (usually 'en' for English wikis)
mylang = 'en'

# The username - use your actual account name (not 'botname')
# Bot passwords from Special:BotPasswords automatically provide bot flag
usernames['freephile']['en'] = 'Greg Rundlett'

# Maximum time to wait for API queries (seconds)
put_throttle = 0

# Minimum delay between edits (seconds)
# Set to 0 for bot accounts, higher for non-bot accounts
minthrottle = 0
maxthrottle = 1

# Make bot flag edits (if your account has bot flag)
simulate = False

# Console encoding
console_encoding = 'utf-8'

# User agent format
user_agent_format = 'Greg Rundlett bot/1.0 (Pywikibot/{version}; +https://wiki.freephile.org/User:Greg Rundlett) {script}'

# Maximum number of retries
max_retries = 3

# Timeout for API requests
# this was not recognized in my pwb installation
# timeout = 120

# Creating MediaWiki Feature Pages with PyWikibot

This directory contains scripts to programmatically create Feature pages on the Freephile Wiki for MediaWiki extensions.

## Overview

The script `create_extension_features.py` uses **PyWikibot** to create Feature pages for all bundled MediaWiki extensions in Meza. It automates the process of creating properly formatted pages using the Feature template.

## Why PyWikibot?

- **Native MediaWiki integration**: Built specifically for MediaWiki operations
- **Page Forms support**: Handles Semantic MediaWiki and Page Forms templates
- **Python-based**: Integrates with Meza's existing Python infrastructure
- **Robust error handling**: Suitable for batch operations
- **Dry-run capability**: Test before making actual edits

## Setup Instructions

### 1. Install PyWikibot

```bash
pip install pywikibot
```

### 2. Configure PyWikibot Family

PyWikibot needs to know about your wiki. Create a family file:

```bash
# Create the family file directory
mkdir -p ~/.pywikibot/families

# Create the freephile_family.py file
cat > ~/.pywikibot/families/freephile_family.py << 'EOF'
from pywikibot import family

class Family(family.Family):
    name = 'freephile'

    langs = {
        'en': 'wiki.freephile.org',
    }

    def protocol(self, code):
        return 'https'

    def scriptpath(self, code):
        return '/wiki'

    def apipath(self, code):
        return '/wiki/api.php'
EOF
```

### 3. Configure User Settings

Copy the configuration template:

```bash
cp scripts/pywikibot-user-config.py ~/.pywikibot/user-config.py
```

Edit `~/.pywikibot/user-config.py` and update:
- `usernames['freephile']['en']` - Set to your actual username (e.g., 'Greg Rundlett')
  - **Note**: Use your account name without 'bot' suffix, even for bot operations
  - Bot flag is automatic when using bot passwords (Special:BotPasswords)

### 4. Login to the Wiki

```bash
python pwb.py login
```

Enter your bot password when prompted (create one at Special:BotPasswords on your wiki). This will store your login credentials.

**Important**:
- Use your regular username (e.g., 'Greg Rundlett'), not 'botname'
- Create a bot password at `https://wiki.freephile.org/wiki/Special:BotPasswords`
- The bot password format is: `username@botname` + password
- PyWikibot will automatically use the bot flag with bot passwords

## Usage

### Dry Run (Recommended First)

Test without making any edits:

```bash
cd /home/greg/src/meza
python scripts/create_extension_features.py --dry-run
```

### Create All Feature Pages

```bash
python scripts/create_extension_features.py
```

### Create Specific Extensions Only

```bash
python scripts/create_extension_features.py --extensions VisualEditor Scribunto Echo
```

### Overwrite Existing Pages

```bash
python scripts/create_extension_features.py --force
```

## Command-Line Options

- `--dry-run` - Show what would be done without making actual edits
- `--force` - Overwrite existing pages (default: skip existing)
- `--extensions EXT1 EXT2` - Only process specific extensions
- `--site SITENAME` - Use different site family (default: freephile)

## What the Script Does

1. Connects to wiki.freephile.org using your bot account
2. For each extension in the list:
   - Creates page: `Feature:<ExtensionName>`
   - Fills in the Feature template with:
     - Title
     - Description (what it does)
     - Notes (technical details, requirements)
     - Tests (how to verify it works)
     - Examples (usage examples)
   - Adds categories: `[[Category:Feature]]` and `[[Category:MediaWiki Extension]]`
3. Reports success/failure for each page

## Example Output

```
Processing: Feature:VisualEditor
  ✓ Successfully created: Feature:VisualEditor

Processing: Feature:Scribunto
  ✓ Successfully created: Feature:Scribunto

Processing: Feature:Echo
  ⚠ Page already exists, skipping (use --force to overwrite)

============================================================
SUMMARY
============================================================
Created/Updated: 2
Skipped: 1
Errors: 0
Total: 3
```

## Extensions Included

The script creates Feature pages for these 35 extensions:

- AbuseFilter
- CategoryTree
- CheckUser
- Cite
- CiteThisPage
- CodeEditor
- ConfirmEdit
- DiscussionTools
- Echo
- Gadgets
- ImageMap
- InputBox
- Linter
- LoginNotify
- Math
- MultimediaViewer
- Nuke
- OATHAuth
- PageImages
- ParserFunctions
- PdfHandler
- Poem
- ReplaceText
- Scribunto
- SecureLinkFixer
- SpamBlacklist
- SyntaxHighlight
- TemplateData
- TemplateStyles
- TextExtracts
- Thanks
- TitleBlacklist
- VisualEditor
- WikiEditor

## Troubleshooting

### "Error connecting to wiki"

1. Verify family file is created correctly at `~/.pywikibot/families/freephile_family.py`
2. Check user-config.py is at `~/.pywikibot/user-config.py`
3. Run `python pwb.py login` to authenticate

### "Page already exists"

Use `--force` flag to overwrite, or edit manually on the wiki.

### "Permission denied"

Make sure your account has:
- Edit permissions
- Page creation permissions
- A bot password created at Special:BotPasswords (provides automatic bot flag)

**Note**: You don't need a separate bot account. Use your regular account with a bot password.

### "Import pywikibot could not be resolved"

This is just a linting warning. Install pywikibot with `pip install pywikibot` to resolve.

## Alternative: JavaScript Approach

If you prefer JavaScript, you could use the MediaWiki API directly:

```javascript
// Using mwn (MediaWiki Node.js) library
const {mwn} = require('mwn');

const bot = await mwn.init({
    apiUrl: 'https://wiki.freephile.org/wiki/api.php',
    username: 'Greg Rundlett',
    password: 'YOUR_BOT_PASSWORD'  // From Special:BotPasswords
});

await bot.create('Feature:VisualEditor', content, 'Creating feature page');
```

However, PyWikibot is recommended for this use case due to better error handling and MediaWiki integration.

## Alternative: AutoWikiBrowser

AutoWikiBrowser (AWB) is Windows-only and GUI-based, making it less suitable for:
- Automated batch operations
- Server-side execution
- Version control integration
- Scripting/automation workflows

## Modifying Extension Data

To add or modify extension information, edit the `EXTENSIONS` list in `create_extension_features.py`. Each extension is a dictionary with these fields:

```python
{
    'name': 'ExtensionName',          # Page will be Feature:ExtensionName
    'title': 'Display Title',
    'description': 'What it does...',  # Mandatory field
    'notes': 'Technical details...',
    'tests': 'How to test...',
    'examples': 'Usage examples...',
}
```

## Bot Best Practices

1. **Always dry-run first**: Use `--dry-run` to preview changes
2. **Use bot passwords**: Create a bot password at Special:BotPasswords for your regular account
   - Use your actual username in config (e.g., 'Greg Rundlett')
   - Bot passwords automatically provide bot flag
   - No need for a separate bot account
3. **Rate limiting**: Script includes throttling to avoid overwhelming the server
4. **Edit summaries**: All edits include clear summaries explaining the automation
5. **Error handling**: Script reports errors and continues processing remaining pages

## See Also

- [PyWikibot Documentation](https://www.mediawiki.org/wiki/Manual:Pywikibot)
- [MediaWiki API](https://www.mediawiki.org/wiki/API:Main_page)
- [Page Forms](https://www.mediawiki.org/wiki/Extension:Page_Forms)
- [Semantic MediaWiki](https://www.semantic-mediawiki.org/)

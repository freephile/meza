#!/usr/bin/env python3
"""
Create Feature pages for MediaWiki extensions using PyWikibot.
This script reads extension data and creates Feature: pages on the wiki
using the Feature form/template structure.

Requirements:
    pip install pywikibot

Setup:
    1. Configure user-config.py for your wiki (see pywikibot documentation)
    2. Login: python pwb.py login
    3. Run: python create_extension_features.py

Usage:
    python create_extension_features.py [--dry-run] [--force]
"""

import argparse
import sys
import pywikibot

# Extension data with Feature template fields
EXTENSIONS = [
    {
        'name': 'AbuseFilter',
        'title': 'AbuseFilter',
        'description': 'Provides automated filtering and moderation tools to prevent vandalism and abuse. Allows administrators to create rules that automatically block or flag edits matching specified patterns, helping maintain wiki quality through automated content moderation.',
        'notes': 'Requires specific user permissions. Can use regular expressions and wiki syntax conditions to detect harmful edits.',
        'tests': 'Create test rules, attempt flagged edits, verify blocking/warnings work correctly',
        'examples': 'Block edits containing external links from new users; Warn users adding common spam patterns; Flag large deletions for review',
    },
    {
        'name': 'CategoryTree',
        'title': 'CategoryTree',
        'description': 'Provides a dynamic tree view of the wiki\'s category structure. Enables users to browse and navigate categories hierarchically with expandable/collapsible trees, making it easier to explore the organization of wiki content.',
        'notes': 'Adds <categorytree> parser function and special page',
        'tests': 'Add categorytree tag to page, verify category expansion works',
        'examples': '<categorytree>Main topic categories</categorytree>; Display full category hierarchy on portal pages',
    },
    {
        'name': 'CheckUser',
        'title': 'CheckUser',
        'description': 'Allows privileged users to check IP addresses and other technical information about user accounts. Critical for identifying sockpuppets, coordinated vandalism, and policy violations by correlating technical data across accounts.',
        'notes': 'Restricted to checkuser user group. Maintains detailed audit logs for privacy compliance.',
        'tests': 'Verify checkuser interface loads, check permissions properly restricted',
        'examples': 'Identify sockpuppet accounts; Investigate coordinated vandalism; Trace abuse patterns',
    },
    {
        'name': 'Cite',
        'title': 'Cite',
        'description': 'Enables footnote citations using <ref> and <references> tags. Essential for creating properly cited content with numbered footnotes, allowing wikis to maintain academic and encyclopedic standards with proper source attribution.',
        'notes': 'Core citation extension used across most wikis',
        'tests': 'Add <ref> tags to content, verify footnotes render correctly',
        'examples': '<ref>Source citation here</ref> with <references /> at bottom; Named references for repeated citations',
    },
    {
        'name': 'CiteThisPage',
        'title': 'CiteThisPage',
        'description': 'Adds a special page that generates citation text for wiki pages in various academic formats (APA, MLA, Chicago, etc.). Helps users properly cite wiki content in their research and publications.',
        'notes': 'Accessible via Special:CiteThisPage or toolbox link',
        'tests': 'Navigate to Special:CiteThisPage, verify citation formats generate correctly',
        'examples': 'Generate APA citation for research papers; Create bibliographic entries; Export citation metadata',
    },
    {
        'name': 'CodeEditor',
        'title': 'CodeEditor',
        'description': 'Provides syntax highlighting and code editing features for editing JavaScript, CSS, Lua, and JSON pages. Enhances the editing experience for technical content with line numbers, syntax coloring, and code-aware indentation.',
        'notes': 'Based on Ace editor. Works in edit mode for supported content types.',
        'tests': 'Edit JavaScript/CSS/Lua page, verify syntax highlighting appears',
        'examples': 'Edit MediaWiki:Common.js with syntax highlighting; Modify Scribunto modules with code completion',
    },
    {
        'name': 'ConfirmEdit',
        'title': 'ConfirmEdit (CAPTCHA)',
        'description': 'Provides CAPTCHA and other confirmation mechanisms to prevent automated spam and bot abuse. Includes multiple CAPTCHA types including ReCaptcha, QuestyCaptcha, and simple math problems.',
        'notes': 'Configure CAPTCHA type in LocalSettings.php. Can trigger on specific actions.',
        'tests': 'Attempt actions requiring CAPTCHA, verify challenge displays',
        'examples': 'Require CAPTCHA for external links; Challenge anonymous edits; Prevent automated account creation',
    },
    {
        'name': 'DiscussionTools',
        'title': 'DiscussionTools',
        'description': 'Modernizes talk page discussions with user-friendly reply tools, visual threading, and inline editing. Makes talk pages more accessible by providing visual comment buttons and structured discussion workflows.',
        'notes': 'Modern alternative to traditional talk page editing',
        'tests': 'Add reply to talk page, verify threading and signatures work',
        'examples': 'Reply to discussions inline; Subscribe to specific topics; Visual comment threading',
    },
    {
        'name': 'Echo',
        'title': 'Echo (Notifications)',
        'description': 'Provides a comprehensive notification system for user interactions. Alerts users about talk page messages, mentions, page links, thanks, and other wiki events through both on-wiki and email notifications.',
        'notes': 'Customizable notification preferences per user',
        'tests': 'Trigger notifications, verify delivery in UI and email',
        'examples': 'Talk page message alerts; Page mention notifications; Thank you notifications; Edit revert alerts',
    },
    {
        'name': 'Gadgets',
        'title': 'Gadgets',
        'description': 'Allows administrators to define JavaScript/CSS gadgets that users can enable in their preferences. Provides a framework for optional user interface enhancements and tools without requiring user technical knowledge.',
        'notes': 'Gadgets defined in MediaWiki namespace. Can be enabled/disabled per user.',
        'tests': 'Create test gadget, verify appears in user preferences',
        'examples': 'Advanced editing toolbars; Navigation helpers; Admin maintenance tools; Custom formatting buttons',
    },
    {
        'name': 'ImageMap',
        'title': 'ImageMap',
        'description': 'Enables creation of clickable image maps with defined regions linking to different pages. Useful for creating interactive diagrams, maps, and visual navigation elements.',
        'notes': 'Uses <imagemap> tag with coordinate-based region definitions',
        'tests': 'Create imagemap with multiple regions, verify clickable areas work',
        'examples': 'Interactive geographical maps; Clickable organizational charts; Visual navigation menus',
    },
    {
        'name': 'InputBox',
        'title': 'InputBox',
        'description': 'Provides simple input forms for creating pages, searching, and commenting. Enables creation of customized input boxes that can be embedded on any wiki page for user interactions.',
        'notes': 'Uses <inputbox> tag with various type options',
        'tests': 'Create inputbox for page creation, verify submission works',
        'examples': 'Create new page forms; Custom search boxes; Comment submission forms; Category page creators',
    },
    {
        'name': 'Linter',
        'title': 'Linter',
        'description': 'Identifies and reports wikitext lint errors that may cause problems with content parsing or display. Helps maintain clean wikitext by flagging deprecated syntax, misnested tags, and parsing issues.',
        'notes': 'Provides Special:LintErrors for tracking issues',
        'tests': 'Create page with lint errors, verify detection in Special:LintErrors',
        'examples': 'Detect misnested tags; Find obsolete HTML; Identify parsing ambiguities',
    },
    {
        'name': 'LoginNotify',
        'title': 'LoginNotify',
        'description': 'Sends notifications to users when their account is accessed from an unfamiliar device or location. Enhances account security by alerting users to potential unauthorized access attempts.',
        'notes': 'Sends Echo notifications and emails for suspicious logins',
        'tests': 'Login from new location/browser, verify notification sent',
        'examples': 'Alert on login from new country; Notify on failed login attempts; Security breach detection',
    },
    {
        'name': 'Math',
        'title': 'Math',
        'description': 'Enables rendering of mathematical formulas using LaTeX syntax via <math> tags. Supports both simple inline equations and complex display mathematics, essential for scientific and technical wikis.',
        'notes': 'Can use MathML, SVG, or PNG rendering modes',
        'tests': 'Add <math> tags with equations, verify proper rendering',
        'examples': '<math>E=mc^2</math>; Complex equations with integrals and matrices; Chemical formulas',
    },
    {
        'name': 'MultimediaViewer',
        'title': 'MultimediaViewer',
        'description': 'Provides an enhanced full-screen image viewing experience with metadata display. Shows images in an attractive lightbox interface with detailed information about licensing, author, and technical details.',
        'notes': 'Can be disabled per-user in preferences',
        'tests': 'Click image on wiki page, verify lightbox viewer appears',
        'examples': 'View high-resolution images; Display image metadata; Navigate image galleries',
    },
    {
        'name': 'Nuke',
        'title': 'Nuke',
        'description': 'Allows administrators to mass delete pages created by spammers or vandals. Provides Special:Nuke for quickly removing large numbers of unwanted pages based on username or pattern.',
        'notes': 'Restricted to sysop group. Use with caution.',
        'tests': 'Create test spam pages, verify mass deletion works',
        'examples': 'Remove spam pages from blocked user; Delete vandalism batches; Clean up test content',
    },
    {
        'name': 'OATHAuth',
        'title': 'OATHAuth (Two-Factor Authentication)',
        'description': 'Provides two-factor authentication (2FA) using TOTP (Time-based One-Time Passwords). Enhances account security by requiring both password and authenticator app verification.',
        'notes': 'Users enable via Special:OATH. Compatible with Google Authenticator, Authy, etc.',
        'tests': 'Enable 2FA for test account, verify login requires both factors',
        'examples': 'Protect administrator accounts; Secure privileged access; Prevent account hijacking',
    },
    {
        'name': 'PageImages',
        'title': 'PageImages',
        'description': 'Identifies and stores representative images for pages. Provides API access to page thumbnail images, used by various extensions and external applications for visual page representations.',
        'notes': 'Used by many extensions including RelatedArticles, PagePreviews',
        'tests': 'Add images to pages, verify pageimages API returns correct image',
        'examples': 'Provide images for page previews; Generate social media thumbnails; Enable visual navigation',
    },
    {
        'name': 'ParserFunctions',
        'title': 'ParserFunctions',
        'description': 'Adds essential parser functions for conditional logic, string manipulation, and calculations. Provides #if, #switch, #time, #expr and other functions critical for template programming and dynamic content.',
        'notes': 'Fundamental extension for advanced templates',
        'tests': 'Use {{#if:}}, {{#expr:}}, verify correct evaluation',
        'examples': '{{#if:{{{param|}}}|show this|or this}}; {{#expr:2+2}}; {{#time:Y-m-d}}; Complex template logic',
    },
    {
        'name': 'PdfHandler',
        'title': 'PdfHandler',
        'description': 'Enables upload and display of PDF files with thumbnail generation. Shows PDF previews on file description pages and allows multi-page PDF navigation within the wiki interface.',
        'notes': 'Requires Ghostscript or similar PDF processing tools',
        'tests': 'Upload PDF file, verify thumbnail generation and preview',
        'examples': 'Upload documentation PDFs; Display research papers; Share presentations',
    },
    {
        'name': 'Poem',
        'title': 'Poem',
        'description': 'Provides <poem> tag for displaying poetry and preformatted text while maintaining line breaks and indentation. Preserves formatting without the visual styling of <pre> tags.',
        'notes': 'Useful for poetry, lyrics, code samples, addresses',
        'tests': 'Add <poem> tag with multi-line content, verify formatting preserved',
        'examples': '<poem>Roses are red\\nViolets are blue</poem>; Display formatted addresses; Show code snippets',
    },
    {
        'name': 'ReplaceText',
        'title': 'ReplaceText',
        'description': 'Provides Special:ReplaceText for performing find-and-replace operations across multiple wiki pages. Enables bulk text replacement with preview and confirmation before applying changes.',
        'notes': 'Restricted to administrators. Can use regular expressions.',
        'tests': 'Use Special:ReplaceText to change text across pages, verify replacements',
        'examples': 'Update renamed project names; Fix recurring typos; Bulk update template calls',
    },
    {
        'name': 'Scribunto',
        'title': 'Scribunto (Lua scripting)',
        'description': 'Enables Lua scripting within wiki templates via Module namespace. Provides powerful programming capabilities for complex templates, calculations, and dynamic content generation beyond basic parser functions.',
        'notes': 'Modules in Module: namespace. Invoked via {{#invoke:}}',
        'tests': 'Create Lua module, invoke from template, verify execution',
        'examples': 'Complex infoboxes; Data processing; String manipulation; Mathematical calculations',
    },
    {
        'name': 'SecureLinkFixer',
        'title': 'SecureLinkFixer',
        'description': 'Automatically upgrades HTTP links to HTTPS where possible. Helps maintain secure browsing by converting insecure external links to their secure equivalents.',
        'notes': 'Works automatically on external links',
        'tests': 'Add HTTP links, verify automatic HTTPS upgrade where available',
        'examples': 'Convert http://wikipedia.org to https://wikipedia.org; Maintain secure browsing context',
    },
    {
        'name': 'SpamBlacklist',
        'title': 'SpamBlacklist',
        'description': 'Prevents addition of URLs matching blacklist patterns. Blocks spam by comparing external links against local and shared blacklists, preventing known spam sites from being added.',
        'notes': 'Uses regex patterns in MediaWiki:Spam-blacklist',
        'tests': 'Add blacklisted URL, verify edit is blocked',
        'examples': 'Block known spam domains; Prevent malicious links; Use shared MediaWiki spam blacklist',
    },
    {
        'name': 'SyntaxHighlight',
        'title': 'SyntaxHighlight',
        'description': 'Provides syntax highlighting for code blocks using Pygments. Supports hundreds of programming languages with <syntaxhighlight> tag, making code examples readable with appropriate color coding.',
        'notes': 'Requires Python and Pygments. Supports line numbers, highlighting specific lines.',
        'tests': 'Add <syntaxhighlight lang="python"> code block, verify highlighting',
        'examples': '<syntaxhighlight lang="python">print("Hello")</syntaxhighlight>; Display code with line numbers; Highlight changed lines',
    },
    {
        'name': 'TemplateData',
        'title': 'TemplateData',
        'description': 'Provides machine-readable documentation for templates using JSON metadata. Enables VisualEditor\'s template dialog to offer user-friendly forms for template parameters with descriptions and suggested values.',
        'notes': 'Uses <templatedata> JSON block in template documentation',
        'tests': 'Add TemplateData to template, verify VisualEditor shows parameter form',
        'examples': 'Document template parameters; Enable visual template editing; Provide parameter descriptions and types',
    },
    {
        'name': 'TemplateStyles',
        'title': 'TemplateStyles',
        'description': 'Allows templates to have associated CSS stylesheets stored as sanitized CSS pages. Enables modular styling per template without cluttering site-wide CSS, improving performance and maintainability.',
        'notes': 'CSS pages in Template: namespace with .css suffix',
        'tests': 'Create TemplateStyles page, use in template, verify styling applies',
        'examples': 'Style infoboxes; Template-specific formatting; Modular CSS design',
    },
    {
        'name': 'TextExtracts',
        'title': 'TextExtracts',
        'description': 'Provides API for extracting plain text summaries and snippets from pages. Used by various extensions and applications to generate page previews, summaries, and search result snippets.',
        'notes': 'API-focused extension. Used by PagePreviews, mobile apps.',
        'tests': 'Query textextracts API, verify summary generation',
        'examples': 'Generate page summaries; Create search result snippets; Provide hover previews',
    },
    {
        'name': 'Thanks',
        'title': 'Thanks',
        'description': 'Allows users to send thanks to other editors for their contributions. Promotes positive community interaction by providing a simple way to acknowledge helpful edits and good contributions.',
        'notes': 'Adds thank links to diffs and history. Sends Echo notifications.',
        'tests': 'Thank another user for edit, verify notification sent',
        'examples': 'Thank editors for helpful contributions; Encourage new users; Build positive community',
    },
    {
        'name': 'TitleBlacklist',
        'title': 'TitleBlacklist',
        'description': 'Prevents creation of pages with titles matching blacklist patterns. Blocks spam and unwanted pages by filtering page names against regex patterns, preventing common spam page titles.',
        'notes': 'Configure in MediaWiki:Titleblacklist',
        'tests': 'Attempt to create blacklisted page title, verify blocking',
        'examples': 'Block spam page patterns; Prevent test pages in main namespace; Restrict page naming',
    },
    {
        'name': 'VisualEditor',
        'title': 'VisualEditor',
        'description': 'Provides WYSIWYG editing interface for wiki pages. Enables users to edit pages without learning wikitext syntax, dramatically lowering the barrier to entry for new editors while maintaining clean underlying markup.',
        'notes': 'Requires Parsoid service. Modern editing experience.',
        'tests': 'Edit page with VisualEditor, verify changes save correctly',
        'examples': 'Visual page editing; Rich text formatting; Template visual editing; Table creation; Image insertion',
    },
    {
        'name': 'WikiEditor',
        'title': 'WikiEditor',
        'description': 'Provides enhanced wikitext editing toolbar with formatting buttons, search/replace, and syntax highlighting. Improves the traditional source editing experience with helpful tools while maintaining full wikitext control.',
        'notes': 'Enhanced toolbar for wikitext editing mode',
        'tests': 'Edit in wikitext mode, verify toolbar and features present',
        'examples': 'Wikitext syntax highlighting; Advanced search/replace; Formatting buttons; Character inserter',
    },
]


def create_feature_page_content(ext_data):
    """Generate wikitext for a Feature page using the Feature template."""
    template = """{{{{Feature
|image=
|imgdesc=
|title={title}
|description={description}
|notes={notes}
|tests={tests}
|examples={examples}
}}}}

[[Category:Feature]]
[[Category:MediaWiki Extension]]
"""

    return template.format(
        title=ext_data['title'],
        description=ext_data['description'],
        notes=ext_data['notes'],
        tests=ext_data['tests'],
        examples=ext_data['examples']
    )


def create_feature_pages(site, extensions, dry_run=False, force=False):
    """
    Create Feature pages for each extension.

    Args:
        site: PyWikibot Site object
        extensions: List of extension dictionaries
        dry_run: If True, show what would be done without actually editing
        force: If True, overwrite existing pages
    """
    created = 0
    skipped = 0
    errors = 0

    for ext in extensions:
        page_title = f"Feature:{ext['name']}"
        page = pywikibot.Page(site, page_title)

        print(f"\nProcessing: {page_title}")

        # Check if page already exists
        if page.exists() and not force:
            print("  ⚠ Page already exists, skipping (use --force to overwrite)")
            skipped += 1
            continue

        content = create_feature_page_content(ext)

        if dry_run:
            print("  ℹ DRY RUN - Would create/update page:")
            print("  " + "="*60)
            print("  " + content[:200] + "...")
            print("  " + "="*60)
            created += 1
            continue

        try:
            # Save the page
            summary = f"Creating Feature page for {ext['name']} extension (automated via Greg Rundlett bot)"
            if page.exists():
                summary = f"Updating Feature page for {ext['name']} extension (automated via Greg Rundlett bot)"

            page.text = content
            page.save(summary=summary, minor=False, botflag=True)
            print(f"  ✓ Successfully {'updated' if page.exists() else 'created'}: {page_title}")
            created += 1

        except (pywikibot.exceptions.Error, OSError) as e:
            print(f"  ✗ Error saving {page_title}: {e}")
            errors += 1

    # Summary
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    print(f"Created/Updated: {created}")
    print(f"Skipped: {skipped}")
    print(f"Errors: {errors}")
    print(f"Total: {len(extensions)}")

    return created, skipped, errors


def main():
    """Main function to run the script."""
    parser = argparse.ArgumentParser(
        description='Create Feature pages for MediaWiki extensions',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Dry run to see what would be created
  python create_extension_features.py --dry-run

  # Create pages for real
  python create_extension_features.py

  # Overwrite existing pages
  python create_extension_features.py --force

  # Create only specific extensions
  python create_extension_features.py --extensions VisualEditor Scribunto
        """
    )

    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show what would be done without making actual edits'
    )

    parser.add_argument(
        '--force',
        action='store_true',
        help='Overwrite existing pages'
    )

    parser.add_argument(
        '--extensions',
        nargs='+',
        help='Only process specific extensions (by name)'
    )

    parser.add_argument(
        '--site',
        default='freephile',
        help='Site family name (default: freephile)'
    )

    args = parser.parse_args()

    # Filter extensions if specific ones requested
    extensions_to_process = EXTENSIONS
    if args.extensions:
        extensions_to_process = [
            ext for ext in EXTENSIONS
            if ext['name'] in args.extensions
        ]
        if not extensions_to_process:
            print(f"Error: No matching extensions found for: {args.extensions}")
            sys.exit(1)
        print(f"Processing {len(extensions_to_process)} extensions: {[e['name'] for e in extensions_to_process]}")

    # Initialize site
    try:
        site = pywikibot.Site()
        site.login()

        # Verify we're logged in as a bot account
        user = site.user()
        print(f"Logged in as: {user}")

        if 'bot' not in user.lower() and not args.dry_run:
            response = input("⚠ You're not logged in as a bot account. Continue? [y/N]: ")
            if response.lower() != 'y':
                print("Aborted.")
                sys.exit(0)

    except (pywikibot.exceptions.Error, OSError, RuntimeError) as e:
        print(f"Error connecting to wiki: {e}")
        print("\nMake sure you have:")
        print("1. Installed pywikibot: pip install pywikibot")
        print("2. Configured user-config.py for your wiki")
        print("3. Logged in: python pwb.py login")
        sys.exit(1)

    # Create the pages
    _created, _skipped, error_count = create_feature_pages(
        site,
        extensions_to_process,
        dry_run=args.dry_run,
        force=args.force
    )

    if args.dry_run:
        print("\n✓ Dry run complete. Use without --dry-run to actually create pages.")
    elif error_count > 0:
        sys.exit(1)
    else:
        print("\n✓ All done!")
if __name__ == '__main__':
    main()

# Copilot Instructions for CNC Resources Documentation

## Project Overview

This is Sienci Labs' public documentation repository for CNC hobbyist resources. The content is published to resources.sienci.com via WordPress sync using the Git-it-Write plugin. All documentation uses markdown with WordPress shortcodes and custom image classes.

## Content Structure

### Knowledge Bases (Product Lines)
- **lmmk2/** - LongMill MK2 CNC (primary hobbyist CNC router)
- **longmill/** - Original LongMill CNC (legacy)
- **mill-one/** - Mill One CNC (entry-level)
- **vortex/** - Vortex Rotary Axis (A-axis add-on)
- **altmill/** - AltMill CNC
- **laserbeam/** - LaserBeam laser module
- **gsender/** - gSender CNC control software
- **superlongboard/** - SuperLongBoard CNC controller (grblHAL-based)
- **cnc-fun/** - General CNC fundamentals and techniques

Each product folder contains:
- **index.md** - Template for new pages in that knowledge base
- **{product}-assembly/** - Assembly instructions
- **{product}-handbook/** - Operation, maintenance, troubleshooting
- **{product}-software/** - Software setup and configuration
- **{product}-the-basics/** - Getting started guides
- **{product}-add-ons/** - Compatible add-ons and upgrades

### Special Directories
- **_images/** - All documentation images (1820+ files)
- **_downloads/** - Downloadable files (CAD, firmware, templates)
- **_community-docs/** - Community-contributed content
- **_git/** - GitHub documentation images

## Maintenance Documentation Patterns

### Key Maintenance Files
- `lmk2-maintenance.md` - Comprehensive LongMill MK2 maintenance guide (PRIMARY REFERENCE)
- `vx-maintenance.md` - Vortex rotary axis maintenance
- `lm-troubleshooting.md` - LongMill troubleshooting guide
- `slb-troubleshooting.md` - SuperLongBoard diagnostics

### Maintenance Content Structure
1. **Typical Maintenance Schedule**
   - Every 10-20 hours: Rails, v-wheels, Delrin nuts cleaning
   - Every 20-30 hours: Linear guides lubrication, loose hardware check
   - Every 1500-2000 hours: V-wheel and anti-backlash nut replacement

2. **Standard Maintenance Sections**
   - Cleaning rails and V-wheels (black splotches removal)
   - Adjusting eccentric nuts (v-wheel tensioning)
   - Adjusting anti-backlash nuts (Delrin or spring-loaded)
   - Lubricating linear guides (Z-axis)
   - Checking loose hardware (set screws, couplers, fasteners)
   - Replacing consumables (v-wheels, nuts)

3. **Troubleshooting Categories**
   - Assembly issues (missing parts, threading problems)
   - Motor/controller issues (connectivity, movement errors)
   - Alarm codes and error messages
   - E-stop functionality
   - Firmware settings

## Writing Conventions

### Front Matter (Required for WordPress Sync)
```yaml
---
title: Page Title with Emoji 🛠️
menu_order: 8
post_status: publish|draft
post_excerpt: 160-character summary for SEO
post_date: YYYY-MM-DD HH:MM:SS
taxonomy:
    knowledgebase_cat: lmk2-handbook
    knowledgebase_tag:
        - mk2
custom_fields:
    KBName: LongMill MK2 CNC
    basepress_post_icon: bp-caret-right
skip_file: no|yes
featured_image: _images/_lmmk2/_handbook/filename.jpg
---
```

### Markdown + WordPress Extensions
- **Images**: `![Alt text](/_images/FILE_NAME "Caption"){.aligncenter .size-medium}`
  - Classes: `.size-medium`, `.flie` (linked), `.nar` (narrow), `.wid` (full-width)
- **Links**: Use `<a href="URL" target="_blank" rel="noopener">text</a>` for external links
- **Tabs**: `[tabby title="Title" open="yes"]Content[tabbyending]`
- **Spoilers**: `[su_spoiler title="Title"]Content[/su_spoiler]`
- **Buttons**: `[su_button url="URL" style="flat" background="var(--sl-blue)"]Text[/su_button]`
- **Tables**: Use `[su_csv_table url="URL" header="yes" responsive="yes"]` or HTML tables
- **Product Links**: Direct Sienci shop URLs work as shortcodes
- **YouTube**: Direct video URLs auto-embed
- **Lists**: Always use `1.` for numbered lists (auto-formatted), indent with 4 spaces

### Style Guidelines
1. Succinct, simple tone - complex terms only when necessary
2. Canadian English spelling (colour, centre, etc.)
3. Numbered steps for procedures, bullets for lists
4. Two line breaks between paragraphs
5. Bold for UI elements: **Click "Connect"**, **Settings** tab
6. Code for settings/commands: `$10 = 511`, `$rst=$`
7. Use emojis in titles sparingly for visual navigation

## Development Workflow

### Git/GitHub Setup
- Branch naming: descriptive feature/fix names
- Commit workflow: Create branch → Edit → Commit → Push → Pull Request
- Use VS Code with:
  - markdownlint extension (structural warnings)
  - Code Spell Checker + Canadian English dictionary
  - Batch Rename for file operations

### WordPress Sync (Git-it-Write Plugin)
- Sync triggered on push to main branch
- Max ~80 images per sync (manual pulls needed for larger batches)
- Images must be uploaded to GitHub first, then referenced
- Changing image filename requires deleting old from WordPress
- Use "ytsb" in URLs/titles to test as draft before publishing
- Matching Title + URL overwrites existing WordPress pages

### File Naming Conventions
- Lowercase with hyphens: `lmk2-maintenance.md`
- Folders start with underscore: `_images/`, `_downloads/`
- No spaces, use dashes
- Product prefixes: `lmk2-`, `lm-`, `mo-`, `vx-`, `slb-`, `gs-`

## Common Tasks

### Creating New Maintenance Section
1. Copy `index.md` from relevant knowledge base folder
2. Name file: `{product}-maintenance.md`
3. Update front matter (title, excerpt, menu_order, date)
4. Follow structure: Overview → Schedule → Procedures → Troubleshooting
5. Include images for each adjustment procedure
6. Reference product-specific parts with shop links
7. Embed videos for complex procedures
8. Set `skip_file: yes` until ready to publish

### Adding Troubleshooting Content
- Use descriptive headers: "### Motor Stalls During Cutting"
- Start with symptoms, then diagnosis steps
- Provide specific EEPROM settings: `$110`, `$111`, etc.
- Link to related maintenance procedures
- Include alarm/error code tables
- Reference forum posts for community solutions

### Updating Maintenance Schedule
- Base on product usage patterns (hobby vs production)
- Consider dust collection effectiveness
- Specify tool requirements (Allen keys, wrenches)
- Note consumable part lifespans
- Include product shop links for replacement parts

## Testing & Quality
- Preview in GitHub (limited - shortcodes won't render)
- Push to WordPress draft to verify full rendering
- Test all external links
- Verify image captions display correctly
- Check mobile responsiveness for tables
- Validate EEPROM settings against firmware version

## Key Resources
- Markdown guide: https://www.markdownguide.org/basic-syntax/
- Git-it-Write docs: https://www.aakashweb.com/docs/git-it-write/
- HTML table generator: https://www.tablesgenerator.com/html_tables
- Text comparison: https://www.textcompare.org/html/

## Notes
- License: CC BY-SA 4.0 (credit required, share-alike)
- Target audience: CNC hobbyists, varying skill levels
- Avoid jargon without explanation
- Link to glossary for technical terms: `cnc-common-terms.md`
- All measurements in metric and imperial

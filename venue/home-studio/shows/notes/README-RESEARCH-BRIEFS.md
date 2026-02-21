# Venue Research Briefs

Research briefs for `home-studio` live in this folder as:
- `<Song Name>.json` (machine-validated; required by generators)
- `<Song Name>.md` (human notes)

Generator enforcement reads from:
- `venue/home-studio/shows/notes/`

## Initialize Draft Brief

```bash
python3 venue/home-studio/shows/notes/init_brief.py "Artist - Song Title"
```

## Validate Briefs

```bash
python3 venue/home-studio/shows/notes/validate_briefs.py
```

Validate all venues:

```bash
python3 venue/home-studio/shows/notes/validate_briefs.py --all-venues
```

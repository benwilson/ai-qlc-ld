---
name: patch
description: >
  DMX patch management for QLC+ venues. Creates and updates venue patch files
  (venue/<name>/patch.md) that map fixtures from plot.md to DMX addresses, channel
  modes, and QLC+ IDs. Use this skill whenever the user mentions patching, DMX
  addressing, fixture addressing, channel modes, assigning addresses, or setting up
  a venue's DMX universe. Also trigger when creating a new venue or adding fixtures
  to an existing one that need DMX addresses. If a show generator needs patch info
  and no patch.md exists, trigger this skill first.
---

# Patch

Create and manage DMX patch files for QLC+ venues. A patch maps each fixture from
a venue's `plot.md` to a DMX address, channel mode, and QLC+ fixture ID.

## When to Use

- User says "patch," "address," "DMX address," "channel mode," or similar
- A new venue is created and fixtures need addressing
- Fixtures are added to an existing venue's `plot.md`
- A show generator needs patch data and no `patch.md` exists yet
- User wants to change a fixture's address or mode

## Workflow

### 1. Identify the Venue

Ask the user which venue to work with if not obvious from context. Read
`venue/<name>/plot.md` to get the fixture list.

### 2. Load or Create patch.md

Check if `venue/<name>/patch.md` exists.

- **Exists**: Read it, show the current patch, ask what the user wants to change.
- **Doesn't exist**: Start the patching workflow from scratch (step 3).

### 3. Walk Through Each Fixture (New Patch)

For each fixture listed in `plot.md`, in order:

1. **Match to a .qxf definition.** The "Type" column in `plot.md` corresponds to the
   `<Model>` element in .qxf files under `fixtures/`. Search for a matching .qxf file.
   If no match is found, tell the user and ask how to proceed.

2. **Determine the channel mode.** Parse the matched .qxf file for all `<Mode Name="...">`
   elements. Count the `<Channel>` children of each mode to get the channel count.
   - If only one mode exists, use it automatically and tell the user.
   - If multiple modes exist, present them with channel counts and ask the user to pick.
   - If no modes are found in the .qxf, report it as an invalid fixture definition.

3. **Assign a DMX address.** Suggest the next available address (starting from 1 for the
   first fixture, or after the last occupied channel for subsequent ones). Show the
   suggested address and the range it will occupy (e.g., "Address 97, channels 97-114").
   Let the user confirm or override.

4. **Assign a QLC+ fixture ID.** Auto-assign sequentially starting from 0 (or the next
   unused ID if some already exist). The user can override if they have a preference.

5. **Confirm and move to the next fixture.**

### 4. Conflict Detection

Before writing patch.md, check all address ranges for overlaps. If any two fixtures
have overlapping ranges (start address through start + channel_count - 1), warn the
user and ask them to resolve the conflict before proceeding.

### 5. Write patch.md

Save the completed patch to `venue/<name>/patch.md` using the format below.

## patch.md Format

```markdown
# Patch: <Venue Name>

Source: venue/<name>/plot.md
Generated: <YYYY-MM-DD>

## Universe 1

| Name | Fixture | QLC+ ID | Mode | Channels | DMX Start | DMX End |
|------|---------|---------|------|----------|-----------|---------|
| Back Left Sharpy | Sharpy Knockoff | 8 | 18 channel | 18 | 97 | 114 |
| ... | ... | ... | ... | ... | ... | ... |

## Address Map

```
001-015: Back Center 4BAR (4BAR, 15ch)
016-048: --free--
049-055: Right Wall Par 1 (36 RGB LED, 7ch)
056-062: Right Wall Par 2 (36 RGB LED, 7ch)
063-096: --free--
097-114: Back Left Sharpy (Sharpy Knockoff, 18ch)
115-144: --free--
145-164: Back Right BSW (Beam Spot Wash 3 in 1, 20ch)
165-192: --free--
193-206: Front Center Profile (Profile Knockoff, 14ch)
207-240: --free--
241-259: Back Wall NI3K (Nausea Inducer 3000, 19ch)
260-512: --free--
```
```

The Address Map section provides a linear view of the full 512-channel DMX universe
showing which ranges are occupied and which are free. This makes it easy to spot gaps
and plan future additions.

## Modifying an Existing Patch

When the user wants to change an existing patch:

1. Read the current `patch.md`.
2. Ask what they want to change (add fixture, move address, change mode, remove fixture).
3. For address changes, re-run conflict detection against all other fixtures.
4. Rewrite `patch.md` with the updated data.

## Notes

- DMX addresses in patch.md are **1-indexed** (1-512) as users think of them. Show
  generators and .qxw files use **0-indexed** addresses (0-511). The patch file uses
  1-indexed because it's a human-facing reference document.
- The .qxf files live in `fixtures/`. Match plot.md "Type" to .qxf `<Model>` element.
- When multiple fixtures share the same type (e.g., two "36 RGB LED" pars), each gets
  its own row with a unique name, ID, and address.
- Leave gaps between fixture address ranges if the user prefers — some users space
  fixtures at round numbers (1, 49, 97, 145...) for easier mental math on the console.

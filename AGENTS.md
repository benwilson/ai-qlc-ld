## Skills
A skill is a set of local instructions to follow that is stored in a `SKILL.md` file.

### Available skills
- qlc-show-workflow: Build and update venue-aware, song-synced QLC+ shows from `songs-data/` using phrase-aware planning and research-gated creative direction. Use this when creating a new show, iterating an existing generator, or running the full workflow (brief -> generator -> `.qxw` -> validation). (file: skills/qlc-show-workflow/SKILL.md)

### How to use skills
- Discovery: Skill bodies live on disk at the listed path.
- Trigger rules: If the user names a skill (with `$SkillName` or plain text) OR the request clearly matches the skill description, use that skill.
- Missing/blocked: If a named skill path cannot be read, say so briefly and continue with the best fallback.

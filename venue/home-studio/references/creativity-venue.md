# Home Studio Venue Creativity Layer

This file contains venue-specific creative mapping for `home-studio`.
Global (venue-agnostic) concepts remain in `references/creativity.md`.

## Fixture Role Mapping

- `PAR_A`: Back Center `4BAR` (4 individually aimable heads, RGB wash)
- `PAR_B`: Right Wall `Par 1 + Par 2` (RGB wall/side wash)
- `M1_BEAM`: Back Left Sharpy (tight beam, punch)
- `M2_HYBRID`: Back Right BSW 3-in-1 (beam/spot/wash behavior)
- `M3_PROFILE`: Front Center Profile (key/specials/texture)
- `M4_FX`: NI3K multi-head effect fixture

## Zone Mapping

Base zones:
- `USL`, `USC`, `USR`, `SL`, `C`, `SR`, `DSL`, `DSC`, `DSR`

Special zones:
- `DJ_BOOTH -> DJ`
- `PAR_WALL -> PAR_WALL`
- `DANCE_FLOOR -> DANCE`
- `DISCO_BALL -> DISCO_BALL`
- `CENTER_CEILING -> CEIL`

## PAR Head Notation (Venue-Specific)

- `A1..A4`: 4BAR heads (role `PAR_A`)
- `B1..B2`: right-wall PAR heads (role `PAR_B`)

## Local Source Files

- `venue/home-studio/plot.md`
- `venue/home-studio/patch.md`
- `venue/home-studio/focus-positions.md`

## Validation

```bash
python3 venue/home-studio/references/validate_profile.py
```

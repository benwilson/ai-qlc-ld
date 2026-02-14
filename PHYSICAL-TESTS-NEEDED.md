# Physical Tests Needed

Things that need to be tested on the actual fixtures using Simple Desk.
Check items off as completed and note the results.

## Sharpy Knockoff (ID 8)

- [ ] **7-color wheel positions (Ch16)**: Slowly sweep Ch16 from 0-255 and note what colors appear at what DMX values. Currently using estimated values.
- [ ] **Gobo wheel positions (Ch10)**: Sweep and note each gobo position. Currently using arbitrary values (20, 40, 60, 80).
- [ ] **Prism engagement thresholds**: What's the minimum Ch11/Ch13 value that actually engages the prism? Currently using 128.
- [ ] **Frost range (Ch5)**: Is it linear 0-255? Or does it engage at a specific threshold?
- [ ] **Color Macro (Ch8) vs 7-color (Ch16)**: Do they interact or are they independent? Can both be used at once?

## Profile Knockoff (ID 4)

- [ ] **Strobe channel (Ch1)**: Uses ShutterStrobeSlowFast preset — what are the actual ranges? Is 0=closed or 0=open? What value gives steady open with no strobe?
- [ ] **Color wheel positions (Ch5)**: Sweep and note colors at each DMX value. Uses ColorMacro preset.
- [ ] **Gobo positions (Ch6, Ch7)**: Two gobo channels — sweep each and note positions.
- [ ] **Prism range (Ch9)**: 0-255 with no defined capabilities. What values engage/disengage?

## Nausea Inducer 3000 (ID 3)

- [ ] **Tilt position mapping**: For tilts 1-3 (Ch1-3), what physical angle does each value 0-127 correspond to? Where is "straight ahead" vs "fully tilted"?
- [ ] **LED effect catalog (Ch11)**: Sweep 16-255 and note interesting effect positions.
- [ ] **Motor effect catalog (Ch12)**: Sweep 16-255 and note interesting effect positions.

## BSW 3-in-1 (ID 1)

- [ ] **Gobo 1 visual catalog**: What do gobos G1-1 through G1-7 actually look like?
- [ ] **Gobo 2 visual catalog**: What do gobos G2-1 through G2-6 actually look like?

## General

- [ ] **Pan/Tilt range mapping for all movers**: Note what pan/tilt values correspond to room boundaries (walls, ceiling, floor edges). This helps constrain movements to the actual room.

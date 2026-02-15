# Physical Tests Needed

Things that need to be tested on the actual fixtures using Simple Desk.
Check items off as completed and note the results.

## Sharpy Knockoff (ID 8)

- [x] **Color filter (Ch16)**: NOT a 7-color wheel. It's a single variable color filter — 0=open/white, gradually overlays filter to 255=full. Leave at 0.
- [ ] **Gobo wheel positions (Ch10)**: Sweep and note each gobo position. Currently using arbitrary values (20, 40, 60, 80).
- [ ] **Prism engagement thresholds**: What's the minimum Ch11/Ch13 value that actually engages the prism? Currently using 128.
- [ ] **Frost range (Ch5)**: Is it linear 0-255? Or does it engage at a specific threshold?
- [x] **Color Macro (Ch8)**: Verified full color wheel — White(0), Red(10), Yellow(20), Blue(30), Green(40), Purple(50), Pink(60), Teal(70), Amber(80), Orange(90), DkYellow(100), Lime(110), Grey(120). Odd values (5,15,25...) are split colors. 150-211=CW rotation fast→slow, 211-255=CCW slow→fast. Ch16 is independent (color filter, not wheel).

## Profile Knockoff (ID 4)

- [x] **Strobe channel (Ch1)**: 0=open (light output confirmed with dimmer at 255). Exact strobe ranges still TBD.
- [x] **Color wheel positions (Ch5)**: Verified — White(0), Red(5), Yellow(10), Blue(15), Green(20), Orange(25), Pink(30), Teal(35). 40-78=split colors. 79-255=wheel rotation slow→fast.
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

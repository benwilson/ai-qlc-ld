---
module: System
date: 2026-02-20
problem_type: test_failure
component: testing_framework
symptoms:
  - "python3 -m unittest discover finds 0 tests in test_phrase_planner.py"
  - "pytest runs tests fine but ci.sh (unittest discover) silently skips them"
  - "28 tests exist as bare def test_*() functions but are invisible to unittest"
root_cause: test_isolation
resolution_type: test_fix
severity: medium
tags: [unittest, test-discovery, pytest, ci]
---

# Troubleshooting: Tests Invisible to unittest discover (Bare Functions)

## Problem
`test_phrase_planner.py` contained 14+ test functions that ran fine under `pytest` but were completely invisible to `python3 -m unittest discover`, which is what `ci.sh` uses. Tests were silently skipped with no warning.

## Environment
- Module: System (testing infrastructure)
- Affected Component: tests/test_phrase_planner.py
- Date: 2026-02-20

## Symptoms
- `python3 -m unittest discover -s tests -v` showed 0 tests from test_phrase_planner.py
- `python3 -m pytest tests/test_phrase_planner.py` ran all tests successfully
- `ci.sh` (which uses unittest discover) reported a passing suite with fewer tests than expected
- No error or warning about skipped files

## What Didn't Work

**Direct solution:** The problem was identified during Task #12 when writing new tests. Noticed that `ci.sh` would never have run the existing tests either.

## Solution

Rewrote all test functions as `unittest.TestCase` methods organized into logical test classes.

**Code changes:**

```python
# Before (broken for unittest discover):
def test_loads_and_has_all_phrase_pools():
    planner = PhraseAwarePlanner(PROJECT_ROOT)
    assert set(planner.phrase_map.keys()) == {"intro", "verse_groove", "build", "drop", "breakdown", "outro"}

def test_phrase_classification_uses_expected_buckets():
    results = set()
    for label, rms, sub, high, prog in CLASSIFY_CASES:
        results.add(classify_phrase(label, rms, sub, high, prog))
    assert results == {"intro", "verse_groove", "build", "drop", "breakdown", "outro"}

# After (fixed - visible to unittest discover):
class PhrasePlannerCoreTests(unittest.TestCase):
    def test_loads_and_has_all_phrase_pools(self):
        planner = PhraseAwarePlanner(PROJECT_ROOT)
        self.assertEqual(
            set(planner.phrase_map.keys()),
            {"intro", "verse_groove", "build", "drop", "breakdown", "outro"},
        )

    def test_phrase_classification_uses_expected_buckets(self):
        results = set()
        for label, rms, sub, high, prog in CLASSIFY_CASES:
            results.add(classify_phrase(label, rms, sub, high, prog))
        self.assertEqual(results, {"intro", "verse_groove", "build", "drop", "breakdown", "outro"})
```

Organized 28 tests into 4 classes:
- `PhrasePlannerCoreTests` (14 tests) - existing tests converted
- `ShowlibWrapperTests` (2 tests) - existing tests converted
- `TransitionEventTests` (8 tests) - new
- `BeatReactivityTests` (4 tests) - new
- `ShowlibTransitionTests` (4 tests) - new

## Why This Works

1. **Root cause:** `python3 -m unittest discover` only finds test methods inside classes that inherit from `unittest.TestCase`. Bare `def test_*()` functions at module level are a pytest convention — pytest's collector finds them, but unittest's discovery mechanism does not.

2. **Silent failure:** unittest discover doesn't warn about files it scans but finds no TestCase classes in. It just moves on. This means a test file full of bare functions silently contributes 0 tests to the suite.

3. **The fix:** Converting to `unittest.TestCase` methods makes them visible to both pytest AND unittest discover. Using `self.assertEqual()` / `self.assertIn()` instead of bare `assert` also gives better failure messages.

## Prevention

- **Convention:** All test files in this project MUST use `unittest.TestCase` classes, not bare functions. `ci.sh` uses `python3 -m unittest discover`.
- **Spot check:** After adding tests, verify the count: `python3 -m unittest discover -s tests -v 2>&1 | tail -1` should show the expected total.
- **Don't mix frameworks:** If using pytest-style bare functions, the CI script must also use pytest. If CI uses unittest discover, all tests must be TestCase classes.

## Related Issues

No related issues documented yet.

# Guide: Writing Effective GitHub Copilot Instructions

This document shows practical, reusable patterns and lots of examples for writing instructions to GitHub Copilot (VS Code Copilot & Copilot Chat). Use these as templates for code generation, refactors, tests, documentation, PRs, automation, and code review prompts.

## What this guide covers

- Principles for clear instructions
- Compact instruction templates you can paste into Copilot Chat or use as inline comments
- Dozens of examples across languages and tasks (generate, refactor, test, review, security)
- Formats & constraints (required output shape, filenames, tests, performance limits)
- How to iterate with Copilot (feedback loops and validation)

## Principles (short)

1. Purpose-first: start with the goal ("Add X to do Y")
2. Context: provide repository/module/file context and relevant constraints
3. Output shape: show exact file names, function signatures, or JSON schema you expect
4. Constraints: performance, security, library versions, style
5. Examples: show an input -> desired output pair when possible
6. Validation: require unit tests or a smoke-run to assert correctness

## Quick instruction template (paste into Copilot Chat)

Use this as a compact template when asking for a change:

"Goal: <one-sentence goal>
Context: <repo path / target file / language / existing functions>
Constraints: <list of constraints>
Output: <file(s) and exact function signatures or JSON schema>
Tests: <unit tests to add>
Notes: <any edge cases or links to docs>"

Example:

"Goal: Add a function that computes the moving average of a list of floats.
Context: repo `src/analytics`, file `src/analytics/time_series.py`, Python 3.11.
Constraints: O(n) runtime, numeric stability for large floats, follow PEP8.
Output: add `def moving_average(values: Sequence[float], window: int) -> List[float]`.
Tests: add pytest tests `tests/test_time_series.py` covering odd/even windows and empty input.
Notes: use only stdlib and numpy is not allowed."

## How to ask for refactors

- Tell Copilot exactly what should not change (public API, DB schema).
- Provide small failing example to show current behavior.
- Ask for a unit test that demonstrates correct behavior and regression.

Example:

"Goal: Refactor `src/db/reader.py` to separate I/O from parsing.
Context: `Reader.read()` currently fetches HTTP and parses JSON then returns domain objects.
Constraints: Keep public method `read(url: str) -> List[Record]` unchanged.
Output: create `src/db/http_client.py` with `fetch_json(url)`, move parsing into `src/db/parse.py`, adapt `Reader` to call these helpers.
Tests: Add unit tests that monkeypatch `fetch_json` to return sample payload and assert `Reader.read()` returns expected `Record` list."

## How to ask for unit tests (examples)

- Be explicit about frameworks: pytest, unittest, or nose.
- Provide test cases and expected outputs.

Example (pytest):

"Goal: Add pytest tests for `normalize_scores(scores: List[int]) -> List[float]`.
Context: file `src/data/normalize.py`.
Output: new file `tests/test_normalize.py` with parameterized tests covering empty list, constant values, and negative numbers. Use `pytest` fixtures where useful."

## How to ask for documentation or README updates

- Specify the section and exact markdown style (table, bullet list)
- Provide any example outputs/screenshots (if applicable)

Example:

"Goal: Add a 'Data Sources' section to `README.md` describing the Kaggle dataset and the odds API.
Context: repo root README already has 'Overview'.
Output: append a `## Data Sources` section with subsections for `Kaggle NFL Scores` and `OddsAPI` including example sample queries and required API keys environment variables."

## Instruction patterns and many examples

Below are many short patterns/examples you can copy-paste and adapt. Each is independent and shows the minimal context needed.

### 1) Generate a small Python utility function

"Goal: Write a function that converts a Madden-style roster CSV to a JSON player list.
Context: repo uses Python 3.11, prefer pure-stdlib.
Output: `src/tools/roster_convert.py` with `def csv_to_players(path: str) -> List[dict]`.
Constraints: Skip rows with missing `player_id`. Write docstring and type annotations. Add a short example in the module's `__main__` block."

### 2) Add a CLI subcommand using the `busta` pattern

"Goal: Add `busta data refresh-now` command wrapper that calls existing pipeline steps.
Context: CLI framework uses click, main script `cli/busta.py`.
Output: new function `def refresh_now(…)` and register subcommand `data refresh-now`.
Tests: Add an integration test that runs the CLI with `--dry-run` and checks printed steps."

### 3) SQL query generator

"Goal: Create a SQL query that returns team_id and moving average of points for last 5 games per team.
Context: Postgres, table `game_stats(team_id int, game_date date, points int)`.
Output: single SQL string and brief explanation of partition window function used."

Example SQL:

```sql
SELECT team_id,
       game_date,
       AVG(points) OVER (PARTITION BY team_id ORDER BY game_date ROWS BETWEEN 4 PRECEDING AND CURRENT ROW) AS ma_5
FROM game_stats
ORDER BY team_id, game_date;
```

### 4) Request tests + implementation for performance constraint

"Goal: Implement `fast_join(left: List[Tuple], right: List[Tuple], key_idx=0)` for large lists.
Constraints: Must handle 1M rows in under 5s on 2020 laptop hardware — use dict/hash approach.
Output: implementation in `src/algorithms/joins.py` and pytest performance test `tests/test_joins_perf.py` using `timeit` (mark as slow)."

### 5) Create a Cronicle plugin wrapper script (shell)

"Goal: Add a Cronicle-friendly plugin `/opt/plugins/run-refresh.sh` that runs the repo `scripts/refresh_now.sh` and emits JSON progress updates.
Context: Use bash, JSON messages must contain keys `complete` (0/1), `progress` (0-1), `description`.
Output: add `scripts/cronicle_refresh.sh` that reads parameters from STDIN and prints progress JSON lines. Include error handling and exit codes."

### 6) Security review prompt

"Goal: Review `src/auth/*.py` for credential leakage and insecure defaults.
Context: repo uses `requests` and local `.env` files. Focus on hard-coded secrets, use of `verify=False`, and logging of tokens.
Output: a short report listing issues with file and line numbers and suggested fixes (config via env vars, use keyring, set `verify=True`)."

### 7) Pull request body generator

"Goal: Draft a PR body for the change that adds `feature/X`.
Context: change adds `src/feature/x.py` and `tests/test_x.py`.
Output: PR body with sections `What`, `Why`, `How to test`, `Risks`, `Rollout plan`, and `Related issues` formatted as Markdown."

### 8) Create integration test harness

"Goal: Add a minimal integration test that runs `busta pipeline sample` in a temporary venv and verifies it exits 0.
Context: CI uses GitHub Actions, tests should be fast (<2 min) and use docker if needed.
Output: add `tests/integration/test_pipeline_smoke.py` and a lightweight GH Action `ci-smoke.yml` that runs the test container."

### 9) Write accessibility guidance for UI changes

"Goal: Update UI docs with accessibility checklist for the Streamlit app.
Output: `docs/accessibility.md` with checklist items: semantic headings, alt text for images, color contrast 4.5:1, keyboard nav tests. Include sample CSS/palette recommendations."

### 10) Generate a code review checklist

"Goal: Provide a code review checklist for PR reviewers.
Output: `docs/review_checklist.md` including tests, type hints, logging, errors, security, dependency updates, and performance impact."

## Many more concrete prompt examples (copy/paste)

Below are short, ready-to-paste instructions grouped by intent.

### Generate code (Python)

1. "Implement `def safe_div(a: float, b: float) -> Optional[float]` that returns `None` when division by zero occurs. Add docstring and tests."
2. "Write function `merge_player_stats(left, right)` that merges two dicts keyed by `player_id` and sums numeric stats."
3. "Create `src/io/parquet_writer.py` with `def write_parquet(df, path)` using pyarrow. Raise a friendly error if pyarrow not installed."

### Generate code (JS/TS)

1. "Create a React component `TeamCard` that accepts `{team, score}` and is responsive. Include PropTypes or TS types, and a Storybook story."
2. "Add utility `formatOdds(american)` that converts American odds to decimal and probability, with tests."

### Refactor/clean-up

1. "Refactor `src/old/module.py` into `src/new/` preserving behavior. Keep function signatures stable and add deprecation warnings in original module."
2. "Inline small helper `def _parse()` into `main()` and remove dead code; provide unit tests proving equivalence."

### Testing & CI

1. "Add pytest config file and a basic `conftest.py` fixture for DB connection that uses sqlite in-memory for tests."
2. "Add GH Action `ci.yml` that runs unit tests and a flake8 check."

### Documentation

1. "Update `docs/quickstart.md` with commands to setup venv, install deps, run sample pipeline, and generate UI payload."
2. "Add a migration guide `docs/migration.md` describing schema changes between v1 and v2 of the feature store."

### Code review and security

1. "Scan `requirements.txt` for pinned versions with known CVEs; if any, flag and recommend patched versions."
2. "Add a lint rule suggestion for `bandit` to check for use of `subprocess` with shell=True."

### Data / SQL

1. "Write a query to compute per-team season totals and exclude forfeits (forfeits are rows with `forfeit=true`). Output rows: team_id, games_played, total_points."
2. "Create an ETL check script `scripts/check_parquets.py` which validates schema for 'gold' parquet files and prints human-friendly diff."

### LLM & prompt engineering examples

1. "Create an LLM prompt template that extracts injury mentions from news articles. Output JSON should include fields: `game_id`, `player_name`, `injury_status`, `confidence` (0-1). Provide a short instruction and one example mapping a sample sentence to JSON."

2. "Design a batch prompt for summarizing 20 news items into a single 'team sentiment' score [-1,1]. Include aggregation rules and examples."

Example mapping:

Input: "Quarterback John Doe suffered a sprained ankle and is questionable for Sunday."
Output:
```json
{"game_id": "2025_wk_1_TEAM_A_TEAM_B", "player_name": "John Doe", "injury_status": "questionable", "confidence": 0.85}
```

### Agent-style instruction for Copilot (multi-step)

"Goal: Implement feature X end-to-end.
Steps:
1. Create module scaffold `src/feature_x`.
2. Implement core function `compute_x`.
3. Add unit tests and CI job.
4. Run tests locally and fix failures.
Constraints: No external paid APIs; keep runtime under 2s for 10k rows.
Output: commit-ready changes and a single PR body with testing steps."

### Examples focusing on output formatting

1. "Return only YAML front-matter for a blog post with fields `title`, `date`, `tags` and `summary` — do not include the markdown body."
2. "Generate a JSON payload that the web UI expects: `{"week": int, "games": [{"home": str, "away": str, "start_time": iso8601}]}`."

## How to iterate and validate answers from Copilot

1. Ask for unit tests in the original instruction. If the tests fail, paste the failing trace back to Copilot with a targeted instruction: "The test `test_x` fails with IndexError at line Y — please fix implementation and keep API stable."
2. Use small, fast tests (unit-level) for rapid feedback loops. Mark heavy tests as `@pytest.mark.slow`.
3. If Copilot produces multiple options, ask for pros/cons and pick one.
4. Always review for security and licensing concerns (do not blindly accept large code blocks that may use non-permissible code).

## Tips for very large or sensitive changes

- Prefer multi-step agent mode instructions and require Copilot to run unit tests between steps.
- When dealing with secrets, include steps to rotate or remove secrets from history and confirm removal via `git filter-repo` or `git filter-branch` guidance.
- Ask for a short migration plan and rollback instructions for DB or API-breaking changes.

## Formatting & style hints for Copilot instructions

- Use short, numbered steps when you want an ordered plan.
- Use `Constraints:` and `Output:` headers — Copilot tends to follow clearly labeled sections.
- Provide exact filenames and function signatures where possible.
- If you want only a snippet, include `---` before and after expected snippet to reduce hallucination.

## Appendix: Example instruction bundles you can reuse

1) Quick bug fix bundle

"Goal: Fix off-by-one bug in `src/analysis/ranks.py`.
Context: function `rank_players(scores)` returns N ranks for N-1 players when N>1.
Output: fix code and add `tests/test_ranks.py` with failing case `scores=[10,9,9,8]`.
"

2) Feature plus monitoring

"Goal: Add 'data source health' job.
Context: needs a small monitor script under `scripts/monitors/health_check.py` that checks remote endpoints and writes `status.json`.
Output: script + GH Action `monitor-check.yml` that runs hourly and opens an issue if service down. Add docs under `docs/monitoring.md`.
"

3) PR-level automation bundle

"Goal: Add automation to label PRs touching `src/ui` with `frontend` label.
Context: use GitHub Actions. Output: `.github/workflows/pr-labeler.yml` that triggers on pull_request and uses `paths` filter. Include test matrix in action to run on Node 18."

## Closing notes

- Start with the smallest reproducible instruction and iterate. Copilot responds best to clear constraints and expected outputs.
- Always ask for tests and a small smoke-run as part of the request.
- Keep instructions short but precise — a paragraph with labeled sections (`Goal`, `Context`, `Constraints`, `Output`, `Tests`) is highly effective.

---

If you'd like, I can:
- Add a short example-specific file to the repo (e.g., `templates/copilot-prompts.txt`) containing reusable prompt snippets; or
- Create GH Action examples that use Copilot as part of a PR automation workflow.

File created: `GITHUB_COPILOT_INSTRUCTIONS_GUIDE.md` in repo root of `ai-sports-analytics-planning`.

---
id: ADH-014
title: Emit Metadata Doc
epic: adhoc
status: accepted
priority: medium
effort: TBD
branch_name: adh-014-emit-metadata-doc
labels:
- accepted
created: '2025-08-27'
accepted_date: '2025-08-27'
author: migration
dependencies: []
---

# emit_metadata Utility — Documentation

Purpose
- Provide a small, flexible metadata writer that can be called from existing pipeline stages.
- Produce standardized metadata (JSON + optional YAML) for files and directories across layers:
  raw → bronze → silver → gold.
- Minimal, format-flexible reader: CSV, parquet, JSON (ndjson or single JSON), and sensible fallbacks.

Location
- Script: `scripts/emit_metadata.py`
  - Uses `from __future__ import annotations`
  - Uses the project's logging config when available, falls back to basic logging
  - Produces JSON and YAML (if PyYAML available)

What it emits
- Default output directory: `data/metadata/`
- Output files: `data/metadata/<source_id>/<layer>/<original_filename>.metadata.json`
  - Optional YAML sibling if PyYAML installed: `.metadata.yaml`

Metadata record (high level)
- `source_id`: canonical source identifier (e.g., `kaggle_nfl_scores`)
- `layer`: raw | bronze | silver | gold
- `file_name`: original filename
- `storage_path`: path to the input file
- `ingestion_timestamp`: UTC timestamp when metadata created
- `file_size_bytes`
- `checksum_sha256`: file checksum
- `schema`: { column: dtype } (from a sample)
- `sample_rows`: up to 5 sample rows
- `record_count`: row count (if reader can determine)
- `date_range`: { column, min, max } (if detectable)
- `error`: present if reading failed

CLI usage
- Example (directory):
  ```shell
  busta emit-metadata --source-id kaggle_nfl_scores --layer raw --input data/raw/kaggle/nfl_scores
  ```
- Example (single file):
  ```shell
  busta emit-metadata --source-id kaggle_nfl_scores --layer raw --input data/raw/kaggle/nfl_scores/spreadspoke_scores.csv
  ```
- Optional flag:
  - `--out-base <path>`  (default: `data/metadata`)

How to integrate
- Preferred approach: call this utility from existing stage runners immediately after writing output for that stage.
  - e.g., at end of normalize stage: run `busta emit-metadata` for the produced bronze files.
- Integration points to consider:
  - scripts or CLI wrappers that already run: normalize, integrate, features, model training
  - CI jobs that run stage smoke-tests — have CI call emit-metadata and commit metadata artifacts or upload them to monitoring storage
- Keep calling pattern simple (single command). The script is file/dir aware and will recurse directories.

Logging & formatting
- Script follows repository standards:
  - `from __future__ import annotations` is used
  - Structured logging via project logging config when available
  - No prints; uses logger (INFO/DEBUG/WARN/ERROR)
- Output is deterministic (files are written to `data/metadata/<source_id>/<layer>/`)

Failure modes & notes
- If pandas or reader fails for a file, an error field is emitted in the metadata record.
- For very large files the script reads the whole file to compute record_count; consider running on partitioned/parquet files or sampling in CI.
- Checksum is computed for the file (SHA256), which can be expensive for large files but useful for lineage/validation.

Recommended small follow-ups
1. Add a short wrapper call to existing stage scripts to emit metadata automatically (one-liner).
2. Add a small CI smoke-test that runs emit_metadata on a sampled file after the stage runs.
3. Add a metadata validation step (simple schema conformance check) that reads the emitted metadata.

Tracking / Implementation Status
- This table is intended to track where `emit_metadata` has been implemented (called) and what remains.

| Item | Location / Command | emit_metadata called? | Notes |
|------|--------------------|-----------------------:|-------|
| emit_metadata script | `scripts/emit_metadata.py` | ✅ Implemented | Script updated to repo formatting & logging standards |
| busta CLI hook | `bin/busta emit-metadata` | ✅ Implemented | Added emit-metadata subcommand to busta CLI |
| Raw ingestion (Kaggle NFL scores) | `data/raw/kaggle/nfl_scores` | ✅ Complete | Generated metadata for raw layer game scores |
| Bronze layer (Kaggle NFL scores) | `data/bronze/game_scores` | ✅ Complete | Generated metadata for bronze layer parquet files |
| Silver layer (Kaggle NFL scores) | `data/silver/games.parquet` | ✅ Complete | Generated metadata for unified silver games data |
| Gold layer (Kaggle NFL scores) | `data/gold/game_features.parquet` | ✅ Complete | Generated metadata for feature-ready gold data |
| End-to-end documentation | `docs/END_TO_END_KAGGLE_NFL_SCORES.md` | ✅ Complete | Complete pipeline flow documented |
| Normalize stage (bronze writer) | `packages/data_pipeline/.../normalize runner` | ❌ Pending | Add wrapper call after writing bronze files |
| Integrate stage (silver writer) | `packages/data_pipeline/.../integrate runner` | ❌ Pending | Add wrapper call after writing silver outputs |
| Features stage (gold writer) | `packages/features/.../build runner` | ❌ Pending | Add wrapper call after writing gold feature parquet |
| CI integration | `.github/workflows` / `scripts/ci.sh` | ❌ Pending | Run metadata emission on smoke tests and archive artifacts |
| Metadata validation tool | `scripts/validate_metadata.py` (not present) | ❌ Pending | Recommend adding a simple validator that checks presence of keys, schema types |

How to mark items as done
- After you add a one-line call to the relevant stage script, update this document (or the inventory) and mark the item as ✅.
- Example wrapper line:
  ```shell
  busta emit-metadata --source-id kaggle_nfl_scores --layer bronze --input data/bronze/games --out-base data/metadata
  ```

Contact / ownership
- Add owner/contact in emitted metadata (recommended) by passing additional fields: the script returns metadata JSON — you can extend `build_metadata_record` to include owner/contact if desired.

Quick example metadata (truncated)
```json
{
  "source_id": "kaggle_nfl_scores",
  "layer": "raw",
  "file_name": "spreadspoke_scores.csv",
  "storage_path": "data/raw/kaggle/nfl_scores/spreadspoke_scores.csv",
  "ingestion_timestamp": "2025-08-21T12:00:00Z",
  "file_size_bytes": 123456,
  "checksum_sha256": "abcd1234...",
  "schema": { "schedule_date": "datetime64[ns]", "team_home": "object", "score_home": "int64" },
  "sample_rows": [{ "schedule_date": "1979-09-09", "team_home": "NYG", "score_home": 17 }],
  "record_count": 14086,
  "date_range": { "column": "schedule_date", "min": "1979-09-09T00:00:00", "max": "2023-12-31T00:00:00" }
}
```

If you want, I can:
- Add one-line wrapper calls to the specific stage scripts you name (I will modify those files).
- Add a CI step to run emit_metadata on a sampled file and store the output

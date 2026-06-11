# wholistic_preprocessing

The **preprocessing stage** of the wholistic whole-brain imaging pipeline:
**preprocessing → registration ([wholistic_reg](https://github.com/laurenminer/wholistic_reg))
→ segmentation ([wholistic_segmentation](https://github.com/laurenminer/wholistic_segmentation))**.

Prepares raw whole-brain recordings (normalization/filtering/threaded conversion) so they're
ready for registration.

## Files
- `preprocess.py` — core preprocessing routine (`main(threads=...)`, multithreaded).
- `preprocess_batch.py` — batch driver that runs preprocessing over multiple datasets.
- `main.py` — package entry-point stub.

## Usage
```bash
uv run python preprocess_batch.py   # edit the data paths at the top first
```

## Requirements
See `pyproject.toml`. Managed with `uv`.

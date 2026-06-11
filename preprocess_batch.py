#%%
from pathlib import Path

from dask.diagnostics.progress import ProgressBar
from preprocess_videos.recording import NeuralRecording
from preprocess_videos.utils import setup_threading

#%%
threads = 16
setup_threading(threads)

data_dir = Path(
    "/store1/lauren/Live_Imaging/cAMP_wholebrain_with_pdfr1_BlaC/NoFood/data_raw"
)
output_dir = data_dir / "pre-processed"
output_dir.mkdir(exist_ok=True)

# How to handle .nd2 files whose .zarr output already exists:
#   "skip"      -> leave existing output untouched, do not reprocess
#   "version"   -> write to {stem}_version2.zarr, _version3.zarr, ...
#   "overwrite" -> replace the existing .zarr in place
existing_mode = "skip"

files = sorted(data_dir.glob("*.nd2"))
print(f"Found {len(files)} .nd2 files to process")

#%%
for i, data_path in enumerate(files, 1):
    print(f"\n[{i}/{len(files)}] Processing {data_path.name}")

    out_path = output_dir / f"{data_path.stem}.zarr"
    if out_path.exists():
        if existing_mode == "skip":
            print(f"  output {out_path.name} exists, skipping")
            continue
        elif existing_mode == "version":
            version = 2
            while (output_dir / f"{data_path.stem}_version{version}.zarr").exists():
                version += 1
            out_path = output_dir / f"{data_path.stem}_version{version}.zarr"
            print(f"  output exists, writing to {out_path.name} instead")
        elif existing_mode == "overwrite":
            print(f"  output {out_path.name} exists, overwriting")
        else:
            raise ValueError(f"unknown existing_mode: {existing_mode!r}")

    recording = NeuralRecording(
        data_path,
        lat_bin_factor=3,
        freely_moving=False,
    )

    dual_channel_data = recording.preprocess(split_axes=False)

    with ProgressBar():
        dual_channel_data.to_zarr(str(out_path), mode="w", compute=True)

    recording.close()

print("\nDone.")
# %%

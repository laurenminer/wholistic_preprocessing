#%%
from pathlib import Path

from dask.diagnostics.progress import ProgressBar
from preprocess_videos.recording import NeuralRecording
from preprocess_videos.utils import setup_threading

#%%
def main(
    threads: int = 16,
):
    # Configure multithreading
    setup_threading(threads)

    data_path = Path("/store1/lauren/Tetramisole_Immobilized_Imaging/2026_PinkyCamp_Immobilized/data_raw/2026-02-26-06.nd2")

    recording = NeuralRecording(
        data_path,
        lat_bin_factor = 3,
        freely_moving = False
    )
 
    dual_channel_data = recording.preprocess(split_axes = False)
    
    with ProgressBar():
        dual_channel_data.to_zarr(
            "/home/lauren/wholistic_preprocessing/preprocessed/{}.zarr".format(data_path.stem), mode="w", compute=True
        )

    recording.close()


main()
# %%

# AUTOGENERATED! DO NOT EDIT! File to edit: ../../nbs/000_test.io.ipynb.

# %% ../../nbs/000_test.io.ipynb 1
from __future__ import annotations

# %% auto 0
__all__ = ['read_chn_file', 'read_multichan_files', 'read_mask_file', 'get_channel_filenames']

# %% ../../nbs/000_test.io.ipynb 3
from PIL import Image
from fastai.vision.all import *

# %% ../../nbs/000_test.io.ipynb 5
def _filter_masked(raw_arr, in_msk: int, out_msk: int):
    "Replace input mask pixel value with selected value"
    return np.select([raw_arr == in_msk], [out_msk], raw_arr)

def read_chn_file(path: str) -> Tensor:
    "Read single channel file into tensor"
    img_arr = np.array(Image.open(path))
    msk_arr = _filter_masked(img_arr, 55537, 9999)
    return Tensor(msk_arr / 10000)

def read_multichan_files(files: list(str)) -> Tensor:
    "Read individual channel tensor files into a tensor of channels"
    return torch.cat([read_chn_file(path)[None] for path in files])

# %% ../../nbs/000_test.io.ipynb 7
# TODO abstract this filter
def _to_bin_seg(img_arr):
    return np.select([img_arr == 255, img_arr < 6, img_arr == 6],[0, 0, 1],img_arr)

def read_mask_file(path: str) -> TensorMask:
    """Read ground truth segmentation label files with values from 0 to n."""
    img_arr = np.array(Image.open(path))
    prc_arr = _to_bin_seg(img_arr)
    return TensorMask(prc_arr)

# %% ../../nbs/000_test.io.ipynb 9
def _get_input(stem: str) -> str:
    "Get full input path for stem"
    return "./images/" + stem

def _tile_img_name(chn_id: str, tile_num: int) -> str:
    "File name from channel id and tile number"
    return f"Sentinel20m-{chn_id}-20200215-{tile_num:03d}.png"

def get_channel_filenames(chn_ids, tile_idx):
    "Get list of all channel filenames for one tile idx"
    return [_get_input(_tile_img_name(x, tile_idx)) for x in chn_ids]

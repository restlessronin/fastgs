# AUTOGENERATED! DO NOT EDIT! File to edit: ../../nbs/09a_vision.augment.ipynb.

# %% ../../nbs/09a_vision.augment.ipynb 1
from __future__ import annotations

# %% auto 0
__all__ = ['TrainMSSAT', 'ValidMSSAT']

# %% ../../nbs/09a_vision.augment.ipynb 3
from fastai.vision.all import *
from .core import *

# %% ../../nbs/09a_vision.augment.ipynb 5
def _ms_seg_alb_xfm_init(self, aug): store_attr()

# %% ../../nbs/09a_vision.augment.ipynb 7
def _ms_seg_alb_xfm_encodes(self, x):
    img,msk = x
    res = self.aug(image=img.permute(1,2,0).numpy(),mask=msk.numpy())
    return (
        TensorImageMS.from_tensor(torch.from_numpy(res["image"]).permute(2,0,1),bands=img.bands,brgtX=img.brgtX),
        TensorMask(torch.from_numpy(res["mask"]))
    )

# %% ../../nbs/09a_vision.augment.ipynb 9
def _create_ms_seg_alb_xfm_cls(clsname, split_idx):
    return type(
        clsname,
        (ItemTransform,),
        {
            "split_idx": split_idx,
            "__init__": _ms_seg_alb_xfm_init,
            "encodes": _ms_seg_alb_xfm_encodes
        }
    )

# %% ../../nbs/09a_vision.augment.ipynb 29
TrainMSSAT = _create_ms_seg_alb_xfm_cls("TrainMSSAT", 0)
ValidMSSAT = _create_ms_seg_alb_xfm_cls("ValidMSSAT", 1)
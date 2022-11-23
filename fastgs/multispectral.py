# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/62_multispectral.ipynb.

# %% ../nbs/62_multispectral.ipynb 1
from __future__ import annotations

# %% auto 0
__all__ = ['BandInputs', 'MSDescriptor', 'createSentinel2Descriptor', 'MSData', 'MaskData', 'MSPipeline']

# %% ../nbs/62_multispectral.ipynb 3
from typing import Callable
from dataclasses import dataclass
from fastai.vision.all import *

from .vision.core import *

# %% ../nbs/62_multispectral.ipynb 5
@dataclass
class BandInputs:
    ids: list[str]
    idxs: list[int]

    @classmethod
    def from_ids(cls, ids: list[str]):
        return cls(ids, [i for i in range(len(ids))])

# %% ../nbs/62_multispectral.ipynb 9
@patch
def _get_index(self: BandInputs, id: str) -> int:
    return self.idxs[self.ids.index(id)]

# %% ../nbs/62_multispectral.ipynb 12
@patch
def _get_bands(self: BandInputs, ids: list[str]) -> tuple[int]:
    assert set(ids).issubset(set(self.ids))
    return tuple(self._get_index(id) for id in ids)

# %% ../nbs/62_multispectral.ipynb 15
@patch
def get_bands_list(self: BandInputs, ids_list: list[list[str]]) -> list[tuple[int]]:
    return [self._get_bands(ids) for ids in ids_list]

# %% ../nbs/62_multispectral.ipynb 18
@dataclass
class MSDescriptor:
    band_ids: list[str]
    res_m: list[int]
    brgtX: list[float]
    rgb_combo: dict[str,list[str]]

# %% ../nbs/62_multispectral.ipynb 20
def createSentinel2Descriptor() -> MSDescriptor:
    return MSDescriptor(
        ["B01","B02","B03","B04","B05","B06","B07","B08","B8A","B09","B10","B11","B12","AOT"],
        [60,10,10,10,20,20,20,10,20,60,60,20,20,20],
        [2.5,4.75,4.25,3.75,3,2,1.7,1.7,2.5,2.5,1.6,1.6,2.2,30],
        {# https://gisgeography.com/sentinel-2-bands-combinations/
            "natural_color": ["B04","B03","B02"],
            "color_infrared": ["B08","B04","B03"],
            "short_wave_infrared": ["B12","B8a","B04"],
            "agriculture": ["B11","B08","B02"],
            "geology": ["B12","B11","B02"],
            "bathymetric": ["B04","B03","B01"]
        }
    )

# %% ../nbs/62_multispectral.ipynb 23
@patch
def get_res_ids(self: MSDescriptor, res: int) -> list[str]:
    indices = [i for i,r in enumerate(self.res_m) if r == res]
    return [self.band_ids[i] for i in indices]

# %% ../nbs/62_multispectral.ipynb 26
@patch
def get_brgtX(self: MSDescriptor, ids: list[str]) -> list[float]:
    indices = [self.band_ids.index(id) for id in ids]
    return [self.brgtX[i] for i in indices]

# %% ../nbs/62_multispectral.ipynb 29
@patch
def get_brgtX_list(self: MSDescriptor, ids_list: list[list[str]]) -> list[list[float]]:
    return [self.get_brgtX(ids) for ids in ids_list]

# %% ../nbs/62_multispectral.ipynb 32
class MSData:
    pass

# %% ../nbs/62_multispectral.ipynb 33
@patch
def __init__(
    self: MSData,
    ms_descriptor: MSDescriptor,
    band_ids: list[str],
    chn_grp_ids: list[list[str]],
    files_getter: Callable[[list[str], Any], list[str]],
    chan_io_fn: Callable[[list[str]], Tensor]
):
    self.ms_descriptor = ms_descriptor
    self.bands = BandInputs.from_ids(band_ids)
    self.chn_grp_ids = chn_grp_ids
    self.files_getter = files_getter
    self.chan_io_fn = chan_io_fn

# %% ../nbs/62_multispectral.ipynb 42
@patch
def _load_image(self: MSData, img_id, cls: TensorImage) -> TensorImage:
    files = self.files_getter(self.bands.ids, img_id)
    ids_list = self.chn_grp_ids
    bands = self.bands.get_bands_list(ids_list)
    brgtX = self.ms_descriptor.get_brgtX_list(ids_list)
    return cls(self.chan_io_fn(files), bands=bands, brgtX=brgtX)

@patch
def load_image(self: MSData, img_id) -> TensorImageMS:
    return self._load_image(img_id, TensorImageMS)                

# %% ../nbs/62_multispectral.ipynb 43
@patch
def num_channels(self: MSData) -> int:
    return len(self.bands.ids)

# %% ../nbs/62_multispectral.ipynb 48
class MaskData:
    pass

# %% ../nbs/62_multispectral.ipynb 49
@patch
def __init__(
    self: MaskData,
    mask_id: str,
    files_getter: Callable[[list[str], Any], list[str]],
    mask_io_fn: Callable[[list[str]], TensorMask],
    mask_codes: list[str]
):
    self.mask_id = mask_id
    self.files_getter = files_getter
    self.mask_io_fn = mask_io_fn
    self.mask_codes = mask_codes

# %% ../nbs/62_multispectral.ipynb 50
@patch
def load_mask(self: MaskData, img_id) -> TensorMask:
    file = self.files_getter([self.mask_id], img_id)[0]
    return self.mask_io_fn(file)

# %% ../nbs/62_multispectral.ipynb 51
@patch
def num_channels(self: MaskData) -> int:
    return len(self.mask_codes)

# %% ../nbs/62_multispectral.ipynb 54
@patch
def create_xform_block(self: MSData) -> DataBlock:
    return TransformBlock(
        type_tfms=[
            partial(MSData.load_image, self),
        ]
    )

# %% ../nbs/62_multispectral.ipynb 55
@patch
def create_xform_block(self: MaskData) -> DataBlock:
    return TransformBlock(
        type_tfms=[
            partial(MaskData.load_mask, self),
            AddMaskCodes(codes=self.mask_codes),
        ]
    )

# %% ../nbs/62_multispectral.ipynb 57
class MSPipeline:
    pass

# %% ../nbs/62_multispectral.ipynb 58
@patch
def __init__(self: MSPipeline, ms_data: MSData, mask_data: MaskData):
    self.ms_data = ms_data
    self.mask_data = mask_data

# %% ../nbs/62_multispectral.ipynb 59
@patch
def create_data_block(self: MSPipeline, splitter=RandomSplitter(valid_pct=0.2, seed=107)) -> DataBlock:
    return DataBlock(
        blocks=(self.ms_data.create_xform_block(), self.mask_data.create_xform_block()),
        splitter=splitter
    )

# %% ../nbs/62_multispectral.ipynb 61
@patch
def create_unet_learner(self: MSPipeline,dl,model,pretrained=True,loss_func=CrossEntropyLossFlat(axis=1),metrics=Dice(axis=1)) -> Learner:
    learner = unet_learner(
        dl,model,normalize=False,n_in=len(self.ms_data.bands.ids),n_out=len(self.mask_data.mask_codes),
        pretrained=pretrained, loss_func=loss_func,metrics=metrics
    )
    if pretrained:
        layer_1 = learner.model[0][0]
        w = layer_1.weight
        w_mean = torch.mean(w[:,:3,:,:],1,True)
        w[:,3:,:,:] = w_mean
        w = w * (3.0 / w.shape[1])
    return learner
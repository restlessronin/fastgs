# AUTOGENERATED! DO NOT EDIT! File to edit: ../../nbs/62_geospatial.sentinel.ipynb.

# %% ../../nbs/62_geospatial.sentinel.ipynb 1
from __future__ import annotations

# %% auto 0
__all__ = ['BandInputs', 'MSDescriptor', 'createSentinel2Descriptor', 'MultiSpectral']

# %% ../../nbs/62_geospatial.sentinel.ipynb 3
from typing import Callable
from dataclasses import dataclass
from fastai.vision.all import *

from ..vision.core import *

# %% ../../nbs/62_geospatial.sentinel.ipynb 5
@dataclass
class BandInputs:
    ids: list[str]
    idxs: list[int]

    @classmethod
    def from_ids(cls, ids: list[str]):
        return cls(ids, [i for i in range(len(ids))])

# %% ../../nbs/62_geospatial.sentinel.ipynb 9
@patch
def _get_index(self: BandInputs, id: str) -> int:
    return self.idxs[self.ids.index(id)]

# %% ../../nbs/62_geospatial.sentinel.ipynb 12
@patch
def _get_bands(self: BandInputs, ids: list[str]) -> tuple[int]:
    assert set(ids).issubset(set(self.ids))
    return tuple(self._get_index(id) for id in ids)

# %% ../../nbs/62_geospatial.sentinel.ipynb 15
@patch
def get_bands_list(self: BandInputs, ids_list: list[list[str]]) -> list[tuple[int]]:
    return [self._get_bands(ids) for ids in ids_list]

# %% ../../nbs/62_geospatial.sentinel.ipynb 18
@dataclass
class MSDescriptor:
    band_ids: list[str]
    res_m: list[int]
    brgtX: list[float]
    rgb_combo: dict[str,list[str]]

# %% ../../nbs/62_geospatial.sentinel.ipynb 20
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

# %% ../../nbs/62_geospatial.sentinel.ipynb 23
@patch
def get_res_ids(self: MSDescriptor, res: int) -> list[str]:
    indices = [i for i,r in enumerate(self.res_m) if r == res]
    return [self.band_ids[i] for i in indices]

# %% ../../nbs/62_geospatial.sentinel.ipynb 26
@patch
def get_brgtX(self: MSDescriptor, ids: list[str]) -> list[float]:
    indices = [self.band_ids.index(id) for id in ids]
    return [self.brgtX[i] for i in indices]

# %% ../../nbs/62_geospatial.sentinel.ipynb 29
@patch
def get_brgtX_list(self: MSDescriptor, ids_list: list[list[str]]) -> list[list[float]]:
    return [self.get_brgtX(ids) for ids in ids_list]

# %% ../../nbs/62_geospatial.sentinel.ipynb 32
class MultiSpectral:
    pass

# %% ../../nbs/62_geospatial.sentinel.ipynb 33
@patch
def __init__(
    self: MultiSpectral,
    ms_descriptor: MSDescriptor,
    band_ids: list[str],
    mask_id: str,
    chn_grp_ids: list[list[str]],
    files_getter: Callable[[list[str], Any], list[str]],
    chan_io_fn: Callable[[list[str]], Tensor],
    mask_io_fn: Callable[[str], TensorMask] = None,
):
    self.ms_descriptor = ms_descriptor
    self.bands = BandInputs.from_ids(band_ids)
    self.mask_id = mask_id
    self.chn_grp_ids = chn_grp_ids
    self.files_getter = files_getter
    self.chan_io_fn = chan_io_fn
    self.mask_io_fn = mask_io_fn

# %% ../../nbs/62_geospatial.sentinel.ipynb 42
@patch
def _load_image(self: MultiSpectral, img_id, cls: TensorImage) -> TensorImage:
    files = self.files_getter(self.bands.ids, img_id)
    ids_list = self.chn_grp_ids
    bands = self.bands.get_bands_list(ids_list)
    brgtX = self.ms_descriptor.get_brgtX_list(ids_list)
    return cls(self.chan_io_fn(files), bands=bands, brgtX=brgtX)

@patch
def load_image(self: MultiSpectral, img_id) -> TensorImageMS:
    return self._load_image(img_id, TensorImageMS)                

# %% ../../nbs/62_geospatial.sentinel.ipynb 47
@patch
def load_mask(self: MultiSpectral, img_id) -> TensorMask:
    file = self.files_getter([self.mask_id], img_id)[0]
    return self.mask_io_fn(file)

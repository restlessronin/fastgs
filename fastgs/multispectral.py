# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/62_multispectral.ipynb.

# %% ../nbs/62_multispectral.ipynb 1
from __future__ import annotations

# %% auto 0
__all__ = ['BandInputs', 'MSDescriptor', 'createSentinel2Descriptor', 'MSData', 'MaskData', 'MSAugment', 'FastGS']

# %% ../nbs/62_multispectral.ipynb 3
from typing import Callable
from dataclasses import dataclass
from fastai.vision.all import *

from .vision.core import *
from .vision.augment import *
from .vision.learner import *
from .vision.load import *

# %% ../nbs/62_multispectral.ipynb 6
@dataclass
class BandInputs:
    ids: list[str]
    idxs: list[int]

    @classmethod
    def from_ids(cls, ids: list[str]):
        return cls(ids, [i for i in range(len(ids))])

# %% ../nbs/62_multispectral.ipynb 10
@patch
def _get_index(self: BandInputs, id: str) -> int:
    return self.idxs[self.ids.index(id)]

# %% ../nbs/62_multispectral.ipynb 13
@patch
def _get_bands(self: BandInputs, ids: list[str]) -> tuple[int]:
    assert set(ids).issubset(set(self.ids))
    return tuple(self._get_index(id) for id in ids)

# %% ../nbs/62_multispectral.ipynb 16
@patch
def get_bands_list(self: BandInputs, ids_list: list[list[str]]) -> list[tuple[int]]:
    return [self._get_bands(ids) for ids in ids_list]

# %% ../nbs/62_multispectral.ipynb 19
class MSDescriptor:
    pass

# %% ../nbs/62_multispectral.ipynb 20
@patch
def __init__(self: MSDescriptor, band_ids, brgtX, res_m, rgb_combo): store_attr()

# %% ../nbs/62_multispectral.ipynb 22
@patch(cls_method=True)
def from_all(
    cls: MSDescriptor,
    band_ids: tuple(str),
    brgtX: list(float),
    res_m: list[int],
    rgb_combo: dict[str, list[str]]={}
):
    return cls(band_ids,brgtX,res_m,rgb_combo)

@patch(cls_method=True)
def from_band_brgt(cls: MSDescriptor, band_ids: tuple(str), brgtX: list[int]):
    return cls.from_all(band_ids,brgtX,[None]*len(band_ids))

@patch(cls_method=True)
def from_bands(cls: MSDescriptor, band_ids: tuple(str)):
    return cls.from_band_brgt(band_ids,[1.0]*len(band_ids))

# %% ../nbs/62_multispectral.ipynb 26
def createSentinel2Descriptor() -> MSDescriptor:
    return MSDescriptor.from_all(
        ["B01","B02","B03","B04","B05","B06","B07","B08","B8A","B09","B10","B11","B12","AOT"],
        [2.5,4.75,4.25,3.75,3,2,1.7,1.7,2.5,2.5,1.6,1.6,2.2,30],
        [60,10,10,10,20,20,20,10,20,60,60,20,20,20],
        {# https://gisgeography.com/sentinel-2-bands-combinations/
            "natural_color": ["B04","B03","B02"],
            "color_infrared": ["B08","B04","B03"],
            "short_wave_infrared": ["B12","B8a","B04"],
            "agriculture": ["B11","B08","B02"],
            "geology": ["B12","B11","B02"],
            "bathymetric": ["B04","B03","B01"]
        }
    )

# %% ../nbs/62_multispectral.ipynb 29
@patch
def get_res_ids(self: MSDescriptor, res: int) -> list[str]:
    indices = [i for i,r in enumerate(self.res_m) if r == res]
    return [self.band_ids[i] for i in indices]

# %% ../nbs/62_multispectral.ipynb 32
@patch
def get_brgtX(self: MSDescriptor, ids: list[str]) -> list[float]:
    indices = [self.band_ids.index(id) for id in ids]
    return [self.brgtX[i] for i in indices]

# %% ../nbs/62_multispectral.ipynb 35
@patch
def get_brgtX_list(self: MSDescriptor, ids_list: list[list[str]]) -> list[list[float]]:
    return [self.get_brgtX(ids) for ids in ids_list]

# %% ../nbs/62_multispectral.ipynb 38
class MSData:
    pass

# %% ../nbs/62_multispectral.ipynb 39
@patch
def __init__(
    self: MSData,
    ms_descriptor: MSDescriptor,
    bands: BandInputs,
    chn_grp_ids: list[list[str]],
    tensor_getter: MSTensorGetter
):
    store_attr()

# %% ../nbs/62_multispectral.ipynb 40
@patch(cls_method=True)
def from_all(
    cls: MSData,
    ms_descriptor: MSDescriptor,
    band_ids: list[str],
    chn_grp_ids: list[list[str]],
    files_getter: Callable[[list[str], Any], list[str]],
    chan_io_fn: Callable[[list[str]], Tensor]
):
    tensor_getter = MSTensorGetter.from_files(files_getter,chan_io_fn)
    return cls(ms_descriptor,BandInputs.from_ids(band_ids),chn_grp_ids,tensor_getter)

@patch(cls_method=True)
def from_delegate(
    cls: MSData,
    ms_descriptor: MSDescriptor,
    band_ids: list[str],
    chn_grp_ids: list[list[str]],
    tg_fn: Callable[[list[str], Any], Tensor]
):
    tensor_getter = MSTensorGetter.from_delegate(tg_fn)
    return cls(ms_descriptor,BandInputs.from_ids(band_ids),chn_grp_ids,tensor_getter)

# %% ../nbs/62_multispectral.ipynb 49
@patch
def _load_image(self: MSData, img_id, cls: TensorImage) -> TensorImage:
    ids_list = self.chn_grp_ids
    bands = self.bands.get_bands_list(ids_list)
    brgtX = self.ms_descriptor.get_brgtX_list(ids_list)
    return cls(self.tensor_getter.load_tensor(self.bands.ids, img_id), bands=bands, brgtX=brgtX)

@patch
def load_image(self: MSData, img_id) -> TensorImageMS:
    return self._load_image(img_id, TensorImageMS)                

# %% ../nbs/62_multispectral.ipynb 50
@patch
def num_channels(self: MSData) -> int:
    return len(self.bands.ids)

# %% ../nbs/62_multispectral.ipynb 55
class MaskData:
    pass

# %% ../nbs/62_multispectral.ipynb 56
@patch
def __init__(
    self: MaskData,
    mask_id: str,
    files_getter: Callable[[list[str], Any], list[str]],
    mask_io_fn: Callable[[list[str]], TensorMask],
    mask_codes: list[str]
):
    store_attr()

# %% ../nbs/62_multispectral.ipynb 57
@patch
def load_mask(self: MaskData, img_id) -> TensorMask:
    file = self.files_getter([self.mask_id], img_id)[0]
    return self.mask_io_fn(file)

# %% ../nbs/62_multispectral.ipynb 58
@patch
def num_channels(self: MaskData) -> int:
    return len(self.mask_codes)

# %% ../nbs/62_multispectral.ipynb 61
class MSAugment:
    pass

# %% ../nbs/62_multispectral.ipynb 62
@patch
def __init__(self: MSAugment,train_aug=None,valid_aug=None): store_attr()

# %% ../nbs/62_multispectral.ipynb 64
@patch
def create_xform_block(self: MSData) -> DataBlock:
    return TransformBlock(type_tfms=[
            partial(MSData.load_image,self),
        ])

# %% ../nbs/62_multispectral.ipynb 65
@patch
def create_xform_block(self: MaskData) -> DataBlock:
    return TransformBlock(type_tfms=[
            partial(MaskData.load_mask,self),
            AddMaskCodes(codes=self.mask_codes),
        ])

# %% ../nbs/62_multispectral.ipynb 66
@patch
def create_item_xforms(self: MSAugment) -> list(ItemTransform):
    if self.train_aug is None and self.valid_aug is None: return []
    elif self.valid_aug is None: return [TrainMSSAT(self.train_aug)]
    elif self.train_aug is None: return [ValidMSSAT(self.valid_aug)]
    else: return [TrainMSSAT(self.train_aug),ValidMSSAT(self.valid_aug)]

# %% ../nbs/62_multispectral.ipynb 68
class FastGS:
    pass

# %% ../nbs/62_multispectral.ipynb 69
@patch
def __init__(self: FastGS, ms_data: MSData, mask_data: MaskData, ms_aug: MSAugment=MSAugment()):
    store_attr()

# %% ../nbs/62_multispectral.ipynb 71
@patch
def create_data_block(self: FastGS, splitter=RandomSplitter(valid_pct=0.2, seed=107)) -> DataBlock:
    return DataBlock(
        blocks=(self.ms_data.create_xform_block(),self.mask_data.create_xform_block()),
        splitter=splitter,
        item_tfms=self.ms_aug.create_item_xforms()
    )

# %% ../nbs/62_multispectral.ipynb 73
@patch
def create_unet_learner(self: FastGS,dl,model,pretrained=True,loss_func=CrossEntropyLossFlat(axis=1),metrics=Dice(axis=1),reweight="avg") -> Learner:
    learner = unet_learner(
        dl,model,n_in=len(self.ms_data.bands.ids),n_out=len(self.mask_data.mask_codes),
        pretrained=pretrained,loss_func=loss_func,metrics=metrics
    )
    if pretrained:
        learner.model[0][0].fastgs_reinit_weights(reweight=reweight)
    return learner

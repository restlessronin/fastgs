# AUTOGENERATED! DO NOT EDIT! File to edit: ../../nbs/002_vision.load.ipynb.

# %% ../../nbs/002_vision.load.ipynb 1
from __future__ import annotations

# %% auto 0
__all__ = ['MSTensorGetter', 'MSMaskGetter']

# %% ../../nbs/002_vision.load.ipynb 3
from typing import Callable
from fastai.vision.all import *
from .core import *

# %% ../../nbs/002_vision.load.ipynb 5
class MSTensorGetter:
    pass

@patch
def load_tensor(self: MSTensorGetter, band_ids: list[str], img_id: Any) -> TensorImageMS:
    pass

# %% ../../nbs/002_vision.load.ipynb 7
class _MSFileTensorGetter(MSTensorGetter):
    pass

@patch
def __init__(
    self: _MSFileTensorGetter,
    files_getter: Callable[[list[str], Any], list[str]],
    chan_io_fn: Callable[list[str], TensorImageMS]
):
    store_attr()

@patch
def load_tensor(self: _MSFileTensorGetter, band_ids: list[str], img_id: Any) -> TensorImageMS:
    files = self.files_getter(band_ids, img_id)
    return self.chan_io_fn(files)

# %% ../../nbs/002_vision.load.ipynb 9
class _MSDelegatingTensorGetter(MSTensorGetter):
    pass

@patch
def __init__(
    self: _MSDelegatingTensorGetter,
    tg_fn: Callable[[list[str], Any], TensorImageMS]
):
    store_attr()

@patch
def load_tensor(self: _MSDelegatingTensorGetter, band_ids: list[str], img_id: Any) -> TensorImageMS:
    return self.tg_fn(band_ids, img_id)

# %% ../../nbs/002_vision.load.ipynb 11
@patch(cls_method=True)
def from_files(
    cls: MSTensorGetter,
    files_getter: Callable[[list[str], Any], list[str]],
    chan_io_fn: Callable[list[str], TensorImageMS]
):
    return _MSFileTensorGetter(files_getter, chan_io_fn)

@patch(cls_method=True)
def from_delegate(
    cls: MSTensorGetter,
    tg_fn: Callable[[list[str], Any], TensorImageMS]
):
    return _MSDelegatingTensorGetter(tg_fn)

# %% ../../nbs/002_vision.load.ipynb 13
class MSMaskGetter:
    pass

@patch
def load_mask(self: MSMaskGetter, band_ids: list[str], img_id: Any) -> TensorMask:
    pass

# %% ../../nbs/002_vision.load.ipynb 14
class _MSFileMaskGetter(MSMaskGetter):
    pass

@patch
def __init__(
    self: _MSFileMaskGetter,
    files_getter: Callable[[list[str], Any], list[str]],
    chan_io_fn: Callable[[list[str]], TensorMask]
):
    store_attr()

@patch
def load_mask(self: _MSFileMaskGetter, mask_id: str, img_id: Any) -> TensorMask:
    file = self.files_getter([mask_id], img_id)[0]
    return self.chan_io_fn(file)

# %% ../../nbs/002_vision.load.ipynb 15
class _MSDelegatingMaskGetter(MSMaskGetter):
    pass

@patch
def __init__(
    self: _MSDelegatingMaskGetter,
    tg_fn: Callable[[str, Any], TensorMask]
):
    store_attr()

@patch
def load_mask(self: _MSDelegatingMaskGetter, mask_id: str, img_id: Any) -> TensorMask:
    return self.tg_fn(mask_id, img_id)

# %% ../../nbs/002_vision.load.ipynb 16
@patch(cls_method=True)
def from_files(
    cls: MSMaskGetter,
    files_getter: Callable[[list[str], Any], list[str]],
    chan_io_fn: Callable[list[str], TensorMask]
):
    return _MSFileMaskGetter(files_getter, chan_io_fn)

@patch(cls_method=True)
def from_delegate(
    cls: MSMaskGetter,
    tg_fn: Callable[[str, Any], TensorMask]
):
    return _MSDelegatingMaskGetter(tg_fn)
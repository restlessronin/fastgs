# AUTOGENERATED! DO NOT EDIT! File to edit: ../../nbs/07a_vision.core.ipynb.

# %% ../../nbs/07a_vision.core.ipynb 2
from __future__ import annotations

# %% auto 0
__all__ = ['TensorImageMS']

# %% ../../nbs/07a_vision.core.ipynb 4
import math
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from IPython.display import display, HTML
import torch
import fastai
from fastai.vision.all import *

# %% ../../nbs/07a_vision.core.ipynb 5
class TensorImageMS(TensorImage):
    def select_bands(self, bands: tuple[int]) -> TensorImageMS:
        assert len(bands) <= 3
        return torch.index_select(self, 0, torch.IntTensor(bands))

    def _brighten(self, multiplier: list[float]) -> TensorImageMS:
        assert self.shape[0] == len(multiplier)
        brightened = self * Tensor(multiplier)[:, None, None]
        return torch.clamp(brightened, 0, 1)

    def _get_brightened_image(
        self, bands: tuple[int], mult: tuple[float]
    ) -> TensorImageMS:
        img_bands: TensorImageMS = self.select_bands(bands)
        return img_bands._brighten(mult)

    @delegates(subplots, keep=True, but=["ctx", "ctxs"])
    def _show_tiles(self, ctxs=None, ncols: int = 1, **kwargs):
        ims = [
            self._get_brightened_image(b, m)
            for b, m in zip(self.band_tuples, self.multipliers)
        ]
        nrows = math.ceil(len(self.band_tuples) / ncols)
        axs = subplots(nrows, ncols, **kwargs)[1].flat if ctxs is None else ctxs
        return [show_image(im, ax=ax) for im, ax in zip(ims, axs)]

    def show_animation(self):
        fig, ax = plt.subplots()
        ax.axis("off")
        ims = [
            [
                ax.imshow(
                    self._get_brightened_image(b, m).permute(1, 2, 0), animated=True
                )
            ]
            for b, m in zip(self.band_tuples, self.multipliers)
        ]
        anim = animation.ArtistAnimation(fig, ims, interval=1000, blit=True)
        plt.close()
        display(HTML(anim.to_html5_video()))

    def _get_grid(self, nrows, **kwargs):
        ncols = self.num_images()
        ncells = nrows * ncols
        return get_grid(ncells, nrows, ncols, **kwargs)

    def show(self, ctxs=None, **kwargs):
        ctxs = self._get_grid(1, **kwargs) if ctxs is None else ctxs
        return self._show_tiles(ctxs=ctxs, **kwargs)

    def num_images(self):
        return len(self.band_tuples)

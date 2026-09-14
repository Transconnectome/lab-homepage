#!/usr/bin/env python3
"""Render an anatomical reference from FreeSurfer fsaverage5 pial surfaces.

Manual asset generation only; not part of the site build. See the source and
license record in public/assets/research/README.md. Requires nibabel, numpy,
matplotlib. Coordinates and faces are preserved; no activity data are overlaid.
"""
import argparse
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import LightSource
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import nibabel as nib
import numpy as np


def render(left, right, output):
    surfaces = [nib.load(path) for path in (left, right)]
    vertices = np.concatenate([surface.darrays[0].data for surface in surfaces])
    lower, upper = vertices.min(axis=0), vertices.max(axis=0)
    center = (upper + lower) / 2
    span = (upper - lower) * 1.10
    fig = plt.figure(figsize=(10, 7), dpi=160)
    ax = fig.add_axes([0, 0, 1, 1], projection="3d", computed_zorder=True)
    ax.set_proj_type("ortho")
    light = LightSource(azdeg=315, altdeg=55)
    for surface in surfaces:
        coordinates, faces = [array.data for array in surface.darrays]
        mesh = Poly3DCollection(coordinates[faces], facecolors="#c8cecb",
                                linewidths=0, antialiased=False,
                                shade=True, lightsource=light, rasterized=True)
        ax.add_collection3d(mesh)
    ax.set_xlim(center[0] - span[0] / 2, center[0] + span[0] / 2)
    ax.set_ylim(center[1] - span[1] / 2, center[1] + span[1] / 2)
    ax.set_zlim(center[2] - span[2] / 2, center[2] + span[2] / 2)
    ax.set_box_aspect(span, zoom=1.6)
    ax.view_init(elev=22, azim=155)
    ax.set_axis_off()
    output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output, transparent=True, metadata={
        "Title": "FreeSurfer fsaverage5 pial surface reference",
        "Description": "Modified static rendering by SNU Connectome Lab website; no functional overlay."
    })
    plt.close(fig)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--left", required=True, type=Path)
    parser.add_argument("--right", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    options = parser.parse_args()
    render(options.left, options.right, options.output)

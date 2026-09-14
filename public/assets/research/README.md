# Cortical surface reference

`cortical-surface.png` is a **modified static rendering** of the left and right
FreeSurfer fsaverage5 pial surfaces. It depicts the cerebral cortex, without
cerebellum or brainstem. No activity, connectivity, functional localization, or
research-area coordinates are overlaid. The original anatomical coordinates and
triangle faces are preserved; viewpoint, scale, lighting and color are chosen
for this website. Rendering: SNU Connectome Lab website, 2026-09-13.

## Source and attribution

FreeSurfer / The General Hospital Corporation (MGH), distributed in GIFTI format
by the Nilearn developers. [Dataset documentation](https://nilearn.github.io/dev/modules/description/fsaverage5.html).
Each hemisphere has 10,242 vertices and 20,480 triangles. The GIFTI metadata
identifies the original FreeSurfer `fsaverage5/surf/lh.pial` and `rh.pial` surfaces.

Pinned Nilearn revision: `aee5750ead87eb4147f65c5d4239b4150e839ed1`.

- [Left pial surface](https://raw.githubusercontent.com/nilearn/nilearn/aee5750ead87eb4147f65c5d4239b4150e839ed1/nilearn/datasets/data/fsaverage5/pial_left.gii.gz)
  SHA256 `1e76fe43ac194c15fd272643f7ae7995621e2a496b3102b2d6175f0f8e6d7fc8`
- [Right pial surface](https://raw.githubusercontent.com/nilearn/nilearn/aee5750ead87eb4147f65c5d4239b4150e839ed1/nilearn/datasets/data/fsaverage5/pial_right.gii.gz)
  SHA256 `fdfae008bc10acf7cba82737ea5db9a7298948c41884a2d3330a785783a60a91`

## Terms

All or portions of this licensed product (such portions are the "Software")
have been obtained under license from The General Hospital Corporation "MGH"
and are subject to the following terms and conditions:

[FreeSurfer Software License Agreement, Version 1.0, including all of Part B](FreeSurfer-LICENSE.txt).
The license covers software and data. This rendering is a modification and is
not an original FreeSurfer visualization or an endorsement by MGH.

[Nilearn BSD license and attribution](Nilearn-LICENSE.txt) are preserved for the
distribution through which the data were obtained. The dataset is not being
relabelled as solely BSD-licensed.

## Reproduction

Download the two pinned GIFTI files above, verify their SHA256 values, and run
the repository's `scripts/render_cortical_surface.py`:

```sh
python3 scripts/render_cortical_surface.py --left pial_left.gii.gz --right pial_right.gii.gz --output public/assets/research/cortical-surface.png
```

This manual rendering step requires Python with nibabel, numpy and matplotlib.
The production site uses the resulting PNG directly and requires no Python,
surface download or WebGL at runtime.

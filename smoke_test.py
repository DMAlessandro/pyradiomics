"""Smoke test run against each built wheel: every 3D image type, LBP3D included.

Mirrors SeedGrow's --check-radiomics probe (synthetic 32^3 image, sphere mask,
parameter dict so the schema is validated), and fails if any image type that
SeedGrow's default preset relies on produces no features.
"""

from __future__ import annotations

import sys

import numpy as np
import SimpleITK as sitk

import radiomics
from radiomics import featureextractor

rng = np.random.default_rng(0)
arr = rng.normal(100.0, 20.0, size=(32, 32, 32)).astype(np.float32)
z, y, x = np.ogrid[:32, :32, :32]
mask_arr = (((z - 16) ** 2 + (y - 16) ** 2 + (x - 16) ** 2) <= 10**2).astype(np.uint8)
arr[mask_arr == 1] += 50.0

image = sitk.GetImageFromArray(arr)
mask = sitk.GetImageFromArray(mask_arr)
for im in (image, mask):
    im.SetSpacing((1.0, 1.0, 1.0))

params = {
    "setting": {"binWidth": 25, "label": 1},
    "imageType": {
        "Original": {},
        "LoG": {"sigma": [1.0, 2.0]},
        "Wavelet": {},
        "Square": {},
        "SquareRoot": {},
        "Logarithm": {},
        "Exponential": {},
        "Gradient": {},
        "LBP3D": {},
    },
    "featureClass": {
        c: None for c in ("shape", "firstorder", "glcm", "glrlm", "glszm", "gldm", "ngtdm")
    },
}
extractor = featureextractor.RadiomicsFeatureExtractor(params)
result = extractor.execute(image, mask)
features = {k: v for k, v in result.items() if not k.startswith("diagnostics_")}

prefixes = {
    "Original": "original_",
    "LoG": "log-sigma-",
    "Wavelet": "wavelet-",
    "Square": "square_",
    "SquareRoot": "squareroot_",
    "Logarithm": "logarithm_",
    "Exponential": "exponential_",
    "Gradient": "gradient_",
    "LBP3D": "lbp-3D-",
}
missing = [name for name, p in prefixes.items() if not any(k.startswith(p) for k in features)]
print(f"pyradiomics {radiomics.__version__}, numpy {np.__version__}, "
      f"SimpleITK {sitk.Version_VersionString()}, Python {sys.version.split()[0]}")
print(f"{len(features)} features; VoxelVolume {float(result['original_shape_VoxelVolume']):g}")
if missing:
    sys.exit(f"FAIL: no features from image types {missing}")
print("smoke test OK: every 3D image type produced features, LBP3D included")

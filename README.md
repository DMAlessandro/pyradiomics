# PyRadiomics wheels for SeedGrow

This fork of [AIM-Harvard/pyradiomics](https://github.com/AIM-Harvard/pyradiomics) exists only to build
wheels once, from one pinned commit, for the SeedGrow segmentation app. It carries no changes to PyRadiomics.

- **Source:** the head of upstream PR [#952](https://github.com/AIM-Harvard/pyradiomics/pull/952)
  (master `8ed5793` + the Python 3.10–3.13 fixes + the cross-version feature-equivalence suite),
  kept here as branch [`pinned/pr952`](../../tree/pinned/pr952). The exact SHA is `SOURCE_SHA` in
  [`.github/workflows/wheels.yml`](.github/workflows/wheels.yml).
- **Why:** no PyRadiomics release installs on Python ≥ 3.10 or supports numpy 2
  (see upstream [#954](https://github.com/AIM-Harvard/pyradiomics/issues/954)).
- **Targets:** CPython 3.12 and 3.13 for manylinux x86_64, Windows amd64, macOS x86_64 and macOS arm64,
  built by [cibuildwheel](https://cibuildwheel.pypa.io/).
- **Checks:** every wheel passes upstream's test suite, `tests/version_equivalence` (944 features × 2 cases
  against PyRadiomics 3.0.1, rtol 1e-6) and [`smoke_test.py`](smoke_test.py) (every 3D image type, LBP3D
  included) before it is released.
- **Wheels:** see [Releases](../../releases). Each release lists `SHA256SUMS`.

The workflow runs only when dispatched by hand. `master` mirrors upstream and is not used.

PyRadiomics is BSD-3-Clause; see `LICENSE.txt` on `pinned/pr952`.

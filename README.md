# muse_cosmic

muse_cosmic is a small project that provides a fast C-based median-style filter
implemented as a Python extension. It's intended for image-processing tasks such
as cosmic-ray removal in integral-field spectrograph (MUSE) data, but can be
used for general 2D array median operations.

This repository contains two small C-backed Python extensions and example/test scripts that demonstrate how to use them.

## Layout

- `fmedian/` ? original filtered-median implementation
  - `fmedian/fmedian_ext.c` ? C extension source (module: `fmedian_ext`, function: `fmedian`)
  - `fmedian/example_fmedian.py` ? runnable example
  - `fmedian/test_fmedian.py` ? small test script

- `fsigma/` ? a copy/adaptation with public names changed to *fsigma*
  - `fsigma/fsigma_ext.c` ? C extension source (module: `fsigma_ext`, function: `fsigma`)
  - `fsigma/example_fsigma.py` ? runnable example
  - `fsigma/test_fsigma.py` ? small test script

## Build & run

Both extensions are built by the top-level `setup.py`. To build in-place (creates `.so` files in the repository root), run:

```bash
python3 setup.py build_ext --inplace
```

After a successful build you can run the examples and tests from their directories. For example:

```bash
python3 fmedian/test_fmedian.py
python3 fmedian/example_fmedian.py

python3 fsigma/test_fsigma.py
python3 fsigma/example_fsigma.py
```

## Notes

- The repository root `setup.py` now builds both `fmedian_ext` and `fsigma_ext` (they are separate compiled modules). The build places the `.so` files in the project root, and each subdirectory contains a small wrapper (`*_ext.py`) that will dynamically locate and load the compiled extension when you import `fmedian_ext` or `fsigma_ext` from inside `fmedian/` or `fsigma/`.

- API summary:
  - `fmedian_ext.fmedian(input_array, output_array, xsize, ysize, exclude_center)`
  - `fsigma_ext.fsigma(input_array, output_array, xsize, ysize, exclude_center)`

  Both functions accept 2-D `np.float64` input/output arrays and write results into `output_array`.

- If you prefer the compiled `.so` files to live inside each subdirectory instead of the project root, I can modify `setup.py` to copy them into `fmedian/` and `fsigma/` after building.

## Contributing / CI

If you want CI (GitHub Actions) to build and run tests automatically on push/PR I can add a workflow that runs the in-place build and executes both test scripts.

If you spot any mismatches between the examples/tests and the C code, tell me and I'll fix them.

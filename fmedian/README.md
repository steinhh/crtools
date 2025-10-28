# muse_cosmic

muse_cosmic is a small project that provides a fast C-based median-style filter
implemented as a Python extension. It's intended for image-processing tasks such
as cosmic-ray removal in integral-field spectrograph (MUSE) data, but can be
used for general 2D array median operations.

This repository contains:

- `fmedian_ext.c` ? CPython extension source implementing the filter.
- `example_fmedian.py` ? a small example demonstrating usage.
- `test_fmedian.py` ? a lightweight test script that exercises the API.
- `USAGE.md` ? detailed usage notes and current API documentation.

Quick start
-----------

1. Install these packages in your Python environment:

```bash
pip install numpy
pip install setuptools
pip install pyflakes
pip install pytest
```

2. Build the extension in-place:

```bash
python setup.py build_ext --inplace
```

3. Run the example or tests:

```bash
python example_fmedian.py
python test_fmedian.py
```

If you want me to add CI (GitHub Actions) to build and run tests automatically, I can add
that as a follow-up.

from setuptools import setup, Extension, find_packages
import numpy

# Define the extension module
fmedian_module = Extension(
    'fmedian.fmedian_ext',  # build as a submodule inside the fmedian package
    sources=['fmedian/fmedian_ext.c'],
    include_dirs=[numpy.get_include()],
    extra_compile_args=['-O3'],
)

# Also build the fsigma extension (copied from fmedian into fsigma/)
fsigma_module = Extension(
    'fsigma.fsigma_ext',  # build as a submodule inside the fsigma package
    sources=['fsigma/fsigma_ext.c'],
    include_dirs=[numpy.get_include()],
    extra_compile_args=['-O3'],
)

# Setup configuration
setup(
    name='crtools',
    version='1.0.0',
    description='crtools: C-accelerated local median and sigma filters for cosmic ray removal',
    packages=find_packages(),
    # Include the top-level convenience shim so `from crtools import ...`
    # works when the package is installed from sdist/wheel.
    py_modules=['crtools'],
    ext_modules=[fmedian_module, fsigma_module],
    install_requires=['numpy'],
)

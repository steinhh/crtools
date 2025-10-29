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
    name='muse_cosmic',
    version='1.0.0',
    description='muse_cosmic: C-accelerated local median and sigma filters',
    packages=find_packages(),
    ext_modules=[fmedian_module, fsigma_module],
    install_requires=['numpy'],
)

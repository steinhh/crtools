from setuptools import setup, Extension
import numpy

# Define the extension module
fmedian_module = Extension(
    'fmedian_ext',
    sources=['fmedian/fmedian_ext.c'],
    include_dirs=[numpy.get_include()],
    extra_compile_args=['-O3'],
)

# Also build the fsigma extension (copied from fmedian into fsigma/)
fsigma_module = Extension(
    'fsigma_ext',
    sources=['fsigma/fsigma_ext.c'],
    include_dirs=[numpy.get_include()],
    extra_compile_args=['-O3'],
)

# Setup configuration
setup(
    name='fmedian_ext',
    version='1.0.0',
    description='Python extension for filtered median computation',
    ext_modules=[fmedian_module, fsigma_module],
    install_requires=['numpy'],
)

"""
Wrapper that loads the compiled `fsigma_ext` extension from the local directory and
re-exports its public symbols.

This allows running scripts from inside `fsigma/` that do `import fsigma_ext`
without needing to modify `sys.path` in every script.
"""
import importlib.machinery
import importlib.util
import os

# Project root is the parent directory of this file
_project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Look for a compiled extension file in the current directory matching fsigma_ext*.so
_so_path = None
current_dir = os.path.dirname(__file__)
for fname in os.listdir(current_dir):
    if fname.startswith('fsigma_ext') and fname.endswith('.so'):
        _so_path = os.path.join(current_dir, fname)
        break

if _so_path is None:
    # As a fallback, try to import top-level module if available
    try:
        _real = __import__('fsigma_ext')
    except Exception as e:
        raise ImportError('Could not find compiled fsigma_ext extension (.so) in local directory and import failed') from e
else:
    # Load the extension using its real module name so the extension's
    # initialization function (PyInit_fsigma_ext) can be found.
    # Using a different name previously caused: "dynamic module does not define
    # module export function" because the init symbol must match the module name.
    _module_name = 'fsigma_ext'
    spec = importlib.util.spec_from_file_location(
        _module_name,
        _so_path,
        loader=importlib.machinery.ExtensionFileLoader(_module_name, _so_path),
    )
    _real = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(_real)

# Re-export public names
for _name in dir(_real):
    if not _name.startswith('_'):
        globals()[_name] = getattr(_real, _name)

# For convenience, set __all__
__all__ = [n for n in dir() if not n.startswith('_')]

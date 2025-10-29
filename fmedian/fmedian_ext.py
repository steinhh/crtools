"""
Wrapper that loads the compiled `fmedian_ext` extension from the project root and
re-exports its public symbols.

This allows running scripts from inside `fmedian/` that do `import fmedian_ext`
without needing to modify `sys.path` in every script.
"""
import importlib.machinery
import importlib.util
import os

# Project root is the parent directory of this file
_project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Look for a compiled extension file in the project root matching fmedian_ext*.so
_so_path = None
for fname in os.listdir(_project_root):
    if fname.startswith('fmedian_ext') and fname.endswith('.so'):
        _so_path = os.path.join(_project_root, fname)
        break

if _so_path is None:
    # As a fallback, try to import top-level module if available
    try:
        _real = __import__('fmedian_ext')
    except Exception as e:
        raise ImportError('Could not find compiled fmedian_ext extension (.so) in project root and import failed') from e
else:
    # Load the extension using its real module name so the extension's
    # initialization function (PyInit_fmedian_ext) can be found.
    # Using a different name previously caused: "dynamic module does not define
    # module export function (PyInit__fmedian_ext_real)" because the init
    # symbol must match the module name.
    _module_name = 'fmedian_ext'
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

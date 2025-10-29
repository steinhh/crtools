""""""

Wrapper that loads the compiled `fmedian_ext` extension from the local directory andWrapper that loads the compiled `fmedian_ext` extension from the local directory and

re-exports its public symbols.re-exports its public symbols.



This allows running scripts from inside `fmedian/` that do `import fmedian_ext`This allows running scripts from inside `fmedian/` that do `import fmedian_ext`

without needing to modify `sys.path` in every script.without needing to modify `sys.path` in every script.

""""""

import importlib.machineryimport importlib.machinery

import importlib.utilimport importlib.util

import osimport os



# Project root is the parent directory of this file# Project root is the parent directory of this file

_project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))_project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))



# Look for a compiled extension file in the current directory matching fmedian_ext*.so# Look for a compiled extension file in the current directory matching fmedian_ext*.so

_so_path = None_so_path = None

current_dir = os.path.dirname(__file__)current_dir = os.path.dirname(__file__)

for fname in os.listdir(current_dir):for fname in os.listdir(current_dir):

    if fname.startswith('fmedian_ext') and fname.endswith('.so'):    if fname.startswith('fmedian_ext') and fname.endswith('.so'):

        _so_path = os.path.join(current_dir, fname)        _so_path = os.path.join(current_dir, fname)

        break        break



if _so_path is None:if _so_path is None:

    # As a fallback, try to import top-level module if available    # As a fallback, try to import top-level module if available

    try:    try:

        _real = __import__('fmedian_ext')        _real = __import__('fmedian_ext')

    except Exception as e:    except Exception as e:

        raise ImportError('Could not find compiled fmedian_ext extension (.so) in local directory and import failed') from e        raise ImportError('Could not find compiled fmedian_ext extension (.so) in local directory and import failed') from e

else:else:

    # Load the extension using its real module name so the extension's    # Load the extension using its real module name so the extension's

    # initialization function (PyInit_fmedian_ext) can be found.    # initialization function (PyInit_fmedian_ext) can be found.

    # Using a different name previously caused: "dynamic module does not define    # Using a different name previously caused: "dynamic module does not define

    # module export function (PyInit__fmedian_ext_real)" because the init    # module export function (PyInit__fmedian_ext_real)" because the init

    # symbol must match the module name.    # symbol must match the module name.

    _module_name = 'fmedian_ext'    _module_name = 'fmedian_ext'

    spec = importlib.util.spec_from_file_location(    spec = importlib.util.spec_from_file_location(

        _module_name,        _module_name,

        _so_path,        _so_path,

        loader=importlib.machinery.ExtensionFileLoader(_module_name, _so_path),        loader=importlib.machinery.ExtensionFileLoader(_module_name, _so_path),

    )    )

    _real = importlib.util.module_from_spec(spec)    _real = importlib.util.module_from_spec(spec)

    spec.loader.exec_module(_real)    spec.loader.exec_module(_real)



# Re-export public names# Re-export public names

for _name in dir(_real):for _name in dir(_real):

    if not _name.startswith('_'):    if not _name.startswith('_'):

        globals()[_name] = getattr(_real, _name)        globals()[_name] = getattr(_real, _name)



# For convenience, set __all__# For convenience, set __all__

__all__ = [n for n in dir() if not n.startswith('_')]__all__ = [n for n in dir() if not n.startswith('_')]

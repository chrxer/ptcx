import importlib.machinery
import importlib.util
from pathlib import Path
from types import ModuleType

def fileimport(file_path: Path) -> ModuleType:
    module_name = module_name=str(file_path.stem)
    loader = importlib.machinery.SourceFileLoader(module_name, str(file_path))
    spec = importlib.util.spec_from_file_location(module_name, str(file_path), loader=loader)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

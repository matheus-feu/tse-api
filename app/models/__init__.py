import importlib
import pkgutil

from pathlib import Path

package = __name__
package_path = Path(__file__).parent


def _walk_and_import(package: str, path: Path) -> None:
    """
    Importa recursivamente todos os módulos e subpacotes abaixo de path.
    """
    for module_info in pkgutil.iter_modules([str(path)]):
        name = module_info.name

        if name.startswith("_"):
            continue

        full_package = f"{package}.{name}"

        if module_info.ispkg:
            sub_path = path / name
            importlib.import_module(full_package)
            _walk_and_import(full_package, sub_path)
        else:
            importlib.import_module(full_package)


_walk_and_import(package, package_path)

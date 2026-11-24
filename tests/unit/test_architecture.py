"""Kiểm tra lớp bên trong không phụ thuộc vào lớp bên ngoài."""

import ast
from pathlib import Path

import pytest

import gas

INNER_MODULES = ["tariff.py", "charge.py", "billing.py", "notifications.py"]
OUTER_PACKAGES = ("django", "gas.web")


def imported_modules(source: Path) -> set[str]:
    tree = ast.parse(source.read_text(encoding="utf-8"))
    modules: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            modules.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            modules.add(node.module)
    return modules


@pytest.mark.parametrize("module", INNER_MODULES)
def test_inner_layers_do_not_import_outer_layers(module: str) -> None:
    # Arrange
    source = Path(gas.__file__).parent / module

    # Act
    modules = imported_modules(source)

    # Assert
    assert not [name for name in modules if name.startswith(OUTER_PACKAGES)]

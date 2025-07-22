#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.9"
# dependencies = [
#     "griffe",
# ]
# [tool.uv.sources]
# griffe = { git = "https://github.com/mkdocstrings/griffe.git", rev = "8ef1486e9b1f0872cca3b1cd2419144b702a0c1e" }
# ///
from __future__ import annotations

import ast
import logging
import sys
from pathlib import Path
from typing import Any, Generator

import griffe
from _griffe.extensions.dataclasses import _set_dataclass_init

logger = griffe.get_logger(__name__)


class FR24CheckSignatureExtension(griffe.Extension):
    def __init__(
        self,
        method_decorator_path: str = "fr24.types.static_check_signature",
    ) -> None:
        super().__init__()
        self.method_decorator_path = method_decorator_path
        self.methods_to_check: dict[griffe.Function, griffe.ExprName] = {}
        self.method_signature_issues = 0

    def on_function_instance(
        self,
        *,
        node: ast.AST | griffe.ObjectNode,
        func: griffe.Function,
        agent: griffe.Visitor | griffe.Inspector,
        **kwargs: Any,
    ) -> None:
        dataclass: griffe.ExprName | None = None
        for decorator in func.decorators:
            if decorator.callable_path == self.method_decorator_path:
                args = decorator.value
                assert (
                    isinstance(args, griffe.ExprCall)
                    and len(args.arguments) == 1
                )
                arg0 = args.arguments[0]
                assert isinstance(arg0, griffe.ExprName)
                dataclass = arg0
                break
        if dataclass:
            self.methods_to_check[func] = dataclass

    def on_package_loaded(
        self, *, pkg: griffe.Module, loader: griffe.GriffeLoader, **kwargs: Any
    ) -> None:
        self.method_signature_issues = 0
        for meth, dataclass_name in self.methods_to_check.items():
            self.method_signature_issues += len(
                collect_errors(loader, meth, dataclass_name)
            )


def cleandoc(text: str) -> str:
    # similar to inspect.cleandoc, but more aggressive
    return " ".join(part.strip() for part in text.split("\n"))


def collect_errors(
    loader: griffe.GriffeLoader,
    meth: griffe.Function,
    dataclass_name: griffe.ExprName,
) -> list[str]:
    method_args = meth.parameters
    dc = loader.modules_collection[dataclass_name.canonical_path]
    _set_dataclass_init(dc)
    dataclass_init: griffe.Function = dc["__init__"]
    param_docs = {}
    if meth.docstring:
        parsed_sections = meth.docstring.parse(griffe.Parser.sphinx)
        for section in parsed_sections:
            if section.kind == griffe.DocstringSectionKind.parameters:
                for param in section.value:
                    param_docs[param.name] = cleandoc(param.description)
    errors = []
    for i, (method_arg, dataclass_field) in enumerate(
        zip(method_args, dataclass_init.parameters)
    ):
        if method_arg != dataclass_field:
            errors.append(
                f"argument {i} `{method_arg.name}`: name or kind mismatch\n"
                f"    expected `{dataclass_field}`\n"
                f"         got `{method_arg}`"
            )

        dm_text = param_docs.get(method_arg.name, None)
        df_text = (
            cleandoc(d.value) if (d := dataclass_field.docstring) else None
        )
        if dm_text != df_text:
            errors.append(
                f"argument {i} `{method_arg.name}`: docstring mismatch\n"
                f"    expected `{df_text}`\n"
                f"         got `{dm_text}`"
            )
    if errors:
        path = f"({meth.relative_filepath}:{meth.lineno})"
        s = "s" if len(errors) > 1 else ""
        err_str = (
            f"{len(errors)} error{s} in `{meth.canonical_path}` {path}:\n"
            + "\n".join(f"  - {error}" for error in errors)
            + "\n= help: update it to something like:\n```py\n"
            + "".join(gen_signature_from_dataclass(meth, dataclass_init))
            + "\n```"
        )
        logger.warning(err_str)
    return errors


def gen_signature_from_dataclass(
    method: griffe.Function, dataclass_init: griffe.Function
) -> Generator[str, None, None]:
    if "async" in method.labels:
        yield "async "
    yield f"def {method.path.split('.')[-1]}("
    n_args = len(dataclass_init.parameters)
    for i, field in enumerate(dataclass_init.parameters):
        yield field.name
        if field.annotation is not None:
            yield f": {field.annotation}"
        if field.default is not None:
            yield f" = {field.default}"
        if i < n_args - 1:
            yield ", "
    yield ")"
    if (r := method.returns) is not None:
        yield f" -> {r}"
    yield ":"

    doc_lines = []
    for param in dataclass_init.parameters:
        if param.docstring:
            doc_lines.append(f":param {param.name}: {param.docstring.value}")
    if doc_lines:
        yield '\n    """'
        for doc_line in doc_lines:
            yield f"\n    {doc_line}"
        yield '\n    """'


def main() -> None:
    """Check for signature issues in service methods."""
    checker = FR24CheckSignatureExtension()
    extensions = griffe.load_extensions(checker)
    griffe.load(
        "fr24",
        extensions=extensions,
        search_paths=[Path(__file__).parent.parent / "src"],
    )
    if err := checker.method_signature_issues:
        logger.error(f"found {err} signature issues{'s' if err > 1 else ''}")
        sys.exit(1)
    else:
        n_methods = len(checker.methods_to_check)
        logger.info(
            f"success: no signature issues found in {n_methods} methods."
        )


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()

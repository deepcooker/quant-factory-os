from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict

from jsonschema import validate, ValidationError


class SchemaValidationError(Exception):
    pass


def load_json_file(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def validate_with_schema(data: Dict[str, Any], schema_path: Path) -> None:
    schema = load_json_file(schema_path)
    try:
        validate(instance=data, schema=schema)
    except ValidationError as e:
        raise SchemaValidationError(
            f"Schema 校验失败: {schema_path.name}\n"
            f"错误路径: {list(e.absolute_path)}\n"
            f"错误信息: {e.message}"
        ) from e

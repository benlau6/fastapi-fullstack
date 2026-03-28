from typing import Any, Dict


def ok(data: Any = None, message: str = "ok") -> Dict[str, Any]:
    return {"code": 0, "message": message, "data": data}


def err(code: int, message: str, data: Any = None) -> Dict[str, Any]:
    return {"code": code, "message": message, "data": data}

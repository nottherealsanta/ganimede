from os import urandom
from base64 import urlsafe_b64encode
from typing import Any


def _generate_random_cell_id(id_length: int = 8) -> str:
    n_bytes = max(id_length * 3 // 4, 1)
    return urlsafe_b64encode(urandom(n_bytes)).decode("ascii").rstrip("=")


class Cell:
    def __init__(
        self,
        id: str = None,
        type: str = "code",
        source: list = "",
        execution_count: int = None,
        outputs: list = [],
        top: int = 0,
        left: int = 0,
        height: int = 0,
        width: int = 0,
    ):
        self._id = id if id else _generate_random_cell_id()
        self._type = type
        self._source = source

        self._execution_count = execution_count
        self._outputs = outputs

        self._top = top
        self._left = left
        self._height = height
        self._width = width

    def to_dict(self) -> dict:
        return {k[1:]: v for k, v in self.__dict__.items()}

    def _save(self) -> dict:
        return {
            "cell_type": self._type,
            "source": self._source,
            "metadata": {
                "gm": {
                    "top": self._top,
                    "left": self._left,
                    "height": self._height,
                    "width": self._width,
                }
            },
        }

    def __getattr__(self, __name: str) -> Any:
        return self.__dict__[f"_{__name}"]

    @property
    def is_heading(self):
        if self.type == "markdown":
            if any(line.lstrip().startswith("#") for line in self.source):
                return True
        return False

    @property
    def heading_level(self):
        if self.is_heading:
            for line in self.source:
                if line.lstrip().startswith("#"):
                    return line.count("#")
        return None

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
        self.id = id if id else _generate_random_cell_id()
        self.type = type
        self.source = source

        self.execution_count = execution_count
        self.outputs = outputs

        self.top = top
        self.left = left
        self.height = height
        self.width = width

        self.state = "idle"  # idle, running, queued, done

    def to_dict(self) -> dict:
        return {k: v for k, v in self.__dict__.items()}

    def _save(self) -> dict:
        return {
            "cell_type": self.type,
            "source": self.source,
            "metadata": {
                "gm": {
                    "top": self.top,
                    "left": self.left,
                    "height": self.height,
                    "width": self.width,
                }
            },
        }

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

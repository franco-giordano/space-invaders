from contextlib import contextmanager
from typing import Any, Generator, Self
from .drawable import Drawable
from blessed import Terminal
from math import floor


class Renderer:

    def __init__(self) -> None:
        self._term = Terminal()
        self._previous_cells: dict[tuple[int, int], str] = {}

    def draw_all(self, drawables: list[Drawable]) -> None:
        cells = {}

        for drawable in drawables:
            for x, y in drawable.positions:
                cells[self._roundxy(x, y)] = drawable.char

        output = []

        for pos in self._previous_cells.keys() - cells.keys():
            output.append(self._term.move_xy(*pos) + " ")

        for pos, char in cells.items():
            if self._previous_cells.get(pos) != char:
                output.append(self._term.move_xy(*pos) + char)

        print("".join(output), end="", flush=True)

        self._previous_cells = cells

    def _roundxy(self, x: float, y: float) -> tuple[int, int]:
        return int(floor(x)), int(floor(y))

    @property
    def max_width(self) -> int:
        return self._term.width

    @property
    def max_height(self) -> int:
        return self._term.height

    def setup(self) -> None:
        print(self._term.home + self._term.black_on_olivedrab4, end="", flush=True)

    def clear(self) -> None:
        print(self._term.clear, end="", flush=True)

    @contextmanager
    def ctx(self) -> Generator[Self, Any, None]:
        with (
            self._term.fullscreen(),
            self._term.cbreak(),
            self._term.hidden_cursor(),
            self._term.enable_kitty_keyboard(
                report_events=True,
                report_all_keys=True,
                report_text=True,
            ),
        ):
            yield self

    def teardown(self) -> None:
        print(self._term.normal + self._term.clear, end="", flush=True)

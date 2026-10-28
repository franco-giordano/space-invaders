class Drawable:
    def __init__(
        self,
        positions: list[tuple[float, float]],
        char: str,
    ) -> None:
        self.positions = positions
        self.char = char

import time
from src.drawable import Drawable
from src.renderer import Renderer


class EnemyBattalion:
    REPRESENTATION = "X"
    BASE_SPEED = 0.3

    def __init__(
        self, max_width: int, start_xs: list[float], start_ys: list[float]
    ) -> None:
        self._x_positions = start_xs
        self._y_positions = start_ys
        self._x_speed = self.BASE_SPEED
        self._max_width = max_width

    def update(self) -> None:
        if min(self._x_positions) < 0 or max(self._x_positions) >= self._max_width:
            self._x_speed *= -1

        for i in range(len(self._x_positions)):
            self._x_positions[i] += self._x_speed

    def as_drawable(self) -> Drawable:
        return Drawable(
            list(zip(self._x_positions, self._y_positions)), self.REPRESENTATION
        )


class Player:
    REPRESENTATION = "O"
    BASE_SPEED = 1.0

    def __init__(
        self, max_width: int, start_x: float, start_y: float, read_input
    ) -> None:
        self._x = start_x
        self._y = start_y
        self._max_width = max_width
        self._keys_held = set()
        self._read_input = read_input

    def update(self) -> bool:
        x_speed, y_speed = 0, 0

        key = self._read_input(timeout=0)

        if key:
            if key.pressed:
                self._keys_held.add(key.key_name)
            elif key.released:
                self._keys_held.discard(key.key_name)

        if "KEY_LEFT" in self._keys_held:
            x_speed = -self.BASE_SPEED
            y_speed = 0
        elif "KEY_RIGHT" in self._keys_held:
            x_speed = self.BASE_SPEED
            y_speed = 0
        elif "KEY_Q" in self._keys_held:
            return True

        self._x = max(0, min(self._x, self._max_width - 1))

        self._x += x_speed
        self._y += y_speed

        return False

    def as_drawable(self) -> Drawable:
        return Drawable([(self._x, self._y)], self.REPRESENTATION)


class GameManager:
    def __init__(self) -> None:
        self.renderer = Renderer()
        max_width, max_height = self.renderer.max_width, self.renderer.max_height
        self.player = Player(
            max_width, max_width // 2, 4 * max_height // 5, self.renderer._term.inkey
        )
        self.enemies = [
            EnemyBattalion(
                max_width,
                [
                    max_width // 2,
                    3 * max_width // 8,
                    5 * max_width // 8,
                    max_width // 4,
                    max_width // 2,
                    3 * max_width // 4,
                ],
                [
                    max_height // 5,
                    max_height // 5,
                    max_height // 5,
                    2 * max_height // 5,
                    2 * max_height // 5,
                    2 * max_height // 5,
                ],
            )
        ]

    def loop(self) -> None:
        self.renderer.setup()
        TICK = 0.02
        with self.renderer.ctx():
            # loop every 20ms
            while True:
                start = time.monotonic()

                is_quit = self.player.update()
                if is_quit:
                    break

                for enemy in self.enemies:
                    enemy.update()

                drawables: list[Drawable] = [self.player.as_drawable()]
                for enemy in self.enemies:
                    drawables.append(enemy.as_drawable())

                self.renderer.draw_all(drawables)

                # monotonic magic for consistent tick rate
                elapsed = time.monotonic() - start
                time.sleep(max(0, TICK - elapsed))

        self.renderer.teardown()


if __name__ == "__main__":
    game = GameManager()
    game.loop()

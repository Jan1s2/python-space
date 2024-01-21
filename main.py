from kivy.config import Config

Config.set("graphics", "width", "700")
Config.set("graphics", "height", "800")
Config.set("graphics", "resizable", False)
import kivy
from kivy.uix.widget import Widget
from kivy.app import App
from kivy.properties import ObjectProperty
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.uix.image import Image
from enum import Enum
from typing import Tuple, List
from random import randint, randrange

ROWS = 5
COLUMNS = 9
GAP = 10
INVADER_SIZE = (40, 40)
COOLDOWN_MIN = 1
COOLDOWN_MAX = 5
SHIP_VELOCITY = 3
MAX_MOVEMENT = Window.width / 7


class Target(Enum):
    PLAYER = 1
    ENEMY = 2

class Invader(Widget):
    source = ObjectProperty(None)

    def __init__(self, pos: List[int], **kwargs):
        super(Invader, self).__init__(**kwargs)
        self.__base_pos = pos
        self.pos = pos
        # print(self.pos)
        self._last_shot = 0
        self.__velocity: Tuple[int, int] = (1, 0)

        self.source = "invader.png"

    def shoot(self):
        return Projectile(self.center, Target.PLAYER, (0, -3))

    def is_out_of_bounds_x(self):
        x, base_x = self.pos[0], self.__base_pos[0]
        return x - MAX_MOVEMENT > base_x or x + MAX_MOVEMENT < base_x

    def reverse_velocity_x(self):
        self.__velocity = (-self.__velocity[0], -self.__velocity[1])

    def move_down(self):
        self.pos[1] -= 5

    def move_with_velocity(self):
        self.pos = [pos + vel for pos, vel in zip(self.pos, self.__velocity)]

    def move(self):
        if self.is_out_of_bounds_x():
            self.reverse_velocity_x()
            self.move_down()
        self.move_with_velocity()


class Player(Widget):
    def __init__(self, **kwargs):
        super(Player, self).__init__(**kwargs)

    def shoot(self):
        return Projectile(self.center, Target.ENEMY, (0, 3))
    
    def check_bounds(self, velocity):
        return self.pos[0] + velocity[0] > GAP and self.pos[0] + self.size[0] + velocity[0] < Window.width - GAP

    def move(self, velocity):
        if self.check_bounds(velocity):
            self.pos = [pos + vel for pos, vel in zip(self.pos, velocity)]
    def move_right(self):
        self.move((SHIP_VELOCITY, 0))
    def move_left(self):
        self.move((-SHIP_VELOCITY, 0))

class Projectile(Widget):
    def __init__(
        self, pos: List[int], target: Target, velocity: Tuple[int, int], **kwargs
    ):
        super(Projectile, self).__init__(**kwargs)
        self.pos: List[int] = pos
        self.__target = target
        self.__vel = velocity

    @property
    def target(self):
        return self.__target

    def move(self):
        self.pos = [pos + vel for pos, vel in zip(self.pos, self.__vel)]

    @property
    def velocity(self):
        return self.__vel

class SpaceInvadersGame(Widget):
    player = ObjectProperty(None)
    def __init__(self, **kwargs):
        super(SpaceInvadersGame, self).__init__(**kwargs)
        self.__keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self.__keyboard.bind(on_key_down=self._on_keyboard_down)
        self.__invaders: List[Invader] = []
        self.__projectiles: List[Projectile] = []
        self.__cooldown = 0

        center_x = Window.width / 2
        start_x = (
            center_x
            - ((COLUMNS - 1) * (INVADER_SIZE[0] + GAP)) / 2
            - INVADER_SIZE[0] / 2
        )

        total_height = ROWS * (INVADER_SIZE[1] + GAP) - GAP
        start_y = Window.height - total_height
        for i in range(ROWS):
            for j in range(COLUMNS):
                # x = center_x - ((COLUMNS - 1) * (INVADER_SIZE[0] + GAP)) / 2 - (INVADER_SIZE[0] + GAP) * j
                # y = center_y - ((ROWS - 1) * (INVADER_SIZE[1] + GAP)) / 2 + (INVADER_SIZE[1] + GAP) * i
                x = start_x + (INVADER_SIZE[0] + GAP) * j
                # y = start_y - (INVADER_SIZE[1] + GAP) * i
                y = start_y + (INVADER_SIZE[1] + GAP) * i

                self.__invaders.append(self.create_invader((x, y)))

    def create_invader(self, pos):
        invader = Invader(pos)
        self.add_widget(invader)
        return invader

    def should_shoot(self):
        return self.__cooldown == 0 and randrange(0, 40) > 30

    def generate_source(self):
        return randrange(0, ROWS * COLUMNS)

    def generate_attack(self, src):
        attack = src.shoot()
        self.__projectiles.append(attack)
        self.add_widget(attack)
        return attack

    def update(self, dt):
        if self.__cooldown > 0:
            self.__cooldown -= 1
        for invader in self.__invaders:
            invader.move()
            pass
        if self.should_shoot():
            self.generate_attack(self.__invaders[self.generate_source()])
            self.__cooldown = 60 * randint(COOLDOWN_MIN, COOLDOWN_MAX)
        for projectile in self.__projectiles:
            projectile.move()

    def _keyboard_closed(self):
        self.__keyboard.unbind(on_key_down=self._on_keyboard_down)
        self.__keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        print(keycode)

        match keycode[1]:
            case "escape":
                keyboard.release()
            case "a":
                self.player.move_left()
                # self.player.move_left()
            case "d":
                self.player.move_right()
                # self.player.move_left()
            case "left":
                self.player.move_left()
            case "right":
                self.player.move_right()

                # self.player.move_right()
            case "spacebar":
               self.generate_attack(self.player)
                # self.player.shoot()

        # Return True to accept the key. Otherwise, it will be used by
        # the system.
        return True


class SpaceInvadersApp(App):
    def build(self):
        game = SpaceInvadersGame()
        Clock.schedule_interval(game.update, 1.0 / 60.0)
        return game


if __name__ == "__main__":
    SpaceInvadersApp().run()

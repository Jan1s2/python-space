from kivy.config import Config

Config.set("graphics", "width", "700")
Config.set("graphics", "height", "800")
Config.set("graphics", "resizable", False)
import kivy
from kivy.uix.widget import Widget
from kivy.app import App
from kivy.properties import ObjectProperty, StringProperty, NumericProperty
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
INVADER_IMAGES = [
        "invader-5.png",
        "invader-4.png",
        "invader-3.png",
        "invader-2.png",
        "invader-1.png",
        ]


class Target(Enum):
    PLAYER = 1
    ENEMY = 2

class Invader(Widget):
    source = ObjectProperty(None)

    def __init__(self, pos: List[int], image: str, **kwargs):
        super(Invader, self).__init__(**kwargs)
        self.__base_pos = pos
        self.pos = pos
        # print(self.pos)
        self._last_shot = 0
        self.__velocity: Tuple[int, int] = (1, 0)

        self.source = image

    def get_type(self):
        return Target.ENEMY

    def shoot(self):
        return Projectile(self.center, Target.PLAYER, (0, -3))

    def is_out_of_bounds_x(self):
        x, base_x = self.x, self.__base_pos[0]
        return x - MAX_MOVEMENT > base_x or x + MAX_MOVEMENT < base_x

    def reverse_velocity_x(self):
        self.__velocity = (-self.__velocity[0], -self.__velocity[1])

    def move_down(self):
        self.y -= 5

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
        self.__cooldown = 0
        self.__lives = 3

    def shoot(self):
        res: Projectile|None = None
        if self.__cooldown == 0:
            res = Projectile(self.center, Target.ENEMY, (0, 3))
            self.__cooldown = 60 * randint(COOLDOWN_MIN, COOLDOWN_MAX) / 4
        return res

    def get_type(self):
        return Target.PLAYER

    @property
    def lives(self):
        return self.__lives
    @lives.setter
    def lives(self, change):
        if self.__lives + change >= 0:
            self.__lives += change

    @property
    def cooldown(self):
        return self.__cooldown
    @cooldown.setter
    def cooldown(self, change):
        if self.__cooldown + change >= 0:
            self.__cooldown = self.__cooldown + change
    
    def check_bounds(self, velocity):
        return self.x + velocity[0] > GAP and self.x + self.width + velocity[0] < Window.width - GAP

    def move(self, velocity):
        if self.__cooldown > 0:
            self.__cooldown -= 1
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
        self.__velocity = velocity

    @property
    def target(self):
        return self.__target

    def move(self):
        self.pos = [pos + vel for pos, vel in zip(self.pos, self.__velocity)]

    @property
    def velocity(self):
        return self.__velocity

class SpaceInvadersGame(Widget):
    player = ObjectProperty(None)
    def __init__(self, **kwargs):
        super(SpaceInvadersGame, self).__init__(**kwargs)
        self.__keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self.__keyboard.bind(on_key_down=self._on_keyboard_down)
        self.__invaders: List[Invader] = []
        self.__projectiles: List[Projectile] = []
        self.__cooldown = 0
        self.__score = 0

        center_x = Window.width / 2
        start_x = (
            center_x
            - ((COLUMNS - 1) * (INVADER_SIZE[0] + GAP)) / 2
            - INVADER_SIZE[0] / 2
        )

        total_height = ROWS * (INVADER_SIZE[1] + GAP) - GAP
        start_y = Window.height - total_height - 50
        for i in range(ROWS):
            for j in range(COLUMNS):
                x = start_x + (INVADER_SIZE[0] + GAP) * j
                y = start_y + (INVADER_SIZE[1] + GAP) * i
                image = INVADER_IMAGES[i]
                self.__invaders.append(self.create_invader((x, y), image))
    
    def check_end(self):
        for invader in self.__invaders:
            if invader.y < 0:
                return True
        return self.player.lives == 0 or len(self.__invaders) == 0

    def end(self):
        Clock.unschedule(self.update)
        self._keyboard_closed()

    def create_invader(self, pos, image):
        invader = Invader(pos, image)
        self.add_widget(invader)
        return invader

    def should_shoot(self):
        return self.__cooldown == 0 and randrange(0, 40) > 30

    def generate_source(self):
        res = randrange(0, len(self.__invaders))
        print(res)
        return res

    def generate_attack(self, src):
        attack = src.shoot()
        if attack is not None:
            self.__projectiles.append(attack)
            self.add_widget(attack)
        return attack

    def update(self, dt):
        self.ids.lives_label.text = f"Lives: {self.player.lives}"
        self.ids.score_label.text = f"Score: {self.__score}"
        if self.check_end():
            self.end()
        if self.player.cooldown > 0:
            self.player.cooldown = -1
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

        for projectile in self.__projectiles:
            if self.check_collision(projectile, self.player):
                print("HIT")
                self.player.lives = -1
                print(f"Player HP: {self.player.lives}")
                self.remove_widget(projectile)
                self.__projectiles.remove(projectile)
                self.__score -= 50
            for invader in self.__invaders:
                if self.check_collision(projectile, invader):
                    print("HIT ENEMY")
                    self.remove_widget(projectile)
                    self.__projectiles.remove(projectile)
                    self.remove_widget(invader)
                    self.__invaders.remove(invader)
                    self.__score += 20
                    break

    def check_collision(self, projectile, target):
        # Simple bounding box collision check
        return (
            projectile.target == target.get_type()
            and projectile.x < target.x + target.width
            and projectile.x + projectile.width > target.x
            and projectile.y < target.y + target.height
            and projectile.y + projectile.height > target.y
        )


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

import kivy
from kivy.uix.widget import Widget
from kivy.app import App
from kivy.properties import ObjectProperty
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.config import Config
from enum import Enum
from typing import Tuple, List
Config.set('graphics', 'resizable', False)

ROWS = 5
COLUMNS = 9

class Target(Enum):
    PLAYER = 1
    ENEMY = 2

class Invader(Widget):
    def __init__(self, pos: Tuple[int, int], **kwargs):
        super(Invader, self).__init__(**kwargs)
        self._base_pos = pos
        self.pos = pos
        self._last_shot = 0

    def shoot(self):
        pass


class Player(Widget):
    def __init__(self, x, y):
        self.__x = x
        self.__y = y

    @property
    def pos(self) -> Tuple[int, int]:
        return (self.__x, self.__y)

    def shoot(self):
        return Projectile(*self.pos, Target.ENEMY, (0, 1))

class Projectile(Widget):
    def __init__(self, x: int, y: int, target: Target, velocity: Tuple[int, int]):
        self.__x = x
        self.__y = y
        self.__target = target
        self.__vel = velocity

    @property
    def target(self):
        return self.__target

    @property
    def pos(self):
        return (self.__x, self.__y)

    @property
    def velocity(self):
        return self.__vel

class SpaceInvadersGame(Widget):
    def __init__(self, **kwargs):
        super(SpaceInvadersGame, self).__init__(**kwargs)
        self.__keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self.__keyboard.bind(on_key_down=self._on_keyboard_down)
        self.__invaders: List[Invader] = []
        center_x = Window.width / 2
        center_y = Window.height / 2

        for i in range(ROWS):
            for j in range(COLUMNS):
                invader_size = (20, 20)
                gap = 50
                x = center_x - ((COLUMNS - 1) * (invader_size[0] + gap)) / 2 + (invader_size[0] + gap) * j
                y = center_y - ((ROWS - 1) * (invader_size[1] + gap)) / 2 + (invader_size[1] + gap) * i

                self.__invaders.append(self.create_invader((x, y)))

    def create_invader(self, pos):
        invader = Invader(pos)
        self.add_widget(invader)
        return invader

    def _keyboard_closed(self):
        self.__keyboard.unbind(on_key_down=self._on_keyboard_down)
        self.__keyboard = None


    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        print(keycode)

        match keycode[1]:
            case 'escape':
                keyboard.release()
            case 'a':
                pass
                # self.player.move_left()
            case 'd':
                pass
                # self.player.move_right()
            case 'space':
                pass
                # self.player.shoot()

        # Return True to accept the key. Otherwise, it will be used by
        # the system.
        return True

class SpaceInvadersApp(App):
    def build(self):
        game = SpaceInvadersGame()
        Window.size = (800, 900)
        return game

if __name__ == "__main__":
    SpaceInvadersApp().run()

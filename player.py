from kivy.uix.widget import Widget
from kivy.core.window import Window
from random import randint

from target import Target
from projectile import Projectile
from constants import COOLDOWN_MIN, COOLDOWN_MAX, GAP, SHIP_VELOCITY
# Widget class representing the player's spaceship
class Player(Widget):
    """Class representing the player's spaceship in the game."""

    def __init__(self, **kwargs):
        """Initialize the Player instance.

        Args:
            **kwargs: Additional keyword arguments.
        """
        super(Player, self).__init__(**kwargs)
        self.__cooldown = 0
        self.__lives = 3

    def shoot(self):
        """Create and return a projectile representing the player's shot."""
        res: Projectile|None = None
        if self.__cooldown == 0:
            res = Projectile(self.center, Target.ENEMY, (0, 3))
            self.__cooldown = 60 * randint(COOLDOWN_MIN, COOLDOWN_MAX) / 4
        return res

    def get_type(self):
        """Get the target type of the player."""
        return Target.PLAYER

    @property
    def lives(self):
        """Get the current number of lives of the player."""
        return self.__lives
    
    @lives.setter
    def lives(self, change):
        """Set the number of lives of the player with the given change."""
        if self.__lives + change >= 0:
            self.__lives += change

    @property
    def cooldown(self):
        """Get the current cooldown of the player's shot."""
        return self.__cooldown
    
    @cooldown.setter
    def cooldown(self, change):
        """Set the cooldown of the player's shot with the given change."""
        if self.__cooldown + change >= 0:
            self.__cooldown += change
    
    def check_bounds(self, velocity):
        """Check if the player's movement is within the screen bounds."""
        return self.x + velocity[0] > GAP and self.x + self.width + velocity[0] < Window.width - GAP

    def move(self, velocity):
        """Move the player based on the given velocity."""
        if self.__cooldown > 0:
            self.__cooldown -= 1
        if self.check_bounds(velocity):
            self.pos = [pos + vel for pos, vel in zip(self.pos, velocity)]

    def move_right(self):
        """Move the player to the right."""
        self.move((SHIP_VELOCITY, 0))

    def move_left(self):
        """Move the player to the left."""
        self.move((-SHIP_VELOCITY, 0))


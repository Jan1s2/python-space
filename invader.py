from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from typing import List,Tuple


from target import Target
from projectile import Projectile
from constants import MAX_MOVEMENT
# Widget class representing an invader
class Invader(Widget):
    """Class representing an invader in the game."""

    source = ObjectProperty(None)

    def __init__(self, pos: List[int], image: str, **kwargs):
        """Initialize the Invader instance.

        Args:
            pos (List[int]): Initial position of the invader.
            image (str): Filename of the invader image.
            **kwargs: Additional keyword arguments.
        """
        super(Invader, self).__init__(**kwargs)
        self.__base_pos = pos
        self.pos = pos
        self._last_shot = 0
        self.__velocity: Tuple[int, int] = (1, 0)
        self.source = image

    def get_type(self):
        """Get the target type of the invader."""
        return Target.ENEMY

    def shoot(self):
        """Create and return a projectile representing the invader's shot."""
        return Projectile(self.center, Target.PLAYER, (0, -3))

    def is_out_of_bounds_x(self):
        """Check if the invader is out of bounds in the horizontal direction."""
        x, base_x = self.x, self.__base_pos[0]
        return x - MAX_MOVEMENT > base_x or x + MAX_MOVEMENT < base_x

    def reverse_velocity_x(self):
        """Reverse the horizontal velocity of the invader."""
        self.__velocity = (-self.__velocity[0], -self.__velocity[1])

    def move_down(self):
        """Move the invader down."""
        self.y -= 5

    def move_with_velocity(self):
        """Move the invader according to its velocity."""
        self.pos = [pos + vel for pos, vel in zip(self.pos, self.__velocity)]

    def move(self):
        """Move the invader, handling boundary conditions."""
        if self.is_out_of_bounds_x():
            self.reverse_velocity_x()
            self.move_down()
        self.move_with_velocity()

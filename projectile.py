from kivy.uix.widget import Widget
from typing import List,Tuple

from target import Target
# Widget class representing a projectile
class Projectile(Widget):
    """Class representing a projectile in the game."""

    def __init__(
        self, pos: List[int], target: Target, velocity: Tuple[int, int], **kwargs
    ):
        """Initialize the Projectile instance.

        Args:
            pos (List[int]): Initial position of the projectile.
            target (Target): Target type of the projectile.
            velocity (Tuple[int, int]): Initial velocity of the projectile.
            **kwargs: Additional keyword arguments.
        """
        super(Projectile, self).__init__(**kwargs)
        self.pos: List[int] = pos
        self.__target = target
        self.__velocity = velocity

    @property
    def target(self):
        """Get the target type of the projectile."""
        return self.__target

    def move(self):
        """Move the projectile based on its velocity."""
        self.pos = [pos + vel for pos, vel in zip(self.pos, self.__velocity)]

    @property
    def velocity(self):
        """Get the velocity of the projectile."""
        return self.__velocity

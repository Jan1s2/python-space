from kivy.config import Config
from kivy.uix.widget import Widget
from kivy.app import App
from kivy.properties import ObjectProperty
from kivy.core.window import Window
from kivy.clock import Clock
from typing import List
from random import randint, randrange


from constants import ROWS, COLUMNS, INVADER_SIZE, GAP, INVADER_IMAGES, COOLDOWN_MIN, COOLDOWN_MAX
from invader import Invader
from projectile import Projectile
# Needed because of Kivy
from player import Player

# Set up the graphics configuration for the Kivy app
Config.set("graphics", "width", "700")
Config.set("graphics", "height", "800")
Config.set("graphics", "resizable", False)

# Widget class representing the main game area
class SpaceInvadersGame(Widget):
    """Class representing the main game area."""

    player = ObjectProperty(None)

    def __init__(self, **kwargs):
        """Initialize the SpaceInvadersGame instance.

        Args:
            **kwargs: Additional keyword arguments.
        """
        super(SpaceInvadersGame, self).__init__(**kwargs)
        self.__keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self.__keyboard.bind(on_key_down=self._on_keyboard_down)
        self.__invaders: List[Invader] = []
        self.__projectiles: List[Projectile] = []
        self.__cooldown = 0
        self.__score = 0

        # Initialize invaders' positions
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
        """Check if the game has reached its end condition."""
        for invader in self.__invaders:
            if invader.y < 0:
                return True
        return self.player.lives == 0 or len(self.__invaders) == 0

    def end(self):
        """End the game."""
        Clock.unschedule(self.update)
        Window.release_keyboard()

    def create_invader(self, pos, image):
        """Create and add an invader to the game area.

        Args:
            pos (Tuple[int, int]): Initial position of the invader.
            image (str): Filename of the invader image.

        Returns:
            Invader: The created invader instance.
        """
        invader = Invader(pos, image)
        self.add_widget(invader)
        return invader

    def should_shoot(self):
        """Determine if an invader should shoot."""
        return self.__cooldown == 0 and randrange(0, 40) > 30

    def generate_source(self):
        """Generate a random source invader for shooting."""
        res = randrange(0, len(self.__invaders))
        print(res)
        return res

    def generate_attack(self, src:Invader|Player):
        """Generate an attack (projectile) from a source invader.

        Args:
            src (Invader|Player): Source of the projectile.

        Returns:
            Projectile: The generated projectile.
        """
        attack = src.shoot()
        if attack is not None:
            self.__projectiles.append(attack)
            self.add_widget(attack)
        return attack

    def update(self, dt):
        """Update the game state."""
        self.ids.lives_label.text = f"Lives: {self.player.lives}"
        self.ids.score_label.text = f"Score: {self.__score}"

        # Check if the game has ended
        if self.check_end():
            self.end()

        # Update cooldowns
        if self.player.cooldown > 0:
            self.player.cooldown = -1
        if self.__cooldown > 0:
            self.__cooldown -= 1

        # Move invaders
        for invader in self.__invaders:
            invader.move()

        # Check if an invader should shoot and generate projectiles
        if self.should_shoot():
            self.generate_attack(self.__invaders[self.generate_source()])
            self.__cooldown = 60 * randint(COOLDOWN_MIN, COOLDOWN_MAX)

        # Move and check collisions for projectiles
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
        """Check for collision between a projectile and a target.

        Args:
            projectile (Projectile): The projectile to check.
            target (Widget): The target to check.

        Returns:
            bool: True if a collision occurred, False otherwise.
        """
        # Simple bounding box collision check
        return (
            projectile.target == target.get_type()
            and projectile.x < target.x + target.width
            and projectile.x + projectile.width > target.x
            and projectile.y < target.y + target.height
            and projectile.y + projectile.height > target.y
        )

    def _keyboard_closed(self):
        """Handle keyboard closure."""
        self.__keyboard.unbind(on_key_down=self._on_keyboard_down)
        self.__keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        """Handle keyboard input events.

        Args:
            keyboard: The keyboard instance.
            keycode: The keycode of the pressed key.
            text: The text representation of the pressed key.
            modifiers: The modifiers applied to the pressed key.

        Returns:
            bool: True if the key event is accepted, False otherwise.
        """
        print(keycode)

        match keycode[1]:
            case "escape":
                keyboard.release()
            case "a":
                self.player.move_left()
            case "d":
                self.player.move_right()
            case "left":
                self.player.move_left()
            case "right":
                self.player.move_right()
            case "spacebar":
                self.generate_attack(self.player)

        # Return True to accept the key. Otherwise, it will be used by the system.
        return True

# Main application class
class SpaceInvadersApp(App):
    """Main application class."""

    def build(self):
        """Build and return the main game instance."""
        game = SpaceInvadersGame()
        Clock.schedule_interval(game.update, 1.0 / 60.0)
        return game

# Run the application if executed as a script
if __name__ == "__main__":
    SpaceInvadersApp().run()

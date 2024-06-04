"""Pygame Simplified Helper 1.0"""
import pygame
import sys

pygame.init()

width = height = screen = fps = clock = None

def init():
    """
    Initialize the game clock and set the frames per second (fps) to 60.
    """
    global fps, clock
    fps = 60
    clock = pygame.time.Clock()
    print("pygame simplified helper is now at version 1.0")

def screen(size, name, icon):
    """
    Set up the display window with the given size, title, and icon.

    Parameters:
    size (tuple): The width and height of the window.
    name (str): The title of the window.
    icon (str): The file path to the icon image.
    """
    global width, height, screen
    width, height = size
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption(name)
    pygame.display.set_icon(pygame.image.load(icon).convert_alpha())

class color:
    """
    A class containing predefined color constants.
    """
    red = (255, 0, 0)
    green = (0, 255, 0)
    blue = (0, 0, 255)
    yellow = (255, 255, 0)
    purple = (128, 0, 128)
    pink = (255, 192, 203)
    orange = (255, 165, 0)
    gray = (128, 128, 128)
    aqua = (0, 255, 255)
    magenta = (255, 0, 255)
    brown = (139, 69, 19)
    black = (0, 0, 0)
    white = (255, 255, 255)
    beige = (255, 228, 196)
    dark_blue = (0, 0, 139)

class backdrop:
    """
    A class to handle the backdrop of the game screen.
    """
    color = color.black
    image = None

    @staticmethod
    def set_image(image):
        """
        Set the backdrop image.

        Parameters:
        image (str): The file path to the image.
        """
        backdrop.image = pygame.image.load(image).convert()

    @staticmethod
    def set_color(color):
        """
        Set the backdrop color.

        Parameters:
        color (tuple): The color of the backdrop.
        """
        backdrop.image = None
        backdrop.color = color

class sprite:
    """
    A class to manage game sprites.
    """
    sprite = []

    class create:
        """
        A class to create and manage individual sprites.
        """
        def __init__(self, costume, costume_id=0, hidden=False):
            """
            Initialize the sprite with costumes and initial settings.

            Parameters:
            costume (list): List of file paths to costume images.
            costume_id (int): The index of the initial costume.
            hidden (bool): Whether the sprite is initially hidden.
            """
            self.costume = [pygame.image.load(i) for i in costume]
            self.costume_id = costume_id
            self.width = self.costume[self.costume_id].get_width()
            self.height = self.costume[self.costume_id].get_height()
            self.x = (width - self.width) // 2
            self.y = (height - self.height) // 2
            self.hidden = hidden
            self.mask = pygame.mask.from_surface(self.costume[self.costume_id])
            sprite.sprite.append(self)

        def move_to(self, x, y):
            """
            Move the sprite to a new position.

            Parameters:
            x (int): The new x-coordinate.
            y (int): The new y-coordinate.
            """
            self.x, self.y = x, y

        def edge(self):
            """
            Check if the sprite is at the edge of the screen.

            Returns:
            bool: True if at the edge, False otherwise.
            """
            return self.x < 0 or self.y < 0 or self.x > width or self.y > height

        def update(self):
            """
            Update the sprite's dimensions and mask based on the current costume.
            """
            self.width = self.costume[self.costume_id].get_width()
            self.height = self.costume[self.costume_id].get_height()
            self.mask = pygame.mask.from_surface(self.costume[self.costume_id])

        def touched(self, sprite):
            """
            Check if this sprite is touching another sprite.

            Parameters:
            sprite (Sprite.Create): Another sprite to check collision with.

            Returns:
            bool: True if the sprites are touching, False otherwise.
            """
            if not (self.hidden or sprite.hidden):
                self.rect = self.costume[self.costume_id].get_rect(topleft=(self.x, self.y))
                rect = sprite.costume[sprite.costume_id].get_rect(topleft=(sprite.x, sprite.y))
                if self.rect.colliderect(rect):
                    offset = (self.rect.x - rect.x, self.rect.y - rect.y)
                    return self.mask.overlap(sprite.mask, offset) is not None
                
            return False

        def delete(self):
            """
            Delete the sprite.
            """
            sprite.sprite.remove(self)
            del self

class sound:
    """
    A class to manage sounds.
    """
    class create:
        """
        A class to create and manage individual sounds.
        """
        def __init__(self, sound, volume=1):
            """
            Initialize the sound with file path and volume.

            Parameters:
            sound (str): The file path to the sound.
            volume (float): The volume of the sound (0.0 to 1.0).
            """
            self.sound = pygame.mixer.Sound(sound)
            self.volume = volume
            self.sound.set_volume(volume)

        def update(self):
            """
            Update the volume of the sound.
            """
            self.sound.set_volume(self.volume)

        def play(self, time=1):
            """
            Play the sound.

            Parameters:
            time (int): The number of times to play the sound.
            """
            self.sound.play(time)

        def delete(self):
            """
            Delete the sound.
            """
            del self

class cursor:
    """
    A class to manage the mouse cursor state.
    """
    x = y = 0
    focused = False

    @staticmethod
    def is_down(button=0):
        """
        Check if the specified mouse button is pressed.

        Parameters:
        button (int): The mouse button to check (0 for left, 1 for middle, 2 for right).

        Returns:
        bool: True if the specified button is pressed, False otherwise.
        """
        return pygame.mouse.get_pressed()[button]

    @staticmethod
    def update():
        """
        Update the cursor position and focus state.
        """
        cursor.x, cursor.y = pygame.mouse.get_pos()
        cursor.focused = pygame.mouse.get_focused()

class text:
    """
    A class to manage text on the screen.
    """
    txt = []

    class create:
        """
        A class to create and manage individual text objects.
        """
        def __init__(self, txt, x, y, size, color=color.white, font=None, bg=None, bold=False, 
                     italic=False, underline=False):
            """
            Initialize the text object with various properties.

            Parameters:
            txt (str): The text content.
            x (int): The x-coordinate.
            y (int): The y-coordinate.
            size (int): The font size.
            color (tuple): The text color.
            font (str): The file path to the font file.
            bg (tuple): The background color.
            bold (bool): Whether the text is bold.
            italic (bool): Whether the text is italicized.
            underline (bool): Whether the text is underlined.
            """
            self.x = x
            self.y = y
            self.bold = bold
            self.italic = italic
            self.underline = underline
            self.font = font
            self.size = size
            self.text = txt
            self.color = color
            self.bg = bg
            self.fnt = pygame.font.Font(self.font, self.size)
            self.fnt.set_bold(self.bold)
            self.fnt.set_italic(self.italic)
            self.fnt.set_underline(self.underline)
            text.txt.append(self)

        def update(self):
            """
            Update the text object's properties.
            """
            self.fnt = pygame.font.Font(self.font, self.size)
            self.fnt.set_bold(self.bold)
            self.fnt.set_italic(self.italic)
            self.fnt.set_underline(self.underline)

        def delete(self):
            """
            Delete the text object.
            """
            text.txt.remove(self)

def _quit():
    pygame.quit()
    sys.exit()

def _update():
    """
    Update the screen with the current backdrop, sprites, and text objects.

    Parameters:
    screen (pygame.Surface): The display surface to update.
    """
    if backdrop.image is None:
        screen.fill(backdrop.color)
    else:
        screen.blit(backdrop.image, (0, 0))
        
    for s in sprite.sprite:
        if not s.hidden:
            screen.blit(s.costume[s.costume_id], (s.x, s.y))

    for t in text.txt:
        screen.blit(t.fnt.render(t.text, True, t.color, t.bg), (t.x, t.y))

    cursor.update()
    
    pygame.display.update()
    clock.tick(fps)

def mainloop(loop=None):
    """
    Main game loop that handles events, executes the user-defined loop function,
    and updates the display.

    Parameters:
    loop (function): A user-defined function to be executed on each iteration of the loop.
    """
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                _quit()

        if loop is not None:
            loop()

        _update()

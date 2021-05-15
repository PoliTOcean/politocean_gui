from .joystick import QJoystick
from .element import QJoystickAxis, QJoystickButton

import sdl2

sdl2.SDL_Init(sdl2.SDL_INIT_JOYSTICK)

import pygame

import clock_client.ui.led as led


class TimeDisplay:
    """ Displays a time of day in hours, minutes, and seconds using a series of 7-segment displays.s """

    @classmethod
    def width(cls, segment_width):
        """ Computes the width of the time display based on a given LED segment width """
        return (6 * led.char_width(segment_width)        # 6 digits
                + 5 * led.char_space(segment_width)      # 5 spaces after digits
                + 2 * led.char_space(segment_width)      # 2 spaces after colons
                + 2 * segment_width                      # 2 colons
                + 2 * 2 * segment_width)                 # left and right padding
    
    @classmethod
    def height(cls, segment_width):
        """ Computes the height of the time display based on a given LED segment width """
        return (led.char_height(segment_width)           # height of digit
                + 2 * 2 * segment_width)                 # top and bottom padding
    
    def __init__(self, surface, xy, segment_width, color):
        """ Initializes a time display instance.

        Args:
            surface: a pygame drawing surface
            xy: pygame coordinate pair (2-tuple or vector) for the top left corner
            segment_width: desired width of each LED segment
            color: a simulated LED display color name (see COLORS in the led module)
        """
        self._surface = surface
        self._clock = pygame.time.Clock()
        
        digit_width = led.char_width(segment_width)
        digit_space = led.char_space(segment_width)

        x = xy[0]
        x += 2*segment_width    # left padding
        y = xy[1]
        y += 2*segment_width    # top padding
        
        self._hour_left = led.Display7Segment(surface, (x, y), segment_width, color)

        x += digit_width + digit_space
        self._hour_right = led.Display7Segment(surface, (x, y), segment_width, color)

        x += digit_width + digit_space
        self._colon_left = led.Colon(surface, (x, y), segment_width, True, color)

        x += segment_width + digit_space
        self._minute_left = led.Display7Segment(surface, (x, y), segment_width, color)

        x += digit_width + digit_space
        self._minute_right = led.Display7Segment(surface, (x, y), segment_width, color)

        x += digit_width + digit_space
        self._colon_right = led.Colon(surface, (x, y), segment_width, True, color)

        x += segment_width + digit_space
        self._second_left = led.Display7Segment(surface, (x, y), segment_width, color)

        x += digit_width + digit_space
        self._second_right = led.Display7Segment(surface, (x, y), segment_width, color)

    def draw(self, hour: int, minute: int, second: int):
        """ Draws the time display on the configured pygame surface.

        Args:
            hour (int): hour number [0..23]
            minute (int): minute number [0..59]
            second (int): second number [0..59]
        """
        self._hour_left.draw(hour // 10 if hour // 10 else None)
        self._hour_right.draw(hour % 10)
        self._colon_left.draw()
        self._minute_left.draw(minute // 10)
        self._minute_right.draw(minute % 10)
        self._colon_right.draw()
        self._second_left.draw(second // 10)
        self._second_right.draw(second % 10)
        
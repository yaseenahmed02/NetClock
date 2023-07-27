import pygame

import clock_client.ui.led as led


class DateDisplay:
    """ Displays a calendar date using a series of 14-segment and 7-segment displays. """

    @classmethod
    def width(cls, segment_width):
        """ Computes the width of the date display given an LED segment width """
        return (6 * led.char_width(segment_width)        # 6 letters
                + 4 * led.char_space(segment_width)      # 4 spaces between letters
                + 6 * led.char_width(segment_width)      # 6 digits
                + 4 * led.char_space(segment_width)      # 4 spaces between digits
                + 3 * led.word_space(segment_width)      # 3 spaces between words
                + 2 * 2 * segment_width)                 # left and right padding
    
    @classmethod
    def height(cls, segment_width):
        """ Computes the height of the date display based given an LED segment width """
        return (led.char_height(segment_width)           # height of character
                + 2 * 2 * segment_width)                 # top and bottom padding
    
    def __init__(self, surface, xy, segment_width, color):
        """ Initializes a date display instance

        Args:
            surface: a pygame drawing surface
            xy: pygame coordinate pair (2-tuple or vector) for the top left corner
            segment_width: desired width of each LED segment
            color: a simulated LED display color name (see COLORS in the led module)
        """
        self._surface = surface
        self._clock = pygame.time.Clock()
        
        char_width = led.char_width(segment_width)
        char_space = led.char_space(segment_width)
        word_space = led.word_space(segment_width)
        
        x = xy[0]
        x += 2*segment_width    # left padding
        y = xy[1]
        y += 2*segment_width    # top padding
        
        self._day_of_week = []
        self._day_of_week.append(led.Display14Segment(surface, (x, y), segment_width, color))

        x += char_width + char_space
        self._day_of_week.append(led.Display14Segment(surface, (x, y), segment_width, color))

        x += char_width + char_space
        self._day_of_week.append(led.Display14Segment(surface, (x, y), segment_width, color))

        self._month = []
        x += char_width + word_space
        self._month.append(led.Display14Segment(surface, (x, y), segment_width, color))

        x += char_width + char_space
        self._month.append(led.Display14Segment(surface, (x, y), segment_width, color))

        x += char_width + char_space
        self._month.append(led.Display14Segment(surface, (x, y), segment_width, color))

        x += char_width + word_space
        self._day_of_month_left = led.Display7Segment(surface, (x, y), segment_width, color)
        
        x += char_width + char_space
        self._day_of_month_right = led.Display7Segment(surface, (x, y), segment_width, color)
                
        x += char_width + word_space
        self._century_left = led.Display7Segment(surface, (x, y), segment_width, color)

        x += char_width + char_space
        self._century_right = led.Display7Segment(surface, (x, y), segment_width, color)

        x += char_width + char_space
        self._year_left = led.Display7Segment(surface, (x, y), segment_width, color)

        x += char_width + char_space
        self._year_right = led.Display7Segment(surface, (x, y), segment_width, color)

    def draw(self, year: int, month: str, day_of_month: str, day_of_week: str):
        """ Draws the date display on the configured pygame surface.

        Args:
            year: year number
            month: month abbreviation (3 uppercase letters)
            day_of_month: day of the month [1..31]
            day_of_week: day of week abbreviation (3 uppercase letters)
        """
        assert len(month) == 3
        assert len(day_of_week) == 3
        
        for i, letter in enumerate(day_of_week):
            self._day_of_week[i].draw(letter)
        
        for i, letter in enumerate(month):
            self._month[i].draw(letter)

        self._day_of_month_left.draw(day_of_month // 10)        
        self._day_of_month_right.draw(day_of_month % 10)        

        century = year // 100
        year = year % 100
        self._century_left.draw(century // 10)
        self._century_right.draw(century % 10)
        self._year_left.draw(year // 10)
        self._year_right.draw(year % 10)
        
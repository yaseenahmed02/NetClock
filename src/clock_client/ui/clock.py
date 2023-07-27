from typing import Callable, Any

import pygame

from .date_display import DateDisplay
from .time_display import TimeDisplay


FRAMES_PERS_SECOND = 10


class ClockUI:
    """ The top-level clock UI simulator """
    
    def __init__(self, time_supplier: Callable[[], Any], color: str, time_segment_width: int, title: str):
        """ Initializes the clock UI instance.

        Args:
            time_supplier (Callable[[], Any]): this is any function that returns a time-of-day object 
                containing the following attributes
                    year (int): year number with century
                    month_name (str): abbreviated day of the month (3 uppercase letters)
                    day_of_month (int): day of the month [1..31]
                    day_name (str): abbreviated day of the week (3 upper case letters)
                    hour (int): hour number [0..23]
                    minute (int): minute number [0..59]
                    second (int): second number [0..59]
            color (str): color for the simulated LED display (see led.COLORS for names)
            time_segment_width (int): desired segment width for the time display
            title (str): title for the UI window
        """
        self._time_supplier = time_supplier
        self._color = color
        self._title = title
    
        time_width = TimeDisplay.width(time_segment_width)
        time_height = TimeDisplay.height(time_segment_width)
        date_segment_width = int(time_segment_width * 3 / 5)
        date_width = DateDisplay.width(date_segment_width)
        date_height = DateDisplay.height(date_segment_width)

        ui_width = max(time_width, date_width)
        ui_height = time_height + date_height

        self._date_segment_width = date_segment_width
        self._date_xy = ((ui_width - date_width) // 2, 0)
        self._time_segment_width = time_segment_width
        self._time_xy = ((ui_width - time_width) // 2, date_height)
        self._ui_size = (ui_width, ui_height)

    def run(self):
        """ Runs a loop to poll the current date and time from the chronometer
            and display it using a pygame screen.
        """
        pygame.init()
        screen = pygame.display.set_mode(self._ui_size)
        pygame.display.set_caption(self._title)
        clock = pygame.time.Clock()
        date_display = DateDisplay(screen, self._date_xy, self._date_segment_width, self._color)
        time_display = TimeDisplay(screen, self._time_xy, self._time_segment_width, self._color)
        
        run = True
        while run:
            clock.tick(FRAMES_PERS_SECOND)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

            screen.fill(0)
            instant = self._time_supplier()
            if instant:
                date_display.draw(instant.year, instant.month_name, instant.day_of_month, instant.day_name)
                time_display.draw(instant.hour, instant.minute, instant.second)
            pygame.display.update()
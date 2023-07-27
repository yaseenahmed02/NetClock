from typing import ByteString, Tuple


class Instant:
    """ An instant in chronological time. """

    _DAYS_OF_WEEK = ("MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN", "???")
    _MONTHS = ("JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC")
    _MONTH_DAYS = (31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)

    @classmethod
    def _day_of_year(cls, month: int, day_of_month: int) -> int:
        """ Computes the day of the year for the given month and day of the month.
            NOTE: this implementation does not account for leap years
        
        Args:
            month (int): month number [1..12]
            day_of_month (int): day of the month [1..31]; caller should bound as appropriate for specified month)

        Returns:
            int: day of the year [1..365]
        """
        day_of_year = 0
        for m in range(0, month - 1):
            day_of_year += cls._MONTH_DAYS[m]
        return day_of_year + day_of_month
        
    @classmethod
    def _month_and_day(cls, day_of_year: int) -> Tuple[int, int]:
        """ Computes the month and day of the month given a day of the year.
            NOTE: this implementation does not account for leap years

        Args:
            day_of_year (int): day of the year [1..365]

        Returns:
            Tuple[int, int]: month [1..12] and day of the month [1..31]
        """
        month = 0
        remaining_days = day_of_year
        while remaining_days - cls._MONTH_DAYS[month] > 0:
            remaining_days -= cls._MONTH_DAYS[month]
            month += 1
        return month + 1, remaining_days        

    def __init__(self, year: int, month: int, day_of_month, day_of_week: int,
                 hour: int, minute: int, second: int, microsecond: int):
        """ Initializes a new instant

        Args:
            year (int): year [2000..)
            month (int): month [1..12]
            day_of_month (int): day of the month [1..31]
            day_of_week (int): day of the week [0..6]
            hour (int): [0..23]
            minute (int): [0..59]
            second (int): [0..59]
            microsecond (int): [0..999999]
        """
        self.year = year
        self.month = month
        self.day_of_month = day_of_month
        self.day_of_week = day_of_week
        self.hour = hour
        self.minute = minute
        self.second = second
        self.microsecond = microsecond
    
    @property
    def month_name(self):
        return self._MONTHS[self.month - 1]

    @property
    def day_name(self):
        return self._DAYS_OF_WEEK[self.day_of_week]
    
    def incr(self, ticks: int) -> "Instant":
        """ Produces a new instant representing this instant plus the given tick count (microseconds).

        Args:
            ticks (int): number of microseconds to add to this new instant

        Returns:
            Instant: new instant = self + ticks
        """
        microseconds = self.microsecond + ticks
        microsecond = microseconds % 1000000
        seconds = self.second + (microseconds // 1000000)
        second = seconds % 60
        minutes = self.minute + (seconds // 60)
        minute = minutes % 60
        hours = self.hour + (minutes // 60)
        hour = hours % 24
        days = hours // 24
        day_of_week = self.day_of_week + (days % 7)
        day_of_year = (self._day_of_year(self.month, self.day_of_month) + days) % 365
        month, day_of_month = self._month_and_day(day_of_year)
        year = self.year + (days // 365)
        return Instant(year, month, day_of_month, day_of_week, hour, minute, second, microsecond)

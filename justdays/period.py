from __future__ import annotations

from .day import Day


class Period:
    """Bundles a startdate and optionally an end date to form a date range"""

    def __init__(self, fromday, untilday=None):
        """Period is initalized with a startdate and optionally an end date
        Start date can be a Day object or a string in the format 'YYYY-MM-DD'"""
        if not isinstance(fromday, Day):
            fromday = Day(fromday)
        self.fromday = fromday
        if untilday and not isinstance(untilday, Day):
            untilday = Day(untilday)
        self.untilday = untilday
        self.current = fromday.prev()  # Initialize iterator

    @classmethod
    def from_week(cls, year, weekno):
        """Returns a Period object for the week of the year"""
        fromday = Day(year, weekno)
        untilday = fromday.plus_weeks(1)
        return cls(fromday, untilday)

    @classmethod
    def from_month(cls, year, month):
        """Returns a Period object for the month of the year"""
        fromday = Day(year, month, 1)
        untilday = fromday.plus_months(1)
        return cls(fromday, untilday)

    def __str__(self) -> str:
        return f'{self.fromday} --> {self.untilday if self.untilday else ""}'

    def __repr__(self) -> str:
        return f"Period({str(self)})"

    def __hash__(self):
        return hash(str(self))

    def __iter__(self) -> Period:
        return self

    def __next__(self) -> Day:
        self.current = self.current.next()
        if self.current >= self.untilday:
            self.current = self.fromday.prev()
            raise StopIteration
        return self.current

    def __contains__(self, other: Day | Period) -> bool:
        if type(other) == Day:
            return self.fromday <= other < self.untilday
        elif type(other) == Period:
            if not self.untilday:
                return self.fromday <= other.fromday
            if not other.untilday:
                return False
            return self.fromday <= other.fromday < self.untilday and self.fromday <= other.untilday < self.untilday
        raise TypeError(f"Invalid type passed to Period.__contains__: {type(other)}")

    def __len__(self) -> int:
        if self.untilday is None:
            return 2**31 - 1  # Maximum value for a 32-bit signed integer
        return (self.untilday - self.fromday).days

    def __eq__(self, other) -> bool:
        return self.fromday == other.fromday and self.untilday == other.untilday

    def __and__(self, other: 'Period') -> 'Period':
        """
        Calculate the overlap between this period and another period using the & operator.
        
        :param other: Another Period object to calculate overlap with
        :return: A new Period object representing the overlap, or None if there's no overlap
        """
        if self.untilday and other.untilday:
            if self.untilday <= other.fromday or other.untilday <= self.fromday:
                return None  # No overlap
        elif self.untilday and self.untilday <= other.fromday:
            return None  # No overlap
        elif other.untilday and other.untilday <= self.fromday:
            return None  # No overlap

        overlap_start = max(self.fromday, other.fromday)
        overlap_end = min(self.untilday, other.untilday) if self.untilday and other.untilday else None

        return Period(overlap_start, overlap_end)

    def overlap(self, other: 'Period') -> 'Period':
        """
        Calculate the overlap between this period and another period.
        
        :param other: Another Period object to calculate overlap with
        :return: A new Period object representing the overlap, or None if there's no overlap
        """
        return self & other

    def is_empty(self) -> bool:
        """Check if the period has no duration."""
        return self.fromday == self.untilday

    def __bool__(self) -> bool:
        """Return True if the period is not empty, False otherwise."""
        return not self.is_empty()

    def __or__(self, other: 'Period') -> 'Period':
        """
        Perform a union of this period with another period using the | operator.
        
        :param other: Another Period object to union with
        :return: A new Period object representing the union
        """
        start = min(self.fromday, other.fromday)
        end = max(self.untilday, other.untilday) if self.untilday and other.untilday else None
        return Period(start, end)

    def union(self, other: 'Period') -> 'Period':
        """Combine this period with another, covering the entire range."""
        return self | other

    def intersects(self, other: 'Period') -> bool:
        """Check if this period overlaps with another period."""
        if not self.untilday or not other.untilday:
            return self.fromday <= other.fromday or other.fromday <= self.fromday
        return self.fromday < other.untilday and other.fromday < self.untilday

    def shift(self, days: int) -> 'Period':
        """Move the period forward or backward by a given number of days."""
        new_start = self.fromday.plus_days(days)
        new_end = self.untilday.plus_days(days) if self.untilday else None
        return Period(new_start, new_end)

    def split(self, duration: int) -> list['Period']:
        """Split the period into smaller periods of a given duration in days."""
        if not self.untilday:
            raise ValueError("Cannot split an open-ended period")
        
        result = []
        current = self.fromday
        while current < self.untilday:
            end = min(current.plus_days(duration), self.untilday)
            result.append(Period(current, end))
            current = end
        return result

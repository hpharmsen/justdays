from justdays.day import Day

class Period:
    """Bundles a startdate and optionally an end date to form a date range"""

    def __init__(self, start: Day, end: Day = None):
        self.start = start
        self.end = end if end else start

    @classmethod
    def from_week(cls, year, weekno):
        start = Day(year, weekno)
        end = start.plus_days(6)
        return cls(start, end)

    @classmethod
    def from_month(cls, year, month):
        start = Day(year, month, 1)
        end = start.last_day_of_month()
        return cls(start, end)

    def overlap(self, other: 'Period') -> 'Period':
        """
        Calculate the overlap between this period and another period.
        
        :param other: Another Period object to calculate overlap with
        :return: A new Period object representing the overlap, or None if there's no overlap
        """
        if self.end < other.start or other.end < self.start:
            return None  # No overlap

        overlap_start = max(self.start, other.start)
        overlap_end = min(self.end, other.end)

        return Period(overlap_start, overlap_end)

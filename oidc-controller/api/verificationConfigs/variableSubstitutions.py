"""
This file contains VariableSubstitutionMap class, which provides a mapping of
static variables that can be used in a proof.
Other users of this project can add their own variable substitutions or override
the entire file to suit their own needs.
"""

from datetime import datetime, timedelta
import time
import re


class VariableSubstitutionMap:
    def __init__(self):
        # Map of static variables that can be used in a proof
        # This class defines threshold_years_X as a dynamic one
        self.static_map = {
            "$now": self.get_now,
            "$today_int": self.get_today_date,
            "$tomorrow_int": self.get_tomorrow_date,
        }

    def get_threshold_years_date(self, years: int) -> int:
        """
        Calculate the threshold date for a given number of years.

        Args:
            years (int): The number of years to subtract from the current year.

        Returns:
            int: The current date minux X years in YYYYMMDD format.
        """
        threshold_date = datetime.today().replace(year=datetime.today().year - years)
        return int(threshold_date.strftime("%Y%m%d"))

    def get_now(self) -> int:
        """
        Get the current timestamp.

        Returns:
            int: The current timestamp in seconds since the epoch.
        """
        return int(time.time())

    def get_today_date(self) -> int:
        """
        Get today's date in YYYYMMDD format as a number.

        Returns:
            int: Today's date in YYYYMMDD format.
        """
        return int(datetime.today().strftime("%Y%m%d"))

    def get_tomorrow_date(self) -> int:
        """
        Get tomorrow's date in YYYYMMDD format as a number.

        Returns:
            int: Tomorrow's date in YYYYMMDD format.
        """
        return int((datetime.today() + timedelta(days=1)).strftime("%Y%m%d"))

    # For "dynamic" variables, use a regex to match the key and return a lambda function
    # So a proof request can use $threshold_years_X to get the years back for X years
    def __contains__(self, key: str) -> bool:
        return key in self.static_map or re.match(r"\$threshold_years_(\d+)", key)

    def __getitem__(self, key: str):
        if key in self.static_map:
            return self.static_map[key]
        match = re.match(r"\$threshold_years_(\d+)", key)
        if match:
            return lambda: self.get_threshold_years_date(int(match.group(1)))
        raise KeyError(f"Key {key} not found in format_args_function_map")


# Create an instance of the custom mapping class
variable_substitution_map = VariableSubstitutionMap()

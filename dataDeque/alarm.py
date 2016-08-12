"""
Alarm class models an alarm. It holds the trigger value and trigger status and
provides checking and acknowledgment.
"""

class Alarm:

    def __init__(self, value):
        """Initialize alarm info"""
        self.triggerValue = value
        self.triggered = False

    def check_alarm(self, value):
        """Checks if a value is above trigger value and returns boolean for
            whether or not alarm is triggered"""
        if value > self.triggerValue:
            self.triggered = True
            return True
        else:
            self.triggered = False
            return False

    def acknowledge_alarm(self):
        self.triggered = False

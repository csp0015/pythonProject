
from identified_object import IdentifiedObject

class Competition(IdentifiedObject):
    def __init__(self, oid, teams, location, date_time=None):
        super().__init__(oid)
        self._teams_competing = teams
        self._location = location
        self._date_time = date_time

    @property
    def teams_competing(self):
        return self._teams_competing

    @property
    def location(self):
        return self._location

    @property
    def date_time(self):
        return self._date_time

    def send_email(self, emailer, subject, message):
        recipients = []
        for team in self.teams_competing:
            recipients.extend([member.email for member in team.members if member.email is not None])
        unique_recipients = list(set(recipients))  # Remove duplicates
        emailer.send_plain_email(unique_recipients, subject, message)

    def __str__(self):
        if self.date_time:
            return f"Competition at {self.location} on {self.date_time} with {len(self.teams_competing)} teams"
        else:
            return f"Competition at {self.location} with {len(self.teams_competing)} teams"

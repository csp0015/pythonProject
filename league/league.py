from identified_object import IdentifiedObject
from duplicate_oid import DuplicateOid

class League(IdentifiedObject):
    def __init__(self, oid, name):
        super().__init__(oid)
        self._name = name
        self._teams = []
        self._competitions = []

    @property
    def name(self):
        return self._name

    @property
    def teams(self):
        return self._teams

    @property
    def competitions(self):
        return self._competitions

    def add_team(self, team):
        existing_team_oids = [t.oid for t in self.teams]
        if team.oid in existing_team_oids:
            raise DuplicateOid(team.oid)
        self._teams.append(team)

    def remove_team(self, team):
        if team in self.teams:
            competitions_with_team = [comp for comp in self.competitions if team in comp.teams_competing]
            if competitions_with_team:
                raise ValueError("Team is in one or more competitions")
            self._teams.remove(team)

    def team_named(self, team_name):
        for team in self.teams:
            if team.name == team_name:
                return team
        return None

    def add_competition(self, competition):
        for team in competition.teams_competing:
            if team not in self.teams:
                raise ValueError("One or more teams in the competition are not part of the league")
        self._competitions.append(competition)

    def teams_for_member(self, member):
        return [team for team in self.teams if member in team.members]

    def competitions_for_team(self, team):
        return [competition for competition in self.competitions if team in competition.teams_competing]

    def competitions_for_member(self, member):
        teams = self.teams_for_member(member)
        competitions = []
        for team in teams:
            competitions.extend(self.competitions_for_team(team))
        return competitions

    def __str__(self):
        return f"League Name: {self.name}, {len(self.teams)} teams, {len(self.competitions)} competitions"



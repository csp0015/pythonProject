import pickle
import csv
from league import League
from team import Team
from team_member import TeamMember
from duplicate_oid import DuplicateOid

class LeagueDatabase:
    _sole_instance = None

    @classmethod
    def instance(cls):
        if cls._sole_instance is None:
            cls._sole_instance = cls()
        return cls._sole_instance

    def __init__(self):
        self._leagues = []
        self._last_oid = 0

    @property
    def leagues(self):
        return self._leagues

    def add_league(self, league):
        self.leagues.append(league)

    def remove_league(self, league):
        if league in self.leagues:
            self.leagues.remove(league)

    def league_named(self, name):
        for league in self.leagues:
            if league.name == name:
                return league
        return None

    def next_oid(self):
        self._last_oid += 1
        return self._last_oid

    def save(self, file_name):
        try:
            with open(file_name, 'wb') as file:
                pickle.dump(self, file)
        except Exception as e:
            print(f"Error saving database: {e}")

    @classmethod
    def load(cls, file_name):
        try:
            with open(file_name, 'rb') as file:
                return pickle.load(file)
        except FileNotFoundError:
            print(f"File '{file_name}' not found.")
            # Attempt to load from backup if it exists
            backup_file = file_name + '.backup'
            if backup_file:
                print(f"Loading from backup file: {backup_file}")
                return cls.load(backup_file)
        except Exception as e:
            print(f"Error loading database: {e}")

    def import_league_teams(self, league, file_name):
        try:
            with open(file_name, 'r', encoding='utf-8') as file:
                reader = csv.reader(file)
                next(reader)  # Skip header
                for row in reader:
                    team_name, member_name, email = row
                    team = league.team_named(team_name)
                    if not team:
                        # Create a new team if it doesn't exist
                        team = Team(self.next_oid(), team_name)
                        league.add_team(team)
                    member = TeamMember(self.next_oid(), member_name, email)
                    team.add_member(member)
        except Exception as e:
            print(f"Error importing league teams: {e}")

    def export_league_teams(self, league, file_name):
        try:
            with open(file_name, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(["Team name", "Member name", "Member email"])
                for team in league.teams:
                    for member in team.members:
                        writer.writerow([team.name, member.name, member.email])
        except Exception as e:
            print(f"Error exporting league teams: {e}")

if __name__ == '__main__':
    league = League("L001", "League1")
    database = LeagueDatabase()
    database.import_league_teams(league, "Teams.csv")

    for team in league.teams:
        print(f"Team: {team.name}")
        # Iterate over each member in the team
        for member in team.members:
            print(f" - {member.name} ({member.email})")

    database.export_league_teams(league, "newTeams.csv")

import unittest
from competition import Competition
from team import Team



class CompetitionAdditionalTests(unittest.TestCase):
    def test_str(self):
        t1 = Team(1, "Team 1")
        t2 = Team(2, "Team 2")
        c = Competition(1, [t1, t2], "Here", None)
        self.assertEqual(str(c), "Competition at Here with 2 teams")

    def test_oid_property(self):
        teams = [Team(1, "Team 1"), Team(2, "Team 2")]
        competition = Competition(1, teams, "Location", None)
        self.assertEqual(1, competition.oid)

    def test_teams_competing_property(self):
        teams = [Team(1, "Team 1"), Team(2, "Team 2")]
        competition = Competition(1, teams, "Location", None)
        self.assertEqual(teams, competition.teams_competing)

    def test_date_time_property(self):
        teams = [Team(1, "Team 1"), Team(2, "Team 2")]
        competition = Competition(1, teams, "Location", None)
        self.assertIsNone(competition.date_time)

    def test_location_property(self):
        teams = [Team(1, "Team 1"), Team(2, "Team 2")]
        competition = Competition(1, teams, "Location", None)
        self.assertEqual("Location", competition.location)

    def test_empty_teams_competing_list(self):
        competition = Competition(1, [], "Location", None)
        self.assertEqual([], competition.teams_competing)

    def test_missing_date_time(self):
        teams = [Team(1, "Team 1"), Team(2, "Team 2")]
        competition = Competition(1, teams, "Location") # Missing date_time argument
        self.assertIsNone(competition.date_time)

    def test_empty_location(self):
        teams = [Team(1, "Team 1"), Team(2, "Team 2")]
        competition = Competition(1, teams, "", None) # Empty location argument
        self.assertEqual("", competition.location)

      


if __name__ == '__main__':
    unittest.main()
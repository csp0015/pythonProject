import unittest
from league import League
from team import Team
from competition import Competition


class LeagueAdditionalTests(unittest.TestCase):
    def test_league_string_representation(self):
        league = League(1, "Test League")
        self.assertEqual(str(league), "League Name: Test League, 0 teams, 0 competitions")

    def test_oid_property(self):
        league = League(1, "Test League")
        self.assertEqual(1, league.oid)

    def test_name_property(self):
        league = League(1, "Test League")
        self.assertEqual("Test League", league.name)

    def test_empty_teams_list(self):
        league = League(1, "Test League")
        self.assertEqual([], league.teams)

    def test_add_empty_team(self):
        league = League(1, "Test League")
        team = Team(1, "Empty Team")
        league.add_team(team)
        self.assertIn(team, league.teams)

    def test_remove_nonexistent_team(self):
        league = League(1, "Test League")
        team = Team(1, "Nonexistent Team")
        league.remove_team(team) # Removing a team that doesn't exist should not raise an error
        self.assertNotIn(team, league.teams)


    def test_remove_team_from_empty_league(self):
        league = League(1, "Test League")
        team = Team(1, "Nonexistent Team")
        league.remove_team(team) # Removing a team from an empty league should not raise an error
        self.assertNotIn(team, league.teams)

    def setUp(self):
        self.league = League(oid=1, name="Test League")
        self.team1 = Team(oid=101, name="Team 1")
        self.team2 = Team(oid=102, name="Team 2")

    def test_remove_team_success(self):
        self.league.add_team(self.team1)
        self.league.add_team(self.team2)

        self.assertEqual(len(self.league.teams), 2)

        self.league.remove_team(self.team1)

        self.assertEqual(len(self.league.teams), 1)
        self.assertNotIn(self.team1, self.league.teams)

    def test_remove_team_not_in_competition(self):
        self.league.add_team(self.team1)
        self.league.add_team(self.team2)

        competition_teams = [self.team2]
        self.league.add_competition(Competition(1, competition_teams, "Here"))

        with self.assertRaises(ValueError):
            self.league.remove_team(self.team2)

    def setUp(self):
        self.league = League(oid=1, name="Test League")
        self.team1 = Team(oid=101, name="Team 1")
        self.team2 = Team(oid=102, name="Team 2")
        comp_teams = [self.team1, self.team2]
        self.competition = Competition(201, comp_teams, "There")

    def test_remove_team_in_competition(self):
        self.league.add_team(self.team1)
        self.league.add_team(self.team2)
        self.league.add_competition(self.competition)

        with self.assertRaises(ValueError):
            self.league.remove_team(self.team2)


if __name__ == '__main__':
    unittest.main()
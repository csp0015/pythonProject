import unittest
from duplicate_oid import DuplicateOid
from duplicate_email import DuplicateEmail
from team import Team
from team_member import TeamMember
from league import League
from competition import Competition


class TestDuplicates(unittest.TestCase):
    def test_oid_exception_message(self):
        oid = "12345"
        exception = DuplicateOid(oid)
        self.assertEqual(str(exception), f"Duplicate OID: {oid}")

    def test_oid_exception_attribute(self):
        oid = "12345"
        exception = DuplicateOid(oid)
        self.assertEqual(exception.oid, oid)


    def test_email_exception_message(self):
        email = "test@example.com"
        exception = DuplicateEmail(email)
        self.assertEqual(str(exception), f"Duplicate Email: {email}")

    def test_email_exception_attribute(self):
        email = "test@example.com"
        exception = DuplicateEmail(email)
        self.assertEqual(exception.email, email)


    def test_team_add_member_duplicate_email(self):
        team = Team("team_oid", "Team 1")
        member1 = TeamMember("member_oid1", "John Doe", "test@example.com")
        member2 = TeamMember("member_oid2", "Jane Doe", "test@example.com")
        team.add_member(member1)
        with self.assertRaises(DuplicateEmail):
            team.add_member(member2)

    def test_team_add_member_duplicate_oid(self):
        team = Team("team_oid", "Team 1")
        member1 = TeamMember("member_oid", "John Doe", "john@example.com")
        member2 = TeamMember("member_oid", "Jane Doe", "jane@example.com")
        team.add_member(member1)
        with self.assertRaises(DuplicateOid):
            team.add_member(member2)

    def test_league_add_team_duplicate_oid(self):
        league = League("league_oid", "League 1")
        team1 = Team("team_oid1", "Team 1")
        team2 = Team("team_oid1", "Team 2")
        league.add_team(team1)
        with self.assertRaises(DuplicateOid):
            league.add_team(team2)

    def test_add_competition_valid_teams(self):
        # Create a league
        league = League("league_oid", "League 1")

        # Create teams
        team1 = Team("team_oid1", "Team 1")
        team2 = Team("team_oid2", "Team 2")

        # Add teams to the league
        league.add_team(team1)
        league.add_team(team2)

        # Create a competition with valid teams
        valid_teams_competition = Competition("comp_oid", [team1, team2], "Location", "Date")

        # Adding the competition to the league should not raise an exception
        league.add_competition(valid_teams_competition)

        # Check if the competition is in the league's competitions list
        self.assertIn(valid_teams_competition, league.competitions)

    def test_add_competition_invalid_teams(self):
        # Create a league
        league = League("league_oid", "League 1")

        # Create teams
        team1 = Team("team_oid1", "Team 1")
        team2 = Team("team_oid2", "Team 2")

        # Add only one team to the league
        league.add_team(team1)

        # Create a competition with invalid teams (one team not part of the league)
        invalid_teams_competition = Competition("comp_oid", [team1, team2], "Location", "Date")

        # Adding the competition to the league should raise a ValueError
        with self.assertRaises(ValueError):
            league.add_competition(invalid_teams_competition)

        # Check if the competition is not in the league's competitions list
        self.assertNotIn(invalid_teams_competition, league.competitions)

if __name__ == '__main__':
    unittest.main()

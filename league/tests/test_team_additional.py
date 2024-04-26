from team import Team
from team_member import TeamMember
import unittest


class TestTeamAdditional(unittest.TestCase):
    def test_str(self):
        t = Team(1, "Curl Jam")
        self.assertEqual("Team Name: Curl Jam, 0 members", str(t))

    def test_oid_property(self):
        team = Team(1, "Test Team")
        self.assertEqual(1, team.oid)

    def test_name_property(self):
        team = Team(1, "Test Team")
        self.assertEqual("Test Team", team.name)

    def test_empty_members_list(self):
        team = Team(1, "Test Team")
        self.assertEqual([], team.members)

    def test_add_empty_member(self):
        team = Team(1, "Test Team")
        member = TeamMember(1, "Empty Member", "empty@example.com")
        team.add_member(member)
        self.assertIn(member, team.members)

    def test_remove_nonexistent_member(self):
        team = Team(1, "Test Team")
        member = TeamMember(1, "Nonexistent Member", "nonexistent@example.com")
        team.remove_member(member) # Removing a member that doesn't exist should not raise an error
        self.assertNotIn(member, team.members) 



    def test_remove_member_from_empty_team(self):
        team = Team(1, "Test Team")
        member = TeamMember(1, "Nonexistent Member", "nonexistent@example.com")
        team.remove_member(member) # Removing a member from an empty team should not raise an error
        self.assertNotIn(member, team.members)       

if __name__ == '__main__':
    unittest.main()

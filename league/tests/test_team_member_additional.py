import unittest
from team_member import TeamMember
from test_team_member import TeamMemberTests

class TestTeamMemberAdditional(unittest.TestCase):
    def test_str(self):
        tm_1 = TeamMember(1, "name", "email")
        tm_2 = TeamMember(1, "other name", "other email")
        self.assertEqual("name<email>", str(tm_1))
        self.assertEqual("other name<other email>", str(tm_2))

    def test_oid_property(self):
        member = TeamMember(1, "John", "john@example.com")
        self.assertEqual(1, member.oid)

    def test_name_property(self):
        member = TeamMember(1, "John", "john@example.com")
        self.assertEqual("John", member.name)

    def test_email_property(self):
        member = TeamMember(1, "John", "john@example.com")
        self.assertEqual("john@example.com", member.email)

    def test_empty_name(self):
        tm = TeamMember(1, "", "email@example.com")
        self.assertEqual("", tm.name)

    def test_empty_email(self):
        tm = TeamMember(1, "John Doe", "")
        self.assertEqual("", tm.email)

    def test_long_name(self):
        long_name = "a" * 256
        tm = TeamMember(1, long_name, "email@example.com")
        self.assertEqual(long_name, tm.name)

    def test_whitespace_name(self):
        tm = TeamMember(1, " John Doe ", "email@example.com")
        self.assertEqual("John Doe", tm.name.strip())

    def test_whitespace_email(self):
        tm = TeamMember(1, "John Doe", " email@example.com ")
        self.assertEqual("email@example.com", tm.email.strip())

    def test_case_sensitive_name_comparison(self):
        tm_1 = TeamMember(1, "John", "email@example.com")
        tm_2 = TeamMember(2, "john", "anotheremail@example.com")
        self.assertNotEqual(tm_1, tm_2)

    def test_case_sensitive_email_comparison(self):
        tm_1 = TeamMember(1, "John", "EMAIL@example.com")
        tm_2 = TeamMember(2, "Jane", "email@example.com")
        self.assertNotEqual(tm_1, tm_2)

    def test_name_with_punctuation(self):
        name_with_punctuation = "John-Doe_Smith"
        tm = TeamMember(1, name_with_punctuation, "email@example.com")
        self.assertEqual(name_with_punctuation, tm.name)

    def test_email_with_punctuation(self):
        email_with_punctuation = "john.doe_smith@example.com"
        tm = TeamMember(1, "John Doe", email_with_punctuation)
        self.assertEqual(email_with_punctuation, tm.email)

    def test_special_characters_name(self):
        special_name = "!@#$%^&*()_+-={}[]|;:,.<>?/~`"
        tm = TeamMember(1, special_name, "email@example.com")
        self.assertEqual(special_name, tm.name)


if __name__ == '__main__':
    unittest.main()

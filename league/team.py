from identified_object import IdentifiedObject
from duplicate_oid import DuplicateOid
from duplicate_email import DuplicateEmail

class Team(IdentifiedObject):
    def __init__(self, oid, name):
        super().__init__(oid)
        self._name = name
        self._members = []

    @property
    def name(self):
        return self._name

    @property
    def members(self):
        return self._members

    def add_member(self, member):
        existing_emails = [m.email.lower() for m in self.members]
        if member.email.lower() in existing_emails:
            raise DuplicateEmail(member.email)
        existing_member = [mem.oid for mem in self.members]
        if member.oid in existing_member:
            raise DuplicateOid(member.oid)
        self._members.append(member)


    def remove_member(self, member):
        if member in self.members:
            self._members.remove(member)

    def member_named(self, name):
        for member in self.members:
            if member.name == name:
                return member
        return None

    def send_email(self, emailer, subject, message):
        recipients = [member.email for member in self.members if member.email is not None]
        emailer.send_plain_email(recipients, subject, message)

    def __str__(self):
        return f"Team Name: {self.name}, {len(self.members)} members"



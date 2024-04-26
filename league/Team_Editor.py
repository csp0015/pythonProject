import sys
from PyQt5 import uic, QtWidgets
from team_member import TeamMember
from additional_functions import AdditionalFunctions
import os

Ui_MainWindow, QtBaseClass = uic.loadUiType('Team_Editor.ui')




class TeamEditor(QtBaseClass, Ui_MainWindow):
    def __init__(self, team=None, league=None, database=None, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        self.team_members = []
        if team is not None:
            self.team = team
            for member in team.members:
                self.team_members.append(member)
        if league is not None:
            self.league = league
        if database is not None:
            self.database = database
        AdditionalFunctions.update_ui(self.member_ListWidget, self.team_members)
        self.add_Member_button.clicked.connect(self.add_member)
        self.delete_Member_button.clicked.connect(self.remove_member)
        self.edit_Member_button.clicked.connect(self.edit_member)

    def add_member(self):
        member_name = self.add_name_LineEdit.text()
        member_email = self.add_email_LineEdit.text()
        if (member_name=='' or member_email=='' or member_name in [member.name for member in self.team_members] or member_email in [member.email for member in self.team_members]):
            return AdditionalFunctions.alert("Please enter a valid name or email", "Name and email are required and cannot be duplicates")

        member_oid = self.database.next_oid()
        adding_member = TeamMember(member_oid, member_name, member_email)

        self.team_members.append(adding_member)
        self.add_name_LineEdit.clear()
        self.add_email_LineEdit.clear()
        AdditionalFunctions.update_ui(self.member_ListWidget, self.team_members)

    def remove_member(self):
        member_row = AdditionalFunctions.get_selected_item(self.member_ListWidget, self.team_members)
        if member_row < 0:
            return AdditionalFunctions.alert("Please select a team member", "You must select a team member in the list")

        removing_member = self.team_members[member_row]
        member_name = removing_member.name
        AdditionalFunctions.confirm_deletion(self, removing_member, member_name, self.team_members, self.member_ListWidget)

    def edit_member(self):
        member_row = AdditionalFunctions.get_selected_item(self.member_ListWidget, self.team_members)
        if member_row < 0:
            return AdditionalFunctions.alert("Please select a team member", "You must select a team member in the list")

        editing_member = self.team_members.pop(member_row)

        new_member_name = self.edit_name_LineEdit.text()
        new_member_email = self.edit_email_LineEdit.text()
        if (new_member_name=='' or new_member_email=='' or new_member_name in [member.name for member in self.team_members] or new_member_email in [member.email for member in self.team_members]):
            self.team_members.insert(member_row, editing_member)
            return AdditionalFunctions.alert("Please enter a valid name or email", "Name and email are required and cannot be duplicates")

        editing_member.name = new_member_name
        editing_member.email = new_member_email
        self.team_members.insert(member_row, editing_member)
        self.add_name_LineEdit.clear()
        self.add_email_LineEdit.clear()
        AdditionalFunctions.update_ui(self.member_ListWidget, self.team_members)

    def update_Team(self, team):
        for member in self.team_members:
            if member not in team.members:
                team.add_member(member)


        remove_member_list = [member for member in team.members if member not in self.team_members]

        for member in remove_member_list:
            team.remove_member(member)



if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = TeamEditor()
    window.show()
    sys.exit(app.exec_())
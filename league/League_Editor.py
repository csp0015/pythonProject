import sys
from PyQt5.QtWidgets import QMessageBox, QFileDialog, QDialog
from league import League
from league_database import LeagueDatabase
from PyQt5 import uic, QtWidgets
from team import Team
from Team_Editor import TeamEditor
from additional_functions import AdditionalFunctions

Ui_MainWindow, QtBaseWindow = uic.loadUiType('League_Editor.ui')


class LeagueEditor(QtBaseWindow, Ui_MainWindow):
    def __init__(self, league=None, database=None, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        # if league is not none, set title, and set up temp teams array and fill with league teams
        self.temp_teams = []
        if league is not None:
            self.league = league
            for team in league.teams:
                self.temp_teams.append(team)
        if database is not None:
            self.database = database
        AdditionalFunctions.update_ui(self.team_ListWidget, self.temp_teams)
        self.add_Team_Button.clicked.connect(self.add_Team)
        self.remove_Team_Button.clicked.connect(self.remove_Team)
        self.edit_Team_Button.clicked.connect(self.edit_Team)
        self.loadFileButton.clicked.connect(self.import_league)
        self.saveButton.clicked.connect(self.save_league)

    def add_Team(self):
        team_name = self.add_Team_LineEdit.text()
        if team_name=='' or team_name in [team.name for team in self.temp_teams]:
            return AdditionalFunctions.alert("Invalid Team Name", "Team must have a name and cannot be a duplicate")

        team_oid = self.database.next_oid()
        adding_team = Team(team_oid, team_name)
        self.temp_teams.append(adding_team)
        self.add_Team_LineEdit.clear()
        AdditionalFunctions.update_ui(self.team_ListWidget, self.temp_teams)

    def remove_Team(self):
        team_row = AdditionalFunctions.get_selected_item(self.team_ListWidget, self.temp_teams)
        if team_row < 0:
            return AdditionalFunctions.alert("Select Team", "Select a team to remove")

        removed_team = self.temp_teams[team_row]
        team_name = removed_team.name
        AdditionalFunctions.confirm_deletion(self, removed_team, team_name, self.temp_teams, self.team_ListWidget)


    def edit_Team(self):
        team_row = AdditionalFunctions.get_selected_item(self.team_ListWidget, self.temp_teams)
        if team_row < 0:
            return AdditionalFunctions.alert("Select Team", "Select a team to edit")

        editing_team = self.temp_teams[team_row]
        dialog = TeamEditor(editing_team, self.league, self.database)
        if dialog.exec_() == QDialog.DialogCode.Accepted:
            dialog.update_Team(editing_team)
            AdditionalFunctions.update_ui(self.team_ListWidget, self.temp_teams)
        else:
            pass

    def update_Team(self, league):
        for team in self.temp_teams:
            if team not in league.teams:
                league.add_team(team)

        remove = [team for team in league.teams if team not in self.temp_teams]

        for team in remove:
            league.remove_team(team)

    def import_league(self):
        leagueOID = self.database.next_oid()
        holder_league = League(leagueOID, "Holder")
        dialog = QFileDialog()
        dialog.setDirectory("/leagueFiles")
        result = dialog.exec()
        if result == QDialog.DialogCode.Accepted:
            file_name = dialog.selectedFiles()[0]
            LeagueDatabase.import_league_teams(self.database, holder_league, file_name)

            for team in holder_league.teams:
                if team.name in [team.name for team in self.temp_teams]:
                    pass
                else:
                    self.temp_teams.append(team)
            AdditionalFunctions.update_ui(self.team_ListWidget, self.temp_teams)
        else:
            pass

    def save_league(self):
        dialog = QMessageBox(self)
        dialog.setIcon(QMessageBox.Question)
        dialog.setWindowTitle("Save League")
        dialog.setText("Must save before export")
        dialog.setInformativeText("Do you want to save this league?")
        confirm_button = dialog.addButton("Save", QMessageBox.ButtonRole.AcceptRole)
        dialog.exec()

        if dialog.clickedButton() == confirm_button:
            self.update_Team(self.league)
            export_dialog = QFileDialog()
            file_name = export_dialog.getSaveFileName(self,'Export League', '/leagueFiles')
            if file_name[0] != '':
                LeagueDatabase.export_league_teams(self.database, self.league, file_name[0])
            else:
                pass
        else:
            pass


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = LeagueEditor()
    window.show()
    sys.exit(app.exec_())
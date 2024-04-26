import sys
from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import QFileDialog, QDialog
from league_database import LeagueDatabase
from additional_functions import AdditionalFunctions
from league import League
from League_Editor import LeagueEditor


Ui_MainWindow, QtBaseWindow = uic.loadUiType('Main_Window.ui')


class MainWindow(QtBaseWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setupUi(self)
        self.database = LeagueDatabase()
        self.add_League_button.clicked.connect(self.add_League)
        self.delete_League_button.clicked.connect(self.remove_League)
        self.edit_League_button.clicked.connect(self.edit_League)
        self.saveButton.clicked.connect(self.save_database)
        self.loadFileButton.clicked.connect(self.load_database)

    def add_League(self):
        league_name = self.ad_league_LineEdit.text()
        if league_name == '' or league_name in [league.name for league in self.database.leagues]:
            return AdditionalFunctions.alert("Invalid league name", "League cannot be blank or cannot be a duplicate name of an existing league.")

        new_oid = self.database.next_oid()
        new_league = League(new_oid, league_name)
        self.database.add_league(new_league)
        self.ad_league_LineEdit.clear()
        AdditionalFunctions.update_ui(self.league_ListWidget, self.database.leagues)

    def remove_League(self):
        row = AdditionalFunctions.get_selected_item(self.league_ListWidget, self.database.leagues)
        if row < 0:
            return AdditionalFunctions.alert("Choose League", "Choose a league to be removed.")

        remove_league = self.database.leagues[row]
        league_name = remove_league.name
        AdditionalFunctions.confirm_deletion(self, remove_league, league_name, self.database.leagues, self.league_ListWidget)

    def edit_League(self):
        row = AdditionalFunctions.get_selected_item(self.league_ListWidget, self.database.leagues)
        if row < 0:
            return AdditionalFunctions.alert("Choose League", "Choose a league to be edited.")

        edit_league = self.database.leagues[row]
        dialog = LeagueEditor(edit_league, self.database)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            dialog.update_Team(edit_league)
            AdditionalFunctions.update_ui(self.league_ListWidget, self.database.leagues)
        else:
            pass

    def save_database(self):
        dialog = QFileDialog()
        file_name = dialog.getSaveFileName(self, 'Save Database', '/databaseFiles')
        if file_name[0] != '':
            self.database.save(file_name[0])
        else:
            pass

    def load_database(self):
        dialog = QFileDialog()
        dialog.setDirectory("/databaseFiles")
        action = dialog.exec()
        if action == QDialog.DialogCode.Accepted:
            file_name = dialog.selectedFiles()[0]
            self.database = LeagueDatabase.load(file_name)
            AdditionalFunctions.update_ui(self.league_ListWidget, self.database.leagues)
        else:
            pass





if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
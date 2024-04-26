from PyQt5.QtWidgets import QMessageBox, QWidget


class AdditionalFunctions:

    @staticmethod
    def get_selected_item(item_list, obj_array):
        """Gets the index from the selected item from UI list object and returns it."""
        selected_items = item_list.selectedItems()
        if not selected_items:
            return -1
        assert len(selected_items) == 1
        selected = selected_items[0]
        for index, item in enumerate(obj_array):
            if str(item) == selected.text():
                return index
        return -1

    @staticmethod
    def alert(title, message):
        """Displays pop-up alert window."""
        warning_box = QMessageBox(QMessageBox.Warning, title, message, QMessageBox.Ok)
        return warning_box.exec()

    @staticmethod
    def update_ui(item_list, obj_array):
        """Updates list with objects from temp list"""
        item_list.clear()
        for item in obj_array:
            item_list.addItem(str(item))

    def confirm_deletion(self, obj, object_name, obj_array, item_list):
        dialog = QMessageBox(self)
        dialog.setIcon(QMessageBox.Question)
        dialog.setWindowTitle('Confirm Deletion')
        dialog.setText(f"Are you sure you want to delete this item?")
        dialog.setInformativeText(f"Name: {object_name}")
        confirm_button = dialog.addButton("Delete", QMessageBox.ButtonRole.AcceptRole)
        cancel_button = dialog.addButton("Cancel", QMessageBox.ButtonRole.RejectRole)
        dialog.exec()
        if dialog.clickedButton() == confirm_button:
            obj_array.remove(obj)
            AdditionalFunctions.update_ui(item_list, obj_array)

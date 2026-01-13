import sys
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QFileDialog, QMessageBox

HEX_VALUES = {
    "21:9 (2560x1080)": "26 B4 17 40",
    "21:9 (3440x1440)": "8E E3 18 40",
    "21:9 (3840x1600)": "9A 99 19 40",
    "32:9": "39 8E 63 40",
}

TARGET_HEX = "39 8E E3 3F"  

def hex_to_bytes(hex_str):
    hex_str = hex_str.replace(" ", "")
    return bytes.fromhex(hex_str)

class UltrawidePatcher(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mio Ultrawide Patch")
        self.setMinimumWidth(400)

        layout = QtWidgets.QVBoxLayout()

        # File selector
        file_layout = QtWidgets.QHBoxLayout()
        self.file_edit = QtWidgets.QLineEdit()
        browse_btn = QtWidgets.QPushButton("Browse Mio EXE")
        browse_btn.clicked.connect(self.browse_file)
        file_layout.addWidget(self.file_edit)
        file_layout.addWidget(browse_btn)

        # Resolution selector
        self.res_combo = QtWidgets.QComboBox()
        self.res_combo.addItems(HEX_VALUES.keys())

        # Patch button
        patch_btn = QtWidgets.QPushButton("Apply Ultrawide Fix")
        patch_btn.clicked.connect(self.patch_file)

        layout.addLayout(file_layout)
        layout.addWidget(QtWidgets.QLabel("Select resolution:"))
        layout.addWidget(self.res_combo)
        layout.addWidget(patch_btn)

        self.setLayout(layout)

    def browse_file(self):
        path, _ = QFileDialog.getOpenFileName(self, "Select mio.exe", "", "Executable (*.exe)")
        if path:
            self.file_edit.setText(path)

    def patch_file(self):
        file_path = self.file_edit.text()
        if not file_path:
            QMessageBox.warning(self, "Error", "Please select an EXE file.")
            return

        new_hex = HEX_VALUES[self.res_combo.currentText()]
        try:
            with open(file_path, "rb") as f:
                data = f.read()

            target_bytes = hex_to_bytes(TARGET_HEX)
            new_bytes = hex_to_bytes(new_hex)

            count = data.count(target_bytes)
            if count == 0:
                QMessageBox.warning(self, "No Matches", "No occurrences of the target hex value were found.")
                return

            patched_data = data.replace(target_bytes, new_bytes)

            with open(file_path, "wb") as f:
                f.write(patched_data)

            QMessageBox.information(self, "Success", f"Patched {count} occurrence(s) successfully!")

        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = UltrawidePatcher()
    window.show()
    sys.exit(app.exec_())

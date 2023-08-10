import os
import re
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QListWidget, QLineEdit, QPushButton, QMessageBox, QFileDialog

class MediaRenamer(QWidget):
    def __init__(self, directory = None):
        super().__init__()
        self.init_ui(directory)

    def init_ui(self, directory = None):
        self.setWindowTitle("Media File Renamer")

        self.list_widget = QListWidget(self)
        self.entry = QLineEdit(self)
        self.entry.returnPressed.connect(self.rename_file)  # Connect Enter key press to rename_file

        layout = QVBoxLayout()
        layout.addWidget(self.list_widget)
        layout.addWidget(self.entry)
        self.setLayout(layout)

        self.directory = directory
        self.video_files = None

    @staticmethod
    def get_all_video_files(directory):
        video_extensions = [".mp4", ".mkv", ".avi", ".mov", ".wmv", ".srt"]
        video_files = []
        for root, _, files in os.walk(directory):
            for file in files:
                if file.lower().endswith(tuple(video_extensions)):
                    video_path = os.path.join(root, file)
                    print(f"[+] Discovered: {video_path}")
                    video_files.append(video_path)
        print(f"[+] Total Files: {len(video_files)}")
        return video_files

    @staticmethod
    def setup_name(filename: str):
        extension = os.path.splitext(filename)[1]
        filename = filename.replace(extension, '')
        filename = filename.replace('.', ' ')
        filename = filename.replace('_', ' ')
        filename = filename.replace('[', '')
        filename = filename.replace(']', '')
        filename = filename.replace('(', '')
        filename = filename.replace(')', '')
        filename = filename.replace('EgyBest', '')
        filename = filename.replace('BluRay', '')
        filename = filename.replace('WEB-DL', '')
        filename = filename.replace('x264', '')
        filename = filename.replace('WEBRip', '')
        filename = filename.replace('720p', '')
        filename = filename.replace('480p', '')
        filename = filename.replace('YIFY', '')
        filename = filename.replace('1080p', '')
        filename = filename.replace('MyCima TO', '')
        filename = filename.replace('MyCima TV', '')

        # # For Tv Shows Only (example: Mr Robot)
        # filename = filename.replace('Mr Robot', '')
        # pattern = r'eps\d\s\d'
        # filename = re.sub(pattern, '', filename)
        # filename = filename.split(" ")[1]


        pattern = r'(\d{4})'
        filename = re.sub(pattern, r'(\1)', filename)
        return filename.strip() + extension

    def load_files(self):
        if not self.directory:
            QMessageBox.information(self, "Information", "No directory selected.")
            return

        self.video_files = self.get_all_video_files(self.directory)

        if not self.video_files:
            QMessageBox.information(self, "Information", "No video files found in the selected directory.")
            return

        for file in self.video_files:
            self.list_widget.addItem(os.path.basename(file))

        self.list_widget.setCurrentRow(0)
        self.entry.setText(self.setup_name(os.path.basename(self.video_files[0])))

    def rename_file(self):
        try:
            selected_item = self.list_widget.currentItem()
            if not selected_item:
                self.list_widget.setCurrentRow(0)  # Automatically select the first item if no selection
                selected_item = self.list_widget.currentItem()

            index = self.list_widget.row(selected_item)
            new_name = self.entry.text().strip()

            if not new_name:
                QMessageBox.information(self, "Information", "Please enter a new name.")
                return

            new_path = os.path.join(os.path.dirname(self.video_files[index]), new_name)
            if new_path != self.video_files[index] and os.path.exists(new_path):
                QMessageBox.warning(self, "Warning", "A file with the new name already exists. Please enter a different name.")
                return
            else:
                print(f"[+] Renaming {os.path.basename(self.video_files[index])} to {new_name}")

            os.rename(self.video_files[index], new_path)
            self.list_widget.takeItem(index)
            self.video_files.remove(self.video_files[index])

            if not self.video_files:
                QMessageBox.information(self, "Information", "All files renamed. Exiting.")
                QApplication.quit()
                return

            self.list_widget.setCurrentRow(0)
            selected_item = self.list_widget.currentItem()
            index = self.list_widget.row(selected_item)
            self.entry.setText(self.setup_name(os.path.basename(self.video_files[0])))
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

if __name__ == "__main__":
    app = QApplication(sys.argv)

    if len(sys.argv) > 1:
        directory = sys.argv[1]
    else:
        directory = QFileDialog.getExistingDirectory(None, "Select Directory with Video Files")

    print(f"[+] Selected Directory: {directory}")

    if not directory:
        sys.exit(1)

    window = MediaRenamer(directory)
    window.show()
    window.load_files()

    sys.exit(app.exec_())

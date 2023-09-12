import sys
import os
import threading
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QLineEdit, QFileDialog, QVBoxLayout, QMessageBox, QProgressBar
from PyQt5.QtCore import Qt, QThread, pyqtSignal
import subprocess
import re
import multiprocessing


class VideoVolumeAdjuster(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Video Volume Adjuster')
        self.setGeometry(100, 100, 400, 200)

        self.file_label = QLabel('Select a video file:')
        self.file_input = QLineEdit()
        self.browse_button = QPushButton('Browse')
        self.volume_label = QLabel('Enter new volume (e.g., 2.0 for double):')
        self.volume_input = QLineEdit()
        self.volume_input.setText('2.0')
        self.adjust_button = QPushButton('Adjust Volume')
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setGeometry(20, 200, 360, 20)
        self.progress_bar.setValue(0)
        self.progress_bar.setVisible(False)


        layout = QVBoxLayout()
        layout.addWidget(self.file_label)
        layout.addWidget(self.file_input)
        layout.addWidget(self.browse_button)
        layout.addWidget(self.volume_label)
        layout.addWidget(self.volume_input)
        layout.addWidget(self.adjust_button)
        layout.addWidget(self.progress_bar)
        self.setLayout(layout)

        self.browse_button.clicked.connect(self.select_file)
        self.adjust_button.clicked.connect(self.adjust_volume)

    def select_file(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly

        file_name, _ = QFileDialog.getOpenFileName(self, 'Select a video file', '', 'Video Files (*.mp4 *.avi *.mov);;All Files (*)', options=options)

        if file_name:
            self.file_input.setText(file_name)

    def adjust_volume(self):
        input_file = self.file_input.text()
        volume = self.volume_input.text()

        if not input_file:
            QMessageBox.warning(self, 'Warning', 'Please select a video file.')
            return

        if not volume:
            QMessageBox.warning(self, 'Warning', 'Please enter a new volume value.')
            return

        try:
            volume = float(volume)
        except ValueError:
            QMessageBox.warning(self, 'Warning', 'Invalid volume value. Please enter a numeric value.')
            return

        if not os.path.isfile(input_file):
            QMessageBox.warning(self, 'Warning', 'The selected file does not exist.')
            return

        output_file = f"adjusted_{os.path.basename(input_file)}"
        # output_file = os.path.join(os.path.dirname(input_file), output_file)

        self.adjust_button.setEnabled(False)
        self.browse_button.setEnabled(False)
        self.progress_bar.setVisible(True)

        # Start FFmpeg processing in a separate thread
        self.ffmpeg_thread = FFmpegThread(input_file, volume, output_file)
        self.ffmpeg_thread.progress_signal.connect(self.update_progress)
        self.ffmpeg_thread.finished_signal.connect(self.process_finished)
        self.ffmpeg_thread.start()

    def update_progress(self, progress):
        self.progress_bar.setValue(progress)

    def process_finished(self):
        # Re-enable UI elements after processing
        self.adjust_button.setEnabled(True)
        self.browse_button.setEnabled(True)
        self.progress_bar.setVisible(False)

        QMessageBox.information(self, 'Success', f"Volume-adjusted video saved as {self.ffmpeg_thread.output_file}")

class FFmpegThread(QThread):
    progress_signal = pyqtSignal(int)
    finished_signal = pyqtSignal()

    def __init__(self, input_file, volume, output_file):
        super().__init__()
        self.input_file = input_file
        self.volume = volume
        self.output_file = output_file

    def run(self):
        ffmpeg_command = f'ffmpeg -threads {multiprocessing.cpu_count() - 1} -i "{self.input_file}" -af "volume={self.volume}" -c:v copy "{self.output_file}" -y'
        process = subprocess.Popen(
            ffmpeg_command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            bufsize=1,
            universal_newlines=True
        )

        duration, current_time = 0, 0

        while True:
            line = process.stdout.readline()
            if not line:
                break

            # Extract duration and time info from FFmpeg output
            if 'Duration:' in line:
                match = re.search(r'Duration: ([\d:.]+)', line)
                if match:
                    duration = self.parse_time(match.group(1))
            elif 'time=' in line:
                match = re.search(r'time=([\d:.]+)', line)
                if match:
                    current_time = self.parse_time(match.group(1))

                # Update progress signal based on current_time and duration
                if duration > 0:
                    progress = int((current_time / duration) * 100)
                    self.progress_signal.emit(progress)

        self.finished_signal.emit()

    def parse_time(self, time_str):
        hours, minutes, seconds = map(float, time_str.split(':'))
        return hours * 3600 + minutes * 60 + seconds

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = VideoVolumeAdjuster()
    window.show()
    sys.exit(app.exec_())

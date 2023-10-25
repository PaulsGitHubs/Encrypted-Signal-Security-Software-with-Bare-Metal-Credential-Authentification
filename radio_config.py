import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QComboBox, QSlider, QPushButton, QFileDialog, QHBoxLayout
from PyQt5.QtCore import Qt

FREQUENCY_RANGES = [
    ("160m: 1.8-2.0 MHz", 1.8e6, 2.0e6),
    ("80m: 3.5-4.0 MHz", 3.5e6, 4.0e6),
    ("40m: 7.0-7.3 MHz", 7.0e6, 7.3e6),
    # ... and so on, for all bands
]

TX_POWER = [
    # Frequency ranges and their respective powers
    (1e6, 10e6, "5 dBm to 15 dBm, generally increasing as frequency increases"),
    (10e6, 2170e6, "5 dBm to 15 dBm, generally decreasing as frequency increases"),
    # ... and so on for all bands
]

class HackRFConfigurator(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        # Frequency selector
        self.frequency_selector = self.create_config_dropdown("Frequency Range:", [f[0] for f in FREQUENCY_RANGES], layout)
        self.frequency_selector.currentIndexChanged.connect(self.update_power_info)

        # Center frequency slider
        self.center_freq_slider = QSlider(Qt.Horizontal)
        self.center_freq_label = QLabel("Center Frequency: ")
        layout.addWidget(self.center_freq_label)
        layout.addWidget(self.center_freq_slider)
        self.center_freq_slider.valueChanged.connect(self.update_center_freq_label)

        # TX Power Information
        self.tx_power_label = QLabel("TX Power: N/A")
        layout.addWidget(self.tx_power_label)

        # Save button
        save_button = QPushButton("Save Configurations")
        save_button.clicked.connect(self.save_configurations)
        layout.addWidget(save_button)

        self.setLayout(layout)
        self.show()

    def create_config_dropdown(self, label_text, options, layout):
        label = QLabel(label_text)
        combobox = QComboBox(self)
        combobox.addItems(options)
        layout.addWidget(label)
        layout.addWidget(combobox)
        return combobox

    def update_power_info(self, index):
        _, low, high = FREQUENCY_RANGES[index]
        self.center_freq_slider.setMinimum(low)
        self.center_freq_slider.setMaximum(high)
        self.update_center_freq_label()

        # TX Power update based on chosen range
        for start, end, power in TX_POWER:
            if low >= start and high <= end:
                self.tx_power_label.setText(f"TX Power for the chosen range: {power}")
                break

    def update_center_freq_label(self):
        self.center_freq_label.setText(f"Center Frequency: {self.center_freq_slider.value()/1e6} MHz")

    def save_configurations(self):
        filename, _ = QFileDialog.getSaveFileName(self, "Save Configurations", "", "CSV Files (*.csv)")
        if filename:
            with open(filename, "w") as f:
                f.write(f"Selected Frequency Range,{self.frequency_selector.currentText()}\n")
                f.write(f"Center Frequency,{self.center_freq_slider.value()}\n")
                f.write(f"TX Power,{self.tx_power_label.text()}\n")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = HackRFConfigurator()
    sys.exit(app.exec_())

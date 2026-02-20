import sys
import os
from dataclasses import dataclass
from enum import Enum

# Add parent Application directory to path so Icons_rc can be imported
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PySide6 import QtCore as qtc
from PySide6 import QtWidgets as qtw
from PySide6 import QtGui as qtg

from Main.UI.main_window_ui import Ui_mw_Main

# The parameters used to generate a recommendation
@dataclass
class PreRecommendationJumpSettings:
    weight: int
    height: float # in feet
    harness: str
    desired_water_height: float
    planned_horizontal_distance: float

class MainWindow(qtw.QMainWindow, Ui_mw_Main):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.show()

        self.pb_request_recommendation.clicked.connect(self.request_recommendation)

        # Height and weight buttons

        # Horizontal sliders
        self.hs_desired_water_height.valueChanged.connect(self.on_hs_desired_water_height_changed)
        self.on_hs_desired_water_height_changed(self.hs_desired_water_height.value())
        self.hs_planned_horizontal_distance.valueChanged.connect(self.on_hs_planned_horizontal_distance_changed)
        self.on_hs_planned_horizontal_distance_changed(self.hs_planned_horizontal_distance.value())

    # Height and weight push buttons


    # Horizontal sliders
    def on_hs_desired_water_height_changed(self, value):
        self.lb_desired_water_height_value.setText(str(value))
    def on_hs_planned_horizontal_distance_changed(self, value):
        self.lb_planned_horizontal_distance_value.setText(str(value))

    def request_recommendation(self):
        harness = "AF"
        if self.rb_ancle_backward.isChecked():
            harness = "AB"
        elif self.rb_body_backward.isChecked():
            harness = "BB"
        elif self.rb_body_forward.isChecked():
            harness = "BF"

        selected_pre_recommendation_settings = PreRecommendationJumpSettings(
            weight = int(self.le_weight.text()),
            height = parse_height(self.le_height.text()),
            harness = harness,
            desired_water_height = float(self.lb_desired_water_height_value.text()),
            planned_horizontal_distance = float(self.lb_planned_horizontal_distance_value.text())
        )
        print("Requesting a recommendation for jump parameters: " + str(selected_pre_recommendation_settings))

def parse_height(height_str: str) -> float:
    """Parse height string like "6' 2\"" into total feet as float."""
    parts = height_str.replace('"', '').split("'")
    feet = int(parts[0])
    inches = int(parts[1].strip()) if len(parts) > 1 and parts[1].strip() else 0
    return feet + inches / 12

if __name__ == "__main__":
    app = qtw.QApplication(sys.argv)
    window= MainWindow()
    sys.exit(app.exec())
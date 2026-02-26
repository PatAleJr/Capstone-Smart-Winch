import sys
import os

# Add parent Application directory to path so Icons_rc can be imported
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PySide6 import QtCore as qtc
from PySide6 import QtWidgets as qtw
from PySide6 import QtGui as qtg

import PySide6.QtAsyncio as QtAsyncio
import asyncio

from Main.UI.main_window_ui import Ui_mw_Main

import ArduinoInterface
import CordRecords
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib
matplotlib.use('QtAgg')

class MainWindow(qtw.QMainWindow, Ui_mw_Main):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.show()

        # Predicted trajectory figure setup
        self.predicted_trajectory_figure = Figure(figsize=(5, 4), dpi=100)
        canvas = FigureCanvas(self.predicted_trajectory_figure)
        self.layout_predicted_trajectory.addWidget(canvas)

        # Jump recommendation button
        self.pb_request_recommendation.clicked.connect(self.request_recommendation)

        # Height and weight buttons
        self.pb_use_weight.clicked.connect(self.on_pb_use_weight_clicked)
        self.pb_use_height.clicked.connect(self.on_pb_use_height_clicked)

        # Horizontal sliders
        self.hs_desired_water_height.valueChanged.connect(self.on_hs_desired_water_height_changed)
        self.on_hs_desired_water_height_changed(self.hs_desired_water_height.value())
        self.hs_planned_horizontal_distance.valueChanged.connect(self.on_hs_planned_horizontal_distance_changed)
        self.on_hs_planned_horizontal_distance_changed(self.hs_planned_horizontal_distance.value())

        # Cords
        self.current_cords_dict = CordRecords.get_currently_used_cords()
        for color, cord in self.current_cords_dict.items():
            if cord is None: continue
            for row in range(self.tb_cords.rowCount()):
                if self.tb_cords.verticalHeaderItem(row).text() != color: continue
                self.tb_cords.setItem(row, 0, qtw.QTableWidgetItem(str(cord.serial_number)))
                self.tb_cords.setItem(row, 1, qtw.QTableWidgetItem(str(cord.number_of_jumps)))
                self.tb_cords.setItem(row, 2, qtw.QTableWidgetItem("To be implemented"))
                self.tb_cords.setItem(row, 3, qtw.QTableWidgetItem("To be implemented"))
                break

        # Anchor offset
        self.pb_set_custom_anchor_offset.clicked.connect(self.setCustomAnchorOffset)
        self.pb_set_recommended_anchor_offset.clicked.connect(self.setRecommendedAnchorOffset)

        # Arduino interface
        self.arduino_interface = ArduinoInterface.ArduinoInterface(port='COM3')  # Update with your port
        # launch the periodic reader as a background asyncio task.  QtAsyncio.run
        # conveniently returns the created Task object so we can cancel it later.
        try:
            self._arduino_loop_task = QtAsyncio.run(self.initialize_periodic_update_of_arduino_readings(3))
        except Exception:
            # some versions of QtAsyncio may not return a task; fall back to None
            self._arduino_loop_task = None

    # Height and weight push buttons
    def on_pb_use_weight_clicked(self):
        self.le_weight.setText(self.lb_weight_value.text())
    def on_pb_use_height_clicked(self):
        self.le_height.setText(self.lb_height_value.text())

    # Horizontal sliders
    def on_hs_desired_water_height_changed(self, value):
        self.lb_desired_water_height_value.setText(str(value))
    def on_hs_planned_horizontal_distance_changed(self, value):
        self.lb_planned_horizontal_distance_value.setText(str(value))

    def get_current_inputs(self):
        problems = []
        harness = None
        if self.rb_ancle_forward.isChecked(): harness = "AF"
        elif self.rb_ancle_backward.isChecked(): harness = "AB"
        elif self.rb_body_backward.isChecked(): harness = "BB"
        elif self.rb_body_forward.isChecked(): harness = "BF"
        else: problems.append("Harness type not selected")

        try: weight = int(self.le_weight.text())
        except ValueError: problems.append("Enter weight as a number")

        try: height = parse_height(self.le_height.text())
        except (ValueError, IndexError): problems.append("Enter height in format like 6' 2\"")

        if problems:
            msg = qtw.QMessageBox(self)
            msg.setWindowTitle("Missing or Invalid Inputs")
            msg.setText("Missing or invalid inputs:\n\n" + "\n".join(problems))
            font = qtg.QFont()
            font.setPointSize(12)  # adjusted to reasonable size
            msg.setFont(font)
            msg.exec()
        else:
            return CordRecords.PreRecommendationJumpSettings(
                weight = weight,
                height = height,
                harness = harness,
                desired_water_height = float(self.lb_desired_water_height_value.text()),
                planned_horizontal_distance = float(self.lb_planned_horizontal_distance_value.text())
            )

    def request_recommendation(self):
        selected_pre_recommendation_settings = self.get_current_inputs()
        if selected_pre_recommendation_settings is None: return
        # Come up with a recommendation
        print("Requesting a recommendation for jump parameters: " + str(selected_pre_recommendation_settings))
        for color, cord in self.current_cords_dict.items():
            if cord is None: continue
            recommended_anchor_offset = cord.get_recommended_anchor_offset(selected_pre_recommendation_settings)
            if 6 < recommended_anchor_offset < 36:
                # Update the UI with the recommendation
                print(f"Recommended anchor offset for cord {cord.serial_number} ({color}): {height_to_inches_and_feet(recommended_anchor_offset)}")
                self.lb_recommended_anchor_offset_value.setText(height_to_inches_and_feet(recommended_anchor_offset))
                self.lb_recommended_cord.setText(f"Use cord: {cord.serial_number} ({color})")

                dummy_jump = CordRecords.JumpDataPoint(
                    mass=selected_pre_recommendation_settings.weight / 32.174,  # convert weight in lbs to mass in slugs
                    anchor_offset=recommended_anchor_offset,
                    measured_water_height=selected_pre_recommendation_settings.desired_water_height,
                    harness_type=selected_pre_recommendation_settings.harness,
                    horizontal_distance=selected_pre_recommendation_settings.planned_horizontal_distance,
                    break_occurred=0,
                    num_uses=cord.number_of_jumps,
                    date = "N/A")

                # Plot the jump
                self.predicted_trajectory_figure.clear()
                cord.simulate_and_plot_jump(dummy_jump, figure=self.predicted_trajectory_figure)

                # Update similar jumps table
                similar_jumps = cord.get_similar_jumps(dummy_jump, 3)
                for jump_index, jump in enumerate(similar_jumps):
                    print("Harness type: " + jump.harness_type)
                    self.tb_similar_jumps.setItem(jump_index, 0, qtw.QTableWidgetItem(jump.date))
                    self.tb_similar_jumps.setItem(jump_index, 1, qtw.QTableWidgetItem(str(jump.mass * 32.174)))  # convert mass in slugs back to weight in lbs for display
                    self.tb_similar_jumps.setItem(jump_index, 2, qtw.QTableWidgetItem(str(jump.anchor_offset)))
                    self.tb_similar_jumps.setItem(jump_index, 3, qtw.QTableWidgetItem(str(jump.horizontal_distance)))
                    self.tb_similar_jumps.setItem(jump_index, 4, qtw.QTableWidgetItem(str(jump.measured_water_height)))
                    self.tb_similar_jumps.setItem(jump_index, 5, qtw.QTableWidgetItem(str(jump.harness_type)))
                return

        print("No cords could provide a safe anchor offset")

    def setCustomAnchorOffset(self):
        try: desired_anchor_offset = parse_height(self.le_custom_anchor_offset.text())
        except: 
            msg = self.createMessageBox("Invalid Anchor Offset", "Enter desired anchor offset in format like 6' 2\"")
            msg.exec()
            return
        msg = self.createMessageBox("Custom Anchor Offset Set", f"Anchor offset set to custom value of {self.le_custom_anchor_offset_value.text()}")
        msg.setStandardButtons(qtw.QMessageBox.Ok | qtw.QMessageBox.Cancel)
        result = msg.exec()
        if result == qtw.QMessageBox.Ok:
            self.lb_current_anchor_offset_value.setText(height_to_inches_and_feet(desired_anchor_offset))

    def setRecommendedAnchorOffset(self):
        msg = self.createMessageBox("Recommended Anchor Offset Set", f"Anchor offset set to recommended value of {self.lb_recommended_anchor_offset_value.text()}")
        msg.setStandardButtons(qtw.QMessageBox.Ok | qtw.QMessageBox.Cancel)
        result = msg.exec()
        if result == qtw.QMessageBox.Ok:
            self.lb_current_anchor_offset_value.setText(self.lb_recommended_anchor_offset_value.text())

    def createMessageBox(self, title: str, text: str) -> qtw.QMessageBox:
        msg = qtw.QMessageBox(self)
        msg.setWindowTitle(title)
        msg.setText(text)
        font = qtg.QFont()
        font.setPointSize(12)
        msg.setFont(font)
        return msg

    def cleanup(self):
        """Cancel outstanding asyncio work and close the serial port."""
        # cancel the periodic update task if it exists
        task = getattr(self, '_arduino_loop_task', None)
        if task is not None:
            try:
                task.cancel()
            except Exception:
                pass
        self.arduino_interface.close()

    def closeEvent(self, event):
        # make sure we tidy up when the window is closed directly
        self.cleanup()
        super().closeEvent(event)

    async def initialize_periodic_update_of_arduino_readings(self, period_seconds = 1):
        while True:
            await self.arduino_interface.open()
            h = await self.arduino_interface.read_humidity()
            print("Humidity from Arduino: " + str(h))
            self.arduino_interface.close()

            self.lb_humidity_value.setText(f"{h:.1f}%")

            await asyncio.sleep(period_seconds)

def height_to_inches_and_feet(height: float) -> str:
    """Convert height in feet as float to a string like "6' 2\"". Rounds inches to nearest whole number."""
    feet = int(height)
    inches = round((height - feet) * 12)
    return f"{feet}' {inches}\""

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
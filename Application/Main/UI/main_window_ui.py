# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_window.ui'
##
## Created by: Qt User Interface Compiler version 6.10.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QGridLayout, QGroupBox,
    QHBoxLayout, QHeaderView, QLabel, QLineEdit,
    QMainWindow, QMenu, QMenuBar, QPushButton,
    QRadioButton, QSizePolicy, QSlider, QSpacerItem,
    QStatusBar, QTableWidget, QTableWidgetItem, QVBoxLayout,
    QWidget)
import Icons_rc

class Ui_mw_Main(object):
    def setupUi(self, mw_Main):
        if not mw_Main.objectName():
            mw_Main.setObjectName(u"mw_Main")
        mw_Main.resize(1297, 867)
        font = QFont()
        font.setPointSize(12)
        mw_Main.setFont(font)
        icon = QIcon()
        icon.addFile(u":/Main/MainIcon.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        mw_Main.setWindowIcon(icon)
        self.action_Quit = QAction(mw_Main)
        self.action_Quit.setObjectName(u"action_Quit")
        icon1 = QIcon()
        icon1.addFile(u":/Buttons/Cross.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.action_Quit.setIcon(icon1)
        self.action_Quit.setFont(font)
        self.actionAdd_Person = QAction(mw_Main)
        self.actionAdd_Person.setObjectName(u"actionAdd_Person")
        self.actionAdd_Person.setFont(font)
        self.centralwidget = QWidget(mw_Main)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.gb_sensor_inputs = QGroupBox(self.centralwidget)
        self.gb_sensor_inputs.setObjectName(u"gb_sensor_inputs")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.gb_sensor_inputs.sizePolicy().hasHeightForWidth())
        self.gb_sensor_inputs.setSizePolicy(sizePolicy)
        font1 = QFont()
        font1.setPointSize(12)
        font1.setBold(True)
        self.gb_sensor_inputs.setFont(font1)
        self.gridLayout_3 = QGridLayout(self.gb_sensor_inputs)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.le_height = QLineEdit(self.gb_sensor_inputs)
        self.le_height.setObjectName(u"le_height")
        font2 = QFont()
        font2.setPointSize(12)
        font2.setBold(False)
        self.le_height.setFont(font2)

        self.gridLayout_3.addWidget(self.le_height, 3, 2, 1, 1)

        self.lb_temperature_value = QLabel(self.gb_sensor_inputs)
        self.lb_temperature_value.setObjectName(u"lb_temperature_value")
        self.lb_temperature_value.setFont(font2)
        self.lb_temperature_value.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_3.addWidget(self.lb_temperature_value, 4, 2, 1, 1)

        self.lb_weight = QLabel(self.gb_sensor_inputs)
        self.lb_weight.setObjectName(u"lb_weight")
        self.lb_weight.setFont(font1)

        self.gridLayout_3.addWidget(self.lb_weight, 0, 0, 1, 1)

        self.lb_weight_value = QLabel(self.gb_sensor_inputs)
        self.lb_weight_value.setObjectName(u"lb_weight_value")
        self.lb_weight_value.setFont(font2)

        self.gridLayout_3.addWidget(self.lb_weight_value, 1, 0, 1, 1)

        self.lb_height = QLabel(self.gb_sensor_inputs)
        self.lb_height.setObjectName(u"lb_height")

        self.gridLayout_3.addWidget(self.lb_height, 2, 0, 1, 3)

        self.pb_use_height = QPushButton(self.gb_sensor_inputs)
        self.pb_use_height.setObjectName(u"pb_use_height")

        self.gridLayout_3.addWidget(self.pb_use_height, 3, 1, 1, 1)

        self.lb_height_value = QLabel(self.gb_sensor_inputs)
        self.lb_height_value.setObjectName(u"lb_height_value")
        self.lb_height_value.setFont(font2)

        self.gridLayout_3.addWidget(self.lb_height_value, 3, 0, 1, 1)

        self.le_weight = QLineEdit(self.gb_sensor_inputs)
        self.le_weight.setObjectName(u"le_weight")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.le_weight.sizePolicy().hasHeightForWidth())
        self.le_weight.setSizePolicy(sizePolicy1)
        self.le_weight.setFont(font2)

        self.gridLayout_3.addWidget(self.le_weight, 1, 2, 1, 1)

        self.pb_use_weight = QPushButton(self.gb_sensor_inputs)
        self.pb_use_weight.setObjectName(u"pb_use_weight")

        self.gridLayout_3.addWidget(self.pb_use_weight, 1, 1, 1, 1)

        self.lb_temperature = QLabel(self.gb_sensor_inputs)
        self.lb_temperature.setObjectName(u"lb_temperature")

        self.gridLayout_3.addWidget(self.lb_temperature, 4, 0, 1, 2)

        self.lb_humidity = QLabel(self.gb_sensor_inputs)
        self.lb_humidity.setObjectName(u"lb_humidity")

        self.gridLayout_3.addWidget(self.lb_humidity, 5, 0, 1, 1)

        self.lb_humidity_value = QLabel(self.gb_sensor_inputs)
        self.lb_humidity_value.setObjectName(u"lb_humidity_value")
        self.lb_humidity_value.setFont(font2)
        self.lb_humidity_value.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_3.addWidget(self.lb_humidity_value, 5, 2, 1, 1)


        self.horizontalLayout_10.addWidget(self.gb_sensor_inputs)

        self.gb_jump_type = QGroupBox(self.centralwidget)
        self.gb_jump_type.setObjectName(u"gb_jump_type")
        sizePolicy.setHeightForWidth(self.gb_jump_type.sizePolicy().hasHeightForWidth())
        self.gb_jump_type.setSizePolicy(sizePolicy)
        self.gb_jump_type.setFont(font1)
        self.gridLayout_2 = QGridLayout(self.gb_jump_type)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.lb_desired_water_height_value = QLabel(self.gb_jump_type)
        self.lb_desired_water_height_value.setObjectName(u"lb_desired_water_height_value")
        self.lb_desired_water_height_value.setFont(font2)
        self.lb_desired_water_height_value.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_2.addWidget(self.lb_desired_water_height_value, 5, 1, 1, 1)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.gridLayout_2.addItem(self.verticalSpacer_2, 4, 0, 1, 1)

        self.lb_planned_horizontal_distance_value = QLabel(self.gb_jump_type)
        self.lb_planned_horizontal_distance_value.setObjectName(u"lb_planned_horizontal_distance_value")
        self.lb_planned_horizontal_distance_value.setFont(font2)
        self.lb_planned_horizontal_distance_value.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_2.addWidget(self.lb_planned_horizontal_distance_value, 11, 1, 1, 1)

        self.lb_desired_water_height = QLabel(self.gb_jump_type)
        self.lb_desired_water_height.setObjectName(u"lb_desired_water_height")

        self.gridLayout_2.addWidget(self.lb_desired_water_height, 5, 0, 1, 1)

        self.rb_body_forward = QRadioButton(self.gb_jump_type)
        self.rb_body_forward.setObjectName(u"rb_body_forward")
        self.rb_body_forward.setFont(font2)

        self.gridLayout_2.addWidget(self.rb_body_forward, 2, 0, 1, 1)

        self.hs_planned_horizontal_distance = QSlider(self.gb_jump_type)
        self.hs_planned_horizontal_distance.setObjectName(u"hs_planned_horizontal_distance")
        self.hs_planned_horizontal_distance.setMaximum(8)
        self.hs_planned_horizontal_distance.setPageStep(10)
        self.hs_planned_horizontal_distance.setOrientation(Qt.Orientation.Horizontal)
        self.hs_planned_horizontal_distance.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.hs_planned_horizontal_distance.setTickInterval(1)

        self.gridLayout_2.addWidget(self.hs_planned_horizontal_distance, 13, 0, 1, 2)

        self.hs_desired_water_height = QSlider(self.gb_jump_type)
        self.hs_desired_water_height.setObjectName(u"hs_desired_water_height")
        self.hs_desired_water_height.setMinimum(-3)
        self.hs_desired_water_height.setMaximum(10)
        self.hs_desired_water_height.setOrientation(Qt.Orientation.Horizontal)
        self.hs_desired_water_height.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.hs_desired_water_height.setTickInterval(1)

        self.gridLayout_2.addWidget(self.hs_desired_water_height, 9, 0, 1, 2)

        self.rb_ancle_forward = QRadioButton(self.gb_jump_type)
        self.rb_ancle_forward.setObjectName(u"rb_ancle_forward")
        self.rb_ancle_forward.setFont(font2)

        self.gridLayout_2.addWidget(self.rb_ancle_forward, 0, 0, 1, 1)

        self.rb_body_backward = QRadioButton(self.gb_jump_type)
        self.rb_body_backward.setObjectName(u"rb_body_backward")
        self.rb_body_backward.setFont(font2)

        self.gridLayout_2.addWidget(self.rb_body_backward, 3, 0, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.gridLayout_2.addItem(self.verticalSpacer, 10, 0, 1, 1)

        self.lb_planned_horizontal_distance = QLabel(self.gb_jump_type)
        self.lb_planned_horizontal_distance.setObjectName(u"lb_planned_horizontal_distance")

        self.gridLayout_2.addWidget(self.lb_planned_horizontal_distance, 11, 0, 1, 1)

        self.rb_ancle_backward = QRadioButton(self.gb_jump_type)
        self.rb_ancle_backward.setObjectName(u"rb_ancle_backward")
        self.rb_ancle_backward.setFont(font2)

        self.gridLayout_2.addWidget(self.rb_ancle_backward, 1, 0, 1, 1)


        self.horizontalLayout_10.addWidget(self.gb_jump_type)

        self.gb_cords = QGroupBox(self.centralwidget)
        self.gb_cords.setObjectName(u"gb_cords")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.gb_cords.sizePolicy().hasHeightForWidth())
        self.gb_cords.setSizePolicy(sizePolicy2)
        self.gb_cords.setFont(font1)
        self.gridLayout_4 = QGridLayout(self.gb_cords)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.tb_cords = QTableWidget(self.gb_cords)
        if (self.tb_cords.columnCount() < 4):
            self.tb_cords.setColumnCount(4)
        __qtablewidgetitem = QTableWidgetItem()
        self.tb_cords.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.tb_cords.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.tb_cords.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.tb_cords.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        if (self.tb_cords.rowCount() < 5):
            self.tb_cords.setRowCount(5)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.tb_cords.setVerticalHeaderItem(0, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.tb_cords.setVerticalHeaderItem(1, __qtablewidgetitem5)
        __qtablewidgetitem6 = QTableWidgetItem()
        self.tb_cords.setVerticalHeaderItem(2, __qtablewidgetitem6)
        __qtablewidgetitem7 = QTableWidgetItem()
        self.tb_cords.setVerticalHeaderItem(3, __qtablewidgetitem7)
        __qtablewidgetitem8 = QTableWidgetItem()
        self.tb_cords.setVerticalHeaderItem(4, __qtablewidgetitem8)
        self.tb_cords.setObjectName(u"tb_cords")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.tb_cords.sizePolicy().hasHeightForWidth())
        self.tb_cords.setSizePolicy(sizePolicy3)
        font3 = QFont()
        font3.setPointSize(12)
        font3.setBold(False)
        font3.setKerning(True)
        self.tb_cords.setFont(font3)
        self.tb_cords.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.tb_cords.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.tb_cords.setRowCount(5)
        self.tb_cords.setColumnCount(4)
        self.tb_cords.horizontalHeader().setVisible(True)
        self.tb_cords.horizontalHeader().setCascadingSectionResizes(False)
        self.tb_cords.horizontalHeader().setMinimumSectionSize(50)
        self.tb_cords.horizontalHeader().setDefaultSectionSize(130)
        self.tb_cords.horizontalHeader().setStretchLastSection(False)
        self.tb_cords.verticalHeader().setCascadingSectionResizes(False)

        self.gridLayout_4.addWidget(self.tb_cords, 5, 0, 1, 1)

        self.pb_update_cords = QPushButton(self.gb_cords)
        self.pb_update_cords.setObjectName(u"pb_update_cords")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.pb_update_cords.sizePolicy().hasHeightForWidth())
        self.pb_update_cords.setSizePolicy(sizePolicy4)
        self.pb_update_cords.setFont(font2)

        self.gridLayout_4.addWidget(self.pb_update_cords, 6, 0, 1, 2)


        self.horizontalLayout_10.addWidget(self.gb_cords)


        self.verticalLayout.addLayout(self.horizontalLayout_10)

        self.hl_bottom = QHBoxLayout()
        self.hl_bottom.setObjectName(u"hl_bottom")
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.gb_cord_recommendations = QGroupBox(self.centralwidget)
        self.gb_cord_recommendations.setObjectName(u"gb_cord_recommendations")
        self.gb_cord_recommendations.setMinimumSize(QSize(300, 0))
        self.gb_cord_recommendations.setFont(font1)
        self.gridLayout_5 = QGridLayout(self.gb_cord_recommendations)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.lb_recommended_cord_color = QLabel(self.gb_cord_recommendations)
        self.lb_recommended_cord_color.setObjectName(u"lb_recommended_cord_color")
        sizePolicy5 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.lb_recommended_cord_color.sizePolicy().hasHeightForWidth())
        self.lb_recommended_cord_color.setSizePolicy(sizePolicy5)
        self.lb_recommended_cord_color.setFont(font2)

        self.gridLayout_5.addWidget(self.lb_recommended_cord_color, 1, 0, 1, 1)

        self.lb_suggested_anchor_offset = QLabel(self.gb_cord_recommendations)
        self.lb_suggested_anchor_offset.setObjectName(u"lb_suggested_anchor_offset")
        sizePolicy5.setHeightForWidth(self.lb_suggested_anchor_offset.sizePolicy().hasHeightForWidth())
        self.lb_suggested_anchor_offset.setSizePolicy(sizePolicy5)
        self.lb_suggested_anchor_offset.setFont(font2)

        self.gridLayout_5.addWidget(self.lb_suggested_anchor_offset, 1, 1, 1, 1)

        self.pb_request_recommendation = QPushButton(self.gb_cord_recommendations)
        self.pb_request_recommendation.setObjectName(u"pb_request_recommendation")
        self.pb_request_recommendation.setMinimumSize(QSize(0, 50))
        self.pb_request_recommendation.setFont(font2)

        self.gridLayout_5.addWidget(self.pb_request_recommendation, 0, 0, 1, 2)


        self.verticalLayout_3.addWidget(self.gb_cord_recommendations)

        self.gb_anchor_offset = QGroupBox(self.centralwidget)
        self.gb_anchor_offset.setObjectName(u"gb_anchor_offset")
        self.gb_anchor_offset.setFont(font1)
        self.gridLayout_7 = QGridLayout(self.gb_anchor_offset)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.lb_current_anchor_offset = QLabel(self.gb_anchor_offset)
        self.lb_current_anchor_offset.setObjectName(u"lb_current_anchor_offset")
        font4 = QFont()
        font4.setPointSize(14)
        font4.setBold(True)
        self.lb_current_anchor_offset.setFont(font4)

        self.gridLayout_7.addWidget(self.lb_current_anchor_offset, 3, 0, 1, 1)

        self.pb_recalibrate_anchor_offset = QPushButton(self.gb_anchor_offset)
        self.pb_recalibrate_anchor_offset.setObjectName(u"pb_recalibrate_anchor_offset")
        self.pb_recalibrate_anchor_offset.setMinimumSize(QSize(0, 50))

        self.gridLayout_7.addWidget(self.pb_recalibrate_anchor_offset, 4, 0, 1, 2)

        self.le_custom_anchor_offset = QLineEdit(self.gb_anchor_offset)
        self.le_custom_anchor_offset.setObjectName(u"le_custom_anchor_offset")
        self.le_custom_anchor_offset.setMinimumSize(QSize(0, 50))

        self.gridLayout_7.addWidget(self.le_custom_anchor_offset, 0, 1, 1, 1)

        self.lb_current_anchor_offset_value = QLabel(self.gb_anchor_offset)
        self.lb_current_anchor_offset_value.setObjectName(u"lb_current_anchor_offset_value")
        self.lb_current_anchor_offset_value.setFont(font4)

        self.gridLayout_7.addWidget(self.lb_current_anchor_offset_value, 3, 1, 1, 1)

        self.pb_set_recommended_anchor_offset = QPushButton(self.gb_anchor_offset)
        self.pb_set_recommended_anchor_offset.setObjectName(u"pb_set_recommended_anchor_offset")
        self.pb_set_recommended_anchor_offset.setMinimumSize(QSize(0, 50))
        self.pb_set_recommended_anchor_offset.setFont(font2)

        self.gridLayout_7.addWidget(self.pb_set_recommended_anchor_offset, 2, 0, 1, 1)

        self.pb_set_custom_anchor_offset = QPushButton(self.gb_anchor_offset)
        self.pb_set_custom_anchor_offset.setObjectName(u"pb_set_custom_anchor_offset")
        self.pb_set_custom_anchor_offset.setMinimumSize(QSize(0, 50))
        self.pb_set_custom_anchor_offset.setFont(font2)

        self.gridLayout_7.addWidget(self.pb_set_custom_anchor_offset, 0, 0, 1, 1)


        self.verticalLayout_3.addWidget(self.gb_anchor_offset)

        self.pb_jump = QPushButton(self.centralwidget)
        self.pb_jump.setObjectName(u"pb_jump")
        sizePolicy6 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        sizePolicy6.setHorizontalStretch(0)
        sizePolicy6.setVerticalStretch(0)
        sizePolicy6.setHeightForWidth(self.pb_jump.sizePolicy().hasHeightForWidth())
        self.pb_jump.setSizePolicy(sizePolicy6)
        self.pb_jump.setMinimumSize(QSize(0, 50))
        self.pb_jump.setFont(font1)

        self.verticalLayout_3.addWidget(self.pb_jump)


        self.hl_bottom.addLayout(self.verticalLayout_3)

        self.gb_predicted_trajectory = QGroupBox(self.centralwidget)
        self.gb_predicted_trajectory.setObjectName(u"gb_predicted_trajectory")
        sizePolicy2.setHeightForWidth(self.gb_predicted_trajectory.sizePolicy().hasHeightForWidth())
        self.gb_predicted_trajectory.setSizePolicy(sizePolicy2)
        self.gb_predicted_trajectory.setMinimumSize(QSize(300, 0))
        self.gb_predicted_trajectory.setFont(font1)
        self.gridLayout = QGridLayout(self.gb_predicted_trajectory)
        self.gridLayout.setObjectName(u"gridLayout")
        self.w_jump_plot = QWidget(self.gb_predicted_trajectory)
        self.w_jump_plot.setObjectName(u"w_jump_plot")
        sizePolicy7 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        sizePolicy7.setHorizontalStretch(0)
        sizePolicy7.setVerticalStretch(0)
        sizePolicy7.setHeightForWidth(self.w_jump_plot.sizePolicy().hasHeightForWidth())
        self.w_jump_plot.setSizePolicy(sizePolicy7)

        self.gridLayout.addWidget(self.w_jump_plot, 0, 0, 1, 1)


        self.hl_bottom.addWidget(self.gb_predicted_trajectory)

        self.gb_similar_jumps = QGroupBox(self.centralwidget)
        self.gb_similar_jumps.setObjectName(u"gb_similar_jumps")
        self.gb_similar_jumps.setFont(font1)
        self.gridLayout_6 = QGridLayout(self.gb_similar_jumps)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.tb_similar_jumps = QTableWidget(self.gb_similar_jumps)
        if (self.tb_similar_jumps.columnCount() < 4):
            self.tb_similar_jumps.setColumnCount(4)
        __qtablewidgetitem9 = QTableWidgetItem()
        self.tb_similar_jumps.setHorizontalHeaderItem(0, __qtablewidgetitem9)
        __qtablewidgetitem10 = QTableWidgetItem()
        self.tb_similar_jumps.setHorizontalHeaderItem(1, __qtablewidgetitem10)
        __qtablewidgetitem11 = QTableWidgetItem()
        self.tb_similar_jumps.setHorizontalHeaderItem(2, __qtablewidgetitem11)
        __qtablewidgetitem12 = QTableWidgetItem()
        self.tb_similar_jumps.setHorizontalHeaderItem(3, __qtablewidgetitem12)
        self.tb_similar_jumps.setObjectName(u"tb_similar_jumps")
        self.tb_similar_jumps.setFont(font2)
        self.tb_similar_jumps.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.tb_similar_jumps.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
        self.tb_similar_jumps.horizontalHeader().setDefaultSectionSize(110)

        self.gridLayout_6.addWidget(self.tb_similar_jumps, 0, 1, 1, 1)


        self.hl_bottom.addWidget(self.gb_similar_jumps)


        self.verticalLayout.addLayout(self.hl_bottom)

        mw_Main.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(mw_Main)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1297, 33))
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        self.menuPerson = QMenu(self.menubar)
        self.menuPerson.setObjectName(u"menuPerson")
        mw_Main.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(mw_Main)
        self.statusbar.setObjectName(u"statusbar")
        mw_Main.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuPerson.menuAction())
        self.menuFile.addAction(self.action_Quit)
        self.menuPerson.addAction(self.actionAdd_Person)

        self.retranslateUi(mw_Main)

        QMetaObject.connectSlotsByName(mw_Main)
    # setupUi

    def retranslateUi(self, mw_Main):
        mw_Main.setWindowTitle(QCoreApplication.translate("mw_Main", u"Sample Application", None))
        self.action_Quit.setText(QCoreApplication.translate("mw_Main", u"Quit", None))
        self.actionAdd_Person.setText(QCoreApplication.translate("mw_Main", u"Add Person", None))
        self.gb_sensor_inputs.setTitle(QCoreApplication.translate("mw_Main", u"Sensor Inputs", None))
        self.lb_temperature_value.setText(QCoreApplication.translate("mw_Main", u"22C", None))
        self.lb_weight.setText(QCoreApplication.translate("mw_Main", u"Weight (lb)", None))
        self.lb_weight_value.setText(QCoreApplication.translate("mw_Main", u"150", None))
        self.lb_height.setText(QCoreApplication.translate("mw_Main", u"Height (ft' in\")", None))
        self.pb_use_height.setText(QCoreApplication.translate("mw_Main", u">", None))
        self.lb_height_value.setText(QCoreApplication.translate("mw_Main", u"5'6\"", None))
        self.pb_use_weight.setText(QCoreApplication.translate("mw_Main", u">", None))
        self.lb_temperature.setText(QCoreApplication.translate("mw_Main", u"Temperature", None))
        self.lb_humidity.setText(QCoreApplication.translate("mw_Main", u"Humidity", None))
        self.lb_humidity_value.setText(QCoreApplication.translate("mw_Main", u"45%", None))
        self.gb_jump_type.setTitle(QCoreApplication.translate("mw_Main", u"Jump Type", None))
        self.lb_desired_water_height_value.setText(QCoreApplication.translate("mw_Main", u"0'", None))
        self.lb_planned_horizontal_distance_value.setText(QCoreApplication.translate("mw_Main", u"0'", None))
        self.lb_desired_water_height.setText(QCoreApplication.translate("mw_Main", u"Desired Water Height:", None))
        self.rb_body_forward.setText(QCoreApplication.translate("mw_Main", u"Body Forward", None))
        self.rb_ancle_forward.setText(QCoreApplication.translate("mw_Main", u"Ancle Forward", None))
        self.rb_body_backward.setText(QCoreApplication.translate("mw_Main", u"Body Backward", None))
        self.lb_planned_horizontal_distance.setText(QCoreApplication.translate("mw_Main", u"Planned Horizontal Distance:", None))
        self.rb_ancle_backward.setText(QCoreApplication.translate("mw_Main", u"Ancle Backward", None))
        self.gb_cords.setTitle(QCoreApplication.translate("mw_Main", u"Cords", None))
        ___qtablewidgetitem = self.tb_cords.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("mw_Main", u"Serial #", None));
        ___qtablewidgetitem1 = self.tb_cords.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("mw_Main", u"Total # jumps", None));
        ___qtablewidgetitem2 = self.tb_cords.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("mw_Main", u"Last time used", None));
        ___qtablewidgetitem3 = self.tb_cords.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("mw_Main", u"# Breaks", None));
        ___qtablewidgetitem4 = self.tb_cords.verticalHeaderItem(0)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("mw_Main", u"Yellow", None));
        ___qtablewidgetitem5 = self.tb_cords.verticalHeaderItem(1)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("mw_Main", u"Red", None));
        ___qtablewidgetitem6 = self.tb_cords.verticalHeaderItem(2)
        ___qtablewidgetitem6.setText(QCoreApplication.translate("mw_Main", u"Blue", None));
        ___qtablewidgetitem7 = self.tb_cords.verticalHeaderItem(3)
        ___qtablewidgetitem7.setText(QCoreApplication.translate("mw_Main", u"Purple", None));
        ___qtablewidgetitem8 = self.tb_cords.verticalHeaderItem(4)
        ___qtablewidgetitem8.setText(QCoreApplication.translate("mw_Main", u"Black", None));
        self.pb_update_cords.setText(QCoreApplication.translate("mw_Main", u"Update Cords", None))
        self.gb_cord_recommendations.setTitle(QCoreApplication.translate("mw_Main", u"Cord Recommendation", None))
        self.lb_recommended_cord_color.setText(QCoreApplication.translate("mw_Main", u"Cord Color: Red", None))
        self.lb_suggested_anchor_offset.setText(QCoreApplication.translate("mw_Main", u"Anchor Offset: 12' 5\"", None))
        self.pb_request_recommendation.setText(QCoreApplication.translate("mw_Main", u"Request Recommendation", None))
        self.gb_anchor_offset.setTitle(QCoreApplication.translate("mw_Main", u"Anchor Offset", None))
        self.lb_current_anchor_offset.setText(QCoreApplication.translate("mw_Main", u"Current Value:", None))
        self.pb_recalibrate_anchor_offset.setText(QCoreApplication.translate("mw_Main", u"Recalibrate", None))
        self.lb_current_anchor_offset_value.setText(QCoreApplication.translate("mw_Main", u"12' 5\"", None))
        self.pb_set_recommended_anchor_offset.setText(QCoreApplication.translate("mw_Main", u"Set recommended", None))
        self.pb_set_custom_anchor_offset.setText(QCoreApplication.translate("mw_Main", u"Set custom:", None))
        self.pb_jump.setText(QCoreApplication.translate("mw_Main", u"Jump!", None))
        self.gb_predicted_trajectory.setTitle(QCoreApplication.translate("mw_Main", u"Predicted Trajectory", None))
        self.gb_similar_jumps.setTitle(QCoreApplication.translate("mw_Main", u"Similar Jumps", None))
        ___qtablewidgetitem9 = self.tb_similar_jumps.horizontalHeaderItem(0)
        ___qtablewidgetitem9.setText(QCoreApplication.translate("mw_Main", u"Serial #", None));
        ___qtablewidgetitem10 = self.tb_similar_jumps.horizontalHeaderItem(1)
        ___qtablewidgetitem10.setText(QCoreApplication.translate("mw_Main", u"Time", None));
        ___qtablewidgetitem11 = self.tb_similar_jumps.horizontalHeaderItem(2)
        ___qtablewidgetitem11.setText(QCoreApplication.translate("mw_Main", u"Anchor Offset", None));
        ___qtablewidgetitem12 = self.tb_similar_jumps.horizontalHeaderItem(3)
        ___qtablewidgetitem12.setText(QCoreApplication.translate("mw_Main", u"Water Height", None));
        self.menuFile.setTitle(QCoreApplication.translate("mw_Main", u"File", None))
        self.menuPerson.setTitle(QCoreApplication.translate("mw_Main", u"Person", None))
    # retranslateUi


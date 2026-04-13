import maya.cmds as cmds
try:
    from PySide2 import QtWidgets, QtCore
except ImportError:
    from PySide6 import QtWidgets, QtCore

class StairGenerator:
    def __init__(self):
        self.group_name = "stairs_grp"

    def create(self, count=10, width=3.0, height=1.0, offset=1.0, handrail=False):
        if cmds.objExists(self.group_name):
            cmds.delete(self.group_name)
        
        main_grp = cmds.group(em=True, name=self.group_name)
        
        for i in range(count):
            step = cmds.polyCube(w=width, h=height, d=1.0, name="step_#")[0]
            cmds.setAttr(step + ".ty", i * offset)
            cmds.setAttr(step + ".tz", i * 1.0)
            cmds.parent(step, main_grp)
            
            if handrail:
                rail = cmds.polyCylinder(r=0.1, h=2.0, name="rail_#")[0]
                cmds.setAttr(rail + ".tx", (width / 2.0) - 0.2)
                cmds.setAttr(rail + ".ty", (i * offset) + 1.0)
                cmds.setAttr(rail + ".tz", i * 1.0)
                cmds.parent(rail, main_grp)

# GUI 
class StairWindow(QtWidgets.QDialog):
    def __init__(self):
        super(StairWindow, self).__init__()
        
        self.setWindowTitle("Stair Generator")
        self.setMinimumWidth(300)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint) 
        
        self.generator = StairGenerator() 
        
        self.create_widgets()
        self.create_layout()
        self.create_connections()

    def create_widgets(self):
        self.count_slider = QtWidgets.QSpinBox()
        self.count_slider.setRange(1, 50)
        self.count_slider.setValue(10)
        
        self.width_slider = QtWidgets.QDoubleSpinBox()
        self.width_slider.setRange(0.1, 10.0)
        self.width_slider.setValue(3.0)
        
        self.handrail_check = QtWidgets.QCheckBox("Create Handrail")
        self.create_btn = QtWidgets.QPushButton("Generate Stairs")

    def create_layout(self):
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(QtWidgets.QLabel("Step Count:"))
        layout.addWidget(self.count_slider)
        layout.addWidget(QtWidgets.QLabel("Step Width:"))
        layout.addWidget(self.width_slider)
        layout.addWidget(self.handrail_check)
        layout.addWidget(self.create_btn)

    def create_connections(self):
        self.create_btn.clicked.connect(self.on_generate_clicked)

    def on_generate_clicked(self):
        count = self.count_slider.value()
        width = self.width_slider.value()
        rail = self.handrail_check.isChecked()
        self.generator.create(count=count, width=width, handrail=rail)


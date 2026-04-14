import maya.cmds as cmds
try:
    from PySide2 import QtWidgets, QtCore
except ImportError:
    from PySide6 import QtWidgets, QtCore


class StairGenerator:
    def __init__(self):
        self.group_name = "stairs_grp"


    def create(self, count=10, width=3.0, height=1.0, depth=1.2, offset=1.0, base_h=0.0, handrail=False):
        if cmds.objExists(self.group_name):
            cmds.delete(self.group_name)
       
        main_grp = cmds.group(em=True, name=self.group_name)
       
        for i in range(count):
            step = cmds.polyCube(w=width, h=height, d=depth, name="stairStep_#")[0]
            pos_y = (i * offset) + base_h + (height / 2.0)
            pos_z = i * depth
           
            cmds.setAttr(step + ".ty", pos_y)
            cmds.setAttr(step + ".tz", pos_z)
            cmds.parent(step, main_grp)
           
            if handrail:
                 #right side
                rail_r = cmds.polyCylinder(r=0.1, h=2.0, name="rail_r_#")[0]
                cmds.setAttr(rail_r + ".tx", (width / 2.0) - 0.2)  
                cmds.setAttr(rail_r + ".ty", pos_y + (height / 2.0) + 1.0)
                cmds.setAttr(rail_r + ".tz", pos_z)
                cmds.parent(rail_r, main_grp)


                #left side
                rail_l = cmds.polyCylinder(r=0.1, h=2.0, name="rail_l_#")[0]
                cmds.setAttr(rail_l + ".tx", -(width / 2.0) + 0.2)
                cmds.setAttr(rail_l + ".ty", pos_y + (height / 2.0) + 1.0)
                cmds.setAttr(rail_l + ".tz", pos_z)
                cmds.parent(rail_l, main_grp)


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
        self.count_spin = QtWidgets.QSpinBox()
        self.count_spin.setRange(1, 100); self.count_spin.setValue(10)
       
        self.width_spin = QtWidgets.QDoubleSpinBox()
        self.width_spin.setValue(4.0)
       
        self.depth_spin = QtWidgets.QDoubleSpinBox()
        self.depth_spin.setValue(1.2)
       
        self.offset_spin = QtWidgets.QDoubleSpinBox()
        self.offset_spin.setValue(0.8)
       
        self.base_h_spin = QtWidgets.QDoubleSpinBox()
        self.base_h_spin.setRange(-10, 50); self.base_h_spin.setValue(0.0)
       
        self.rail_check = QtWidgets.QCheckBox("Enable Handrails")
        self.gen_btn = QtWidgets.QPushButton("Generate Stairs")
        self.gen_btn.setMinimumHeight(40)


    def create_layout(self):
        layout = QtWidgets.QVBoxLayout(self)
       
        layout.addWidget(QtWidgets.QLabel("Step Count"))
        layout.addWidget(self.count_spin)
        layout.addWidget(QtWidgets.QLabel("Step Width"))
        layout.addWidget(self.width_spin)
        layout.addWidget(QtWidgets.QLabel("Step Depth"))
        layout.addWidget(self.depth_spin)
        layout.addWidget(QtWidgets.QLabel("Step Offset"))
        layout.addWidget(self.offset_spin)
        layout.addWidget(QtWidgets.QLabel("Base Height"))
        layout.addWidget(self.base_h_spin)
       
        layout.addSpacing(10)
        layout.addWidget(self.rail_check)
        layout.addWidget(self.gen_btn)


    def create_connections(self):
        self.gen_btn.clicked.connect(self.on_generate_clicked)


    def on_generate_clicked(self):
        count = self.count_spin.value()
        width = self.width_spin.value()
        depth = self.depth_spin.value()
        offset = self.offset_spin.value()
        base_h = self.base_h_spin.value()
        rail = self.rail_check.isChecked()


        self.generator.create(count=count, width=width, depth=depth, offset=offset, base_h=base_h, handrail=rail)


def show_window():
    global my_stair_win
    try:
        my_stair_win.close()
        my_stair_win.deleteLater()
    except:
        pass
       
    my_stair_win = StairWindow()
    my_stair_win.show()


show_window()
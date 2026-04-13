import maya.cmds as cmds

class StairGenerator:
    
    def __init__(self):
       
        self.group_name = "stairs_grp"

    def create(self, count=10, width=3.0, height=1.0, offset=1.0, handrail=False):

        if cmds.objExists(self.group_name):
            cmds.delete(self.group_name)
   
        main_grp = cmds.group(em=True, name=self.group_name)
        
        for i in range(count):
          
            step_name = "step_{0}".format(i)
            step = cmds.polyCube(w=width, h=height, d=1.0, name=step_name)[0]
 
            pos_y = i * offset
            pos_z = i * 1.0 
            
            cmds.setAttr(step + ".ty", pos_y)
            cmds.setAttr(step + ".tz", pos_z)

            cmds.parent(step, main_grp)
     
            if handrail:
                rail = cmds.polyCylinder(r=0.1, h=2.0, name="rail_{0}".format(i))[0]

                cmds.setAttr(rail + ".tx", (width / 2.0) - 0.2)
                cmds.setAttr(rail + ".ty", pos_y + 1.0)
                cmds.setAttr(rail + ".tz", pos_z)
                cmds.parent(rail, main_grp)
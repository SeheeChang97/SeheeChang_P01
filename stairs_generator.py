import maya.cmds as cmds

def create_stairs(count=10, width=3.0, height=1.0, offset=1.0, handrail=False):
  
    group_name = "stairs_grp"
    if cmds.objExists(group_name):
        cmds.delete(group_name)
    
    main_grp = cmds.group(em=True, name=group_name)
    
    for i in range(count):    
        step = cmds.polyCube(w=width, h=height, d=1.0, name="step_#")[0]
          
        pos_y = i * offset
        pos_z = i * 1.0 
        
        cmds.setAttr(step + ".ty", pos_y)
        cmds.setAttr(step + ".tz", pos_z)
        
        cmds.parent(step, main_grp)
        
create_stairs(count=12, width=4.0, handrail=True)
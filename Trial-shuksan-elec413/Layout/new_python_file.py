
# Enter your Python code here

# -*- coding: utf-8 -*-
"""
Created on Sat Sep 30 19:58:16 2023

@author: jsheri1
"""

def replace_cell(layout, top, ebeam_GC_Air_te1310_BB, ebeam_GC_Air_te1310):
    target_cell_inst = layout.cell_by_name(ebeam_GC_Air_te1310_BB)
    replacement_cell_inst = layout.cell_by_name(ebeam_GC_Air_te1310)
    
    for each_inst in top.each_inst():
        if each_inst.cell.name == target_cell:
            # If the current instance's cell name matches the target cell
            logger.info(f'Found {each_inst.cell.name}, replacing with {replacement_cell}')
            inst_trans = each_inst.trans
            if each_inst.is_regular_array():
                # If the instance is a regular array, replace it with a new array of the replacement cell
                top.replace(each_inst, pya.CellInstArray.new(replacement_cell_inst, inst_trans, each_inst.a, each_inst.b, each_inst.na, each_inst.nb))
            else:
                # If it's not an array, replace it with a single instance of the replacement cell
                top.replace(each_inst, pya.CellInstArray.new(replacement_cell_inst, inst_trans))
        else:
            if each_inst.cell.child_cells() > 0:
                # If the current instance has child cells, recursively call the function on them
                replace_cell(layout, each_inst.cell, target_cell, replacement_cell)

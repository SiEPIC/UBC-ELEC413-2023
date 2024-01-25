from pya import *
from SiEPIC.utils import get_technology_by_name

def design_ZZZ(cell, cell_y, inst_wg1, inst_wg2, inst_wg3, waveguide_type):
    
    # load functions
    from SiEPIC.scripts import connect_pins_with_waveguide, connect_cell
    ly = cell.layout()
    library = ly.technology().name

    # Create a physical text label so we can see under the microscope
    # How do we find out the PCell parameter variables?
    '''
    c = ly.create_cell('TEXT','Basic')
    [p.name for p in c.pcell_declaration().get_parameters() if c.is_pcell_variant]
    c.delete()
    '''
    # returns: ['text', 'font_name', 'layer', 'mag', 'inverse', 'bias', 'cspacing', 'lspacing', 'eff_cw', 'eff_ch', 'eff_lw', 'eff_dr', 'font']
    TECHNOLOGY = get_technology_by_name(library)
    cell_text = ly.create_cell('TEXT', "Basic", {
        'text':cell.name,
        'layer': TECHNOLOGY['M1'],
        'mag': 30,
         })
    if not cell_text:
        raise Exception ('Cannot load text label cell; please check the script carefully.')
    cell.insert(CellInstArray(cell_text.cell_index(), Trans(Trans.R0, 25000,125000)))                

    # instantiate y-branch (attached to another cell)
    inst_y1 = connect_cell(inst_wg1, 'opt2', cell_y, 'opt2')

    # Waveguides:
    connect_pins_with_waveguide(inst_y1, 'opt3', inst_wg3, 'opt1', waveguide_type=waveguide_type)
    connect_pins_with_waveguide(inst_y1, 'opt1', inst_wg2, 'opt1', waveguide_type=waveguide_type)

    return inst_wg1, inst_wg2, inst_wg3
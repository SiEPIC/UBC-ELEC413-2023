from pya import *


def design_HangZou_w_330_dW_72_period_319_overetch_0_NG_11_rec(cell, cell_y, inst_wg1, inst_wg2, inst_wg3, waveguide_type):
    
    # load functions
    from SiEPIC.scripts import connect_pins_with_waveguide, connect_cell
    ly = cell.layout()
    library = ly.technology().name

    cell_taper = ly.create_cell('ebeam_taper_350nm_2000nm_te1310', library)

    #####
    # designer circuit:

    # Create a physical text label so we can see under the microscope
    # How do we find out the PCell parameter variables?
    '''
    c = ly.create_cell('TEXT','Basic')
    [p.name for p in c.pcell_declaration().get_parameters() if c.is_pcell_variant]
    c.delete()
    '''
    # returns: ['text', 'font_name', 'layer', 'mag', 'inverse', 'bias', 'cspacing', 'lspacing', 'eff_cw', 'eff_ch', 'eff_lw', 'eff_dr', 'font']
    from SiEPIC.utils import get_technology_by_name
    TECHNOLOGY = get_technology_by_name(library)
    cell_text = ly.create_cell('TEXT', "Basic", {
        'text':cell.name,
        'layer': TECHNOLOGY['M1'],
        'mag': 30,
         })
    if not cell_text:
        raise Exception ('Cannot load text label cell; please check the script carefully.')
    cell.insert(CellInstArray(cell_text.cell_index(), Trans(Trans.R0, 25000,125000)))                

    # load the cells from the PDK
    # choose appropriate parameters
    cell_bragg = ly.create_cell('ebeam_pcell_bragg_grating', library, {
        'number_of_periods':11,
        'grating_period': 0.319,
        'corrugation_width': 0.072,
        'wg_width': 0.37,
        'sinusoidal': False})
    if not cell_bragg:
        raise Exception ('Cannot load Bragg grating cell; please check the script carefully.')
    
    waveguide_type_mm = 'Multimode Strip TE 1310 nm, w=2000 nm'
    
    # instantiate y-branch (attached to input waveguide)
    inst_y1 = connect_cell(inst_wg1, 'opt2', cell_y, 'opt2')

    # instantiate Bragg grating (attached to y branch)
    inst_bragg1 = connect_cell(inst_y1, 'opt1', cell_bragg, 'opt1')

    # instantiate a taper (attached to the first Bragg grating)
    inst_taper1 = connect_cell(inst_bragg1, 'opt2', cell_taper, 'opt')

    # instantiate a taper (attached to the first taper, then move)
    inst_taper2 = connect_cell(inst_taper1, 'opt2', cell_taper, 'opt2')
    # move the taper to the right
    inst_taper2.transform(Trans(230000,0))

    # Waveguide between taper 1 and taper 2 (wide multimode waveguide)
    connect_pins_with_waveguide(inst_taper1, 'opt2', inst_taper2, 'opt2', waveguide_type=waveguide_type_mm)

    # instantiate a taper (attached to the first taper, then move)
    inst_taper3 = connect_cell(inst_taper1, 'opt2', cell_taper, 'opt2')
    # move the taper to the right and up
    inst_taper3.transform(Trans(230000,20000))

    # Waveguide between taper 2 and taper 3 (single mode waveguide)
    connect_pins_with_waveguide(inst_taper2, 'opt', inst_taper3, 'opt', waveguide_type=waveguide_type)

    # instantiate a taper (attached to the third taper, then move)
    inst_taper4 = connect_cell(inst_taper3, 'opt2', cell_taper, 'opt2')
    # move the taper to the right and up
    inst_taper4.transform(Trans(-230000,0))

    # Waveguide between taper 3 and taper 4 (wide multimode waveguide)
    connect_pins_with_waveguide(inst_taper3, 'opt2', inst_taper4, 'opt2', waveguide_type=waveguide_type_mm)

    # instantiate a taper (attached to the third taper, then move)
    inst_taper5 = connect_cell(inst_taper3, 'opt2', cell_taper, 'opt2')
    # move the taper to the right and up
    inst_taper5.transform(Trans(-230000,20000))

    # Waveguide between taper 4 and taper 5 (single mode waveguide)
    connect_pins_with_waveguide(inst_taper4, 'opt', inst_taper5, 'opt', waveguide_type=waveguide_type)

    # instantiate a taper (attached to the fifth taper, then move)
    inst_taper6 = connect_cell(inst_taper5, 'opt2', cell_taper, 'opt2')
    # move the taper to the right and up
    inst_taper6.transform(Trans(204372,0))

    # Waveguide between taper 5 and taper 6 (wide multimode waveguide)
    connect_pins_with_waveguide(inst_taper5, 'opt2', inst_taper6, 'opt2', waveguide_type=waveguide_type_mm)

    # instantiate Bragg grating (attached to the last taper)
    inst_bragg2 = connect_cell(inst_taper6, 'opt', cell_bragg, 'opt2')

    # End of Fabry-Perot cavity    

    # Waveguides for the two Fabry-Perot outputs:
    connect_pins_with_waveguide(inst_y1, 'opt3', inst_wg3, 'opt1', waveguide_type=waveguide_type)
    connect_pins_with_waveguide(inst_bragg2, 'opt1', inst_wg2, 'opt1', waveguide_type=waveguide_type, turtle_A = [10, 90, 20, -90, 20, -90], error_min_bend_radius=False)

    return inst_wg1, inst_wg2, inst_wg3
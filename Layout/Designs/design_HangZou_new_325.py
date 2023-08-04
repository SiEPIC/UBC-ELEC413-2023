from pya import *


def design_HangZou_new_325(cell, cell_y, inst_wg1, inst_wg2, inst_wg3, waveguide_type):
    
    # load functions
    from SiEPIC.scripts import connect_pins_with_waveguide, connect_cell
    ly = cell.layout()
    library = ly.technology().name

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
    cell_bragg = ly.create_cell('Bragg_grating', library, {
        'number_of_periods':20,
        'grating_period': 0.292,
        'corrugation_width': 0.046,
        'wg_width': 0.35,
        'sinusoidal': False})
    if not cell_bragg:
        raise Exception ('Cannot load Bragg grating cell; please check the script carefully.')

    # instantiate y-branch (attached to input waveguide)
    inst_y1 = connect_cell(inst_wg1, 'opt2', cell_y, 'opt2')

    # instantiate Bragg grating (attached to y branch)
    inst_bragg1 = connect_cell(inst_y1, 'opt1', cell_bragg, 'opt1')

    # instantiate Bragg grating (attached to the first Bragg grating)
    inst_bragg2 = connect_cell(inst_bragg1, 'opt2', cell_bragg, 'opt2')
    
    # move the Bragg grating to the right, and up
    inst_bragg2.transform(Trans(190000,110000))

    # End of Fabry-Perot
    # Waveguides for the two outputs:
    connect_pins_with_waveguide(inst_y1, 'opt3', inst_wg3, 'opt1', waveguide_type=waveguide_type)
    connect_pins_with_waveguide(inst_bragg2, 'opt1', inst_wg2, 'opt1', waveguide_type=waveguide_type)
    
    '''
    make a long waveguide, back and forth, 
    target 0.2 nm FSR assuming ng = 4
    > wavelength=1270e-9; ng=4; fsr=0.2e-9;
    > L = wavelength**2/2/ng/fsr
    > L * 1e6
    > 1000 [microns]
    using "turtle" routing
    https://github.com/SiEPIC/SiEPIC-Tools/wiki/Scripted-Layout#adding-a-waveguide-between-components
    '''
    connect_pins_with_waveguide(inst_bragg1, 'opt2', inst_bragg2, 'opt2', waveguide_type=waveguide_type,
        turtle_A = [250,90,20,90,250,-90,20,-90,250,90,20,90,250,-90,20,-90] )
        #turtle_A = [250,90,20,90,250,-90,30,-90,250] )
        #turtle_A = [250] )

    return inst_wg1, inst_wg2, inst_wg3
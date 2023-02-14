
# Enter your Python code here

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
    

    # load the cells from the PDK
    # choose appropriate parameters
    cell_bragg = ly.create_cell('Bragg_grating', library, {
        'number_of_periods':100,
        'grating_period': 0.278,
        'corrugation_width': 0.06,
        'wg_width': 0.35,
        'sinusoidal': False})
    if not cell_bragg:
        raise Exception ('Cannot load Bragg grating cell; please check the script carefully.')
        
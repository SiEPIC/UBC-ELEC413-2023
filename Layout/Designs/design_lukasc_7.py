'''
Design by Lukas Chrostowski, for UBC ELEC 413, 2023
This file creates a library that contains a PCell (BraggWaveguide_holes)
The circuit is design_lukasc_x, where x is an integer
This file can be copied many times, and simply changing the file and 
 design name integer will create a different circuit (i.e., _x is a parameter)

This file already creates a Library, with a new parameterized cell, BraggWaveguide_holes
'''

from pya import *
from . import *
import pya
import math
from SiEPIC.utils import get_technology_by_name



class BraggWaveguide_holes(pya.PCellDeclarationHelper):
  """
  Define a Parameterized cell (PCell) for a  
  Waveguide Bragg grating using holes
  by Lukas Chrostowski  
  """

  def __init__(self):

    # Important: initialize the super class
    super(BraggWaveguide_holes, self).__init__()
    TECHNOLOGY = get_technology_by_name('SiEPICfab_EBeam_ZEP')

    # declare the parameters
    self.param("number_of_periods", self.TypeInt, "Number of grating periods", default = 10)     
    self.param("grating_period", self.TypeDouble, "Grating period (microns)", default = 0.260)     
    self.param("fill_factor", self.TypeDouble, "Grating fill factor", default = 0.5)     
    self.param("hole_width", self.TypeDouble, "Corrugration width (microns)", default = 0.07)     
    self.param("wg_width", self.TypeDouble, "Waveguide width", default = 0.35)     
    self.param("layer", self.TypeLayer, "Layer", default = pya.LayerInfo(1, 0))
    self.param("clad", self.TypeLayer, "Cladding Layer", default = TECHNOLOGY['Si_clad'])
    self.param("pinrec", self.TypeLayer, "PinRec Layer", default = TECHNOLOGY['PinRec'])
    self.param("devrec", self.TypeLayer, "DevRec Layer", default = TECHNOLOGY['DevRec'])
#    self.param("textl", self.TypeLayer, "Text Layer", default = LayerInfo(10, 0))

  def display_text_impl(self):
    # Provide a descriptive text for the cell
    return "BraggWaveguide_holes_%s-%.3f-%.3f-%.3f" % \
    (self.number_of_periods, self.grating_period, self.hole_width, self.fill_factor)
  
  def coerce_parameters_impl(self):
    pass

  def can_create_from_shape(self, layout, shape, layer):
    return False
    
  def produce_impl(self):
  
    # fetch the parameters
    dbu = self.layout.dbu
    ly = self.layout
    shapes = self.cell.shapes

    LayerSi = self.layer
    LayerSiN = ly.layer(LayerSi)
    LayerPinRecN = ly.layer(self.pinrec)
    LayerDevRecN = ly.layer(self.devrec)
    LayerCladN = ly.layer(self.clad)

    from SiEPIC.extend import to_itype
    
    # Draw the Bragg grating:
    grating_period = to_itype(self.grating_period,dbu)
    w = to_itype(self.wg_width,dbu)
    hole_width = to_itype(self.hole_width,dbu)
    fill_factor = self.fill_factor
    
    for i in range(0,self.number_of_periods):
        x = i * grating_period
        box1 = Box(x, -w/2, x + grating_period * (1-fill_factor), w/2)
        box2 = Box(x + grating_period * (1-fill_factor), -hole_width/2, x + grating_period, -w/2)
        box3 = Box(x + grating_period * (1-fill_factor), hole_width/2, x + grating_period, w/2)
        shapes(LayerSiN).insert(box1)
        shapes(LayerSiN).insert(box2)
        shapes(LayerSiN).insert(box3)
        length = x + grating_period

    # Draw the cladding
    path = Path([Point(0, 0), Point(length, 0)], 3*w)
    shapes(LayerCladN).insert(path.simple_polygon())
    
    # Create the pins on the waveguides, as short paths:
    from SiEPIC._globals import PIN_LENGTH as pin_length

    t = Trans(Trans.R0, 0,0)
    pin = Path([Point(pin_length/2, 0), Point(-pin_length/2, 0)], w)
    pin_t = pin.transformed(t)
    shapes(LayerPinRecN).insert(pin_t)
    text = Text ("opt1", t)
    shape = shapes(LayerPinRecN).insert(text)
    shape.text_size = 0.3/dbu

    t = Trans(Trans.R0, length,0)
    pin = Path([Point(-pin_length/2, 0), Point(pin_length/2, 0)], w)
    pin_t = pin.transformed(t)
    shapes(LayerPinRecN).insert(pin_t)
    text = Text ("opt2", t)
    shape = shapes(LayerPinRecN).insert(text)
    shape.text_size = 0.3/dbu
    shape.text_halign = 2

    # Compact model information
    t = Trans(Trans.R0, 0, 0)
    text = Text ('Lumerical_INTERCONNECT_library=Design kits/ebeam', t)
    shape = shapes(LayerDevRecN).insert(text)
    shape.text_size = 0.1/dbu
    t = Trans(Trans.R0, length/10, 0)
    text = Text ('Component=ebeam_bragg_te1550', t)
    shape = shapes(LayerDevRecN).insert(text)
    shape.text_size = 0.1/dbu
    t = Trans(Trans.R0, length/9, 0)
    text = Text \
      ('Spice_param:number_of_periods=%s grating_period=%.3g hole_width=%.3g fill_factor=%.3g' %\
      (self.number_of_periods, self.grating_period*1e-6, self.hole_width*1e-6, self.fill_factor), t )
    shape = shapes(LayerDevRecN).insert(text)
    shape.text_size = 0.1/dbu

    # Create the device recognition layer -- make it 1 * wg_width away from the waveguides.
    t = Trans(Trans.R0, 0,0)
    path = Path([Point(0, 0), Point(length, 0)], 3*w)
    shapes(LayerDevRecN).insert(path.simple_polygon())

    print('Done: BraggWaveguide_holes')


class Library_lukasc(pya.Library):
  # Create a library with PCells

  def __init__(self):
    library = "Library_lukasc"
    self.technology="SiEPICfab_EBeam_ZEP"
    print("Initializing '%s' Library." % library)
    self.description= 'v0.1'

    # add all the PCells from this library    
    self.layout().register_pcell("BraggWaveguide_holes", BraggWaveguide_holes())
    
    # Register us the library with the technology name
    # If a library with that name already existed, it will be replaced then.
    self.register(library)


def design_lukasc_7(cell, cell_y, inst_wg1, inst_wg2, inst_wg3, waveguide_type):
 
    # Load the custom library (only the first time)
    if not(pya.Library().library_by_name('Library_lukasc','SiEPICfab_EBeam_ZEP')):
        Library_lukasc()
    
    # Get the name of the design, and extract the number as a parameter (number of periods)
    N = [int(i) for i in cell.name.split('_') if i.isdigit()][0]
    
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
    TECHNOLOGY = get_technology_by_name('SiEPICfab_EBeam_ZEP')
    cell_text = ly.create_cell('TEXT', "Basic", {
        'text':cell.name,
        'layer': TECHNOLOGY['M1'],
        'mag': 30,
         })
    if not cell_text:
        raise Exception ('Cannot load text label cell; please check the script carefully.')
    cell.insert(CellInstArray(cell_text.cell_index(), Trans(Trans.R0, 25000,125000)))                
    

    # load the cells from the custom Library
    # choose appropriate parameters
    cell_bragg = ly.create_cell('BraggWaveguide_holes', "Library_lukasc", {
        'number_of_periods':N,
        'grating_period': 0.320,
        'hole_width': 0.07,
        'wg_width': 0.35 })
    if not cell_bragg:
        raise Exception ('Cannot load Bragg grating cell; please check the script carefully.')
        
    cell_taper = ly.create_cell('taper_350nm_2000nm', library)
    if not cell_taper:
        raise Exception ('Cannot load taper cell; please check the script carefully.')
    waveguide_type_mm = 'Multimode Strip TE 1310 nm, w=2000 nm'

    # instantiate y-branch (attached to input waveguide)
    inst_y1 = connect_cell(inst_wg1, 'opt2', cell_y, 'opt2')

    # Create the Fabry Perot cavity:
   
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
    inst_taper4.transform(Trans(-250000,0))

    # Waveguide between taper 3 and taper 4 (wide multimode waveguide)
    connect_pins_with_waveguide(inst_taper3, 'opt2', inst_taper4, 'opt2', waveguide_type=waveguide_type_mm)

    # instantiate a taper (attached to the third taper, then move)
    inst_taper5 = connect_cell(inst_taper3, 'opt2', cell_taper, 'opt2')
    # move the taper to the right and up
    inst_taper5.transform(Trans(-250000,20000))

    # Waveguide between taper 4 and taper 5 (single mode waveguide)
    connect_pins_with_waveguide(inst_taper4, 'opt', inst_taper5, 'opt', waveguide_type=waveguide_type)

    # instantiate a taper (attached to the fifth taper, then move)
    inst_taper6 = connect_cell(inst_taper5, 'opt2', cell_taper, 'opt2')
    # move the taper to the right and up
    inst_taper6.transform(Trans(200000,0))

    # Waveguide between taper 5 and taper 6 (wide multimode waveguide)
    connect_pins_with_waveguide(inst_taper5, 'opt2', inst_taper6, 'opt2', waveguide_type=waveguide_type_mm)

    # instantiate Bragg grating (attached to the last taper)
    inst_bragg2 = connect_cell(inst_taper6, 'opt', cell_bragg, 'opt2')

    # End of Fabry-Perot cavity    

    # Waveguides for the two Fabry-Perot outputs:
    connect_pins_with_waveguide(inst_y1, 'opt3', inst_wg3, 'opt1', waveguide_type=waveguide_type)
    connect_pins_with_waveguide(inst_bragg2, 'opt1', inst_wg2, 'opt1', waveguide_type=waveguide_type, turtle_A = [10, 90, 20, -90, 20, -90], error_min_bend_radius=False)

    return inst_wg1, inst_wg2, inst_wg3
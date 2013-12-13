import os
import sys

# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

import amt_
import bgl
import blf

import auroramdltools

# Globals
minimap_size   = 32
z_offset       = 0.0
input_path     = 'in'
output_path    = 'out'
emtpy_blend    = os.fsencode('.\\empty.blend')
light_color    = (1.0,1.0,1.0)
lightsrc_imp   = False
fading_obj_imp = True

def processfile(filepath):
    '''
    Process a single mdl file:
     - Set up cameras & lights
     - Render minimap
    '''
    # Import mdl file
    amt_.ops.amt.importmdl(filepath=mdlfile, import_items={'GEOMETRY'}, import_walkmesh=False, import_lights=lightsrc_imp, import_fading_obj=fading_obj_imp)
    
    # Render minimap
    render_scene = amt_.context.scene   
    mdlbase = auroramdltools.nvb_utils.get_mdlbase(render_scene) 
    if (mdlbase is not None):
        filename = 'mi_' + mdlbase.name
        render_scene.render.filepath = os.fsencode(os.path.join(output_path, filename))
        mdlbase.auroraprops.minimapsize    = minimap_size
        mdlbase.auroraprops.minimapzoffset = z_offset
        auroramdltools.nvb_utils.nvb_minimap_render_setup(mdlbase, render_scene, light_color)
        amt_.ops.render.render(write_still=True)
    else:
        print('WARNING: ');

    
for arg in sys.argv:
    words=arg.split('=')   
    if (words[0] == 'nvb_msize'):
        try:
            minimap_size = int(words[1]) 
        except:
            print('ERROR: Could not read MINIMAP_SIZE from generator.ini')
            minimap_size = 32 
    if (words[0] == 'nvb_zoff'):
        try:
            z_offset = float(words[1]) 
        except:
            print('ERROR: Could not read Z_OFFSET from generator.ini')
            z_offset = 0.0             
    elif (words[0] == 'nvb_input'):
        input_path = words[1]
    elif (words[0] == 'nvb_output'):
        output_path = words[1]
    elif (words[0] == 'nvb_implight'):
        try:    
            lightsrc_imp = (int(words[1]) >= 1)
        except:
            print('ERROR: Could not read IMPORT_LIGHTS from generator.ini')
            lightscr_im = False
    elif (words[0] == 'nvb_impfade'):
        try:    
            fading_obj_imp = (int(words[1]) >= 1)
        except:
            print('ERROR: Could not read IMPORT_FADING_OBJ from generator.ini')
            fading_obj_imp = True           
    elif (words[0] == 'nvb_lcolor'):
        print(words[1])
        cval_string = words[1].split(',')
        try:    
            cval_list = [ float(cval_string[0]), 
                          float(cval_string[1]), 
                          float(cval_string[2]) ]                       
        except:
            print('ERROR: Could not read LIGHT_COLOR from generator.ini')
            cval_list = [1.0,1.0,1.0]      
        # Make sure the light colors are in [0.0,1.0]
        for idx, cval in enumerate(cval_list):
            if cval < 0.0:
                cval_list[idx] = 0.0
            elif cval > 1.0:
                cval_list[idx] = 1.0
        light_color = tuple(cval_list)
        
        
# Get all mdl files in the input directory
for filename in os.listdir(input_path):
    if filename.endswith('.mdl'):
        mdlfile = os.fsencode(os.path.join(input_path, filename))
        print('Processing ' + filename)
        # Load an empty file
        amt_.ops.wm.open_mainfile(filepath=emtpy_blend)
        processfile(mdlfile)       
#!/usr/bin/env python

from gimpfu import *

# use in console with
# image = gimp.image_list()[0]
# pdb.python_fu_rpg_character_sketch(image, image.layers[0])

# based on this tutorial
# https://www.youtube.com/watch?v=eLgsSN2MsMo

def sketchCharacter (image, drawable) :
    # gimp.progress_init("Sketching...")
    # steps = 10
    # gimp.progress_update(10)
       
    # Set up an undo group, so the operation will be undone in one step.
    gimp.pdb.gimp_undo_push_group_start(image)

    # create two duplicates of active layer
    image.add_layer(image.active_layer.copy())
    image.add_layer(image.active_layer.copy())
    
    # adjust saturation of top layer
    layer = image.layers[0]
    # TODO: Verify this works:
    pdb.gimp_drawable_hue_saturation(layer, HUE_RANGE_ALL, 0, 0, -100, 0)
    layer.mode = SATURATION_MODE
    
    # create blur on middle layer
    layer = image.layers[1]
    pdb.plug_in_gauss_iir(image, layer, 10, TRUE, TRUE)
    layer.mode = DODGE_MODE
    
    # adjust threshold of lowest layer
    layer = image.layers[2]
    pdb.gimp_drawable_levels(layer, HISTOGRAM_VALUE, 0.04, 1, FALSE, 1.0, 0, 1, FALSE)

    # flatten
    layer = pdb.gimp_image_merge_visible_layers(image, EXPAND_AS_NECESSARY)
    #image.flatten()
    
    # cartoon
    pdb.plug_in_cartoon(image, layer, 9, 0.7)

    pdb.plug_in_autocrop(image, layer)

    # Close the undo group.
    pdb.gimp_undo_push_group_end(image)

    gimp.displays_flush()

register(
    "python_fu_rpg_character_sketch",
    "makes image look hand-drawn",
    "makes image look hand-drawn",
    "Nicholas Shewmaker",
    "Nicholas Shewmaker",
    "2019",
#    "<Image>/Filters/Artistic/_Character Sketch",
    "<Image>/Filters/Custom/_Character Sketch",
    "*",      # Alternately use RGB, RGB*, GRAY*, INDEXED etc.
    [],
    [],
    sketchCharacter)

main()
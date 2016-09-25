"""TODO: DOC."""

import bpy
from . import nvb_def


def nvb_update_shadow_prop(self, context):
    """Set the lamps shadow to match the aurora shadow property."""
    select_object = context.object
    if (select_object) and (select_object.type == 'LAMP'):
        try:
            if (select_object.nvb.shadow):
                select_object.data.shadow_method = 'RAY_SHADOW'
            else:
                select_object.data.shadow_method = 'NOSHADOW'
        except:
            pass


class NVB_PG_ANIMEVENT(bpy.types.PropertyGroup):
    """Properties for a single event in the even list."""

    name = bpy.props.StringProperty(
                name='Name',
                description='Name for this event',
                default='Unnamed')

    frame = bpy.props.IntProperty(
                name='Frame',
                description='Frame at which the event should fire',
                default=1)


class NVB_PG_ANIM(bpy.types.PropertyGroup):
    """Properties for a single animation in the animation list."""

    name = bpy.props.StringProperty(
                name='Name',
                description='Name for this event',
                default='Unnamed')
    ttime = bpy.props.FloatProperty(
                name='Transitiontime',
                description='Used for for animations only',
                default=1, min=0)
    root = bpy.props.StringProperty(
                name='Root',
                description='Entry point of the animation',
                default='')
    mute = bpy.props.BoolProperty(
                name='Mute',
                description='Ignore animation during export',
                default=False)
    marker = bpy.props.StringProperty(
                name='Marker',
                description='Start marker in the timeline',
                default='')
    frameStart = bpy.props.IntProperty(
                name='Start',
                description='Animation Start',
                default=0,
                min=0)
    frameEnd = bpy.props.IntProperty(
                name='End',
                description='Animation End',
                default=0,
                min=0)

    eventList = bpy.props.CollectionProperty(type=NVB_PG_ANIMEVENT)
    eventListIdx = bpy.props.IntProperty(
        name='Index for event List',
        default=0)


class NVB_PG_FLARE(bpy.types.PropertyGroup):
    """Properties for a single flare in the flare list."""

    texture = bpy.props.StringProperty(name='Texture',
                                       description='Texture name',
                                       default=nvb_def.null)
    size = bpy.props.FloatProperty(name='Size',
                                   description='Flare size',
                                   default=1)
    position = bpy.props.FloatProperty(name='Position',
                                       description='Flare position',
                                       default=1)
    colorshift = bpy.props.FloatVectorProperty(name='Colorshift',
                                               description='Colorshift',
                                               subtype='COLOR_GAMMA',
                                               default=(0.0, 0.0, 0.0),
                                               min=-1.0, max=1.0,
                                               soft_min=0.0, soft_max=1.0)


class NVB_PG_OBJECT(bpy.types.PropertyGroup):
    """Holds additional properties needed for the mdl file format.

    This class defines all additional properties needed by the mdl file
    format. It hold the properties for meshes, lamps and empties.
    """

    # For all objects
    wirecolor = bpy.props.FloatVectorProperty(
                name='Wirecolor',
                description='Color of the wireframe',
                subtype='COLOR_GAMMA',
                default=(1.0, 1.0, 1.0),
                min=0.0, max=1.0,
                soft_min=0.0, soft_max=1.0)
    imporder = bpy.props.IntProperty(name='Order of Import',
                                     default=0)

    # For all emptys
    emptytype = bpy.props.EnumProperty(
                name='Type',
                items=[(nvb_def.Emptytype.DUMMY, 'Dummy', 'Simple dummy object', 0),
                       (nvb_def.Emptytype.REFERENCE, 'Reference node', 'Used in spells. Points to "fx_ref" by default', 1),
                       (nvb_def.Emptytype.PATCH, 'Patch node', 'Unknown purpose.', 2)],
                default=nvb_def.Emptytype.DUMMY)
    # For MDL Rootdummy
    supermodel = bpy.props.StringProperty(
        name='Supermodel',
        description='Name of the model to inherit animations from',
        default=nvb_def.null)
    classification = bpy.props.EnumProperty(
                name='Classification',
                items=[(nvb_def.Classification.UNKNOWN, 'Unknown', 'Unknown classification', 0),
                       (nvb_def.Classification.TILE, 'Tile', 'Tiles for tilesets', 1),
                       (nvb_def.Classification.CHARACTER, 'Character', 'Creatures, characters or placeables', 2),
                       (nvb_def.Classification.DOOR, 'Door', 'Doors', 3),
                       (nvb_def.Classification.EFFECT, 'Effect', 'Effects', 4),
                       (nvb_def.Classification.GUI, 'Gui', 'Gui', 5),
                       (nvb_def.Classification.ITEM, 'Item', 'Items or placeables', 6)],
                default=nvb_def.Classification.UNKNOWN)
    dummytype = bpy.props.EnumProperty(
                name='Subtype',
                items=[('NONE', 'None', 'Simple dummy object', 0),
                       ('HAND', 'Hand', 'Hand node for vfx', 1),
                       ('HEAD', 'Head', 'Head node for vfx', 2),
                       ('HHIT', 'Head hit', 'Head hit node for vfx', 3),
                       ('IMPC', 'Impact', 'Impact node for vfx', 4),
                       ('GRND', 'Ground', 'Ground node for vfx', 5),
                       ('USE1', 'Use 1', 'Node for "Use" animation', 6),
                       ('USE2', 'Use 2', 'Node for "Use" animation', 7),
                       ('O101', 'DWK: Open 1 1st', '1st node for "Use" animation', 8),
                       ('O102', 'DWK: Open 1 2nd', '2nd node for "Use" animation', 9),
                       ('O201', 'DWK: Open 2 1st', '1st node for "Use" animation', 10),
                       ('O202', 'DWK: Open 2 2nd', '2nd node for "Use" animation', 11),
                       ('CL01', 'DWK: Closed 1st', '1st node for "Use" animation', 12),
                       ('CL02', 'DWK: Closed 2nd', '2nd node for "Use" animation', 13)],
                default='NONE')
    animscale = bpy.props.FloatProperty(
                name='Animationscale',
                description='Animation scale for all animations',
                default=1.00, min=0.0)
    # Animation Data (for being able to seperate them)
    animList = bpy.props.CollectionProperty(type=NVB_PG_ANIM)
    animListIdx = bpy.props.IntProperty(name='Index for anim List',
                                        default=0)

    # For reference emptys
    refmodel = bpy.props.StringProperty(
                name='Reference Model',
                description='Name of another mdl file',
                default='fx_ref')
    reattachable = bpy.props.BoolProperty(
                name='Reattachable',
                default=False)
    # Minimap generation
    minimapzoffset = bpy.props.FloatProperty(name='Minimap Z Offset',
                                             default=0.00,
                                             min=0.00)
    minimapsize = bpy.props.IntProperty(name='Size',
                                        default=32,
                                        min=16)

    # For mesh objects
    meshtype = bpy.props.EnumProperty(
                name='Type',
                items=[(nvb_def.Meshtype.TRIMESH, 'Trimesh', 'desc', 0),
                       (nvb_def.Meshtype.DANGLYMESH, 'Danglymesh', 'desc', 1),
                       (nvb_def.Meshtype.SKIN, 'Skinmesh', 'desc', 2),
                       (nvb_def.Meshtype.AABB, 'AABB Walkmesh', 'desc', 3),
                       (nvb_def.Meshtype.EMITTER, 'Emitter', 'desc', 4),
                       (nvb_def.Meshtype.ANIMMESH, 'Animesh', 'desc', 5)],
                default=nvb_def.Meshtype.TRIMESH)
    smoothgroup = bpy.props.EnumProperty(
                name='Smoothgroup',
                items=[('SEPR', 'Seperate', 'Each face has it\'s own smoothgroup', 0),
                       ('SING', 'Single', 'All faces belong to the same smoothgroup', 1),
                       ('AUTO', 'Auto', 'Generate smoothgroups either from edges marked as sharp', 2)],
                default='SEPR')

    shadow = bpy.props.BoolProperty(
                name='Shadow',
                description='Whether to cast shadows',
                default=True,
                update=nvb_update_shadow_prop)
    render = bpy.props.BoolProperty(
                name='Render',
                description='Whether to render this object in the scene',
                default=True)

    tilefade = bpy.props.EnumProperty(
                name='Tilefade',
                items=[(nvb_def.Tilefade.NONE, 'None', 'Tilefade disabled', 0),
                       (nvb_def.Tilefade.FADE, 'Fade', 'Tilefade enabled', 1),
                       (nvb_def.Tilefade.BASE, 'Base', '???', 2),
                       (nvb_def.Tilefade.NEIGHBOUR, 'Neighbour', 'Tilefade if Neighbouring Tile fades', 3)],
                default=nvb_def.Tilefade.NONE)
    beaming = bpy.props.BoolProperty(
                name='beaming',
                description='Object casts beams (?)',
                default=False)
    inheritcolor = bpy.props.BoolProperty(
                name='Inheritcolor',
                description='Unused (?)',
                default=False)
    rotatetexture = bpy.props.BoolProperty(
                name='Rotatetexture',
                description='Automatically rotates texture to prevent seams',
                default=False)
    transparencyhint = bpy.props.IntProperty(
                name='Transparency Hint',
                description='Order of tranparency evaluation',
                default=0,
                min=0, max=32)
    selfillumcolor = bpy.props.FloatVectorProperty(
                name='Selfilluminationcolor',
                description='Makes the object glow but does not emit light',
                subtype='COLOR_GAMMA',
                default=(0.0, 0.0, 0.0),
                min=0.0, max=1.0,
                soft_min=0.0, soft_max=1.0)
    ambientcolor = bpy.props.FloatVectorProperty(name='Ambientcolor',
                                                 description='Ambient color',
                                                 subtype='COLOR_GAMMA',
                                                 default=(1.0, 1.0, 1.0),
                                                 min=0.0, max=1.0,
                                                 soft_min=0.0, soft_max=1.0)
    shininess = bpy.props.IntProperty(name='Shininess',
                                      default=1, min=0, max=32)

    # For danglymeshes
    period = bpy.props.FloatProperty(name='Period',
                                     default=1.0, min=0.0, max=32.0)
    tightness = bpy.props.FloatProperty(name='Tightness',
                                        default=1.0, min=0.0, max=32.0)
    displacement = bpy.props.FloatProperty(name='Displacement',
                                           default=0.5, min=0.0, max=32.0)
    constraints = bpy.props.StringProperty(
                name='Danglegroup',
                description='Name of the vertex group to use for the weights',
                default='')

    # For skingroups
    skingroup_obj = bpy.props.StringProperty(
                name='Bone',
                description='Name of the bone to create the skingroup for',
                default='')

    # For lamps
    lighttype = bpy.props.EnumProperty(
                name='Type',
                items=[('NONE', 'None', 'Simple light', 0),
                       ('MAINLIGHT1', 'Mainlight 1', 'Mainlight for tiles (Editable in toolset)', 1),
                       ('MAINLIGHT2', 'Mainlight 2', 'Mainlight for tiles (Editable in toolset)', 2),
                       ('SOURCELIGHT1', 'Sourcelight 1', 'Editable in toolset', 3),
                       ('SOURCELIGHT2', 'Sourcelight 2', 'Editable in toolset', 4)],
                default='NONE')
    ambientonly = bpy.props.BoolProperty(
                name='Ambient Only',
                default=False)
    lightpriority = bpy.props.IntProperty(
                name='Lightpriority',
                default=3, min=1, max=5)
    fadinglight = bpy.props.BoolProperty(
                name='Fading light',
                default=False)
    isdynamic = bpy.props.BoolProperty(
                name='Is Dynamic',
                default=False)
    affectdynamic = bpy.props.BoolProperty(
                name='Affect Dynamic',
                description='Affect dynamic objects',
                default=False)
    negativelight = bpy.props.BoolProperty(
                name='Negative Light',
                default=False)
    lensflares = bpy.props.BoolProperty(
                name='Lensflares',
                default=False)
    flareradius = bpy.props.FloatProperty(
                name='Flare Radius',
                default=0.0, min=0.0, max=100.0)
    flareList = bpy.props.CollectionProperty(type=NVB_PG_FLARE)
    flareListIdx = bpy.props.IntProperty(
                name='Index for flare list',
                default=0)

    # For emitters
    rawascii = bpy.props.StringProperty(
        name='Text node',
        description='Name of the raw text node',
        default='')

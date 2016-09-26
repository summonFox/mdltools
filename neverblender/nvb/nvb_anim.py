"""TODO: DOC."""

import bpy

from . import nvb_def
from . import nvb_utils
from . import nvb_animnode


class Animation():
    """TODO: DOC."""

    def __init__(self, name='UNNAMED'):
        """TODO: DOC."""
        self.name = name
        self.length = 1.0
        self.transtime = 1.0
        self.animroot = ''
        self.events = []
        self.nodes = []

        self.frameStart = 0
        self.frameEnd = 0

    def create(self, rootDummy, nodeNameResolver, options):
        """Create animations with a list of imported objects."""
        # Add new animation to list
        newAnim = nvb_utils.createAnimListItem(rootDummy)
        newAnim.name = self.name
        newAnim.ttime = self.transtime
        newAnim.root = self.animroot
        newAnim.frameEnd = newAnim.frameStart + \
            nvb_utils.nwtime2frame(self.length)

        # Add events for new animation
        for ev in self.events:
            newEvent = newAnim.eventList.add()
            newEvent.name = ev[1]
            newEvent.frame = newAnim.frameStart + \
                nvb_utils.nwtime2frame(ev[0])

        # Load the animation into the objects/actions
        for node in self.nodes:
            objName = nodeNameResolver.findObj(node.name,
                                               node.parent,
                                               node.idx)
            if objName and objName in bpy.data.objects:
                node.create(bpy.data.objects[objName], newAnim)

    def loadAsciiAnimHeader(self, asciiData):
        """TODO: DOC."""
        lines = asciiData.splitlines()
        for line in lines:
            try:
                label = line[0].lower()
            except IndexError:
                continue  # Probably empty line, skip it
            if (label == 'newanim'):
                self.name = nvb_utils.getAuroraString(line[1])
            elif (label == 'length'):
                self.length = float(line[1])
            elif (label == 'transtime'):
                self.transtime = float(line[1])
            elif (label == 'animroot'):
                try:
                    self.animroot = line[1]
                except:
                    self.animroot = ''
            elif (label == 'event'):
                self.events.append((float(line[1]), line[2]))

    def loadAsciiAnimNodes(self, asciiData):
        """TODO: DOC."""
        dlm = 'node '
        nodeList = [dlm+block for block in asciiData.split(dlm) if block != '']
        for idx, asciiNode in enumerate(nodeList):
            asciiLines = [l.strip().split() for l in asciiNode.splitlines()]
            node = nvb_animnode.Node()
            node.loadAscii(asciiLines, idx)
            self.nodes.append(node)

    def loadAscii(self, asciiData):
        """Load an animation from a block from an ascii mdl file."""
        animNodesStart = asciiData.find('node ')
        if (animNodesStart > -1):
            self.loadAsciiAnimHeader(asciiData[:animNodesStart-1])
            self.loadAsciiAnimNodes(asciiData[animNodesStart:])
        else:
            print('Neverblender - WARNING: Failed to load an animation.')

    @staticmethod
    def generateAsciiNodes(obj, anim, asciiLines):
        """TODO: Doc."""
        nvb_animnode.Node.generateAscii(obj, anim, asciiLines)

        childList = []
        for child in obj.children:
            childList.append((child.nvb.imporder, child))
        childList.sort(key=lambda tup: tup[0])

        for (imporder, child) in childList:
            Animation.generateAsciiGeometry(child, anim, asciiLines)

    @staticmethod
    def generateAscii(rootDummy, anim, asciiLines, options):
        """TODO: Doc."""
        if anim.mute:
            # Don't export mute animations
            return

        animScene = bpy.context.scene
        animLength = nvb_utils.frame2nwtime(anim.frameStart-anim.frameEnd,
                                            animScene.render.fps)

        asciiLines.append('newanim ' + anim.name + ' ' + rootDummy.name)
        asciiLines.append('  length ' + str(round(animLength, 5)))
        asciiLines.append('  transtime ' + str(round(anim.ttime, 3)))
        asciiLines.append('  animroot ' + anim.root)

        for event in anim.eventList:
            eventTime = nvb_utils.frame2nwtime(event.frame,
                                               animScene.render.fps)
            asciiLines.append('  event ' + str(round(eventTime, 5)) + ' ' +
                              event.name)

        Animation.generateAsciiNodes(rootDummy, anim, asciiLines)

        asciiLines.append('doneanim ' + anim.name + ' ' + rootDummy.name)
        asciiLines.append('')

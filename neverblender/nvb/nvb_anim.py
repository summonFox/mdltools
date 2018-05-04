"""TODO: DOC."""

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

    @staticmethod
    def createRestPose(obj, frame=1):
        """TODO: DOC."""
        nvb_animnode.Animnode.create_restpose(obj, frame)

    def create(self, rootDummy, noderesolver, options):
        """Create animations with a list of imported objects."""
        # Add new animation to list
        fps = options.scene.render.fps
        newAnim = nvb_utils.createAnimListItem(rootDummy)
        newAnim.name = self.name
        newAnim.ttime = self.transtime
        newAnim.root = self.animroot
        newAnim.frameEnd = fps * self.length + newAnim.frameStart
        # Add events for new animation
        for ev in self.events:
            newEvent = newAnim.eventList.add()
            newEvent.name = ev[1]
            newEvent.frame = fps * ev[0] + newAnim.frameStart
        # Load the animation into the objects/actions
        for node in self.nodes:
            obj = noderesolver.get_obj(node.name, node.nodeidx)
            if obj:
                node.create(obj, newAnim, self.length, options)
                if options.anim_restpose:
                    Animation.createRestPose(obj, newAnim.frameStart-5)

    def loadAsciiAnimHeader(self, asciiBlock):
        """TODO: DOC."""
        asciiLines = [l.strip().split() for l in asciiBlock.splitlines()]
        for line in asciiLines:
            try:
                label = line[0].lower()
            except (IndexError, AttributeError):
                continue  # Probably empty line, skip it
            if (label == 'newanim'):
                self.name = nvb_utils.getAuroraIdentifier(line[1])
            elif (label == 'length'):
                self.length = float(line[1])
            elif (label == 'transtime'):
                self.transtime = float(line[1])
            elif (label == 'animroot'):
                try:
                    self.animroot = line[1]
                except (ValueError, IndexError):
                    self.animroot = ''
            elif (label == 'event'):
                self.events.append((float(line[1]), line[2]))

    def loadAsciiAnimNodes(self, asciiData):
        """TODO: DOC."""
        dlm = 'node '
        nodeList = [dlm+block for block in asciiData.split(dlm) if block != '']
        for idx, asciiNode in enumerate(nodeList):
            asciiLines = [l.strip().split() for l in asciiNode.splitlines()]
            animnode = nvb_animnode.Animnode()
            animnode.load_ascii(asciiLines, idx)
            self.nodes.append(animnode)

    def loadAscii(self, asciiData):
        """Load an animation from a block from an ascii mdl file."""
        animNodesStart = asciiData.find('node ')
        if (animNodesStart > -1):
            self.loadAsciiAnimHeader(asciiData[:animNodesStart-1])
            self.loadAsciiAnimNodes(asciiData[animNodesStart:])
        else:
            print('Neverblender - WARNING: Failed to load an animation.')

    @staticmethod
    def generateAsciiNodes(obj, anim, asciiLines, options):
        """TODO: Doc."""
        nvb_animnode.Animnode.generate_ascii(obj, anim, asciiLines, options)

        # Sort children to restore original order before import
        # (important for supermodels/animations to work)
        children = [c for c in obj.children]
        children.sort(key=lambda c: c.nvb.imporder)
        for c in children:
            Animation.generateAsciiNodes(c, anim, asciiLines, options)

    @staticmethod
    def generateAscii(rootDummy, anim, asciiLines, options):
        """TODO: Doc."""
        if anim.mute:
            # Don't export mute animations
            return
        fps = options.scene.render.fps
        animLength = (anim.frameEnd-anim.frameStart) / fps
        asciiLines.append('newanim ' + anim.name + ' ' + rootDummy.name)
        asciiLines.append('  length ' + str(round(animLength, 5)))
        asciiLines.append('  transtime ' + str(round(anim.ttime, 3)))
        if anim.root:
            asciiLines.append('  animroot ' + anim.root)
        else:
            asciiLines.append('  animroot ' + rootDummy.name)

        for event in anim.eventList:
            eventTime = (event.frame-anim.frameStart) / fps
            asciiLines.append('  event ' + str(round(eventTime, 5)) + ' ' +
                              event.name)

        Animation.generateAsciiNodes(rootDummy, anim, asciiLines, options)

        asciiLines.append('doneanim ' + anim.name + ' ' + rootDummy.name)
        asciiLines.append('')

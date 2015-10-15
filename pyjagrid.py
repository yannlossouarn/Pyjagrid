#!/usr/bin/env python

import sys, inkex, pathmodifier
# The simplestyle module provides functions for style parsing.
from simplestyle import *
from simpletransform import *
import gettext
_ = gettext.gettext

debug = True # Turns debugging output on - Use debug = False to turn debugging output 'off'

class PyjaGridEffect(inkex.Effect):
    """
    Example Inkscape effect extension.
    Creates a new layer with a "Hello World!" text centered in the middle of the document.
    """
    def __init__(self):
        """
        Constructor.
        Defines the "--what" option of a script.
        """
        # Call the base class constructor.
        inkex.Effect.__init__(self)

        # Define string option "--what" with "-w" shortcut and default value "World".
        self.OptionParser.add_option('-p', '--pyjamaColumns', action = 'store',
          type = 'float', dest = 'pyjamaColumns', default = 16,
          help = 'How many columns on your pyjama ?')
        self.OptionParser.add_option('-v', '--verticalLines', action = 'store',
          type = 'float', dest = 'verticalLines', default = 12,
          help = 'How many lines on your vertical grid ?')

    def effect(self):
        """
        Effect behaviour.
        Overrides base class' method and inserts "Hello World" text into SVG document.
        """
        # Get script's options 
        pyjamaColumns = self.options.pyjamaColumns
        nbBigLines = self.options.verticalLines

        # Get access to main SVG document element and get its dimensions.
        svg = self.document.getroot()
        # or alternatively
        # svg = self.document.xpath('//svg:svg',namespaces=inkex.NSS)[0]

        # Again, there are two ways to get the attibutes:
        width  = inkex.unittouu(svg.get('width'))
        height = inkex.unittouu(svg.attrib['height'])

        # Reglages

        self.bbox = computeBBox(self.selected.values())

        maxY = self.bbox[2]
        minY = self.bbox[3]

        maxX = self.bbox[1]
        minX = self.bbox[0]

        maxYapprox = int(math.floor(self.bbox[2]))
        minYapprox = int(math.floor(self.bbox[3]))

        maxXapprox = int(math.floor(self.bbox[1]))
        minXapprox = int(math.ceil(self.bbox[0]))

        areaHeight = minY - maxY
        areaWidth = maxX - minX

        lineSpacing = areaHeight / (nbBigLines * 3)
        #inkex.debug(str(areaWidth) + "*" + str(areaHeight))

        nbLines = (nbBigLines + 1) + (nbBigLines * 2)

        nLargeurTraitBold = 0.9
        nLargeurTraitFin = 0.5
        couleurTraitBold = "rgb(125,125,125)"
        couleurTraitFin = "rgb(200,200,200)"

        columnsWidth = areaWidth / pyjamaColumns


        stylePyjamaColumnClair = {      'stroke'        : '#FFFFFF',
                                        'stroke-width'  : '0',
                                        'fill'          : '#FFFFFF'
        }
        stylePyjamaColumnFonce = {      'stroke'        : '#F9F9F9',
                                        'stroke-width'  : '0',
                                        'fill'          : '#F9F9F9'
        }




        # Just for 'fun' - report Python version
        if debug:
            cur_version = sys.version_info
            message = self.selected
            # myWidth = message.get('width')

            #inkex.debug(self.bbox)
            #inkex.debug(self.bbox[0])
            #for i, v in enumerate(message):
            #    inkex.debug(self.getElementById(v))



        # Create a new layer for the pyjama
        layer = inkex.etree.SubElement(svg, 'g')
        layer.set(inkex.addNS('label', 'inkscape'), 'Pyjagrid %s Layer' % ("pyjama" + '-' + str(nbBigLines)))
        layer.set(inkex.addNS('groupmode', 'inkscape'), 'layer')

        for n in range(1,int(pyjamaColumns)+1):
            if n & 0x1:
                columnAttribs = {
                    'style'     : simplestyle.formatStyle(stylePyjamaColumnFonce),
                    'height'    : str(areaHeight),
                    'width'     : str(columnsWidth),
                    'x'         : str(minX + (columnsWidth * (n-1))),
                    'y'         : str(maxY)
                }
            else:
                columnAttribs = {
                    'style'     : simplestyle.formatStyle(stylePyjamaColumnClair),
                    'height'    : str(areaHeight),
                    'width'     : str(columnsWidth),
                    'x'         : str(minX + (columnsWidth * (n-1))),
                    'y'         : str(maxY)
                }
            circ = inkex.etree.Element(inkex.addNS('rect','svg'), columnAttribs )
            layer.append(circ)


        # Create a new layer.
        layer = inkex.etree.SubElement(svg, 'g')
        layer.set(inkex.addNS('label', 'inkscape'), 'Pyjagrid %s Layer' % ("verticalLines" + '-' + str(nbBigLines)))
        layer.set(inkex.addNS('groupmode', 'inkscape'), 'layer')

        # Create text element
        #text = inkex.etree.Element(inkex.addNS('text','svg'))
        #text.text = 'Hello %s!' % (what)

        #inkex.debug(str(maxY) + " " + str(minY) + " " + str(lineSpacing))
        ligne = inkex.etree.Element(inkex.addNS('line',"svg"))

        ligne.set("x1", str(minX))
        ligne.set("y1", str(maxY))
        ligne.set("x2", str(maxX))
        ligne.set("y2", str(maxY))
        ligne.set("stroke","rgb(100,100,100)")
        ligne.set("stroke-width",str(nLargeurTraitBold))
        layer.append(ligne)
        lineMarker = "first"

        for n in range(1,int(nbLines)+1):
            if n == 1:
                lineMarker = "firstSmall"
                stroke = couleurTraitBold
                strokeWidth = str(nLargeurTraitBold)
            elif n == nbLines:
                stroke = couleurTraitBold
                strokeWidth = str(nLargeurTraitBold)
            elif lineMarker == "firstSmall":
                lineMarker = "secondSmall"
                stroke = couleurTraitFin
                strokeWidth = str(nLargeurTraitFin)
            elif lineMarker == "secondSmall":
                lineMarker = "middleBold"
            elif lineMarker == "middleBold":
                lineMarker = "firstSmall"
                stroke = couleurTraitFin
                strokeWidth = str(nLargeurTraitBold)

            ligne = inkex.etree.Element(inkex.addNS('line',"svg"))
            ligne.set("x1", str(minX))
            ligne.set("y1", str(maxY + (lineSpacing * (n-1) )))
            ligne.set("x2", str(maxX))
            ligne.set("y2", str(maxY + (lineSpacing * (n-1) )))
            ligne.set("stroke",stroke)
            ligne.set("stroke-width",strokeWidth)
            layer.append(ligne)



        # Set text position to center of document.
        #text.set('x', str(width / 2))
        #text.set('y', str(height / 2))

        # Center text horizontally with CSS style.
        #style = {'text-align' : 'center', 'text-anchor': 'middle'}
        #text.set('style', formatStyle(style))

        # Connect elements together.
        #layer.append(text)

# Create effect instance and apply it.
effect = PyjaGridEffect()
effect.affect()
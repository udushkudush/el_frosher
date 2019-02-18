from pymel.core import *
import elFrosher.app as ep
reload(ep)
from elFrosher.app import FrosherFileManager

mayaWindow = ui.PyUI('MayaWindow').asQtObject()
widget = FrosherFileManager(mayaWindow)

widget.show()
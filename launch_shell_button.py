from pymel.core import *
import elFrosher.app as ep
reload(ep)
from elFrosher.app import SomeFuckingShit

mayaWindow = ui.PyUI('MayaWindow').asQtObject()
widget = SomeFuckingShit(mayaWindow)

widget.show()
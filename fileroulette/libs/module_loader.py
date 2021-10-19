"""The dynamic module loader.

This is the list of modules available to the user. To add custom modules,
you'll need to add them to the import list as well as to the 'MODULE_DICT'.
These modules can be found in the 'modules' folder.
"""

from fileroulette.modules import upfile, gofileio

MODULE_DICT = {"upfile": upfile.Module, "gofileio": gofileio.Module}

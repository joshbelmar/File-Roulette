"""FileRoulette: Find random data on various hosting services."""

from fileroulette.libs import module_loader

# Load a dictionary of all installed modules.
MODULE_DICT = module_loader.MODULE_DICT

# Describe the purpose of this application.
DESCRIPTION = "Find random data on various hosting services."


def run_module(module_name, agent=False, proxy=False):
    """Initialize and run the specified module."""
    # Initialize the specified module.
    module = MODULE_DICT[module_name](agent=agent, proxy=proxy)
    # Run the specified module.
    module.run()

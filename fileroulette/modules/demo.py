"""Demo data source module.

This module is designed to demonstrate the layout of a data source module. It
includes only the most basic features that are required of a module, without
any additional fluff.

This module is non-functional and is not intended for actual use, but rather to
demonstrate how a data source module can be constructed.

Useful Functions
----------------
The following functions are defined in the fileroulette.libs.__init__.py file
to make it easier for you to write new modules.

self._split_before(source, target)
self._split_after(source, target)
    These two convenience functions take two arguments: the source and target
    strings. The function will attempt to find the target string in the source
    string. If it can be found, the functions will split the source string
    before or after the target string (respectively), and return the split
    parts. If the target string cannot be found, the function will return two
    empty strings.

"""

from fileroulette.modules import BaseModule

# Set the module name based on this file's name.
MODULE_NAME = __name__.split(".")[-1]


class Module(BaseModule):
    """Define the demo data source module.

    Note: The name of a data source Module class must always be 'Module.' This
    allows the module_loader to automatically load each module.
    """

    # A description of this particular module.
    description = "a demonstration data source"

    # Set the base url for random generation. The random key will replace
    # the brackets {} in the string.
    base_url = "https://example.site/files/{}"
    # Set the character types allowed in the key. This can include digits,
    # upper-case and/or lower-case letters, which will enable digits,
    # upper-case and/or lower-case letters in the randomly-generated key.
    # For example, this allowed_chars variable enables all three:
    allowed_chars = "aA1"
    # Set the randomly-generated key length.
    key_length = 5

    def __init__(self, agent, proxy):
        """Initialize the demo data source module."""
        # Initialize the BaseModule with the module name.
        super(Module, self).__init__(MODULE_NAME, agent, proxy)

    def check_output(self, content):
        """Check the content of the page to extract useful information.

        This function exists in the BaseModule class, but needs to be redefined
        in each derivative module in order to custom-tailor the module to the
        targeted site.

        Parameters
        ----------
        content : str
            The content returned by the server, typically text or HTML.

        Returns
        -------
        dict or False
            If the content is useful, return a dict containing the useful info.
            If there is no good data, return False to continue scanning.

        """
        # Define the rules for determining whether this is desirable content,
        # and for how to extract the useful information.
        if "download this file" in content:
            # If the content contains information that should be saved, create
            # a return_data dict and store the data inside it.
            return_data = {"status": "success"}
            # Then return that data.
            return return_data
        # If the content is undesirable, return False.
        return False

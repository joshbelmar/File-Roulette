"""Gofile.io data source module."""

import requests, json
from fileroulette.modules import BaseModule

# Set the module name based on this file's name.
MODULE_NAME = __name__.split(".")[-1]


class Module(BaseModule):
    """Define the Gofile.io data source module."""
    # A description of this particular module.
    description = "Find files on Gofile.io"
    # Set the base url for random generation.
    base_url = "https://api.gofile.io/getUpload.php?c={}"
    # Set the character types allowed in the key.
    allowed_chars = "a1"
    # Set the randomly-generated key length.
    key_length = 6

    def __init__(self, agent, proxy):
        """Initialize the UploadFiles.io data source module."""
        # Initialize the BaseModule with the module name.
        super(Module, self).__init__(MODULE_NAME, agent, proxy)

    def check_output(self, content):
        """Check the json response from the gofile.io api request to extract useful information."""
        try:
            #Serialize the json string from the page
            #Check against the status: ok is valid file, error is non valid
            data = json.loads(content)
            if data['status'] != "error":
                return_dict = {"File Name": data['data'][0]['name'], "File Size": data['data'][0]['size']}
                return return_dict
            else:
                return False
        except Exception as exception:
            # TODO: Handle this exception better.
            print("Exception: {}".format(exception))
            raise

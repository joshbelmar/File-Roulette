"""UploadFiles.io data source module."""

import re

from bs4 import BeautifulSoup

from fileroulette.modules import BaseModule

# Set the module name based on this file's name.
MODULE_NAME = __name__.split(".")[-1]


class Module(BaseModule):
    """Define the UploadFiles.io data source module."""

    # A description of this particular module.
    description = "find files on uploadfiles.io"

    # Set the base url for random generation.
    base_url = "https://uploadfiles.io/{}"
    # Set the character types allowed in the key.
    allowed_chars = "a1"
    # Set the randomly-generated key length.
    key_length = 5

    def __init__(self, agent, proxy):
        """Initialize the UploadFiles.io data source module."""
        # Initialize the BaseModule with the module name.
        super(Module, self).__init__(MODULE_NAME, agent, proxy)

    def check_output(self, content):
        """Check the content of the page to extract useful information."""
        # Avoid files that are inaccessible or missing.
        if "Sorry it's gone..." in content or "Premium Access Only" in content:
            return False
        # Attempt to extract the file name and size from the data.
        try:
            soup = BeautifulSoup(content, features="html.parser")
            _, post = self._split_after(content, '<div class="details">')
            _, post = self._split_after(post, "<h3>")
            file_name, _ = self._split_before(post, "</h3>")
            details_div = soup.find("div", class_="details")
            size_string = re.search("Size:(.*)", str(details_div.p)).group(0)
            _, file_size = self._split_after(size_string, ": ")
        except Exception as exception:
            # TODO: Handle this exception better.
            print("Exception: {}".format(exception))
            raise
        # Determine if the file exists.
        if file_name != "None" and "" not in [file_name, file_size]:
            # If so, return its information.
            return_dict = {"File Name": file_name, "File Size": file_size}
            return return_dict
        # If this isn't a file, return False.
        return False

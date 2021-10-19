"""Generate a random URL with the specified ruleset.

This module defines the urlgen function. This function can generate random URLs
for all kinds of services.
"""

import random
import string


def urlgen(template: str, charset: str, length: int) -> str:
    """Generate a random URL with the specified rules.

    Parameters
    ----------
    template : str
        A URL template with {} in the place where the generated key goes.
    charset : str
        A string specifying the types of characters to be included in the key.
        The string can be any combination of the following:
            - a lowercase letter (a-z)
            - an uppercase letter (A-Z)
            - a digit (0-9)
        If the charset contains a lowercase letter, it specifies that the key
        can contain lowercase letters. If it contains an uppercase letter, the
        key can contain uppercase letters. If it contains a digit, the key can
        contain digits.
    length : int
        The length of the key.

    Returns
    -------
    new_url : str
        A randomly-generated URL that matches the definition.

    """
    # Generate the random pool based on the specified charset. First, we need
    # to initialize the character pool.
    pool = set()
    # Next, parse each character in the specified charset.
    for character in list(charset):
        # Define the enabled character sets.
        charsets = [
            string.ascii_lowercase,
            string.ascii_uppercase,
            string.digits,
        ]
        # Check to see which character sets have been enabled.
        for chars in charsets:
            # Depending on the character type, append that set of characters
            # to the pool.
            pool = pool.union(set(chars) if character in chars else set())
    # Check to ensure that we've generated a valid character pool.
    if not pool:
        raise ValueError("Invalid charset specification.")
    # Convert the pool set into a string.
    pool = "".join(pool)
    # Now we need to generate the random key from the pool set.
    key = "".join([random.choice(pool) for _ in range(length)])
    # Finally, insert the new key into the template URL.
    new_url = template.format(key)
    if new_url == template:
        # If the new URL is the same as the template, they failed to specify
        # which part of the URL to replace with the random string.
        raise ValueError("Template URL missing {} specification.")
    # Return the new URL.
    return new_url

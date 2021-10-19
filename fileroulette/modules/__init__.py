"""FileRoulette Module Library.

This library defines the BaseModule template, from which new data source
modules can be derived. To learn more about making a new data source module,
see the demo.py module.
"""

# TODO: Enable multithreading and proxies, and allow for users to choose
#       whether they want to use random user agents or not.

import random
import requests
import sys

from fileroulette.libs import urlgen

# Just to prevent some SSL errors. This may not be necessary.
# requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += (
#     ":ECDHE-ECDSA-AES128-GCM-SHA256"
# )

# A list of user agents, in case we wish to pick at random.
AGENTS = [
    "Mozilla/5.0 (Windows NT 6.1; rv:52.0) Gecko/20100101 Firefox/52.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, "
    "like Gecko) Chrome/70.0.3538.77 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/41.0.2227.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like "
    "Gecko) Chrome/41.0.2227.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/41.0.2227.1 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML like "
    "Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14931",
    "Chrome (AppleWebKit/537.1; Chrome50.0; Windows NT 6.3) "
    "AppleWebKit/537.36 (KHTML like Gecko) Chrome/51.0.2704.79 Safari/537.36 "
    "Edge/14.14393",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML like "
    "Gecko) Chrome/46.0.2486.0 Safari/537.36 Edge/13.9200",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML like "
    "Gecko) Chrome/46.0.2486.0 Safari/537.36 Edge/13.10586",
    "Mozilla/5.0 (X11; Linux i686; rv:64.0) Gecko/20100101 Firefox/64.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:64.0) Gecko/20100101 Firefox/64.0",
    "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.10; rv:62.0) Gecko/20100101 "
    "Firefox/62.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:10.0) Gecko/20100101 "
    "Firefox/62.0",
    "Mozilla/5.0 (iPad; CPU OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, "
    "like Gecko) Version/6.0 Mobile/10A5355d Safari/8536.25",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/537.13+ "
    "(KHTML, like Gecko) Version/5.1.7 Safari/534.57.2",
    "Mozilla/5.0 (iPad; CPU OS 5_1 like Mac OS X) AppleWebKit/534.46 (KHTML, "
    "like Gecko ) Version/5.1 Mobile/9B176 Safari/7534.48.3",
    "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_7; da-dk) "
    "AppleWebKit/533.21.1 (KHTML, like Gecko) Version/5.0.5 Safari/533.21.1",
]
# Default to the Tor Browser user agent.
DEF_AGENT = "Mozilla/5.0 (Windows NT 6.1; rv:52.0) Gecko/20100101 Firefox/52.0"

# The following dictionary contains dicts of HTTP status codes that would
# signal some kind of problem with our request. If any of these codes should
# warrant a rejection of the URL without user notification, move them to the
# "rejected" dict.
STATUS_CODES = {
    "rejected": {400: "Bad Request", 404: "Not Found", 410: "Gone"},
    "forbidden": {401: "Unauthorized", 403: "Forbidden"},
    "unexpected": {
        405: "Method Not Allowed",
        406: "Not Acceptable",
        418: "I'm a Teapot!",
        420: "Enhance Your Calm",
    },
    "error": {
        408: "Request Timeout",
        421: "Misdirected Request",
        423: "Locked",
        429: "Too Many Requests",
        496: "SSL Certificate Required",
        500: "Internal Server Error",
        502: "Bad Gateway",
        503: "Service Unavailable",
        504: "Gateway Timeout",
        505: "HTTP Version Not Supported",
        509: "Bandwidth Limit Exceeded",
    },
    "cloudflare": {
        520: "Unknown Error (Cloudflare)",
        521: "Website is Down (Cloudflare)",
        522: "Connection Timed Out (Cloudflare)",
        523: "Origin is Unreachable (Cloudflare)",
        524: "A Timeout Occurred (Cloudflare)",
        525: "SSL Handshake Failed (Cloudflare)",
        527: "Railgun Error (Cloudflare)",
        530: "Origin DNS Error (Cloudflare)",
    },
}


# ---[ BASE MODULE DEFINITION ]--- #


class BaseModule:
    """Define the core structures common to all data source modules.

    Attributes
    ----------
    allowed_chars : str
        This defines what kind of characters can be used in the
        randomly-generated key. This string only needs up to three characters,
        one upper-case letter, one lower-case letter, and/or one number. This
        will determine whether upper-case letters, lower-case letters, or
        numbers (respectively) will be included in the key. For example, to
        allow all three, you could set allowed_chars to 'aA1'.
    base_url : str
        The template URL which will be modified with the randomly-generated key
        as defined by the allowed_chars and key_length variables. The key will
        be inserted wherever the open and closed brackets {} appear.
    key_length : int
        An integer which defines the length of the randomly-generated key.
    proxies : list
        If random_proxy is enabled, this list will be populated with (ip, port)
        tuples pulled from the `proxies.txt` file in the app's root directory.
    random_agent : bool
        This will determine whether each newly-generated requests session will
        use a random user agent. If not, it will use a Tor Browser user agent.
    random_proxy : bool
        This will determine whether random proxies should be assigned to each
        new session as it's created.

    """

    allowed_chars = str()
    base_url = str()
    key_length = int()
    proxies = list()
    random_agent = False
    random_proxy = False

    def __init__(self, module_name, agent, proxy):
        """Initialize the module.

        Parameters
        ----------
        module_name : str
            The name of the module that derived from this BaseModule class.

        """
        # Set the module's name.
        self.name = module_name
        # Enable or disable random user agents.
        self.random_agent = agent
        # Enable or disable random proxies.
        self.random_proxy = proxy

        if self.random_proxy:
            # If proxies are enabled, load them from the `proxies.txt` file.
            self._load_proxies()

    def _create_new_session(self):
        """Create a new requests session.

        Returns
        -------
        session or False
            A new instance of requests.sessions.Session with the qualities
            specified by the user's requirements. If a session cannot be made,
            this will return False instead.

        """
        session = requests.Session()
        # Check whether to enable a random User-Agent.
        if self.random_agent:
            # Choose a random agent from the AGENTS list.
            session.headers.update({"User-Agent": random.choice(AGENTS)})
        else:
            # Default to the Tor Browser user agent.
            session.headers.update({"User-Agent": DEF_AGENT})
        # Check whether to enable a random proxy.
        if self.random_proxy:
            # Let the user know we're searching.
            print("Searching for a working proxy", end="", flush=True)
        while self.random_proxy:
            try:
                # Choose a proxy from the list.
                (ip, port) = self.proxies.pop(0)
            except IndexError:
                # We are out of live proxies. Halt the program.
                print("No more proxies available!")
                sys.exit(0)
            # Format and assign the chosen proxy.
            proxy = "socks5h://{}:{}".format(ip, port)
            session.proxies = {"http": proxy, "https": proxy}
            # Test the proxy to see if it's working. To test the proxy, try to
            # establish a connection to a website that should always be online,
            # such as google.com.
            print(".", end="", flush=True)
            try:
                # Retrieve google.com.
                result = session.get("https://google.com/", timeout=1)
                # If successful, re-add the proxy to the list to be used again.
                self.proxies.append((ip, port))
                print("Success!")
                break
            except (
                requests.exceptions.ConnectionError,
                requests.exceptions.InvalidSchema,
                requests.exceptions.Timeout,
            ):
                # If unsuccessful, loop back and try another proxy.
                continue
        return session

    def _execute_scan(self, session):
        """Execute a single scan using the specified session.

        Parameters
        ----------
        session
            The requests session used to execute the scan.

        Returns
        -------
        bool
            Return True if we found useful data, otherwise False.

        """
        # Generate a new URL.
        url = self._new_url()
        # Retrieve the content of that URL.
        content = self._get_page_content(session, url)
        # Check to see if the content was retrieved successfully.
        if content:
            # The content was retrieved. Check to see if it's valuable.
            result = self.check_output(content)
            # Check if the result was a success.
            if isinstance(result, dict):
                # We got valid data!
                print("Found one!")
                print("Live URL: {}".format(url))
                # Get the keys from the result, then sort them.
                keys = list(result.keys())
                keys.sort()
                # Display the data collected.
                for key in keys:
                    print(" * {}: {}".format(key, result[key]))
                # Return True to indicate our success.
                return True
        # The content couldn't be retrieved, or the data was invalid.
        return False

    def _get_page_content(self, session, url):
        """Retrieve the HTML content for the specified URL.

        Parameters
        ----------
        session
            The session with which we will retrieve the URL.
        url
            The URL we will be retrieving.

        Returns
        -------
        content or False
            This function returns False if the content could not be loaded,
            otherwise it will return the text content of the retrieved page.

        """
        # Retrieve the page's header.
        (header, url) = self._get_page_header(session, url)
        # DEBUG: We're just checking what status code we get.
        # print("Status code: {}".format(header.status_code))
        if header.status_code == 200:
            # The request was a success. Return the text of the site.
            return session.get(url).content.decode()
        # Check for alternate status codes.
        if header.status_code in STATUS_CODES["rejected"]:
            # The URL is invalid or unavailable.
            return False
        for _, codes in STATUS_CODES.items():
            # There's an unexpected status code.
            if header.status_code in codes.keys():
                # Print out the status code information.
                print(
                    "{}: {} ({})".format(
                        header.status_code, codes[header.status_code], url
                    )
                )
                return False
        # We've encountered an unknown status code.
        print("{}: Unknown ({})".format(header.status_code, url))
        return False

    @staticmethod
    def _get_page_header(session, url):
        """Retrieve the HTTP header for the specified URL.

        Parameters
        ----------
        session
            The session with which we will retrieve the URL.
        url
            The URL we will be retrieving.

        Returns
        -------
        header
            The HTTP result header returned from the target site.
        url
            The URL of the page. If the header redirects to another URL, it
            will return the target URL. Otherwise, it will return the original.

        """
        header = session.head(url)
        if header.is_redirect:
            # If we're being redirected, grab the headers for the target URL.
            url = header.headers["Location"]
            header = session.head(url)
        return (header, url)

    def _load_proxies(self):
        """Load the `proxies.txt` file and store it in `self.proxies`."""
        try:
            with open("proxies.txt", "r") as proxy_file:
                # Read the proxy list.
                lines = proxy_file.readlines()
        except FileNotFoundError:
            # The file doesn't exist.
            print("The file 'proxies.txt' could not be found.")
            sys.exit(0)
        for line in lines:
            # Parse the list. Check each line for the ":" separator to ensure
            # that the line contains an IP:port pairing.
            if ":" in line:
                try:
                    # Extract the IP and port from the line.
                    ip, port = line.split(":")
                    # Append them to the self.proxies list.
                    self.proxies.append((ip, int(port)))
                except ValueError:
                    # If there's a problem assigning the IP and port, there is
                    # something wrong with how the proxy file is formatted.
                    print("Proxy file contains improper formatting.")
                    sys.exit(0)
        # Now that we've loaded the proxies into the file... Shuffle 'em up.
        random.shuffle(self.proxies)

    def _new_url(self):
        """Generate a new random URL.

        Returns
        -------
        str
            A randomly-generated URL which follows the specified constraints.

        """
        return urlgen(self.base_url, self.allowed_chars, self.key_length)

    @staticmethod
    def _split_after(source, target):
        """Split a string after the target string, returning both parts.

        If the target string cannot be found in the source string, this
        function will return two empty strings.

        Parameters
        ----------
        source : str
            The string which will be split.
        target : str
            The substring to be found in the source string, after which the
            source string will be split.

        Returns
        -------
        pre : str
            The string preceeding and including the target substring.
        post : str
            The string proceeding the target substring.

        """
        if target not in source:
            return "", ""
        index = source.find(target) + len(target)
        pre = source[:index]
        post = source[index:]
        return pre, post

    @staticmethod
    def _split_before(source, target):
        """Split a string before the target string, returning both parts.

        If the target string cannot be found in the source string, this
        function will return two empty strings.

        Parameters
        ----------
        source : str
            The string which will be split.
        target : str
            The substring to be found in the source string, before which the
            source string will be split.

        Returns
        -------
        pre : str
            The string preceeding the target substring.
        post : str
            The string proceeding and including the target substring.

        """
        if target not in source:
            return "", ""
        index = source.find(target)
        pre = source[:index]
        post = source[index:]
        return pre, post

    def check_output(self, content):
        """Check the content of the page to extract useful information.

        This function needs to be defined in each individual module, as this is
        the method which determines if the page contains data we wish to save,
        such as a live file or useful text.

        Parameters
        ----------
        content : str
            The content returned by the server, typically text or HTML.

        Returns
        -------
        dict or False
            If the content is useful, return a dict containing the useful info
            (such as file names and sizes). This information will be either
            printed to the screen or saved in a file, depending on the user's
            preference. If there is no good data, return False to continue
            scanning.

        """
        return False

    def run(self):
        """Start the module's main loop."""
        print("Running {} module...".format(self.name))
        session = self._create_new_session()
        while not session:
            # Skip sessions that fail.
            session = self._create_new_session()
        # Scan until we find a match.
        while not self._execute_scan(session):
            pass

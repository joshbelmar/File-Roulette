#!/usr/bin/env python3

"""Create a `proxies.txt` file from David Storm's regular PasteBin proxies."""

import requests
from bs4 import BeautifulSoup


def create_session():
    """Create a new Requests session.

    Returns
    -------
    session
        A new Requests session.

    """
    # Create the new Session.
    session = requests.Session()
    # Update the headers to use a default User-Agent.
    headers = {
        "user-agent": (
            # We'll use the Tor Browser agent. It's short.
            "Mozilla/5.0 (Windows NT 6.1; rv:52.0) Gecko/20100101 Firefox/52.0"
        )
    }
    # Update the session headers.
    session.headers.update(headers)
    # Return the session.
    return session


def retrieve_latest_link(session):
    """Poll David Storm's PasteBin page to extract the latest paste URL.

    Parameters
    ----------
    session
        The Requests session used to retrieve the link from PasteBin.

    Returns
    -------
    url
        The URL for the most recently-posted proxy list.

    """
    # Retrieve the page source.
    page_source = session.get("https://pastebin.com/u/DavidStorm").text
    # Parse it with Beautiful Soup.
    soup = BeautifulSoup(page_source, "html.parser")
    # Find the main table and grab the link for latest post.
    latest_pastes = soup.find("table", class_="maintable")
    link = latest_pastes.find("a")
    # Return the latest URL.
    return "https://pastebin.com/raw" + link["href"]


def get_fresh_proxies(verbose=False):
    """Build the list of proxies, then save it to `proxies.txt`."""
    if verbose:
        print("[*] Retrieving latest proxy list...")
    # Create an empty proxy list.
    proxies = list()
    # Create a new session.
    session = create_session()
    try:
        # Retrieve the source code of the latest proxy list.
        page_source = session.get(
            retrieve_latest_link(session), timeout=5
        ).text
    except requests.exceptions.ConnectionError:
        print("Could not establish connection.")
        sys.exit(0)
    except requests.exceptions.Timeout:
        print("Request timed out.")
        sys.exit(0)
    # Parse the page_source and extract the proxies.
    if verbose:
        print("[*] Parsing list and extracting proxies...")
    for line in page_source.split("\n"):
        # Ensure the line contains a live proxy.
        if "LIVE" in line:
            # Split the line into its parts.
            current_line = line.strip().split()
            # Extract the proxy.
            proxy = current_line[2]
            proxies.append(proxy)
            if verbose:
                print("[+] Proxy Added : ", proxy)
    # Write the proxies to the `proxies.txt` file.
    with open("proxies.txt", "w") as proxy_file:
        proxy_file.write("\n".join(proxies))
    if verbose:
        print("[!] Completed! Proxies saved in 'proxies.txt'.")


if __name__ == "__main__":
    # Create the `proxies.txt` file with the latest proxy list.
    get_fresh_proxies(verbose=True)

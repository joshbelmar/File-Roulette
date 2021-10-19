FileRoulette
============
A script to seek and discover random files on various hosting services.

Introduction
------------
File-Roulette began as a toy project on the X9 Security Discord chat. The original goal was to find random uploadfile.io files by testing random urls to see if they were alive. Since then, we've been tweaking and updating the script, and have expanded it into something bigger than we had previously planned. This project is in a state of flux, constantly growing and evolving as we expand our scope and refine our skills.

Contributing
------------
If you're interested in contributing to this project, simply fork it and get to work!

Requirements
------------
* Python 3.5 or newer
* pysocks
* requests
* beautifulsoup4

Installation
------------
To use this software, it is advised that you set up a virtualenv. Once that's done, activate the virtualenv and run `pip install -r requirements.txt`. This will get your environment ready to run the application.

There are two main executable files currently in the root directory:
* `fileroulette.py`: The original FileRoulette script, with threading and support for a couple different targets. This file is outdated, but is being kept for the time being for use as reference as we develop the newer, modular code.
* `roulette.py`: The newer, modular code. Currently it does not support threading and only features one module (targeting uploadfiles.io), but it is under active development and will replace `fileroulette.py` in time.

It is advised that you use the `roulette.py` script instead of the `fileroulette.py` script, as it is under active development and your input can aid us in making the script better!

Usage
-----
To learn how to use the `roulette.py`, simply run the script with the `-h` tag:

    usage: roulette.py [-h] [-a] [-p] [-m MODULE]

    Find random data on various hosting services.

    optional arguments:
      -h, --help  show this help message and exit
      -a          enable random user-agent
      -p          enable proxies (requires a proxies.txt file)
      -d          download a fresh proxies.txt file
      -m MODULE   choose data source module (omit to list available modules)

To see which modules exist, use `./roulette.py` without any arguments at all:

    Find random data on various hosting services.

    Available modules:
    ------------------
    - upfile  find files on uploadfiles.io

    For usage information, type ./roulette.py --help

To enable random User-Agents, use the `-a` tag.

To enable random SOCKS5 proxies, use the `-p` tag. In order for this to work, you'll need to have a proxy list (called `proxies.txt`) in the same directory with `roulette.py`. The proxy list must be formatted with one proxy per line, like this:

    1.2.3.4:5678
    1.2.3.4:5679
    1.2.3.4:5670

To download a fresh proxy list from [David Storm's PasteBin Proxy Page](https://pastebin.com/u/DavidStorm), use the `-d` tag. You can use this tag in conjunction with `-p` to download proxies before running the script, or you can use it without the `-p` tag to download proxies even if you're not going to use them.

The script will only accept SOCKS5 proxies. If you wish to use Tor, you can use the following proxies in your `proxies.txt`:

    127.0.0.1:9050
    127.0.0.1:9150

Port 9050 is used by the default Tor daemon, whereas port 9150 is enabled by the Tor Browser Bundle.

Feedback
--------
If you have any problems, suggestions, or other feedback, please open a new issue with the "Issues" tab above!


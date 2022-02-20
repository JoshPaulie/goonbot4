""" Config file """
"""I'm not super sure what is going on from in this file."""

import os

import dotenv
from rich.console import Console

__version__ = "Beta-2"
dotenv.load_dotenv()


console = Console()
dev_server = 510865274594131968
goon_server = 177125557954281472
all_servers = [dev_server, goon_server]

# User ids
bexli = 177131156028784640

if os.getenv("ENV_NAME") == "DEV":
    all_servers.remove(goon_server)

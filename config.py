""" Config file """

import os

import dotenv
from rich.console import Console

__version__ = "Beta-2"
dotenv.load_dotenv()


console = Console()
dev_server = 510865274594131968
goon_server = 177125557954281472
all_servers = [dev_server, goon_server]


if os.getenv("ENV_NAME") == "DEV":
    all_servers.remove(goon_server)

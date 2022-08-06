
__author__ = "Myron Walker"
__copyright__ = "Copyright 2020, Myron W Walker"
__credits__ = []
__version__ = "1.0.0"
__maintainer__ = "Myron Walker"
__email__ = "myron.walker@gmail.com"
__status__ = "Development" # Prototype, Development or Production
__license__ = "MIT"

import os

import click

HELP_RESULT_DIR = "The results folder where the results will be served from."
HELP_PORT = "The service port to serve result content on."

@click.command("results-server", help="Runs a results server.")
@click.option("--resultdir", required=True, help=HELP_RESULT_DIR)
@click.option("--port", "svcport", required=False, default=8888 ,help=HELP_PORT)
def command_akit_servers_results_server(resultdir, svcport):
    # pylint: disable=unused-import,import-outside-toplevel

    os.environ["AKIT_SERVICE_NAME"] = "testresults"

    # We want to run the scan as a console application so we import the console
    # environment in order to setup the appropriate logging
    import akit.activation.service

    from akit.networking.simplewebserver import SimpleWebServer, SimpleWebContentHandler

    if not os.path.exists(resultdir):
        errmsg = "The result directory specified does not exist. path={}".format(resultdir)
        click.BadArgumentUsage(errmsg)

    SimpleWebContentHandler.index_pages.append("testsummary.html")

    server = SimpleWebServer(("", svcport), resultdir, protocol="HTTP/1.0")

    server.server_start()
    server.serve_forever()

    return

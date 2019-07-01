#!/usr/bin/env python3

"""
🕷️️  🕷️️  🕷️️  🕷️️  🕷️️  🕷️️  🕷️️  🕷️️  🕷️️  🕷️️  🕷️️

🕷️️  🕷️️  🕷️️  Black Widow  🕷️️  🕷️️  🕷️️  🕷️️

🕷️️  🕷️️  🕷️️  🕷️️  🕷️️  🕷️️  🕷️️  🕷️️  🕷️️  🕷️️  🕷️️
"""

import app
import os
import plugins
import sys


VERSION = '1.0.0#alpha'


class AppType:
    CMD = 'CMD'
    GUI = 'GUI'


# Startup
def init(app_type):
    app.utils.helpers.logger.Log.info(app.env.APP_NAME + ' ' + str(app_type) + ' started, PID=' + str(os.getpid()))


# Main function for GUI app
def main_gui():
    init(AppType.GUI)
    # Ignore arguments
    app.gui.main.open()


# Main function for command line app
def main_cmd(arguments):
    init(AppType.CMD)
    if arguments.pcap:
        if arguments.pcap_int is None:
            print('Please, specify an interface! (ex. --pcap-int=wlan0)\n')
            sys.exit(1)
        if arguments.pcap_src is not None:
            src_file = arguments.pcap_src.name
        else:
            src_file = None
        if arguments.pcap_dest is not None:
            dest_file = arguments.pcap_dest.name
        else:
            dest_file = None
        app.utils.sniffing.sniff_pcap(src_file=src_file, interface=arguments.pcap_int, dest_file=dest_file,
                                      filters=arguments.pcap_filters, limit_length=arguments.pcap_limit)
    elif arguments.sql:
        if arguments.sql_url is None:
            print('Please, specify an url! (ex. --sql-url=https://black-widow.io)\n')
            sys.exit(1)
        if arguments.sql_deep:
            app.utils.sql.deep_inject_form(arguments.sql_url)
        else:
            app.utils.sql.inject_form(arguments.sql_url)


# Main function generic app
def main():
    arguments = plugins.args.get_arguments(VERSION)
    if arguments.gui:
        main_gui()
    else:
        main_cmd(arguments)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3

"""
🕷️️  🕷️️  🕷️️  🕷️️  🕷️️  🕷️️  🕷️️  🕷️️  🕷️️  🕷️️

🕷️️  🕷️️  🕷️️  Black Widow  🕷️️  🕷️️  🕷️️

🕷️️  🕷️️  🕷️️  🕷️️  🕷️️  🕷️️  🕷️️  🕷️️  🕷️️  🕷️️
"""

import app
import os
import sys
from app_plugins import args


class AppType:
    CMD = 'CMD'
    GUI = 'GUI'


# Startup
def init(app_type):
    app.utils.helpers.logger.Log.info(app.env.APP_NAME + ' ' + str(app_type) + ' started, PID=' + str(os.getpid()))


# Main function for TEST app
def main_test():
    init(AppType.CMD)
    ip = app.utils.helpers.network.get_ip_address()
    print('ip: ' + str(ip))


# Main function for GUI app
def main_gui():
    init(AppType.GUI)
    app.gui.django_gui()


# Main function for command line app
def main_cmd(arguments):
    init(AppType.CMD)
    if arguments.django:
        django_args = str.split(arguments.django)
        app.utils.helpers.logger.Log.info('Django manager executed')
        app.utils.helpers.logger.Log.info('Django arguments: '+str(django_args))
        app.gui.django_cmd(django_args)
        sys.exit(0)

    elif arguments.pcap:
        if arguments.pcap_int is None:
            print('Please, specify an interface! (ex. --pcap-int=wlan0)\n')
            sys.exit(1)
        app.utils.sniffing.sniff_pcap(src_file=arguments.pcap_src, interface=arguments.pcap_int,
                                      dest_file=arguments.pcap_dest, filters=arguments.pcap_filters,
                                      limit_length=arguments.pcap_limit)
    elif arguments.sql:
        if arguments.sql_url is None:
            print('Please, specify an url! (ex. --sql-url=https://black-widow.io)\n')
            sys.exit(1)
        if arguments.sql_deep:
            app.utils.sql.deep_inject_form(arguments.sql_url, arguments.sql_depth)
        else:
            app.utils.sql.inject_form(arguments.sql_url)


# Main function generic app
def main():
    arguments = args.get_arguments()
    if arguments.gui:
        main_gui()
    elif arguments.test:
        main_test()
    else:
        main_cmd(arguments)


if __name__ == "__main__":
    main()

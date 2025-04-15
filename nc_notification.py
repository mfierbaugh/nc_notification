#! /usr/bin/env python3
#
import ncclient.manager, argparse, signal, sys, logging

parser = argparse.ArgumentParser(description='nc_notification.py: subscribe to netconf notifications')
parser.add_argument('-d','--device', help='Device Hostname',required=True)
parser.add_argument('-u','--username',help='Device Username', required=True)
parser.add_argument('-p','--password',help='Device Password', required=True)
parser.add_argument('-v', '--verbose', action='store_true',
                        help="Exceedingly verbose logging to the console")

#parser.add_argument('-f','--filter',help='xpath filter', required=True)

args = parser.parse_args()

if args.verbose:
        handler = logging.StreamHandler()
        # for l in ['ncclient.transport.session', 'ncclient.operations.rpc']:
        for l in ['ncclient.transport.ssh', 'ncclient.transport.session', 'ncclient.operations.rpc']:
            logger = logging.getLogger(l)
            logger.addHandler(handler)
            logger.setLevel(logging.DEBUG)

username = args.username
password = args.password
device = args.device

m = ncclient.manager.connect_ssh(host=device, port=830,
                                 username=username,
                                 password=password,
                                 allow_agent=False,
                                 look_for_keys=False,
                                 hostkey_verify=False,
                                 timeout=120)
m.create_subscription()

def sigint_handler(signal, frame):
        m.close_session()
        sys.exit(0)

signal.signal(signal.SIGINT, sigint_handler)

while True:
    print('Waiting for next notification')

    # This will block until a notification is received because
    # we didn't pass a timeout or block=False
    n = m.take_notification()
    print(n.notification_xml)
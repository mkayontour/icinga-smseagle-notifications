#!/usr/bin/env python

import urllib
import urllib2
import argparse
import sys

ap = argparse.ArgumentParser()
ap.add_argument("-u", "--username", required=True,
                help="Username of SMSEagle HTTP API")
ap.add_argument("-p", "--password", required=True,
                help="Password for username SMSEagle HTTP API")
ap.add_argument("-c", "--contactname",
                help="Contact defined in addressbook of SMSEagle")
ap.add_argument("-H", "--hostname", required=True,
                help="Hostname of notified problem")
ap.add_argument("-t", "--notification-type", required=True,
                help="Icinga Notification type")
ap.add_argument("-s", "--state", required=True,
                help="Service /Host state")
ap.add_argument("-o", "--output",
                help="Output for Host notifications, Service Output could be to long!")
ap.add_argument("-S", "--service", help="If notification is type service")
ap.add_argument("-e", "--eaglehost", required=True,
                help="SMSEagle HTTP API Host")
ap.add_argument("-P", "--protocol", default="http",
                help="set http protocol: DEFAULT=http")
ap.add_argument("-d", "--date", required=True,
                help="display longdatae output from icinga in sms")
ap.add_argument("-g", "--send_togroup", action='store_true',
                help="Send to group instead to user")
ap.add_argument("-n", "--group_name", help="Group name to send to")
ap.add_argument("-v", "--verbose", action='store_true',
                help="print verbose messages")
ap.add_argument("-V", "--version", help="print version", action='store_true')
args = vars(ap.parse_args())

if args['service']:
    message = '** Service ' + args['notification_type'] + ' on ' + args['hostname'] + '**\n'
    message += args['service'] + ' on ' + args['hostname'] + ' is ' + args['state'] + '! \n'
    message += 'Date: ' + args['date']
else:
    message = '** Host ' + args['notification_type'] + ' ** \n'
    message += args['hostname'] + ' is ' + args['state'] + '! \n'
    message += 'Output: ' + args['output'] + '\n'
    message += 'Date: ' + args['date']

if args['verbose']:
    print message + '\n'

# Build the url query
base_url = args['protocol'] + '://' + args['eaglehost']

if args['send_togroup']:
    base_url += '/index.php/http_api/send_togroup'
    query_args = {'login': args['username'], 'pass': args['password'],
                  'groupname': args['group_name'], 'message': message}
else:
    base_url += '/index.php/http_api/send_tocontact'
    query_args = {'login': args['username'], 'pass': args['password'],
                  'contactname': args['contactname'], 'message': message}
encoded_args = urllib.urlencode(query_args)

if args['verbose']:
    print encoded_args + '\n'

url = base_url + '?' + encoded_args

if args['verbose']:
    print url + '\n'

result = urllib2.urlopen(url).read()

if args['verbose']:
    print result + '\n'

# SMSEagle Response
if 'OK' in result:
        print 'Message sent succesfully to ' + args['contactname'] + '\n'
        sys.exit(0)
else:
        print 'Sending SMS failed: ' + result + '\n'
        sys.exit(1)

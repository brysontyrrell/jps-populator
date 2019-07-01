#!/usr/local/bin/python3

import argparse
from getpass import getpass
import json
import os
import random
import time
import uuid

try:
    from xml.etree import cElementTree as Etree
except ImportError:
    from xml.etree import ElementTree as Etree

import names
import requests


SERIAL_CHAR_SETS = {
    'computer': [
        ['C'],
        ['0', '2', '1', 'P'],
        ['7', '2', 'V', 'M', 'W', 'F', 'Q', 'X'],
        ['K', 'L', 'F', 'G', 'M', 'N', 'J', 'H', 'D', 'P', 'Q', 'R', 'S'],
        ['8', 'G', '5', '7', 'L', 'T', 'M', '2', 'P', '9', 'X', '4', 'K', 'J',
         'D', 'W', 'C', 'H', 'F', 'Q', 'V', 'N', 'R', '3', '6', '1', 'Y'],
        ['1', '9', '0', '7', '5', '2', '6', 'B', 'A', 'P', '4', 'E', '3', 'K',
         'F', 'R', 'G', 'U', 'W', 'C', 'L', 'V', '8', 'J', 'D', 'T', 'X', 'Y',
         'M', 'Z', 'N', 'S', 'H'],
        ['9', 'U', '2', 'S', 'Q', 'H', 'M', 'V', 'Z', 'J', 'G', 'P', 'D', 'N',
         '5', 'Y', 'X', '7', '3', 'E', '6', '0', 'K', 'T', '4', 'L', 'C', 'F',
         '8', 'A', 'B', 'W', '1', 'R'],
        ['4', 'E', 'N', 'C', 'Y', 'H', 'F', 'A', 'G', '1', 'B', '3', '0', '5',
         '8', 'M', 'J', 'W', 'L', 'T', 'S', 'D', 'V', 'P', 'R', 'K', 'U', '6',
         'Z', '2', 'Q', '7', '9', 'X'],
        ['D', 'F', 'G', 'H'],
        ['Y', '6', 'D', 'R', 'H', '5', 'W', 'G', 'F', '0', '8', 'T', 'K', 'V',
         'L', '2', 'N', '3', 'J', '9', '1', 'C', 'Q'],
        ['3', 'T', 'Q', '0', 'Y', 'P', '5', 'V', 'R', '8', '4', '2', 'J', '7',
         '1', 'C', 'M', 'H', 'N', 'D', 'F', '6', 'G', 'W'],
        ['H', '6', 'X', '4', '5', 'W', 'L', 'J', '8', 'G', '3', 'P', '7', 'T',
         'N', '9', '1', 'F', 'M', 'V', '0', 'D', 'R', 'K', '2', 'C', 'Y']
    ],
    'mobile': [
        ['F', 'D', 'C', 'H'],
        ['4', 'L', 'Q', '7', 'M', '3', 'K', 'N', '2', '9', '5', 'C', '8', '1',
         'X', 'Y', '6', '0', 'J', 'F', 'T', 'G', 'D', 'A', 'P', 'R'],
        ['L', 'X', 'T', '8', 'Q', '9', 'K', 'V', 'P', '7', 'R', 'J', 'F', '6',
         'G', 'N', '3', 'M', '5', 'Y', 'W', '4', '1', 'H', '2', 'C', 'D'],
        ['K', 'M', 'L', 'J', 'H', 'G', 'N', 'F', '3', 'P', 'B', 'Q', 'R', 'S',
         'A'],
        ['H', '6', '4', 'C', 'G', 'V', 'J', '5', 'T', 'R', 'N', 'K', 'X', '1',
         'F', 'L', '9', 'Q', '8', 'W', 'M', '2', 'P', 'D', '7', '3', 'Y', 'A'],
        ['J', '1', '2', '8', 'B', 'W', '0', 'C', '4', '7', 'F', '5', '6', 'M',
         '3', 'G', 'A', 'E', 'Q', 'S', 'N', 'R', 'D', 'Z', 'X', '9', 'P', 'K',
         'V', 'Y', 'H', 'U', 'T', 'L'],
        ['3', '2', 'S', 'Y', 'V', 'R', 'M', 'Q', 'F', 'J', '1', '8', '9', 'L',
         '6', 'H', 'W', 'A', '4', '0', 'E', 'T', 'U', '5', 'N', '7', 'X', 'Z',
         'K', 'G', 'B', 'D', 'C', 'P'],
        ['V', '7', 'Z', 'R', 'P', 'C', 'G', '8', 'A', '2', 'J', 'X', 'Q', '4',
         'D', 'E', 'N', 'B', '9', '0', 'H', 'K', 'Y', '3', '6', '1', 'L', 'T',
         '5', 'M', 'W', 'F', 'U', 'S'],
        ['F', 'D', 'G', '9', '7', 'H', '1'],
        ['1', 'C', 'N', 'K', 'F', 'J', '8', 'R', 'T', '2', 'P', 'V', '3', 'L',
         '4', 'H', '5', '0', '6', 'D', 'M', 'X', '9', 'G'],
        ['9', 'M', 'D', '1', 'J', 'H', '8', 'C', '2', 'F', 'P', 'G', 'W', 'T',
         'Y', '5', 'R', 'Q', '7', '3', 'V', 'N', 'K', 'X', 'L', '6', '0'],
        ['6', '5', 'K', '4', 'J', 'W', 'T', '2', '0', 'V', 'M', 'Y', '9', 'N',
         '8', '3', '1', 'H', 'Q', 'L', 'D', 'R', '7', 'P', 'G', 'C', 'F', 'X']
    ]
}

MODEL_IDENTIFIERS = {
    'mac': [
        'Macmini8,1',
        'MacBookAir8,1',
        'MacBookPro15,1',
        'MacBookPro15,2',
        'MacBookPro15,3',
        'iMac19,1',
        'iMac19,2'
    ],
    'ipad': [
        'iPad7,5',
        'iPad7,6',
        'iPad8,1',
        'iPad8,2',
        'iPad8,3',
        'iPad8,4',
        'iPad8,5',
        'iPad8,6',
        'iPad8,7',
        'iPad8,8',
        'iPad11,1',
        'iPad11,2',
        'iPad11,3',
        'iPad11,4'
    ],
    'iphone': [
        'iPhone10,1',
        'iPhone10,2',
        'iPhone10,3',
        'iPhone10,4',
        'iPhone10,5',
        'iPhone10,6',
        'iPhone11,2',
        'iPhone11,6',
        'iPhone11,8'
    ]
}

OS_VERSIONS = {
    'computer': [
        '10.13',
        '10.13.1',
        '10.13.2',
        '10.13.3',
        '10.13.4',
        '10.13.5',
        '10.13.6',
        '10.14',
        '10.14.1',
        '10.14.2',
        '10.14.3',
        '10.14.4',
        '10.14.5'
    ],
    'mobile': [
        '11.0',
        '11.0.1',
        '11.0.2',
        '11.0.3',
        '11.1',
        '11.1.1',
        '11.1.2',
        '11.2',
        '11.2.1',
        '11.2.2',
        '11.2.5',
        '11.2.6',
        '11.3',
        '11.3.1',
        '11.4',
        '11.4.1',
        '12.0',
        '12.0.1',
        '12.1',
        '12.1.1',
        '12.1.2',
        '12.1.3',
        '12.1.4',
        '12.2',
        '12.3',
        '12.3.1',
        '12.3.2'
    ]
}


def generate_random_name(mode):
    """Generate a name a device in the format of 'Device-a12b3c4d5e6f'.
     """
    return f"{mode.capitalize()}-{os.urandom(6).hex()}"


def generate_mac_address():
    """Generate a mock MAC address for a device."""
    return "{:02x}:{:02x}:{:02x}:{:02x}:{:02x}:{:02x}".format(
        random.randint(0, 255),
        random.randint(0, 255),
        random.randint(0, 255),
        random.randint(0, 255),
        random.randint(0, 255),
        random.randint(0, 255)
    )


def generate_serial(mode):
    """Generate a mock serial number for a device based on the input `mode`.

    Valid options are:
      * computer
      * mobile
      """
    return ''.join(
        [random.choice(SERIAL_CHAR_SETS[mode][i]) for i in range(12)]
    )


def generate_uuid():
    """Return a UUID value as a string"""
    return str(uuid.uuid4()).upper()


def generate_ip_address(prefix=None):
    """Generate a mock IP address. Can provide a custom prefix (e.g. '10.100').
    """
    if prefix:
        return prefix + '.' + \
               '.'.join(str(random.randint(0, 255)) for _ in range(2))
    else:
        return '.'.join(str(random.randint(0, 255)) for _ in range(4))


def generate_phone_number():
    return f"555-{random.randint(100,999)}-{random.randint(1000,9999)}"


def generate_user(domain='jamf.com'):
    """Returns a tuple of the following values:
        * full name
        * username
        * email address
        * phone number
      """
    first_name = names.get_first_name()
    last_name = names.get_last_name()
    return (
        f"{first_name.lower()}.{last_name.lower()}",
        f"{first_name} {last_name}",
        f"{first_name.lower()}.{last_name.lower()}@{domain.lower()}",

    )


def get_model_identifier(device):
    """Return a random model ID for a device based on the input `device`.

    Valid options are:
      * mac
      * ipad
      *iphone
    """
    return random.choice(MODEL_IDENTIFIERS[device])


def get_os_version(mode):
    """Return a random OS version for a device based on the input `mode`.

    Valid options are:
      * computer
      * mobile
    """
    return random.choice(OS_VERSIONS[mode])


def generate_timestamps():
    """Generate the following timestamps for an inventory record:
      * The first enrollment will be within 30-60 days.
      * The last enrollment will be within 15-30 days.
      * The last report will be within 24 hours.
      * The last check-in will be within 24 hours (but sooner than last report).

    The last report date will be a random time within one half of the last

    Returns a tuple of the following values:
    """
    def days_to_seconds(days):
        return days * 86400

    now = int(time.time())

    first_enroll = (now - days_to_seconds(random.randint(30, 60))) * 1000
    last_enroll = (now - days_to_seconds(random.randint(15, 30))) * 1000
    last_report = (now - random.randint(0, 86400)) * 1000
    last_checkin = (now - random.randint(0, last_report))

    return first_enroll, last_enroll, last_report, last_checkin


class Device:
    mode = ''
    root = ''

    user = None

    general_attributes = tuple()

    def location_xml(self, root_object):
        if not self.user or not isinstance(self.user, User):
            return

        location = Etree.SubElement(root_object, 'location')
        Etree.SubElement(location, 'username').text = self.user.name
        Etree.SubElement(location, 'realname').text = self.user.full_name
        Etree.SubElement(location, 'real_name').text = self.user.full_name
        Etree.SubElement(location, 'email_address').text = self.user.email_address
        Etree.SubElement(location, 'phone').text = self.user.phone_number
        Etree.SubElement(location, 'phone_number').text = self.user.phone_number

    def custom_xml(self, root_object):
        """Override in child classes. Define XML attributes that are not a part
        of general.
        """
        pass

    def generate_xml(self):
        root = Etree.Element(self.root)
        general = Etree.SubElement(root, 'general')

        for i in self.general_attributes:
            Etree.SubElement(general, i).text = str(getattr(self, i))

        self.custom_xml(root)
        self.location_xml(root)
        return Etree.tostring(root).decode()


class Computer(Device):
    mode = 'computer'
    root = 'computer'

    mdm_capable = 'true'
    platform = 'Mac'

    general_attributes = (
        'name',
        'jamf_version',
        'platform',
        'serial_number',
        'udid',
        'mac_address',
        'alt_mac_address',
        'last_reported_ip',
        'ip_address',
        'report_date_epoch',
        'initial_entry_date_epoch',
        'last_enrolled_date_epoch',
        'last_contact_time_epoch',
        'last_cloud_backup_date_epoch'
    )

    def __init__(self, jamf_version, ip_prefix='10.100', user=None):
        # general
        self.name = generate_random_name(self.mode)
        self.jamf_version = jamf_version

        self.serial_number = generate_serial(self.mode)
        self.udid = generate_uuid()
        self.mac_address = generate_mac_address()
        self.alt_mac_address = generate_mac_address()

        self.last_reported_ip = generate_ip_address()
        self.ip_address = generate_ip_address(ip_prefix)

        timestamps = generate_timestamps()
        self.initial_entry_date_epoch = timestamps[0]
        self.last_enrolled_date_epoch = timestamps[1]
        self.report_date_epoch = timestamps[2]
        self.last_contact_time_epoch = timestamps[3]
        self.last_cloud_backup_date_epoch = timestamps[2]

        # hardware
        self.model_identifier = get_model_identifier('mac')
        self.os_version = get_os_version(self.mode)

        self.user = user

    def custom_xml(self, root_object):
        management = Etree.SubElement(root_object.find('general'), 'remote_management')
        Etree.SubElement(management, 'managed').text = 'true'
        Etree.SubElement(management, 'management_username').text = 'jamfadmin'
        Etree.SubElement(management, 'management_password').text = 'supersecure'

        hardware = Etree.SubElement(root_object, 'hardware')
        Etree.SubElement(hardware, 'make').text = 'Apple'
        Etree.SubElement(hardware, 'model_identifier').text = \
            self.model_identifier
        Etree.SubElement(hardware, 'os_name').text = 'Mac OS X'
        Etree.SubElement(hardware, 'os_version').text = self.os_version


class MobileDevice(Device):
    mode = 'mobile'
    root = 'mobile_device'

    managed = 'true'
    supervised = 'true'

    general_attributes = (
        'name',
        'os_type',
        'os_version',
        'model_identifier',
        'serial_number',
        'udid',
        'ip_address',
        'wifi_mac_address',
        'bluetooth_mac_address',
        'initial_entry_date_epoch',
        'last_enrollment_epoch',
        'last_inventory_update_epoch'
    )

    def __init__(self, device, ip_prefix='10.100', user=None):
        if device.lower() not in ('ipad', 'iphone'):
            raise Exception("Mobile devices must be either 'ipad' or 'iphone'.")

        self.device = device

        self.name = generate_random_name(self.mode)
        self.os_type = 'iOS'  # Update in future to toggle between iOS/iPadOS
        self.os_version = get_os_version(self.mode)

        self.model_identifier = get_model_identifier(self.device)
        self.serial_number = generate_serial(self.mode)
        self.udid = generate_uuid()

        self.ip_address = generate_ip_address(ip_prefix)
        self.wifi_mac_address = generate_mac_address()
        self.bluetooth_mac_address = generate_mac_address()

        timestamps = generate_timestamps()
        self.initial_entry_date_epoch = timestamps[0]
        self.last_enrollment_epoch = timestamps[1]
        self.last_inventory_update_epoch = timestamps[2]

        self.user = user


class User:
    def __init__(self, domain='jamf.com'):
        attributes = generate_user(domain)
        self.name = attributes[0]
        self.full_name = attributes[1]
        self.email_address = attributes[2]
        self.phone_number = generate_phone_number()

    def generate_xml(self):
        root = Etree.Element('user')

        Etree.SubElement(root, 'name').text = self.name
        Etree.SubElement(root, 'full_name').text = self.full_name
        Etree.SubElement(root, 'email').text = self.email_address
        Etree.SubElement(root, 'email_address').text = self.email_address
        Etree.SubElement(root, 'phone_number').text = self.phone_number
        Etree.SubElement(root, 'enable_custom_photo_url').text = 'false'

        return Etree.tostring(root).decode()


class JamfProClient:
    def __init__(self, url, username, password, verify=True):
        if not url.startswith('https://'):
            raise Exception("You must provide a URL beginning with 'https://'")

        self. url = os.path.join(url, 'JSSResource')

        self.session = requests.Session()
        self.session.auth = (username, password)

        self.session.headers = {
            'Accept': 'application/json',
            'Content-Type': 'text/xml'
        }

        self.version = self.get_version()

    def _make_request(self, path, method, data=None):
        resp = self.session.request(
            method,
            os.path.join(self.url, path),
            data=data
        )
        try:
            resp.raise_for_status()
        except requests.HTTPError as err:
            if resp.status_code == 400:
                print('There was an error during this request')
                return None
            else:
                print(f"Error: {err}")
                raise SystemExit(resp.status_code)
        try:
            return resp.json()
        except json.JSONDecodeError:
            return None

    def get_version(self):
        return self._make_request('jssuser', 'get')['user']['version']

    def create_record(self, path, xml):
        return self._make_request(path, 'post', xml)

    def get_all_record_ids(self, path, key):
        return [i['id'] for i in self._make_request(path, 'get')[key]]

    def get_record(self, path, record_id):
        pass

    def delete_record(self, path, record_id):
        uri = f"{path}/id/{record_id}"
        self._make_request(uri, 'delete')


def get_jamf_pro_client():
    url = input("Enter the URL for the server beginning with 'https://': ")
    username = input("Enter the API username: ")
    password = getpass("Enter the API password: ")

    client = JamfProClient(url, username, password)
    print(f"\nSuccessfully connected to Jamf Pro, version {client.version}")
    return client


class CommandHelpFormatter(argparse.RawDescriptionHelpFormatter):
    def _format_action(self, action):
        parts = super(argparse.RawDescriptionHelpFormatter, self)._format_action(action)
        if action.nargs == argparse.PARSER:
            parts = "\n".join(parts.split("\n")[1:])
        return parts


def arguments():
    parser = argparse.ArgumentParser(formatter_class=CommandHelpFormatter)
    subparsers = parser.add_subparsers(title='options')

    # ----- FULL INVENTORY POPULATION -----

    full_populate = subparsers.add_parser(
        'full', help='Quickly create users that are linked to various computer '
                     'and mobile device records'
    )
    full_populate.set_defaults(func=cli_full)

    full_populate.add_argument(
        '--count',
        help='The number of users to create',
        metavar='C',
        type=int,
        default=10
    )

    full_populate.add_argument(
        '--devices',
        help='Create devices of the given type(s)',
        choices=[
            'mac',
            'mac+iphone',
            'mac+ipad',
            'ipad',
            'ipad+iphone',
            'random',
            'all'
        ],
        default='all'
    )

    # ----- COMPUTER INVENTORY POPULATION -----

    computers_only = subparsers.add_parser(
        'computers', help='Manage computer records'
    )
    computers_only.set_defaults(func=cli_computers)

    # ----- MOBILE DEVICE INVENTORY POPULATION -----

    mobile_only = subparsers.add_parser(
        'mobile', help='Manage mobile device records'
    )
    mobile_only.set_defaults(func=cli_mobile)

    # ----- USER RECORD POPULATION -----

    users_only = subparsers.add_parser(
        'users', help='Manage only user records'
    )
    users_only.set_defaults(func=cli_users)

    # ----- INVENTORY DATA PURGE -----

    purge = subparsers.add_parser(
        'purge', help='Mass delete data from Jamf Pro'
    )
    purge.set_defaults(func=cli_purge)
    purge_options = purge.add_mutually_exclusive_group(required=True)

    purge_options.add_argument(
        '--computers',
        help='Purge all computer records',
        action='store_true'
    )

    purge_options.add_argument(
        '--mobile',
        help='Purge all mobile device records',
        action='store_true'
    )

    purge_options.add_argument(
        '--users',
        help='Purge all user records',
        action='store_true'
    )

    purge_options.add_argument(
        '--all',
        help='Purge all computer, mobile device, and user records',
        action='store_true'
    )

    return parser.parse_args()


def cli_full(args, client):
    devices = args.devices.split('+')
    randomize = True if 'random' in devices else False

    def _meets_condition(options):
        if options.intersection(set(devices)):
            if randomize:
                return bool((random.randint(0, 1) == 1))
            else:
                return True
        else:
            return False

    print(f"Creating {args.count} new user records...")
    for _ in range(0, args.count):
        user = User()
        print(f"\nCreating new user: {user.full_name}")
        client.create_record('users', user.generate_xml())

        if _meets_condition({'mac', 'all', 'random'}):
            mac = Computer(client.version, user=user)
            print(f"- Creating new Mac record ({mac.model_identifier})")
            client.create_record('computers', mac.generate_xml())

        if _meets_condition({'ipad', 'all', 'random'}):
            ipad = MobileDevice('ipad', user=user)
            print(f"- Creating new iPad record ({ipad.model_identifier})")
            client.create_record('mobiledevices', ipad.generate_xml())

        if _meets_condition({'iphone', 'all', 'random'}):
            iphone = MobileDevice('iphone', user=user)
            print(f"- Creating new iPhone record ({iphone.model_identifier})")
            client.create_record('mobiledevices', iphone.generate_xml())

    print("\nInventory population job is complete!")


def cli_computers(args, client):
    pass


def cli_mobile(args, client):
    pass


def cli_users(args, client):
    pass


def cli_purge(args, client):

    def _do_purge(label, path, key):
        print(f"\nPurging all {label} records...")
        record_ids = client.get_all_record_ids(path, key)
        print(f"Found {len(record_ids)} {label} records")

        for idx in record_ids:
            print(f"Deleting {label} record {idx}")
            client.delete_record(path, idx)

    if args.computers or args.all:
        _do_purge('computer', 'computers', 'computers')

    if args.mobile or args.all:
        _do_purge('mobile device', 'mobiledevices', 'mobile_devices')

    if args.users or args.all:
        _do_purge('user', 'users', 'users')

    print("\nPurge operation is complete")


def main():
    args = arguments()
    client = get_jamf_pro_client()
    args.func(args, client)
    raise SystemExit(0)


if __name__ == '__main__':
    main()

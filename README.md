# Jamf Pro Populator (jps-populator)

A script to populate a Jamf Pro server with dummy inventory data.

## Setup

`jps-populator` requires Python 3.6+. You can download latest version of Python from https://www.python.org/downloads/.

You can install the required packages using `pipenv` and the included `Pipfile`:
 
```bash
$ cd /path/to/jps-populator
$ pipenv install
```
 
Or, you can install using `pip` and the included `requirements.txt` file.

```bash
$ cd /path/to/jps-populator
$ pip3 install -r requirements.txt
```

## Usage

```text
(jps-populator) bash-3.2$ python jpspopulator.py -h
usage: jpspopulator.py [-h] {full,computers,mobile,users,purge} ...

optional arguments:
  -h, --help            show this help message and exit

options:
    full                Quickly create users that are linked to various
                        computer and mobile device records
    computers           Manage computer records
    mobile              Manage mobile device records
    users               Manage only user records
    purge               Mass delete data from Jamf Pro

```

`jps-populator` will prompt for a Jamf Pro server URL (https only), an API username and password before executing the selected command. Here is an example run:

```text
(jps-populator) bash-3.2$ python jpspopulator.py full --count 5 --devices random
Enter the URL for the server beginning with 'https://': https://myjamf.domain.com
Enter the API username: apiuser
Enter the API password: 

Successfully connected to Jamf Pro, version 10.13.0-t1559772983
Creating 5 new user records...

Creating new user: Lillie Long

Creating new user: Betty Melendez
- Creating new iPad record (iPad8,1)
- Creating new iPhone record (iPhone10,3)

Creating new user: Shirley Ballard
- Creating new iPad record (iPad8,6)

Creating new user: Gloria Brown
- Creating new iPad record (iPad8,2)
- Creating new iPhone record (iPhone10,4)

Creating new user: John Swann
- Creating new iPad record (iPad8,3)
- Creating new iPhone record (iPhone11,2)

Inventory population job is complete!
```

### _full_ command

Create user records equal to the value of `--count`. For each user record devices will be created and assigned to them.

The `--devices` option will limit what type or combination of devices are created for each user.

The default values for this commant are `10` users with one of each devices  (`all`).

```text
(jps-populator) bash-3.2$ python jpspopulator.py full -h
usage: jpspopulator.py full [-h] [--count C]
                            [--devices {mac,mac+iphone,mac+ipad,ipad,ipad+iphone,random,all}]

optional arguments:
  -h, --help            show this help message and exit
  --count C             The number of users to create
  --devices {mac,mac+iphone,mac+ipad,ipad,ipad+iphone,random,all}
                        Create devices of the given type(s)

```

### _purge_ command

Delete user and device records from Jamf Pro.

> THESE ACTIONS ARE DESTRUCTIVE AND ARE NOT REVERSIBLE!

```text
(jps-populator) bash-3.2$ python jpspopulator.py purge -h
usage: jpspopulator.py purge [-h] (--computers | --mobile | --users | --all)

optional arguments:
  -h, --help   show this help message and exit
  --computers  Purge all computer records
  --mobile     Purge all mobile device records
  --users      Purge all user records
  --all        Purge all computer, mobile device, and user records
```

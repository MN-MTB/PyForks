<a href ="https://mn-mtb.com">
  <img src="./doc/PyForks.png"
    title="PyForks" align="left" height=100 length=100 />
    </a>


# PyForks

[![PyForks Tests](https://github.com/cribdragg3r/PyForks/actions/workflows/python-app.yml/badge.svg)](https://github.com/cribdragg3r/PyForks/actions/workflows/python-app.yml)
[![GitHub](https://img.shields.io/github/license/cribdragg3r/PyForks?style=flat-square)](https://github.com/cribdragg3r/PyForks/blob/main/LICENSE)
[![PyPI](https://img.shields.io/pypi/v/PyForks?style=flat-square)](https://pypi.org/project/PyForks/)


Python Trailforks Library (Unofficial) for interacting with Trailforks.com. Help [support](https://github.com/sponsors/cribdragg3r) this project and more.

## About

PyForks has been designed to help me automate much of the manual data aggregation I was doing in order to build metrics for my local city and state trail systems. For example: [wlmt.mn-mtb.com](http://wlmt.mn-mtb.com). The end goal of this project is the ability to make it much easier to pull data down that people are interested in and analyze it in a way that non-technical individuals can digest and understand impact in hopes of additional funding and interest. 

## Installation & Documentation

- Install: `pip install pyforks`
- Documentation: [PyForks.mn-mtb.com](https://PyForks.mn-mtb.com)

### Quick Start
Currently, PyForks can interact with Users and Regions to obtain data that either requires Authentication or No Authentication. Functions that require Auth contain tha `@authorization` decorator which, can be seen in the Documentation.

**Get Information on a User**

```python
from PyForks.user import User
from pprint import pprint

# Get Basic information about a user
tf_u = User()
user_info = tf_u.get_user_info("mnmtb")
pprint(user_info)

# Get the User's Gear
tf_u.username = "<your_username>"
tf_u.password = "<your_password>"
tf_u.login()
user_gear = tf_u.get_user_gear("mnmtb")
pprint(user_gear)

"""
EXAMPLE OUTPUT:
{
  'admin_region': 
    {
    'region_link': 'https://www.trailforks.com/region/minnesota/',
    'region_name': 'Minnesota'
    },
 'city': 'Lakeville',
 'country': 'USA',
 'is_regional_admin': True,
 'profile_link': 'https://www.trailforks.com/profile/mnmtb',
 'recent_ride_locations': ['West Lake Marion Park',
                           'Murphy-Hanrehan Park',
                           'Lebanon Hills',
                           'Spirit Mountain Bike Park',
                           'Battle Creek',
                           'Cottage Grove Bike Park',
                           'Lakeville'],
 'state': 'Minnesota',
 'username': 'mnmtb'}
 """
```

**Get Information on a region**
```python
from PyForks.region import Region
tf_r = Region(username=<username>, password=<password>)
tf_r.login()

# Download All of a regions trails in CSV:
tf_r.download_all_region_trails(region, region_id)

# Download all region ridelogs in csv
tf_r.download_all_region_ridelogs(region)

# Download all region ridecounts in CSV
tf_r.download_region_ridecounts(region)

```

## Contribute

Send all the pull requests you want!

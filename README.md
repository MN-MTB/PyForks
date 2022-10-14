<a href ="https://mn-mtb.com">
  <img src="./doc/PyForks.png"
    title="PyForks" align="left" height=75 length=75 />
    </a>


# PyForks

[![PyForks Tests](https://github.com/cribdragg3r/PyForks/actions/workflows/python-app.yml/badge.svg)](https://github.com/cribdragg3r/PyForks/actions/workflows/python-app.yml)
[![GitHub](https://img.shields.io/github/license/pepperize/cdk-ses-smtp-credentials?style=flat-square)](https://github.com/cribdragg3r/PyForks/blob/main/LICENSE)
[![PyPI](https://img.shields.io/pypi/v/PyForks?style=flat-square)](https://pypi.org/project/PyForks/)


Python Trailforks Library for interacting with Trailforks.com

## About

PyForks has been designed to help me automate much of the manual data aggregation I was doing in order to build metrics for my local city and state trail systems. For example: [wlmt.mn-mtb.com](http://wlmt.mn-mtb.com). The end goal of this project is the ability to make it much easier to pull data down that people are interested in and analyze it in a way that non-technical individuals can digest and understand impact in hopes of additional funding and intrest. 

## Installation & Documentation

- Install: `pip install pyforks`
- Documentation: [PyForks.mn-mtb.com](https://PyForks.mn-mtb.com)

### Quick Start
Currently, PyForks can interact with Users and Regions to obtain data that either requires Authentication or No Authentication. Functions that require Auth contain tha `@authorization` decorator which, can be seen in the Documentation.

**Get Information on a User**

```python
from PyForks.trailforks_user import TrailforksUser
from pprint import pprint

# Get Basic information about a user
tf = TrailforksUser()
user_info = tf.get_user_info("mnmtb")
pprint(user_info)

# Get the User's Gear
tf.username = "<your_username>"
tf.password = "<your_password>"
tf.login()
user_gear = tf.get_user_gear("mnmtb")
pprint(user_gear)
```
  

## Contribute

Send all the pull requests you want!

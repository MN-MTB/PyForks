<a href ="https://mn-mtb.com">
  <img src="docs/_static/PyForks.png"
    title="PyForks" align="left" height=100 length=100 />
    </a>


# PyForks

[![PyForks Tests](https://github.com/MN-MTB/PyForks/actions/workflows/python-app.yml/badge.svg)](https://github.com/MN-MTB/PyForks/actions/workflows/python-app.yml)
[![GitHub](https://img.shields.io/github/license/cribdragg3r/PyForks?style=flat-square)](https://github.com/MN-MTB/PyForks/blob/main/LICENSE)
[![PyPI](https://img.shields.io/pypi/v/PyForks?style=flat-square)](https://pypi.org/project/PyForks/)
[![codecov](https://codecov.io/gh/MN-MTB/PyForks/graph/badge.svg?token=225DIC4PVS)](https://codecov.io/gh/MN-MTB/PyForks)


Python TrailForks Library (Unofficial) for interacting with [TrailForks](Trailforks.com). Help [support](https://account.venmo.com/u/mnmtb) this project and more.

## About

This package uses the [Official TrailForks API](https://www.trailforks.com/about/api). This means that in order to use this package, you must have a valid TrailForks `app_id` and `app_secret`. See the API link to get your keys.

PyForks has been designed to help me automate much of the manual data aggregation I was doing in order to build metrics for my local city and state trail systems. For example: [app.mn-mtb.com](https://app.mn-mtb.com). 

## Installation & Documentation

- Install: `pip install pyforks`
- Documentation: [PyForks.mn-mtb.com](https://PyForks.mn-mtb.com)

### Quick Start

**Get Information on a region**

```python
from PyForks import Region, Trails, Events

app_id = "id"
app_secret = "secret"
west_lake_marion_region_id = 20367
region = Region(app_id=app_id, app_secret=app_secret)
r_data = region.get_region(west_lake_marion_region_id)
```

## Contribute

There's a ton of opportunity to help if you're interestined:

- Create all the pull requests you want to PyForks
- We also have a website (Node, backend Python API): [app.mn-mtb.com](https://app.mn-mtb.com)
- AWS Infrastructre (terraform).
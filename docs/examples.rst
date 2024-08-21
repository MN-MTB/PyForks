Examples
========

This is a collection of examples that show how to use the library. It does not cover every function, but it does cover the most common ones. The examples are broken down into three classes:

- :class:`.Regions` - Trailforks regions.
- :class:`.Trails`  - Trailforks region trails.
- :class:`.Events`  - Events for a region/area.

Regions
-------

Regions for Trailforks can have several layers. It's best to think of them as a tree even though all of them are "Regions". For example, Minnesota (region id: ``3203``) is a region, but so are the many different bike parks/trails within Minnesota, such as Lebanon Hills (region id: ``3438``). There is a geographic hierarchy, but it really does not matter for the API as a region is simply a region as long as it has a region id.

Get Region Information
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python
    :linenos:

    from PyForks import Regions

    region_api = Regions(app_id='your_app_id', app_secret='your_app_secret')
    params = {'filter': 'rid::12345'}
    region_api.get_region(**params)

Get Region Status
~~~~~~~~~~~~~~~~~

.. code-block:: python
    :linenos:

    from PyForks import Regions
    from PyForks.lookups import trail_status_short
    from datetime import datetime
    import time

    regions = Regions(app_id=app_id, app_secret=app_secret)             # Create a new instance of the Regions class

    date_obj = datetime.strptime("2022-01-01", "%Y-%m-%d")              # Create a datetime object
    since_timestamp = int(time.mktime(date_obj.timetuple()))            # Convert the datetime object to a timestamp
    args = {"rids": west_lake_marion_id}                                # Create a dictionary of arguments to pass to the get_region_status method

    region_status = regions.get_region_status(since_timestamp, **args)
    # Columns: id,status,condition,status_ts,last_report_ts,changed
    columns = region_status.get("data", {}).get("updates", {}).get("regions_info", {}).get("columns", [])
    rows = region_status.get("data", {}).get("updates", {}).get("regions_info", {}).get("rows", [])

    for row in rows:
        print(trail_status_short.get(row[1]))
        print(trail_status.get(row[1]))


Trails
------

TBD

Events
------

TBD

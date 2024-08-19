Getting Started
===============

Installation
------------

=======

The library is available on PyPi and can be installed using pip:

.. code-block:: bash
    :linenos:

    pip install pyforks

API Key
-------

=======

To use the Trailforks API you will need to obtain an API key. The top right of the `Trailforks API page <https://www.trailforks.com/about/api/>`_ has instructions on how to obtain an API key.

Usage
-----

=======

This is a collection of examples that demonstrate how to use the library. There are three classes that are used in the examples:

- :class:`.Regions` - Trailforks regions.
- :class:`.Trails`  - Trailforks region trails.
- :class:`.Events`  - Events for a region/area.

Function Parameters
~~~~~~~~~~~~~~~~~~~

Each function allows for ``**kwargs`` given the Trailforks API allows for a wide range of parameters. The parameters are passed as keyword arguments to the function. As such, it will be very common to define a dictionary of parameters and pass it to the function. For example:

.. code-block:: python
    :linenos:

    from PyForks import Regions

    region_api = Regions(app_id='your_app_id', app_secret='your_app_secret')
    params = {'filter': 'rid::12345'}
    region_api.get_region(**params)

Some functions have required parameters. These are defined in the function signature. Trailforks has not defined many of the parameters and filters that could be used, so it is up to the user to ensure the correct parameters are passed based on the limited documentation both on the Trailforks website as well as within these docs. However, for required parameters, the function signature will define them as well.

I've also taken some time to add each REST API and therefore each PyForks function to a swagger.json file:

- `PyForks Swagger <https://github.com/MN-MTB/PyForks/blob/formal/notebooks/swagger.json>`_


Enums
~~~~~

Trailforks has many different Enums that are used by the API to define specific values. All Enums are defined in the :mod:`.lookups` module as dictionaries. Each dictionary is based off of the `offical Trailforks documentation metadata <https://www.trailforks.com/about/metadata/>`_. For example:

.. code-block:: python
    :linenos:

    trail_conditions = {
        0: "Unknown",
        1: "Snow Packed",
        2: "Prevalent Mud",
        3: "Wet",
        4: "Variable",
        5: "Dry",
        6: "Very Dry",
        7: "Snow Covered",
        8: "Freeze/thaw Cycle",
        9: "Icy",
        10: "Snow Groomed",
        11: "Ideal",
        12: "Snow Cover Partial"
    }

    difficulty_short = {
        1: "Access Road/Trail",
        2: "White",
        3: "Green",
        4: "Blue",
        5: "Black",
        6: "Double Black Diamond",
        7: "Secondary Access Road/Trail",
        8: "Proline",
        12: "Lift"
    }


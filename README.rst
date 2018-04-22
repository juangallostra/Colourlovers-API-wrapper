Colourlovers-API-wrapper
========================

.. image:: https://img.shields.io/pypi/v/colourlovers.svg
    :target: https://pypi.org/project/colourlovers/

.. image:: https://img.shields.io/github/issues-pr/juangallostra/Colourlovers-API-wrapper.svg?style=flat-square
    :target: https://github.com/juangallostra/Colourlovers-API-wrapper/pulls

.. image:: https://img.shields.io/github/issues/juangallostra/Colourlovers-API-wrapper.svg?style=flat-square
    :target: https://github.com/juangallostra/Colourlovers-API-wrapper/issues

.. image:: https://img.shields.io/github/contributors/juangallostra/Colourlovers-API-wrapper.svg?style=flat-square
    :target: https://github.com/juangallostra/Colourlovers-API-wrapper


    

Python wrapper for the `API <https://www.colourlovers.com/api>`__
provided by www.colourlovers.com

Requirements
------------

-  Python 3 (Check `elbaschid's
   wrapper <https://github.com/elbaschid/python-colourlovers>`__ if
   using Python 2)
-  Pillow

How to use it
-------------

Import the wrapper
~~~~~~~~~~~~~~~~~~

1. Download the wrapper via ``pip``:
   ``pip install colourlovers``
   Alternatively, clone the repository by typing in a terminal:
   ``git clone https://github.com/juangallostra/Colourlovers-API-wrapper.git``
2. Start a Python terminal session in the directory where you cloned the
   repository
3. Import the wrapper by:

   .. code:: python

           >>> from colourlovers import clapi
           >>> cl = clapi.ColourLovers()

Queries
~~~~~~~

Once we have created the API wrapper object (``cl`` in the present
case) we are ready to query the API. Note that a query, even if it
is for a single object, always returns a list. The ColourLovers API
queries are structured in three levels:

1. Object of the query. The possible query objects are: Color/s,
   Pattern/s, Palette/s, Lover/s or stats. Note that most of the objects
   can be queried in plural or in singular. The wrapper offers a
   different method for each object, all of them being:

   .. code:: python

           >>> cl.search_palette()  # Query for a single palette
           >>> cl.search_pattern()  # Query for a single pattern
           >>> cl.search_color()  # Query for a single color
           >>> cl.search_lover()  # Query for a single user
           >>> cl.search_palettes()  # Query for multiple palettes
           >>> cl.search_patterns()  # Query for multiple patterns
           >>> cl.search_colors()  # Query for multiple colors
           >>> cl.search_lovers()  # Query for multiple users
           >>> cl.search_stats()  # Query for a single pattern

   Each of these methods only accepts keyword arguments. Optionally, a
   first boolean positional argument can be passed specifying whether
   the response of the query should be returned as raw data or as a
   Python object. By default the response of a query will be returned as
   a Python object. Hence, the general form of a query to the API is:

   .. code:: python

           >>> cl.search_patterns(True, kwargs)  # Response will be returned as raw data
           >>> cl.search_patterns(kwargs)  # Response will be returned as a Python object

   We will get back to this later.

2. Type of the query. These are general, normally non-object dependent types.
   However, not all the types are supported by all the objects. The possible
   query types and the keyword used to specify them for each type of object are:

   +------------+-------------+----------------------------------------------------+
   | Object     |   Keyword   |               Value                                |
   +============+=============+====================================================+
   | Palettes   | ``request`` |  ``new``, ``top``, ``random``                      |
   +------------+-------------+----------------------------------------------------+
   | Patterns   | ``request`` |  ``new``, ``top``, ``random``                      |
   +------------+-------------+----------------------------------------------------+
   | Colors     | ``request`` |  ``new``, ``top``, ``random``                      |
   +------------+-------------+----------------------------------------------------+
   | Lovers     | ``request`` |  ``new``, ``top``                                  |
   +------------+-------------+----------------------------------------------------+
   | Palette    | ``id``      | valid id as ``int`` or ``str``                     |
   +------------+-------------+----------------------------------------------------+
   | Pattern    | ``id``      | valid id as ``int`` or ``str``                     |
   +------------+-------------+----------------------------------------------------+
   | Color      | ``hexvalue``| valid hex color value as ``str``                   |
   +------------+-------------+----------------------------------------------------+
   | Lover      | ``username``| valid username ``str``                             |
   +------------+-------------+----------------------------------------------------+
   | Stats      | ``request`` | ``colors``, ``palettes``, ``patterns``, ``lovers`` |   |
   +------------+------------------------------------------------------------------+

   The ``random`` query type is exclusive. When using it, no other
   parameters can be specified. Some examples of valid queries are:

   .. code:: python

           >>> cl.search_patterns(request='new')
           >>> cl.search_colors(request='top')
           >>> cl.search_stats(request='patterns')
           >>> cl.search_palettes(request='random')
           >>> cl.search_pattern(id=1145)
           >>> cl.search_lover(username='whatever')
           >>> cl.search_color(hexvalue='C6C5AC')

3. Object specific query parameters. These depend on the object of the
   query and are also specified as keyword arguments. To see which are
   the parameters supported by each object follow the links to the
   official API page in the following table. Note the differences in the
   available parameters when querying for multiple objects or for a
   single object.

   +-------------+-------------------------------------------------------------+
   | Object      | Supported Types                                             |
   +=============+=============================================================+
   | Palette/s   | `Parameters <https://www.colourlovers.com/api#palettes>`__  |
   +-------------+-------------------------------------------------------------+
   | Pattern/s   | `Parameters <https://www.colourlovers.com/api#patterns>`__  |
   +-------------+-------------------------------------------------------------+
   | Color/s     | `Parameters <https://www.colourlovers.com/api#colors>`__    |
   +-------------+-------------------------------------------------------------+
   | Lover/s     | `Parameters <https://www.colourlovers.com/api#lovers>`__    |
   +-------------+-------------------------------------------------------------+
   | Stats       | `Parameters <https://www.colourlovers.com/api#stats>`__     |
   +-------------+-------------------------------------------------------------+

   Examples of valid queries are:

   .. code:: python

           >>> cl.search_palettes(request='top', keywords='river', numresults=15)
           >>> cl.search_lovers(request='new', orderCol='numVotes')

   Note that the parameters are case-sensitive and that some of them
   expect predefined values. This edge cases are all listed at the
   `official API documentation <https://www.colourlovers.com/api>`__.


Other possible sources for color palettes
-----------------------------------------

1. https://www.colr.org/api.html - (https://www.colr.org/)
2. https://www.pictaculous.com/api/ - (https://www.pictaculous.com/)
3. It is also worth mentioning
   https://github.com/elbaschid/python-colourlovers

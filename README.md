# Colourlovers-API-wrapper
Python wrapper for the [API](http://www.colourlovers.com/api) provided by www.colourlovers.com

## Requirements
* PIL or Pillow
* colorsys

## How to use it

### Import the wrapper

1. First clone the repository by typing in a terminal: ``` git clone https://github.com/juangallostra/Colourlovers-API-wrapper.git```
2. Start a Python terminal session in the directory where you cloned the repository
3. Import the wrapper by: 
	```python
		>>> from colourlovers import CLapi
		>>> cl = CLapi.ColourLovers()
	```
### Queries
Once we have created the API wrapper object (```cl``` in the present case) we are ready to query the API. The ColourLovers API queries are structured in three levels:
1. Object of the query. The possible query objects are: Color/s, Pattern/s, Palette/s, Lover/s or stats. Note that most of the objects can be queried in plural or in singular. The wrapper offers a different method for each object, all of them being:

	```python
		>>> cl.search_palette()  # Query for a single palette
		>>> cl.search_pattern()  # Query for a single pattern
		>>> cl.search_color()  # Query for a single color
		>>> cl.search_lover()  # Query for a single user
		>>> cl.search_palettes()  # Query for multiple palettes
		>>> cl.search_patterns()  # Query for multiple patterns
		>>> cl.search_colors()  # Query for multiple colors
		>>> cl.search_lovers()  # Query for multiple users
		>>> cl.search_stats()  # Query for a single pattern
	```

    Each of these methods only accepts keyword arguments. Optionally, a first boolean positional argument can be passed specifying whether the response of the query should be returned as raw data or as a Python object. By default the response of a query will be returned as a Python object. Hence, the general form of a query to the API is:
	
	```python
		>>> cl.search_patterns(True, kwargs)  # Response will be returned as raw data
		>>> cl.search_patterns(kwargs)  # Response will be returned as a Python object
	```

    We will get back to this later.

2. Type of the query. These are general, non-object dependent types and are specified via the ```request``` keyword. However, not all the types are supported by all the objects. The possible query types for each type of object are:
 
    | Object          | Supported Types                                            |
    | :-------------: | :--------------------------------------------------------: |
    | Palettes        | ```new```, ```top```, ```random``` or None                 |
    | Patterns        | ```new```, ```top```, ```random``` or None                 |
    | Colors          | ```new```, ```top```, ```random``` or None                 |
    | Lovers          | ```new```, ```top```, or None                              |
    | Palette         | None                                                       |
    | Pattern         | None                                                       |
    | Color           | None                                                       |
    | Lover           | None                                                       |
    | Stats           | ```colors```, ```palettes```, ```patterns```, ```lovers``` |

    The ```random``` query type is exclusive. When using it, no other parameters can be specified. Some examples of valid queries are:

	```python
		>>> cl.search_patterns(request='new')
		>>> cl.search_colors(request='top')
		>>> cl.search_stats(request='patterns')
		>>> cl.search_palettes(request='random')
	```
3. Object specific query parameters. These depend on the object of the query and are also specified as keyword arguments. To see which are the parameters supported by each object follow the links to the official API page in the following table. Note the differences in the available parameters when querying for multiple objects or for a single object.
 
    | Object          | Supported Types                                            |
    | :-------------: | :--------------------------------------------------------: |
    | Palette/s       | [Parameters](http://www.colourlovers.com/api#palettes)     |
    | Pattern/s       | [Parameters](http://www.colourlovers.com/api#patterns)     |
    | Color/s         | [Parameters](http://www.colourlovers.com/api#colors)       |
    | Lover/s         | [Parameters](http://www.colourlovers.com/api#lovers)       |
    | Stats           | [Parameters](http://www.colourlovers.com/api#stats)        |

    Examples of valid queries are:
	
	```python
		>>> cl.search_palettes(request='top', keywords='river', numresults=15)
	```


## TO DO
- Make a python wrapper for the colourlovers API (or similar) to get color palettes
 * It consists of two modules (**_Currently working on this_**):
    - ```colourlovers_wrapper.py``` is in charge of making requests to the the API and retrieving its responses. **It still doesn't handle all the possible request that are accepted by the API**. Lack of support for ~~searching with parametres _new_, _top_ and _random_ as well as~~ the _switches_ in Color and Lover searches.)
    - ```colourlovers_data_containers.py``` Implements ~~xml~~ json deserializing for the API responses. (~~if finally using colourlovers API~~) It presents the data returned by the API request as class instances of the specified search type (Colors, Palettes, Patterns, Lovers or Stats). The attributes that this classes have are the data fields returned by the API for that concrete search type (**Work in progress**).
- It would be nice to have a tool to preview and organize the selected colors (The obtained classes from the search now implement a method, ```draw()```, which draws the Pattern, Color or Palette it is called on)

## Other possible sources for color palettes
1. http://www.colr.org/api.html - (http://www.colr.org/)
2. http://www.pictaculous.com/api/ - (http://www.pictaculous.com/)
3. It is also worth mentioning https://github.com/elbaschid/python-colourlovers

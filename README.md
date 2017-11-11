# Colourlovers-API-wrapper
Python wrapper for the [API](http://www.colourlovers.com/api) provided by www.colourlovers.com

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

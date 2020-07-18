# Imports
import collections
import json
from urllib.request import Request, urlopen, URLError
from colourlovers.data_containers import *


# TODO
#       - proper error raising
# 	   	- implement switches (Lover -> ?comments=1)
# DONE 	- implement searches for new, top and random parameters.
# DONE	- check than when random is used no more parameters are used.
# DONE	- valid parameter types when doing unique searches
# 		- unicode to string conversion ? 
# DONE	- stats search
#       - allow search by id in pattern, palette


# API Wrapper
class ColourLovers(object):
    """
    ColourLovers API python wrapper
    """
    def __init__(self):

        self.__API_URL = "http://www.colourlovers.com/api/"
        # When searching for new, top or random use the request keyword in the called search method
        self.__API_REQUEST_KEYWORDS = {
            "palettes": "request",
            "patterns": "request",
            "colors": "request",
            "stats": "request",
            "color": "hexvalue",
            "palette": "id",
            "pattern": "id",
            "lover": "username",
        }
        self.__API_EXCLUSIVE_REQUEST = "random"
        self.__API_REQUEST_TYPE = {
            "colors": set(
                {
                    "new",
                    "top",
                    "random"
                }
            ),
            "palettes": set(
                {
                    "new",
                    "top",
                    "random"
                }
            ),
            "patterns": set(
                {
                    "new",
                    "top",
                    "random"
                }
            ),
            "lovers": set(
                {
                    "new",
                    "top"
                }
            ),
            "stats": set(
                {
                    "colors",
                    "palettes",
                    "patterns",
                    "lovers"
                }
            ),
            "color": set(),
            "palette": set(),
            "pattern": set(),
            "lover": set()
        }
        self.__API_PARAMETERS = {
            "colors": set(
                {
                    "lover",
                    "hueRange",
                    "briRange",
                    "keywords",
                    "keywordExact",
                    "orderCol",
                    "sortBy",
                    "numResults",
                    "resultOffset",
                    "format",
                    "jsonCallback"
                }
            ),
            "palettes": set(
                {
                    "lover",
                    "hueOption",
                    "hex",
                    "hex_logic",
                    "keywords",
                    "keywordExact",
                    "orderCol",
                    "sortBy",
                    "numResults",
                    "resultOffset",
                    "format",
                    "jsonCallback",
                    "showPaletteWidths"
                }
            ),
            "patterns": set(
                {
                    "lover",
                    "hueOption",
                    "hex",
                    "hex_logic",
                    "keywords",
                    "keywordExact",
                    "orderCol",
                    "sortBy",
                    "numResults",
                    "resultOffset",
                    "format",
                    "jsonCallback"
                }
            ),
            "lovers": set(
                {
                    "orderCol",
                    "sortBy",
                    "numResults",
                    "resultOffset",
                    "format",
                    "jsonCallback"
                }
            ),
            "stats": set(
                {
                    "format",
                    "jsonCallback"
                }
            ),
            "color": set(
                {
                    "format",
                    "jsonCallback"
                }
            ),
            "palette": set(
                {
                    "format",
                    "jsonCallback"
                }
            ),
            "pattern": set(
                {
                    "format",
                    "jsonCallback"
                }
            ),
            "lover": set(
                {
                    "comments",
                    "format",
                    "jsonCallback"
                }
            )
        }
        self.__API_SWITCHES = {
            "palette": set({"showPaletteWidths"}),
            "lover": set({"comments"})
        }
        self.__API_ADD_PARAM = ["&", "=", "?", "/"]
        self.__API_COLORS = "colors"
        self.__API_PALETTES = "palettes"
        self.__API_PATTERNS = "patterns"
        self.__API_LOVERS = "lovers"
        self.__API_STATS = "stats"
        self.__API_COLOR = "color"
        self.__API_PALETTE = "palette"
        self.__API_PATTERN = "pattern"
        self.__API_LOVER = "lover"
        self.__ALLOW_FLEXIBLE_REQUEST = [
            "color",
            "palette",
            "lover",
            "pattern",
        ]
        # Public methods
        self.search_colors = self.__public_api_method(self.__API_COLORS, Color)
        self.search_color = self.__public_api_method(self.__API_COLOR, Color)
        self.search_palettes = self.__public_api_method(self.__API_PALETTES, Palette)
        self.search_palette = self.__public_api_method(self.__API_PALETTE, Palette)
        self.search_patterns = self.__public_api_method(self.__API_PATTERNS, Pattern)
        self.search_pattern = self.__public_api_method(self.__API_PATTERN, Pattern)
        self.search_lovers = self.__public_api_method(self.__API_LOVERS, Lover)
        self.search_lover = self.__public_api_method(self.__API_LOVER, Lover)
        self.search_stats = self.__public_api_method(self.__API_STATS, Stats)

    # Private methods
    def __public_api_method(self, search_type, data_container):
        """
        Closure that, given a main search type (patterns, palettes,
        colours, lovers, ...) and the class that will store the
        obtained data from the API response, returns a function that
        will know how to query the API for info of that specific type

        :param search_type: The type of search we want the function to
        perform: patterns, palettes, colors, ...
        :param data_container: The class that will store the data obtained
        from the query to the API
        :return: function that will know how to make queries for the specified
        type and process and store the obtained data
        """
        def _api_search(raw_data=False, **kwargs):
            """
            This method validates the request parameters and, if all
            of them are valid, builds the request and posts it to the
            API. It will return the data obtained from the response either
            as raw data or as a Python object.

            :param raw_data: Specifies how the data from the response
            should be treated. If True, the data is returned as it is obtained
            from the API response without any treatment. If False, the
            corresponding Python object to store the obtained data is created and
            returned
            :param kwargs: query parameters for the specified type of request (Pattern,
            Palette, ...). The keyword is the parameter name and the value is the parameter
            value
            :return: The data obtained from the request, either as raw data or as a
            Python object
            """
            # Validate the type of request (new, top, random, ...) taking into account the
            # type of request (pattern, palette, colour, ...) that is to be performed
            processed_request = self.__process_optional_requests(search_type, **kwargs)
            if type(raw_data) != bool:
                raise ValueError("Invalid parameter "+str(raw_data))

            if not raw_data:
                # if user hasn't asked for the raw data of the API
                # response build container objects. For that, we need
                # the data in json format
                processed_request.kwargs["format"] = "json"
            # Once request type has been validated make the query to the API
            api_response = self.__query(search_type,
                                        processed_request.optional_request,
                                        **processed_request.kwargs).decode()
            # Process the data obtained from the query. We will build container
            # objects by default unless otherwise specified
            containers = self.__process_response(raw_data, api_response, data_container)
            if containers is not None:
                return containers
            else:
                print("The data you asked for could not be retrieved")
        return _api_search

    def __query(self, search_term, optional_request_term, **kwargs):
        """
        Make the API query after checking parameter validity (request type has
        already been validated for the specific search type) and return the obtained
        response as raw data, either in json or xml format.

        :param search_term: the main type of query to be performed from the different
        available types (pattern, palette, lover, color, ...)
        :param optional_request_term: if an optional request term has to be included
        in the query (new, top, random)
        :param kwargs: parameters of the query as keyword arguments where the keyword
        is the parameter name and its value is the parameter value
        :return: the response of the request as raw data in json or xml format
        """
        # Check parameter validity  both by name and type
        try:
            self.__check_args(search_term, **kwargs)
        except ValueError as e:
            print(e)
        # If no errors were raised make the query to the API and return the
        # obtained raw data
        return self.__request(search_term, optional_request_term, **kwargs)

    def __check_args(self, search_term, **kwargs):
        """
        Check the validity of optional request parameters type and name as
        taking into account the type of query (pattern, palette, color, ...)
        to be performed.

        :param search_term: the main type of the query to be performed. It will
        be used to know which is the list of valid parameters.
        :param kwargs: Name and value of the optional parameters
        :return: True if the parameters are valid. Otherwise an exception will be
        raised
        """
        # First check the validity of the type of request
        if search_term not in self.__API_REQUEST_TYPE.keys():
            raise ValueError("Unsupported search " + search_term)
        # Then check the validity of the optional parameters
        elif kwargs is not None:
            # Look for invalid parameter names
            invalid_parameters = set(kwargs.keys()) - self.__API_PARAMETERS[search_term]
            if invalid_parameters:
                raise ValueError("Unsupported search argument/s " + ', '.join(invalid_parameters))
            # Look for invalid parameter value types
            types = [(i, type(value)) for (i, value) in enumerate(kwargs.values())]
            for parameter_type in types:
                if parameter_type[1] not in [list, str, int]:
                    raise ValueError("Unsupported argument value type " + str(parameter_type))
                # If the argument value is a list, the type of all the elements in the list should be
                # a valid type and also, all the values should be of the same type
                elif parameter_type[1] == list:
                    parameter_values_types = [type(parameter_value) for parameter_value in
                                              kwargs.values()[parameter_type[0]]]
                    # Select the type of the first value in list as the parameter type
                    # and look for inconsistencies or invalid types
                    type_selector = parameter_values_types[0]
                    if type_selector not in [str, int]:
                        raise ValueError("Unsupported value type in argument " + str(kwargs.keys()[parameter_type[0]]))
                    for parameter_value_type in parameter_values_types:
                        if parameter_value_type != type_selector:
                            raise ValueError(
                                "Inconsistent value types in argument " + str(kwargs.keys()[parameter_type[0]]))
        return True

    def __request(self, search_term, optional_request_term, **kwargs):
        """
        Build API request url and make the request with the specified parameters.

        :param search_term: the main type of query to be performed from the different
        available types (pattern, palette, lover, color, ...)
        :param optional_request_term: if an optional request term has to be included
        in the query (new, top, random)
        :param kwargs: parameters of the query as keyword arguments where the keyword
        is the parameter name and its value is the parameter value
        :return: the response of the request as raw data in json or xml format
        """
        # build API request
        try:
            api_request_url = self.__API_URL + search_term + optional_request_term
        except:
            api_request_url = self.__API_URL + search_term

        for argument in kwargs.keys():
            # build API parameter specification string
            if type(kwargs[argument]) == list:
                values = ','.join([str(value) for value in kwargs[argument]])
            else:
                values = str(kwargs[argument])
            additional_parameter = self.__API_ADD_PARAM[0] + argument + self.__API_ADD_PARAM[1] + values
            # add parameter to API request
            api_request_url += additional_parameter
        # HTTP API request
        req = Request(api_request_url, headers={'User-Agent': "Magic Browser"})
        # Make request and read response
        try:
            response = urlopen(req)
            data = response.read()
            return data
        except URLError as e:
            print(e)

    def __process_response(self, raw_data, api_response, request_type_class):
        """
        Once a request to the API has been made, process the obtained data 
        and parse it as requested.

        Note: This method returns more than one type of object. It should be
        refactored so that only one type of data is returned.

        :param raw_data: Boolean specifying wether the obtained data should be 
        processed or returned as is 
        :param api_response: Raw data obtained from the API query
        :param request_type_class: The type of data the request asked for
        :return: Either None if no response was obtained, the raw data if
        specified or the data wrapped in container objects 
        """
        if not api_response:
            return None
        if raw_data:
            return api_response
        else:
            parsed_json = json.loads(api_response)
            if type(parsed_json) == dict:
                response_containers = request_type_class(parsed_json)
            else:
                response_containers = []
                for element in parsed_json:
                    response_containers += [request_type_class(element)]
            return response_containers

    def __process_optional_requests(self, search_type, **kwargs):
        """

        :param search_type:
        :param kwargs:
        :return:
        """
        processed_request = collections.namedtuple('Processed_request', ['kwargs', 'optional_request'])
        optional_request_term = None
        # Only process optional request if it is present in the keywords
        valid_keyword = self.__API_REQUEST_KEYWORDS[search_type] or None
        if valid_keyword in kwargs.keys():
            if type(kwargs[valid_keyword]) not in [str, int]:
                raise ValueError("Unsupported request argument type " + str(type(kwargs[valid_keyword])))

            if not self.__validate_optional_request(search_type, kwargs[valid_keyword]):
                raise ValueError("Unsupported request argument/s " + kwargs[valid_keyword])

            optional_request_term = self.__API_ADD_PARAM[3] + str(kwargs[valid_keyword])
            # if the optional request is random/the search is for stats
            # then ignore the rest of arguments since they are not allowed
            if self.__API_EXCLUSIVE_REQUEST == kwargs[valid_keyword] or search_type == self.__API_STATS:
                kwargs = {}
            else:
                del kwargs[valid_keyword]

        return processed_request(kwargs=kwargs, optional_request=optional_request_term)

    def __validate_optional_request(self, search_type, request_value):
        """
        :param search_type:
        :param request_value:
        :return:
        """
        request = set({request_value})
        if bool(request.intersection(self.__API_REQUEST_TYPE[search_type])):
            return True
        elif search_type in self.__ALLOW_FLEXIBLE_REQUEST:
            return True
        return False

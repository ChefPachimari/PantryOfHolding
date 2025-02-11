import requests
import json
import base64

from django.conf import settings

from google.cloud import secretmanager

class KrogerClient():

    def __init__(self):
        """ Initializes the KrogerClient, loads the credentials from the /dev/ directory or from secrets manager
        """
        client_id = None
        client_secret = None
        self.access_token = self.get_access()
        
    def _kroger_request(self, method, endpoint, headers={}, data=None, timeout=5):
        """ Generalizes the HTTP calls to the Kroger API, this is a private function and should not be called directly

        Args:
            method (_type_): HTTP method to use, currently only GET and POST are supported
            endpoint (_type_): API Endpoint to call
            headers (_type_): data to contain any authentication + additional headers.
            data (_type_, optional): data to pass along to the endpoint. Defaults to None.
            timeout (int, optional): timeout default to ensure endpoint doesn't hang. Defaults to 5.

        Raises:
            ValueError: Ensures that the method is either GET or POST
            e: Raises for unsupported HTTP method

        Returns:
            _type_: json response from the API
        """
        endpoint = f"https://api-ce.kroger.com/v1/{endpoint}"
        # merge auth into headers
        headers |= {'Authorization': f'bearer {self.access_token}'}
        try:
            if method == 'GET':
                response = requests.get(endpoint, headers=headers, params=data, timeout=timeout)
            elif method == 'POST':
                response = requests.post(endpoint, headers=headers, data=data, timeout=timeout)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
            
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"HTTP request error: {e}")
            raise e

    def get_access(self):
        """ Gets an access token from the Kroger API, first we pass in the client_id and client_secret to get the access token
        Kroger returns an token which will be used by other requests.  There is a token refresh endpoint not currently utilized

        Raises:
            e: error return getting the access token, likely client_id or client_secret is incorrect

        Returns:
            _string_: just the access token
        """
        if settings.DEBUG:
            with open('dev/creds', 'r') as file:
                creds = json.load(file)
            client_id = creds.get('client_id')
            client_secret = creds.get('client_secret')
        else:
            pass
            # TODO: finish building the GCP secrets manager version, important for production
            # nested method simplifies calling the secret manager since we don't need this outside of this function
            # def access_secret_version(project_id, secret_id, version_id):
            #     client = secretmanager.SecretManagerServiceClient()
            #     name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"
            #     response = client.access_secret_version(request={"name": name})
            #     return response.payload.data.decode("UTF-8")

            # project_id = "your-gcp-project-id"
            # client_id_secret_id = "your-client-id-secret-id"
            # client_secret_secret_id = "your-client-secret-secret-id"
            # version_id = "latest"

            # client_id = access_secret_version(project_id, client_id_secret_id, version_id)
            # client_secret = access_secret_version(project_id, client_secret_secret_id, version_id)
            # client_id = ''
            # client_secret = ''
        encoded_credentials = base64.b64encode(f"{client_id}:{client_secret}".encode('utf-8')).decode('utf-8')
        payload = {
            'grant_type': 'client_credentials',
            'scope': 'product.compact',
        }
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': 'Basic ' + encoded_credentials,
        }
        
        response = requests.post(
            'https://api-ce.kroger.com/v1/connect/oauth2/token',
            headers=headers,
            data=payload
        )
        response.raise_for_status()
        return response.json()['access_token']

    def get_products(self, term, **kwargs):
        """ Gets products based on criteria from Kroger public API.  Currently implementing a subsect of filters
        with kwargs for future expansion.
        Full documentation: https://developer.kroger.com/api-products/api/product-api-partner

        Args:
            term (_tstringype_): required, search term used for Kroger's fuzzy search
        """      
        # the term is the only one we are enforcing currently
        payload = {'filter.term': kwargs['term'],
                'filter.brand': kwargs.get('brand', None),
                'filter.locationId': kwargs.get('location_id', None),
                }
        # Add additional filters from kwargs
        # payload |= kwargs
        response = self._kroger_request('GET', 'products', data=payload)
        return response['data']

    def get_location(self, zipcode):
        """ gets the location of a Kroger store based on a zipcode.  Can be used by get_products to get products in a specific store

        Args:
            zipcode (string): US zipcode to search for Kroger locations

        Returns:
            _list_: list of locations within the radius of the zipcode
        """       
        # for now we're basing off a 25mi radius around a zipcode and only looking for Kroger locations
        # TODO: do we want to expand this to other chains?
        data = {
            'filter.zipCode.near': zipcode,  # TODO: look into other filters, address maybe?
            'filter.radiusInMiles': 25,  # TODO: make this configurable down the road
            'filter.chain': 'Kroger'
        }
        response = self._kroger_request('GET', 'locations', data=data)
        return response['data'][0]

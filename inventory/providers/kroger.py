import requests
import json
import base64

from django.conf import settings

from google.cloud import secretmanager

class KrogerClient():
    
    client_id = None
    client_secret = None

    def _load_credentials(self):
        """ Load the creds from the /dev/ directory or from secrets manager
        """
        if settings.DEBUG:
            with open('dev/creds', 'r') as file:
                creds = json.load(file)
            self.client_id = creds.get('client_id')
            self.client_secret = creds.get('client_secret')
        else:
            # TODO: Finish this skeleton off before deployment for production
            pass
            # project_id = "skeleton"
            # client_id_secret_id = "skeleton"
            # client_secret_secret_id = "skeleton"
            # version_id = "latest"

            # client = secretmanager.SecretManagerServiceClient()
            
            # client_id_name = f"projects/{project_id}/secrets/{client_id_secret_id}/versions/{version_id}"
            # client_secret_name = f"projects/{project_id}/secrets/{client_secret_secret_id}/versions/{version_id}"
            
            # client_id_response = client.access_secret_version(request={"name": client_id_name})
            # client_secret_response = client.access_secret_version(request={"name": client_secret_name})
            
            # self.client_id = client_id_response.payload.data.decode("UTF-8")
            # self.client_secret = client_secret_response.payload.data.decode("UTF-8")

    def _kroger_request(self, method, endpoint, headers, data=None, timeout=5):
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
        try:
            if method == 'GET':
                response = requests.get(endpoint, headers=headers, params=params, timeout=timeout)
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
        # intentionally left blank, please fill in the client_id and client_secret

        # nested method simplifies calling the secret manager since we don't need this outside of this function
        def access_secret_version(project_id, secret_id, version_id):
            client = secretmanager.SecretManagerServiceClient()
            name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"
            response = client.access_secret_version(request={"name": name})
            return response.payload.data.decode("UTF-8")

        project_id = "your-gcp-project-id"
        client_id_secret_id = "your-client-id-secret-id"
        client_secret_secret_id = "your-client-secret-secret-id"
        version_id = "latest"

        client_id = access_secret_version(project_id, client_id_secret_id, version_id)
        client_secret = access_secret_version(project_id, client_secret_secret_id, version_id)
        client_id = ''
        client_secret = ''
        encoded_credentials = base64.b64encode(f"{client_id}:{client_secret}".encode('utf-8')).decode('utf-8')
        payload = {
            'grant_type': 'client_credentials',
            'scope': 'product.compact',
        }
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': 'Basic ' + encoded_credentials,
        }
        
        kroger_request('POST', 'connect/oauth2/token', headers, payload)
        return response['access_token']

    def get_products(self, term, access_token, **kwargs):
        """ Gets products based on criteria from Kroger public API.  Currently implementing a subsect of filters
        with kwargs for future expansion.
        Full documentation: https://developer.kroger.com/api-products/api/product-api-partner

        Args:
            term (_tstringype_): required, search term used for Kroger's fuzzy search
            access_token (string): required, token from get_access
        """
        headers = {'Authorization': f'bearer {access_token}'}
        
        # the term is the only one we are enforcing currently
        payload = {'filter.term': term}
        # Add additional filters from kwargs
        for key, value in kwargs.items():
            params[f'filter.{key}'] = value

        return _kroger_request('GET', 'products', headers=headers, data=payload)

    def get_location(self, zipcode, access_token):
        """ gets the location of a Kroger store based on a zipcode.  Can be used by get_products to get products in a specific store

        Args:
            zipcode (string): US zipcode to search for Kroger locations
            access_token (string): required, token from get_access

        Returns:
            _list_: list of locations within the radius of the zipcode
        """
        headers = {'Authorization': f'bearer {access_token}'}
        
        # for now we're basing off a 25mi radius around a zipcode and only looking for Kroger locations
        # TODO: do we want to expand this to other chains?
        params = {
            'filter.zipCode.near': zipcode,  # TODO: look into other filters, address maybe?
            'filter.radiusInMiles': 25,  # TODO: make this configurable down the road
            'filter.chain': 'Kroger'
        }
        kroger_request('GET', 'locations', headers=headers, params=params)
        api_response = requests.get(api_url, headers=headers, params=params, timeout=5)
        return json.loads(api_response.json())

    # usage samples
    # access_token = get_access()
    # get_location('12345', access_token)
    # get_products('milk', 'Kroger', 0, 10, access_token)


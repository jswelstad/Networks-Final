END_POINT = 'https://us-west-2.aws.data.mongodb-api.com/app/'
END_POINT += 'data-ubxif/endpoint/data/v1'
API_KEY = 'j5Cmx7b9Luv8Yz0TVXcMrKYS8XAE5XJ4uSbNIn8YpnBiqclCGINDmaJ5j8kWSJeV'
DATA_SOURCE = 'Cluster0'
DB_NAME = 'words'
HEADERS = {'Content-Type': 'application/json',
           'Access-Control-Request-Headers': '*',
           'api-key': f'{API_KEY}'}

PAYLOAD = {
    "collection": None,
    "database": DB_NAME,
    "dataSource": DATA_SOURCE
}
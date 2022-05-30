URLS_TO_MONITOR = ['www.skipq.org', 'www.google.com', 'www.facebook.com', 'www.youtube.com', 'www.instagram.com', 'www.yahoo.com']
URL_TO_MONITOR = {
    'url': 'www.skipq.org',
    'url': 'www.google.com',
    'url': 'www.facebook.com',
    'url': 'www.youtube.com',
    'url': 'www.instagram.com',
    'url': 'www.yahoo.com'
}
URL_NAMESPACE = 'Voyager-SaadHassan'
METRIC_NAME_AVAIL = "availibilty"
METRIC_NAME_LAT = 'latency'

THRESHOLD_AVAIL = 1
THRESHOLD_LAT = 0.3

sec_lim = 60
email = "saad.hassan.skipq@gmail.com"


API_URL = "https://vspms1iix6.execute-api.us-west-1.amazonaws.com/prod/url"


API_DATA = {"url" : "www.testme.com"}
API_UPDATE_DATA = {"url" : "www.NEW_PUT_METHOD_TEST.com"} 
import requests
import sys,os
import json
import logging
import logging.handlers
from urllib.parse import urlparse
from requests.exceptions import RequestException

def setup_logger(level):
     logger = logging.getLogger('my_search_command')
     logger.propagate = False # Prevent the log messages from being duplicated in the python.log file
     logger.setLevel(level)
     file_handler = logging.handlers.RotatingFileHandler(os.environ['SPLUNK_HOME'] + '/var/log/splunk/customwebhook_alert.log', maxBytes=25000000, backupCount=5)
     formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
     file_handler.setFormatter(formatter)
     logger.addHandler(file_handler)
     return logger
 
logger = setup_logger(logging.INFO)

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--execute":
        payload = json.loads(sys.stdin.read())
        flattened_payload = flatten_json(payload)
        logger.info(flattened_payload)
        config = payload.get('configuration')
        listurl = config.get('listurl')
        if listurl:
            parsed_url = urlparse(listurl)
            if parsed_url.scheme != "https":
                logger.error("URL scheme must be HTTPS")
                sys.exit(1)
        listheaders = config.get('listheaders')
        listbody = config.get('listbody')
        listheaders = listheaders.encode('utf-8').decode('unicode_escape')
        listbody = listbody.encode('utf-8').decode('unicode_escape')
        logger.debug("Body: {}", repr(listbody))
        event_result = payload.get('result')

        url = listurl
        payload = listbody
        headers = listheaders
        
        logger.info(url)
        headers = json.loads(listheaders)
        flattened_headers = flatten_json(headers)
        logger.info(flattened_headers)
        logger.info("Initiating web request")

        try:
            response = requests.request("POST", url, headers=headers, data=payload)
            response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
            logger.info("Webhook request completed successfully")
            # Process the successful response
            flattened_response = flatten_json(response.text)
            #logger.info(flattened_response)
        except requests.exceptions.HTTPError as http_err:
            logger.info("HTTP error")
            logger.info(http_err)
        except requests.exceptions.ConnectionError as conn_err:
            logger.info("Conn error")
            logger.info(conn_err)
        except requests.exceptions.Timeout as timeout_err:
            logger.info("Time out error")
            logger.info(timeout_err)
        except RequestException as req_err:
            logger.info("Req error")
            logger.info(req_err)
        except Exception as err:
            logger.info("other errors")
            logger.info(err)

def flatten_json(json_object):
  """Flattens a JSON object into a single line string."""
  return json.dumps(json_object)

if __name__ == "__main__":
    main()
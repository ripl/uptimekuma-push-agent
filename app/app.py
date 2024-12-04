import os
import time
import schedule
import requests
import argparse
import pingparsing
import logging
import sys


DEFAULT_PUSH_INTERVAL = int(os.getenv("PUSH_INTERVAL", default=60))
DEFAULT_PUSH_URL = os.getenv("PUSH_URL", default=None)
DEFAULT_PING_IP = os.getenv("PING_IP", default="8.8.8.8")


# The program has been updated to incorporate the use of ping following:
# https://github.com/carlbomsdata/uptime-kuma-agent/tree/main

def main(isp, push_url, ping, transmitter):

    # Perform the ping test and extract the average ping time
    try:
        result = transmitter.ping()
        ping_result = ping.parse(result).as_dict()["rtt_avg"]
    except Exception as e:
        logging.error(f"Ping failed: {e}")
        ping_result = 'N/A'

    # Construct the request URL with the dynamic ping value
    url = f"{push_url}?status=up&msg=OK\&ping={ping_result}"

    logging.info(f"FULL_URL: {url}")

    # Execute the HTTP request
    try:
        response = requests.get(url)
        logging.info(f"CURL command executed. Response status: {response.status_code}, Response body: {response.text}")
    except Exception as e:
        logging.error(f"Failed to execute CURL command: {e}")


if __name__ == "__main__":

    # Parse command-line arguments
    parser = argparse.ArgumentParser(description='Push-based agent for Uptime Kuma that sends the results of pinging an ISP')
    parser.add_argument('--isp', type=str, help='ISP server to ping', default=DEFAULT_PING_IP)
    parser.add_argument('--push_url', type=str, help='Base URL for the HTTP request', default=DEFAULT_PUSH_URL)
    parser.add_argument('--push_interval', type=int, help='Interval time in seconds to rerun the script', default=DEFAULT_PUSH_INTERVAL)

    args = parser.parse_args()

    # Redirect logging stdtout and let Docker handle the logging
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

    isp = args.isp
    push_url = args.push_url
    push_interval = args.push_interval
    
    logging.info("Starting agent...")
    logging.info(f"ISP: {isp}")
    logging.info(f"PUSH_URL: {push_url}")
    logging.info(f"PUSH_INTERVAL: {push_interval}")


    # Exit if push_url was not provided
    if not isp:
        logging.error("No ISP provided. Please provide an ISP to ping.")
    if not push_url:
        logging.error("Script terminated due to missing push_url.")
        sys.exit(1)


    # Instantiate the ping interface
    ping = pingparsing.PingParsing()
    transmitter = pingparsing.PingTransmitter()
    transmitter.destination = isp
    transmitter.count = 1

    # call main at startup
    main(isp, push_url, ping, transmitter)   
    schedule.every(push_interval).seconds.do(main,isp=isp, push_url=push_url, ping=ping, transmitter=transmitter)
  
    while True:
        schedule.run_pending()
        time.sleep(1)
import requests
import time


def requests_debugger(url, headers, proxies=None, retry=2):
    try:
        response = requests.get(url=url, headers=headers, proxies=None, timeout=10)  # Change None to proxies if you
        # need to connect proxy
        print(f'[SUCCESS] {url} {response.status_code}')  # If the attempt was fortunate, print message
        return response
    except Exception as ex:
        if retry > 1:
            time.sleep(20)  # Delay between attempts to send a retry request; 30 seconds should be enough
            print(f'[ERROR] => ex: retries left: {retry} => {url}')
            return requests_debugger(url, headers, proxies=proxies, retry=(retry - 1))  # Recursion / Next retry
        elif retry == 1:
            print(f'[ERROR]: retries left: {retry} => {url}')
            try:
                response = requests.get(url=url, headers=headers, proxies=proxies, timeout=10)
                print(f'[INFO] {proxies} => SUCCESS')
                return response
            except Exception:
                raise

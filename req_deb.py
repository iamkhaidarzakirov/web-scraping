import requests
import time


def requests_debugging(url, headers, retry=5):
    try:
        response = requests.get(url=url, headers=headers)
        print(f'[+] {url} {response.status_code}')  # If the attempt was fortunate, print message
    except Exception as ex:
        ex = str(ex).split(':')[0]  # The exception's main short information
        time.sleep(30)  # Delay between attempts to send a retry request; 30 seconds should be enough
        if retry != 0:
            print(f'{ex} | [INFO]: retry={retry} => {url}')
            return requests_debugging(url, headers, retry=(retry - 1))  # Recursion / Next retry
        else:
            raise
    else:
        return response

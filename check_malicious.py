import requests
from config import config
import pyshorteners


def search_url(api_key, url):
    api_url = f"https://www.virustotal.com/vtapi/v2/url/report"
    params = {"apikey": api_key, "resource": url}
    response = requests.get(api_url, params=params)

    if response.status_code == 200:
        result = response.json()
        if result["response_code"] == 1:
            print(f"URL: {url}")
            print(f"Scan Date: {result['scan_date']}")
            print(f"Positives/Total Scans: {result['positives']}/{result['total']}")
            print("Scan Results:")
            for scan, result in result["scans"].items():
                print(f"\t{scan}: {result['result']}")
        else:
            print(f"URL {url} not found in the VirusTotal database.")
    else:
        print(f"Error: {response.status_code}")


def scan_url(api_key, url):
    api_url = "https://www.virustotal.com/vtapi/v2/url/scan"
    params = {"apikey": api_key, "url": url}
    response = requests.post(api_url, data=params)

    if response.status_code == 200:
        result = response.json()
        if result["response_code"] == 1:
            print(f"Scan ID: {result['scan_id']}")
            print("URL submitted for scanning successfully.")
            return result["scan_id"]

        else:
            print(f"Error: {result['verbose_msg']}")
    else:
        print(f"Error: {response.status_code}")


def check_scan_report(api_key, scan_id):
    api_url = "https://www.virustotal.com/vtapi/v2/url/report"
    params = {"apikey": api_key, "resource": scan_id, "allinfo": True}
    response = requests.get(api_url, params=params)

    if response.status_code == 200:
        result = response.json()
        from pprint import pprint

        if result["response_code"] == 1:
            pprint(result)

            # print(f"Scan ID: {result['scan_id']}")
            # print(f"URL: {result['url']}")
            # print(f"Scan Date: {result['scan_date']}")
            # print(f"Positives/Total Scans: {result['positives']}/{result['total']}")
            # print("Scan Results:")
            # for scan, result in result["scans"].items():
            #     print(f"\t{scan}: {result['result']}")
        # else:
        #     print(f"Error: {result['verbose_msg']}")
    else:
        print(f"Error: {response.status_code}")


def unshorted(url):
    s1 = pyshorteners.Shortener()
    expanded_url = s1.tinyurl.expand(url)
    return expanded_url


if __name__ == "__main__":
    # Replace 'YOUR_API_KEY' with your actual VirusTotal API key
    api_key = config.get_vt_api()

    # Replace 'example.com' with the URL you want to search
    url_to_search = "http://tinyurl.com/v9x7dn58"

    # search_url(api_key, url_to_search)
    # scan_id = scan_url(api_key, url_to_search)
    # scan_id = (
    #     "8804341e4574a30898f1f4226fe57c7f7cf8f266fd8877184d16d211ed350ddd-1704861044"
    # )
    # check_scan_report(api_key, scan_id)
    # print(scan_id)
    uri = unshorted(url_to_search)
    print(uri)

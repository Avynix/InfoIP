from curl_cffi import requests
import socket
from IPy import IP

session = requests.Session()

GREEN = "\033[32m"
RED = "\033[31m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
RESET = "\033[0m"
CYAN = "\033[36m"

headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=+;",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Cache-Control": "max-age=0",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
    }

ip_checker_url = "http://ip-api.com/json/"

def get_hostname():
    try:
        while True:
            target_host = input(f"{BLUE}[*] Enter the IP or the hostname: {RESET}").strip()
            if len(target_host) > 0:
                break
            else:
                print(f"{RED}[!] ERROR: No input where found. {RESET}")
        try:
            target_ip = IP(target_host)
        except ValueError:
            target_ip = socket.gethostbyname(target_host)
        return target_ip

    except ValueError:
        print(f"{RED}[!] invalid input. {RESET}")
        exit(1)
    except KeyboardInterrupt:
        print(f"{YELLOW}\n[*] Quiting... {RESET}")
        exit(0)

def scan_ip(ip):
    try:
        full_url = f"{ip_checker_url}{ip}?fields=status,message,country,countryCode,region,regionName,city,zip,lat,lon,timezone,isp,org,as,proxy,query,hosting"
        response = session.get(full_url, headers=headers, impersonate="chrome120", timeout=10)
        status = response.status_code
        if status == 200:
            data = response.json()
            return data
        else:
            print(f"{RED}[!] HTTP Error.{RESET}")
            exit(1)

    except Exception as e:
        print(f"{RED}[!] Error: {e} {RESET}")

def print_data(data):
    try:
        if data.get('status') == "fail":
            print(f"{RED}[!] Failed to trace: {data.get('message')}")
            return

        is_proxy   = data.get('proxy') is True
        is_hosting = data.get('hosting') is True

        query = data.get('query') or "NOT FOUND"
        status = data.get('status') or "NOT FOUND"
        country = data.get('country') or "NOT FOUND"
        countrycode = data.get('countryCode') or "NOT FOUND"
        region = data.get('region') or "NOT FOUND"
        regionname = data.get('regionName') or "NOT FOUND"
        city = data.get('city') or "NOT FOUND"
        zipcode = data.get('zip') or "NOT FOUND"
        lat = data.get('lat') or "NOT FOUND"
        lon = data.get('lon') or "NOT FOUND"
        timezone = data.get('timezone') or "NOT FOUND"
        isp = data.get('isp') or "NOT FOUND"
        org = data.get('org') or "NOT FOUND"
        as_ = data.get('as') or "NOT FOUND"
        proxy = "VPN/TOR/Proxy Detected" if is_proxy else "Residental"
        hosting = "Hosting Server Detected" if is_hosting else "Residental"

        print(f"\n{GREEN}[+] TRACE SUCCESSFUL FOR TARGET: {query} {RESET}")
        print(f"{CYAN}="*45 + f"{RESET}")

        if is_hosting or is_proxy:
            print(f"{YELLOW}[!] WARNING: ANONYMOUS USER (PROXY/VPN/TOR/HOSTING){RESET}")
        else:
            pass
        
        print(f" ├─ [GEOLOCATION] Country  : {RED}{country} ({countrycode}){RESET}")
        print(f" ├─ [GEOLOCATION] Region   : {RED}{regionname}{RESET}")
        print(f" ├─ [GEOLOCATION] City     : {RED}{city} ({zipcode}){RESET}")
        print(f" ├─ [COORDINATES] Lat/Lon  : {RED}{lat}, {lon}{RESET}")
        print(f" ├─ [TIMEZONE]    Zone     : {RED}{timezone}{RESET}")
        print(f" ├─ [NETWORK]     ISP      : {RED}{isp}{RESET}")
        print(f" ├─ [NETWORK]     Org      : {RED}{org}{RESET}")
        print(f" ├─ [NETWORK]     Proxy    : {RED}{proxy}{RESET}")
        print(f" ├─ [NETWORK]     Hosting  : {RED}{hosting}{RESET}")
        print(f" └─ [ROUTING]     AS Info  : {RED}{as_}{RESET}")
    except Exception as e:
        print(f"{RED}[!] Error: {e}{RESET}")

def main():
    try:
        ip = get_hostname()
        data = scan_ip(ip)
        print_data(data)
    except KeyboardInterrupt:
        print(f"{YELLOW}[*] Quiting...")
        exit(1)
    except socket.gaierror:
        print(f"{RED}[!] Failed to find the hostname/IP.{RESET}")

if __name__ == "__main__":
    main()
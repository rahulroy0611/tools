import requests, argparse

parser = argparse.ArgumentParser(description="Check if a subdomain is valid.")
parser.add_argument("-d", help="The subdomain to check")
args = parser.parse_args()

subdomain = args.d

url = f"https://crt.sh/?q={subdomain}&output=json"

response = requests.get(url)
parsed_response = response.json()

subdomain_list = []

for entry in parsed_response:
    subdomain_list.append(entry.get("common_name"))

subdomain_list = list(set(subdomain_list))

for each_entry in subdomain_list:
    print(each_entry)
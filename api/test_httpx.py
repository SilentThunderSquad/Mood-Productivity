import httpx
try:
    client = httpx.Client(proxy="http://example.com")
    print("Success: proxy argument accepted")
except TypeError as e:
    print(f"Error: {e}")

try:
    client = httpx.Client(proxies="http://example.com")
    print("Success: proxies argument accepted")
except TypeError as e:
    print(f"Error: {e}")

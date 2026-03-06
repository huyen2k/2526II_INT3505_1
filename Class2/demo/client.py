import requests


def main():

    url = "http://127.0.0.1:5000/books"

    r = requests.get(url)

    print("Status:", r.status_code)
    print("Cache header:", r.headers.get("Cache-Control"))
    print("Data:", r.json())


if __name__ == "__main__":
    main()

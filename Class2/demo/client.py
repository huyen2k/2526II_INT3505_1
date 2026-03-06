import requests


def main():

    url = "http://127.0.0.1:5000/script"

    r = requests.get(url)

    print("Status:", r.status_code)
    print("Received script:")
    print(r.text)


if __name__ == "__main__":
    main()

import urllib.request
from html.parser import HTMLParser


class MyHTMLParser(HTMLParser):
    def handle_data(self, data):
        if data.strip():
            print(data)


def fetch_and_display(url):
    print(f"\nFetching content from: {url}\n")
    try:
        with urllib.request.urlopen(url) as response:
            html = response.read().decode('utf-8')

        parser = MyHTMLParser()
        parser.feed(html)
    except Exception as e:
        print(f"Failed to fetch content from {url}. Error: {e}")


def main_menu():
    while True:
        print("\nFilos Browse - CMD Web Browser")
        print("1. Enter URL")
        print("2. View Bookmarks (Not Implemented)")
        print("3. History (Not Implemented)")
        print("4. Refresh (Not Implemented)")
        print("5. Exit")

        choice = input("Select an option: ")

        if choice == "1":
            url = input("Enter URL (include http:// or https://): ")
            fetch_and_display(url)
        elif choice == "5":
            print("Exiting Browse...")
            break
        else:
            print("Option not implemented.")


if __name__ == "__main__":
    main_menu()

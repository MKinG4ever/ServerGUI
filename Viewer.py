import urllib.request
import random as r
import time as t
from typing import Dict, List, Any


class Viewer:
    """
    Simple page viewer class using the 'urllib.request' module.

    This class provides functionality to fetch and display the content of a web page.
    It can handle both HTTP and HTTPS protocols.
    """

    def __init__(self, url: str = 'www.example.com', secure: bool = False):
        """
        Initializes the Viewer instance with a URL and protocol type.

        :param url: The web service address (default is 'www.example.com').
        :param secure: A boolean indicating whether to use HTTPS (True) or HTTP (False) (default is False).
        """
        self.url = url
        self.secure = secure
        self.user_agent = self._generate_user_agent()  # Set user_agent
        self.headers = self._generate_headers()  # Set headers

    def __repr__(self) -> str:
        """
        Returns a string representation of the Viewer object.

        :return: String representation of the Viewer object.
        """
        return (f"Viewer Object {self.version}\n"
                f"Address \t:{self.full_url}\n"
                f"User-Agent \t:{self.user_agent}\n"
                f"Headers \t:{self.headers}\n"
                f"Object ID \t:{id(self)}\n")

    @property
    def version(self) -> str:
        """
        Return the version of the Viewer.

        :return: A string representing the version.
        """
        return "Custom v3.2"

    @property
    def full_url(self) -> str:
        """
        Constructs the full URL using the specified protocol (HTTP or HTTPS).

        :return: The full URL as a string.
        """
        protocol = "https" if self.secure else "http"
        return f"{protocol}://{self.url}"

    @property
    def html_present(self):
        return {'Viewer Object': self.version,
                'Target': self.full_url,
                'User-Agent': self.user_agent,
                'Headers': self.headers,
                'Object ID': id(self),
                }

    @staticmethod
    def _generate_user_agent() -> str:
        """
        Generates a random User-Agent string for the request.

        :return: The generated User-Agent string.
        """
        browsers = {
            'chrome': ['91.0.4472.124', '90.0.4430.93', '89.0.4389.82', '88.0.4324.150'],
            'firefox': ['89.0', '88.0', '87.0', '86.0', '85.0'],
            'ie': ['11.0', '10.0', '9.0'],
            'safari': ['14.0.3', '14.0', '13.1']
        }
        browser = r.choice(list(browsers.keys()))
        version = r.choice(browsers[browser])
        os_types = ['Windows', 'Macintosh', 'Linux']
        os_type = r.choice(os_types)

        if browser == 'chrome':
            return f"Mozilla/5.0 ({os_type}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{version} Safari/537.36"
        elif browser == 'firefox':
            return f"Mozilla/5.0 ({os_type}; rv:{version}) Gecko/20100101 Firefox/{version}"
        elif browser == 'ie':
            return f"Mozilla/5.0 (Windows NT {os_type}; Trident/7.0; rv:{version}.0) like Gecko"
        else:  # Safari
            return f"Mozilla/5.0 ({os_type}) AppleWebKit/537.36 (KHTML, like Gecko) Version/{version} Safari/537.36"

    @staticmethod
    def _generate_headers() -> Dict[str, str]:
        """
        Generates randomized headers for the request.

        :return: Dictionary of headers.
        """
        _headers = {
            'Accept-Language': ['en-US', 'en-GB', 'fr-FR', 'de-DE', 'es-ES', 'it-IT', 'pt-PT', 'ja-JP'],
            # Specifies the accepted language of the response
            'Accept-Encoding': ['utf-8'],  # Specifies the accepted content encoding
            'Referer': [f"https://{r.choice(['google.com', 'bing.com', 'yahoo.com', 'facebook.com'])}"],
            # Provides the address of the previous web page
            'Accept': ['text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'],
            # Specifies the media types that are acceptable for the response
            'Cache-Control': [f'max-age={"".join(r.choices("0123456789"))}'],
            # Directs caches not to store a response
            'Connection': ['keep-alive', 'close'],  # Specifies options for maintaining the connection
            'Content-Type': ['application/x-www-form-urlencoded'],  # Indicates the content type of the request body
            'Origin': [f"https://{r.choice(['google.com', 'bing.com', 'yahoo.com', 'facebook.com'])}"],
            # Specifies the origin URL of the request
            'Upgrade-Insecure-Requests': ['1', '2', '3'],  # Instructs the browser to upgrade to HTTPS if possible
            'Pragma': ['cache', 'no-cache'],  # Includes pragma directives that apply to the request
            'If-None-Match': [f'"xyz{int(r.random() * 10 ** 9)}"'],  # Provides a cache validation token
            'Range': ['bytes=0-1023'],  # Requests only the first 1024 bytes of the resource
            'DNT': [f"{r.choice(['1', '0'])}"],  # Indicates the Do Not Track preference
            'X-Forwarded-For': ['.'.join(str(r.randint(0, 255)) for _ in range(4))],
            # Simulates different IP addresses in X-Forwarded-For header
            'X-Requested-With': ['XMLHttpRequest'],  # Indicates that the request is an AJAX request
            'X-Purpose': ['preview'],  # Custom header indicating the purpose of the request
            'X-Custom-Header': ['unknown'],  # Example of a custom header
            'If-Range': [f'{t.strftime(f"%d, %m %b %Y {t.gmtime().tm_hour}:{t.gmtime().tm_min}:%S GMT")}'],
            # Specifies a precondition header
            'Max-Forwards': ['10', '25'],  # Limits the number of proxies or gateways that can forward the request
            'Expect': ['100-continue'],  # Indicates that the client expects a 100 (Continue) response
            'TE': ['trailers'],  # Specifies the transfer encoding the client is willing to accept
            # Example of Authorization header with a placeholder for access token
            'Cookie': [f'sessionid={"".join(r.choices("0123456789abcdef", k=16))}'],
            # Example of Cookie header with a random session ID
            'If-Match': ['*'],  # Specifies the ETag value that the server must match
            'X-Frame-Options': ['DENY'],  # Prevents the page from being rendered in a frame or iframe
            'X-XSS-Protection': ['1; mode=block'],  # Enables XSS filtering in the browser
            'X-Content-Type-Options': ['nosniff'],  # Prevents MIME-sniffing attacks
        }

        # Randomized all headers
        all_headers = {key: r.choice(values) for key, values in _headers.items()}

        # List the dict values
        listed_headers = [{key: val} for key, val in all_headers.items()]

        # Shuffle the list of headers
        r.shuffle(listed_headers)

        # Random number for length of return
        num = r.randint(a=1, b=len(listed_headers))

        # Select shuffled headers from 0 to num
        selected_headers = listed_headers[:num]

        # Combine into single dic again
        combined_headers = {key: val for header in selected_headers for key, val in header.items()}

        # Return limited headers in random order
        return combined_headers

    def _make_request(self, url: str) -> str:
        """
        Makes an HTTP request to fetch the content of the web page.

        :param url: The URL of the web page.
        :return: The content of the web page as a string.
        """
        request = urllib.request.Request(url, headers={**self.headers, 'User-Agent': self.user_agent})
        try:
            with urllib.request.urlopen(request) as response:
                return response.read().decode("utf-8")  # Return page content
        except Exception as e:
            return f"Error: {e}"

    def view_page(self) -> str:
        """
        Fetches and displays the content of the web page specified in the URL.

        :return: The content of the web page as a string or an error message.
        """
        # Make a view and return the page content
        return self._make_request(self.full_url)

    def view_pages(self, views: int, delay: int, verbose: bool = True) -> List[str]:
        """
        Fetches and displays multiple pages with a delay between each view.

        :param views: Number of pages to view.
        :param delay: Delay (in seconds) between each page view.
        :param verbose: If True, print each page's content to console.
        :return: List of page content strings or error messages.
        """
        pages = []  # Storage
        for i in range(views):
            page_content = self.view_page()  # Send request
            pages.append(page_content)
            if verbose:
                # Show first 500 characters of page content in console
                print(f"[{i + 1}:] {page_content[:500]}...")
            t.sleep(delay)  # Interrupt
        # Return the pages
        return pages

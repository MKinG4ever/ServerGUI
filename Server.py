from Viewer import Viewer
import http.server  # Import the HTTP server module
import socketserver  # Import the socket server module
from urllib.parse import parse_qs  # Import to parse POST data
import os  # Import the os module for interacting with the operating system


class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    """
    1xx: Informational responses indicating that the request was received and understood.
    2xx: Success codes indicating that the request was successfully received, understood, and accepted.
    3xx: Redirection codes indicating further action needs to be taken to complete the request.
    4xx: Client error codes indicating that there was an issue with the request (e.g., 404 for Not Found, 403 for Forbidden).
    5xx: Server error codes indicating that there was a problem with the server processing the request (e.g., 500 for Internal Server Error).
    """

    def __init__(self, *args, server_instance=None, **kwargs):
        """
        Initialize the request handler.

        :param args: Positional arguments for the parent class.
        :param server_instance: The server instance, if any.
        :param kwargs: Keyword arguments for the parent class.
        """
        self.server_instance = server_instance  # Assign server instance
        super().__init__(*args, **kwargs)  # Call parent class initializer

    @property
    def version(self):
        """
        Return the version of the request handler.

        :return: A string representing the version.
        """
        return "v2.0"

    @staticmethod
    def present(msg=None, **kwargs):
        _html = str()
        _msg = f"<p>{msg}</p>" if msg is not None else ""
        for key, value in kwargs.items():
            _html += f"<p>{key.title()}: {value}</p>"
        return f"{_msg}<div class='present'>{_html}</div>"

    def secure(self):
        """
        Secure the server by stopping it.
        """
        self.server_instance.stop()

    def send_error(self, code, message=None, **kwargs):
        """
        Send a custom error page for the given error code.

        :param code: The HTTP error code.
        :param message: The error message.
        :param kwargs: Additional keyword arguments.
        """
        # Paths to custom error pages
        error_pages = {
            404: "404.html",  # Path to 404 error page
            403: "403.html",  # Path to 403 error page
            'default': "500.html"  # Path to default error page
        }

        try:
            # Determine the error page based on the code
            error_page = error_pages.get(code, error_pages['default'])

            # Send response and headers
            self.send_response(code)
            self.send_header("Content-type", "text/html")
            self.end_headers()

            # Open and send the corresponding error page
            with open(error_page, 'rb') as file:
                self.wfile.write(file.read())

        except Exception as e:
            # Handle exceptions by sending a 500 error page and printing the error
            self.log_error(f"Error handling error page: {e}")
            self.send_response(500)
            self.send_header("Content-type", "text/plain")
            self.end_headers()

            # Print error in console
            print(e)

            # Show the 500 error page
            with open(error_pages['default'], 'rb') as file:
                self.wfile.write(file.read())

    def handle_reViewer(self):
        """
        Handle custom reViewer logic.
        """
        content_length = int(self.headers['Content-Length'])  # Get the length of the POST data
        post_data = self.rfile.read(content_length).decode('utf-8')  # Read and decode the POST data
        post_params = parse_qs(post_data)  # Parse the POST data

        params = {
            'url': post_params.get('_ip', [''])[0],  # Store the extracted 'url'
            'views': post_params.get('_view', [''])[0],  # Store the extracted 'views'
            'delay': post_params.get('_delay', [''])[0]  # Store the extracted 'delay'
        }

        # Present params
        print(*params.items(), sep='\n')  # DeBug Mode

        # Create 'Viewer Object'
        obj = Viewer(params['url'])

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        with open('monitor.html', 'r') as file:
            page_content = file.read()
            page_content = page_content.replace('<p>Monitor - 01</p>', self.present(msg='Form Data', **params))
            page_content = page_content.replace('<p>Monitor - 02</p>', self.present(msg='Viewer', **obj.html_present))
            self.wfile.write(page_content.encode('utf-8'))

        # Start reViewer
        obj.view_pages(int(params['views']), int(params['delay']))

    def do_POST(self):
        """
        Handle a POST request.
        """
        if self.path == '/secure':
            self.secure()
        elif self.path == '/monitor.html':
            self.handle_reViewer()
        else:
            self.send_error(404)  # Page not found error

    def do_GET(self):
        """
        Handle a GET request.
        """
        super().do_GET()


class MyHTTPServer:
    def __init__(self, ip, port, root_dir, handler_class):
        """
        Initialize the HTTP server.

        :param ip: The IP address to bind the server to.
        :param port: The port to bind the server to.
        :param root_dir: The root directory for the server.
        :param handler_class: The request handler class.
        """
        self.ip = ip  # Server IP address
        self.port = port  # Server port
        self.root_dir = root_dir  # Root directory
        self.handler_class = handler_class  # Request handler class
        self.httpd = socketserver.TCPServer((self.ip, self.port), self.handler_class)  # Create the server

    @property
    def version(self):
        """
        Return the version of the HTTP server.

        :return: A string representing the version.
        """
        return "v2.0"

    def start(self):
        """
        Start the HTTP server.
        """
        os.chdir(self.root_dir)  # Change the root directory
        print(f"[Server] http://{self.ip}:{self.port} |  {self.root_dir}")  # Print server details
        self.httpd.serve_forever()  # Execute the server

    def stop(self):
        """
        Stop the HTTP server.
        """
        if hasattr(self, 'httpd') and self.httpd:
            self.httpd.shutdown()  # Stop the server

from Server import MyHTTPServer, MyHTTPRequestHandler  # Import the custom HTTP server and request handler
import os  # Import the os module for interacting with the operating system
import time  # Import the time module for handling delays
import platform  # Import the platform module to get system information
import random  # Import the random module for generating random numbers


def main():
    """
    Main function to prepare and start the server.
    Timestamp 1719389297.5613282
    Version 1.0
    """
    # Presentation message indicating server preparation
    echo('Preparing the Server on : http://127.0.0.1:1000', delay=0.1, end='\n')

    # Start the server on all nodes
    run_server(ip="0.0.0.0", port=1000)


def run_server(ip="127.0.0.1", port=1000, root_dir=None):
    """
    Function to set up and run the server.

    :param ip: The IP address to bind the server to.
    :param port: The port to bind the server to.
    :param root_dir: The root directory for the server.
    """
    # Determine the current working directory
    current_location = os.getcwd().split('\\') if platform.system() == 'Windows' else os.getcwd().split('/')

    # Default root directory for the server's pages
    _root = f"{'/'.join(current_location)}/pages"

    # Set the root directory to the provided value or use the default
    root_dir = _root if root_dir is None else root_dir

    # Custom error handler with server instance
    handler = lambda *args, **kwargs: MyHTTPRequestHandler(*args, **kwargs, server_instance=server)

    # Create an instance of the custom HTTP server
    server = MyHTTPServer(ip, port, root_dir, handler)

    # Start the server
    server.start()


def echo(msg: str, **kwargs):
    """
    Function to display a message with a typing effect.

    :param msg: The message to be displayed.
    :param kwargs: Additional keyword arguments (delay, end).
    """
    # Setup delay time between characters
    delay = kwargs.get('delay', random.random())

    # Setup end character for print()
    end = kwargs.get('end', '\n')

    # Initialize an empty string for constructing the message
    m = str()

    # Iterate over each character in the input message
    for _ in msg:
        m += _  # Append the character to the message
        print(f"\r{m}", end='')  # Print the echoed message, replacing the previous one
        time.sleep(delay)  # Pause for the specified delay
    print(end=end)  # Move to the next line after echoing all characters


if __name__ == '__main__':
    main()  # Call the main function to start the script

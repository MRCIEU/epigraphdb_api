import socket
from urllib.parse import urlparse


def ping_service(url):
    """Check connection to a url (parsible to hostname and port)."""

    def check_running(ip, port):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.connect((ip, int(port)))
            s.shutdown(2)
            return True
        except socket.gaierror:
            return False

    parsed_uri = urlparse(url)
    return check_running(parsed_uri.hostname, parsed_uri.port)

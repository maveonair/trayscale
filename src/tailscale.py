import http.client
import json
import socket

from typing import Any
from http.client import HTTPConnection

unix_socket_path = "/var/run/tailscale/tailscaled.sock"
base_url = "http://local-tailscaled.sock/localapi/v0"


class TailscaleClient:
    def connect(self) -> None:
        self._set_preference("WantRunning", True)

    def disconnect(self) -> None:
        self._set_preference("WantRunning", False)

    def is_online(self) -> bool:
        status = self.get_tailscale_status()
        return status["Self"]["Online"]

    def get_tailscale_status(self) -> dict[str, Any]:
        url = f"{base_url}/status"
        return self._request(method="GET", url=url)

    def _set_preference(self, key: str, value: str) -> None:
        url = f"{base_url}/prefs"
        paylaod = {
            f"{key}Set": True,
            key: value,
        }

        self._request(method="PATCH", url=url, payload=paylaod)

    def _request(
        self, method: str, url: str, payload: dict[str, Any] = None
    ) -> dict[str, Any]:
        connection = self._get_http_connection()

        try:
            if payload:
                json_data = json.dumps(payload)
                connection.request(method, url, body=json_data, headers={'Content-Type': 'application/json'})
            else:
                connection.request(method, url)

            response = connection.getresponse()
            data = response.read()

            return json.loads(data.decode())
        finally:
            connection.close()

    def _get_http_connection(self) -> HTTPConnection:
        sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        sock.connect(unix_socket_path)

        conn = HTTPConnection("local-tailscaled.sock", timeout=5)
        conn.sock = sock

        return conn

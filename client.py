import tempfile
from pathlib import Path

import requests


class Client:
    def __init__(self, url: str):
        self.url = url
        self.session = requests.Session()

    def request(self, method: str, path: str, **kwargs):
        return self.session.request(method, self.url + path, **kwargs)

    def post(self, path: str, **kwargs):
        return self.request("POST", path, **kwargs)

    def get(self, path: str, **kwargs):
        return self.request("GET", path, **kwargs)

    def delete(self, path: str, **kwargs):
        return self.request("DELETE", path, **kwargs)


def main():
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)

        # Create a large file
        large_file = tmpdir / "large_file"
        with large_file.open("wb") as f:
            f.write(b"0" * 5 * 1024 * 1024)  # 1 MB

        # Upload the file

        client = Client("http://127.0.0.1:8000")
        response = client.post(
            "/mpu/create",
            json={
                "path": "large_file",
                "num_parts": 5,
            },
        )
        response.raise_for_status()
        data = response.json()
        print(data)

        chunk_size = 1024 * 1024  # 1 MB

        try:
            for i in range(data["num_parts"]):
                with large_file.open("rb") as f:
                    f.seek(i * chunk_size)
                    chunk = f.read(chunk_size)

                response = requests.put(data["creds"][i]["url"], data=chunk)
                response.raise_for_status()

            response = client.post(
                "/mpu/complete",
                json={
                    "path": "large_file",
                    "upload_id": data["upload_id"],
                    "part_ids": [c["headers"]["ETag"] for c in data["creds"]],
                },
            )
        except:
            response = client.post(
                "/mpu/abort",
                json={
                    "path": "large_file",
                    "upload_id": data["upload_id"],
                },
            )
            response.raise_for_status()
            raise


if __name__ == "__main__":
    main()

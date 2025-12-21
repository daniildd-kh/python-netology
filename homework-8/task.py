from http.server import BaseHTTPRequestHandler
from http.server import HTTPServer
import os
from requests import get, put
import urllib.parse
import json


def run(handler_class=BaseHTTPRequestHandler):
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, handler_class)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        httpd.server_close()


def ensure_local_folder(path):
    os.makedirs(path, exist_ok=True)


def ensure_backup_folder(token):
    resp = put(
        "https://cloud-api.yandex.net/v1/disk/resources",
        params={"path": "disk:/Backup"},
        headers={"Authorization": f"OAuth {token}"},
    )
    if resp.status_code not in {201, 409}:
        print("Failed to ensure Backup folder:", resp.status_code, resp.text)


def get_uploaded_names(token, limit=100):
    url = "https://cloud-api.yandex.net/v1/disk/resources"
    params = {
        "path": "disk:/Backup",
        "limit": limit,
        "offset": 0,
        "fields": "_embedded.items.name,_embedded.limit,_embedded.offset,_embedded.total",
    }
    headers = {"Authorization": f"OAuth {token}"}
    names = set()
    while True:
        resp = get(url, params=params, headers=headers)
        if resp.status_code == 404:
            ensure_backup_folder(token)
            return names
        if resp.status_code != 200:
            print("Failed to fetch uploaded files:", resp.status_code, resp.text)
            return names
        data = resp.json()
        embedded = data.get("_embedded", {})
        items = embedded.get("items", [])
        names.update(item.get("name") for item in items if item.get("name"))
        total = embedded.get("total")
        if total is None and len(items) < limit:
            break
        params["offset"] += limit
        if total is not None and params["offset"] >= total:
            break
    return names


class HttpGetHandler(BaseHTTPRequestHandler):
    token = None

    def do_GET(self):
        ensure_local_folder("pdfs")
        uploaded = get_uploaded_names(self.token)

        def fname2html(fname):
            uploaded_class = " uploaded" if fname in uploaded else ""
            return f"""
                <li class="item{uploaded_class}" onclick="fetch('/upload', {{'method': 'POST', 'body': '{fname}'}})">
                    {fname}
                </li>
            """

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write("""
            <html>
                <head>
                    <style>
                        .item {{ padding: 6px 10px; cursor: pointer; }}
                        .uploaded {{ background: rgba(0, 200, 0, 0.25); }}
                    </style>
                </head>
                <body>
                    <ul>
                      {files}
                    </ul>
                </body>
            </html>
        """.format(files="\n".join(map(fname2html, os.listdir("pdfs")))).encode())

    def do_POST(self):
        ensure_local_folder("pdfs")
        content_len = int(self.headers.get('Content-Length'))
        fname = self.rfile.read(content_len).decode("utf-8")
        local_path = f"pdfs/{fname}"
        ya_path = f"disk:/Backup/{urllib.parse.quote(fname)}"
        ensure_backup_folder(self.token)
        resp = get(
            "https://cloud-api.yandex.net/v1/disk/resources/upload",
            params={"path": ya_path, "overwrite": "true"},
            headers={"Authorization": f"OAuth {self.token}"},
        )
        print(resp.text)
        upload_url = json.loads(resp.text).get("href")
        if not upload_url:
            self.send_response(500)
            self.end_headers()
            return
        print(upload_url)
        resp = put(upload_url, files={'file': (fname, open(local_path, 'rb'))})
        print(resp.status_code)
        self.send_response(200)
        self.end_headers()


if __name__ == "__main__":
    token = input("Введите OAuth-токен Яндекс.Диска: ").strip()
    HttpGetHandler.token = token
    run(handler_class=HttpGetHandler)

import threading
import requests
import json
import time

def send_request_async(method, url, headers, body, callback):
    """Runs request in background thread and returns data to callback."""
    def worker():
        try:
            start = time.time()
            response = requests.request(method, url, headers=headers or None, json=body, timeout=30)
            elapsed = round(time.time() - start, 3)

            try:
                pretty_body = json.dumps(response.json(), indent=4, ensure_ascii=False)
            except Exception:
                pretty_body = response.text

            result = {
                "status": response.status_code,
                "headers": dict(response.headers),
                "body": pretty_body,
                "time": elapsed
            }
            callback(result)
        except Exception as e:
            callback({"error": str(e)})

    threading.Thread(target=worker, daemon=True).start()

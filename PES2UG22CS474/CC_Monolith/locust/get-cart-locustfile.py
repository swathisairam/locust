from locust import task, run_single_user, FastHttpUser
from insert_product import login


class AddToCart(FastHttpUser):
    def __init__(self, environment):
        super().__init__(environment)
        self.token = login("test123", "test123").get("token")  # Inline login for brevity

    host = "http://127.0.0.1:5000"
    default_headers = {
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "en-US,en;q=0.5",
        "Connection": "keep-alive",
        "DNT": "1",
        "Sec-GPC": "1",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0",
    }

    @task
    def t(self):
        # Merge token into headers dynamically
        headers = {
            **self.default_headers,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8",
            "Cookie": f"token={self.token}",  # Fixed typo ('Cookies' -> 'Cookie')
            "Referer": "http://127.0.0.1:5000/product/1",
            "Upgrade-Insecure-Requests": "1",
        }

        with self.client.get("/cart", headers=headers, catch_response=True) as resp:
            if resp.status_code == 200:
                resp.success()
            else:
                resp.failure(f"Failed with status code {resp.status_code}")


if __name__ == "__main__":
    run_single_user(AddToCart)
from locust import task, run_single_user
from locust import FastHttpUser


class BrowseUser(FastHttpUser):
    host = "http://127.0.0.1:5000"
    default_headers = {
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "en-US,en;q=0.5",
        "Connection": "keep-alive",
        "DNT": "1",
        "Sec-GPC": "1",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8",
        "Host": "127.0.0.1:5000",
        "Priority": "u=0, i",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "cross-site",
        "Upgrade-Insecure-Requests": "1",
    }

    @task
    def browse_task(self):
        with self.client.get(
            "/browse",
            headers=self.default_headers,
            catch_response=True,
        ) as response:
            if response.status_code != 200:
                response.failure(f"Failed! Status code: {response.status_code}")
            else:
                response.success()

if __name__ == "__main__":
    run_single_user(BrowseUser)

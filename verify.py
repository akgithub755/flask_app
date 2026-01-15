# url_generator.py

import random
from typing import List


class URLGenerator:
    """
    Generates enterprise-scale URL datasets
    """

    FAST = "fast"
    SLOW = "slow"
    FLAKY = "flaky"
    DOWN = "down"

    def __init__(self, base_domain: str = "http://service.local"):
        self.base_domain = base_domain

    def generate(self, total_urls: int) -> List[dict]:
        """
        Generates URLs with simulated behavior types
        """
        urls = []

        for i in range(total_urls):
            service_type = random.choices(
                [self.FAST, self.SLOW, self.FLAKY, self.DOWN],
                weights=[60, 20, 15, 5]
            )[0]

            urls.append({
                "url": f"{self.base_domain}/api/service/{i}",
                "service_type": service_type
            })

        return urls


if __name__ == "__main__":
    generator = URLGenerator()
    urls = generator.generate(1000)

    for u in urls[:10]:
        print(u)

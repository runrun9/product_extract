import subprocess


if __name__ == "__main__":
    filename = "product_data.csv"
    subprocess.call(["scrapy", "crawl", "main", "-o", filename])

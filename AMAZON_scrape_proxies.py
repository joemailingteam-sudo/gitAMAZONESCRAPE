import asyncio
import csv
import json
import random

from playwright.async_api import async_playwright

import requests

# Use your Web Unblocker credentials here.
USERNAME, PASSWORD = "USERNAME", "PASSWORD"

# Define proxy dict.
proxies = {
    "http": f"http://{USERNAME}:{PASSWORD}@unblock.oxylabs.io:60000",
    "https": f"https://{USERNAME}:{PASSWORD}@unblock.oxylabs.io:60000",
}

response = requests.request(
    "GET",
    "https://ip.oxylabs.io/location",
    verify=False,  # Ignore the SSL certificate
    proxies=proxies,
)

# Print result page to stdout
print(response.text)

# Save returned HTML to result.html file
with open("result.html", "w") as f:
    f.write(response.text)

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"
)

BASE_DOMAIN = "https://www.amazon.eg"


async def scrape_amazon(
    query="pressure cooker",
    output="csv",
    max_pages=2,
    playwright_proxy=None,
    headless=True,
):
    products = []
    browser = None

    async with async_playwright() as p:
        try:
            browser = await p.chromium.launch(headless=headless, proxy=playwright_proxy)
            context = await browser.new_context(
                user_agent=USER_AGENT,
                locale="en-US",
            )
            page = await context.new_page()

            for page_num in range(1, max_pages + 1):
                print(f"Scraping page {page_num}...")
                url = f"{BASE_DOMAIN}/-/en/s?k={query}&page={page_num}"

                try:
                    await page.goto(url, wait_until="domcontentloaded", timeout=60000)
                except Exception as e:
                    print(f"Failed to load page {page_num}: {e}")
                    break

                # Detect CAPTCHA / block page before assuming "no products"
                if (
                    await page.locator(
                        "text=Enter the characters you see below"
                    ).count()
                    > 0
                ):
                    print(f"CAPTCHA hit on page {page_num}. Stopping scrape.")
                    break

                try:
                    await page.wait_for_selector(
                        'div[data-component-type="s-search-result"]',
                        timeout=20000,
                    )
                except Exception:
                    print(f"No products found on page {page_num}. Ending scrape.")
                    break

                # More reliable anchor than presentation classes like s-widget-container
                product_elements = await page.query_selector_all(
                    'div[data-component-type="s-search-result"]'
                )

                for product in product_elements:
                    try:
                        title_element = await product.query_selector(
                            "h2.a-size-base-plus"
                        )
                        price_element = await product.query_selector(
                            "span.a-price-whole"
                        )
                        rating_element = await product.query_selector("span.a-icon-alt")
                        link_element = await product.query_selector(
                            "a.a-link-normal.s-line-clamp-3.s-link-style.a-text-normal"
                        )

                        title = (
                            await title_element.inner_text() if title_element else "N/A"
                        )
                        price = (
                            await price_element.inner_text() if price_element else "N/A"
                        )
                        rating = (
                            await rating_element.get_attribute("aria-label")
                            if rating_element
                            else "N/A"
                        )
                        link = (
                            await link_element.get_attribute("href")
                            if link_element
                            else "N/A"
                        )

                        if link != "N/A" and not link.startswith("http"):
                            link = f"{BASE_DOMAIN}{link}"

                        products.append(
                            {
                                "title": title.strip() if title != "N/A" else title,
                                "price": (
                                    price.strip().replace("\n", "")
                                    if price != "N/A"
                                    else price
                                ),
                                "rating": rating.strip() if rating != "N/A" else rating,
                                "link": link.strip() if link != "N/A" else link,
                            }
                        )

                    except Exception as e:
                        print(f"Error extracting product data: {e}")
                        continue

                if page_num < max_pages:
                    delay = random.uniform(3, 6)
                    print(f"Waiting {delay:.1f}s before next page...")
                    await asyncio.sleep(delay)

        except Exception as e:
            print(f"An error occurred: {e}")

        finally:
            if browser:
                await browser.close()

    # Save data (outside the browser context, still inside the function)
    file_name = f"{query}_product.{output}"

    if output == "csv":
        with open(file_name, "w", newline="", encoding="utf-8") as file:
            fieldnames = ["title", "price", "rating", "link"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(products)

    elif output == "json":
        with open(file_name, "w", encoding="utf-8") as file:
            json.dump(products, file, indent=4, ensure_ascii=False)

    print(f"Successfully scraped {len(products)} products into {file_name}")
    return products


if __name__ == "__main__":
    asyncio.run(
        scrape_amazon(
            query="pressure cooker",
            output="csv",
            max_pages=2,
            headless=False,  # set True once selectors are confirmed working
        )
    )

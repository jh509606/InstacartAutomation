import csv
import re  # Import the re module for regular expressions
import time

from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.connect_over_cdp("http://localhost:9222")
    context = browser.contexts[0]
    page = context.pages[0]
    page.goto("https://www.instacart.com/")
    page.locator('div:text-is("ALDI")').click()

    def read_max_allowed(filepath: str):
        map_item_to_max = {}
        with open(filepath, 'r', newline='') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # Skip the first line (header)

            for row in reader:
                if len(row) == 2:  # Ensure the row has the expected number of columns
                    try:
                        item_name = row[0].strip()
                        max_quantity = int(row[1].strip())
                        map_item_to_max[item_name] = max_quantity
                    except ValueError as e:
                        print(f"Error parsing row: {row}. Skipping. Error: {e}")  # Handle errors during type conversion
                    except IndexError as e:
                        print(f"Error: Missing data in row: {row}. Skipping. Error: {e}")
                else:
                    print(f"Warning: Skipping malformed row: {row} (expected 3 columns).")
        return map_item_to_max

    max_items_allowed_map = read_max_allowed("MaxItemsAllowed.txt")

    def read_items_have_quantity(filepath: str):
        map_item_to_have = {}
        with open(filepath, 'r', newline='') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # Skip the first line (header)

            for row in reader:
                if len(row) == 2:  # Ensure the row has the expected number of columns
                    try:
                        item_name = row[0].strip()
                        item_quantity_have = int(row[1].strip())
                        map_item_to_have[item_name] = item_quantity_have
                    except ValueError as e:
                        print(f"Error parsing row: {row}. Skipping. Error: {e}")  # Handle errors during type conversion
                    except IndexError as e:
                        print(f"Error: Missing data in row: {row}. Skipping. Error: {e}")
                else:
                    print(f"Warning: Skipping malformed row: {row} (expected 3 columns).")
        return map_item_to_have

    items_have_quantity_map = read_items_have_quantity("ItemsQuantity.txt")

    def search_and_add_item(key) -> None:

        needToOrderQuantity = max_items_allowed_map[key] - items_have_quantity_map[key]
        if needToOrderQuantity <=0:
            return
        page.locator("#search-bar-input").fill(key)
        page.keyboard.press("Enter")

        for i in range (0, needToOrderQuantity):
            if i==0:
                    page.get_by_text(re.compile(r"^Add$|^Add to cart$", re.IGNORECASE), exact=True).first.click()
            else:
                page.get_by_role("button", name=re.compile(r"Increment", re.IGNORECASE)).first.click()

    for key in items_have_quantity_map:
        print(f"Adding {max_items_allowed_map[key]-items_have_quantity_map[key]} quantity for item: {key}")
        search_and_add_item(key)

    page.get_by_role("button", name=re.compile(r"View Cart", re.IGNORECASE)).first.click()
    page.get_by_role("button", name=re.compile(r"Go to checkout", re.IGNORECASE)).first.click()
    page.get_by_role("button", name=re.compile(r"Continue to checkout", re.IGNORECASE)).first.click()


    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)

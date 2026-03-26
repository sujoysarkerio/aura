# instagram_creator.py - Core creation logic
import time
import random
import datetime
import csv
import os
from playwright.sync_api import sync_playwright

def load_names():
    if not os.path.exists("names.txt"):
        print("names.txt not found!")
        return []
    with open("names.txt", "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip() and not line.startswith("#")]
    names = []
    for line in lines:
        parts = line.split(maxsplit=1)
        first = parts[0].strip()
        last = parts[1].strip() if len(parts) > 1 else ""
        full = f"{first} {last}".strip()
        names.append((first, last, full))
    return names

def generate_username(first, last):
    base = f"{first.lower()}{last.lower()}"
    base = ''.join(c for c in base if c.isalnum())
    return base + str(random.randint(11, 999))

def generate_password():
    return f"Insta{random.randint(10000,99999)}!{random.randint(100,999)}"

def generate_birthday():
    year = random.randint(1998, 2006)
    month = random.randint(1, 12)
    day = random.randint(1, 28)
    return {"day": str(day), "month": str(month), "year": str(year)}

def create_one_account():
    names = load_names()
    if not names:
        return

    first, last, full_name = random.choice(names)
    email = f"auto{random.randint(10000,99999)}@1secmail.com"
    password = generate_password()
    birthday = generate_birthday()
    username = generate_username(first, last)

    print(f"Creating account: {full_name} | {email} | @{username}")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        page.goto("https://www.instagram.com/accounts/emailsignup/", wait_until="domcontentloaded", timeout=60000)

        # Fill form with maximum robustness
        try:
            page.locator('input[placeholder*="Mobile number or email"]').fill(email)
        except:
            try:
                page.locator('input[placeholder*="email"]').fill(email)
            except:
                page.locator('input[type="text"]').nth(0).fill(email)

        try:
            page.locator('input[placeholder*="Password"]').fill(password)
        except:
            page.locator('input[type="password"]').fill(password)

        # Birthday
        try:
            page.locator('select').filter(has_text="Month").first.select_option(label=birthday["month"])
            page.locator('select').filter(has_text="Day").first.select_option(label=birthday["day"])
            page.locator('select').filter(has_text="Year").first.select_option(label=birthday["year"])
        except:
            pass

        try:
            page.locator('input[placeholder*="Full name"]').fill(full_name)
        except:
            page.locator('input[placeholder*="Name"]').fill(full_name)

        try:
            page.locator('input[placeholder*="Username"]').fill(username)
        except:
            page.locator('input[name*="username"]').fill(username)

        page.get_by_role("button", name="Sign up").click()

        print(f"Submitted → @{username} | {password}")

        input("Enter OTP in browser then press Enter here to continue... ")

        browser.close()

    # Save result
    with open("instagram_results.csv", "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), full_name, email, password, username, "Submitted"])

if __name__ == "__main__":
    create_one_account()

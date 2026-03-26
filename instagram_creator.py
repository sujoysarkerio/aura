import time
import random
import datetime
import csv
import os
from playwright.sync_api import sync_playwright

def load_names():
    if not os.path.exists("names.txt"):
        print("Error: names.txt not found!")
        print("Create names.txt with one 'First Last' per line.")
        exit()
    with open("names.txt", "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip() and not line.startswith("#")]
    names = []
    for line in lines:
        parts = line.split(maxsplit=1)
        first = parts[0].strip()
        last = parts[1].strip() if len(parts) > 1 else ""
        full = f"{first} {last}".strip()
        names.append((first, last, full))
    print(f"Loaded {len(names)} names")
    return names

def generate_username(first, last):
    base = f"{first.lower()}{last.lower()}"
    base = ''.join(c for c in base if c.isalnum())
    return base + str(random.randint(11, 999))

def generate_password():
    return f"Insta{random.randint(10000,99999)}!{random.randint(100,999)}"

def main():
    print("=" * 90)
    print("Instagram Account Creator v12.5 - Final Robust Version")
    print("=" * 90)

    names = load_names()

    password = input("Password for all accounts (press Enter for auto): ").strip()
    if not password:
        password = generate_password()
        print(f"Auto password: {password}")

    accounts = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # Keep visible for control
        context = browser.new_context(
            viewport={"width": 1366, "height": 768},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36"
        )
        page = context.new_page()

        for i, (first, last, full_name) in enumerate(names, 1):
            print(f"\n--- Account {i}/{len(names)} : {full_name} ---")

            page.goto("https://www.instagram.com/accounts/emailsignup/", wait_until="domcontentloaded", timeout=60000)

            email = f"auto{random.randint(10000,99999)}@1secmail.com"

            # ROBUST FIELD FILLING - Multiple fallbacks for your screenshot
            try:
                page.locator('input[placeholder*="Mobile number or email"]').fill(email)
            except:
                try:
                    page.locator('input[placeholder*="email"]').fill(email)
                except:
                    try:
                        page.locator('input[name*="email"]').fill(email)
                    except:
                        page.locator('input[type="text"]').nth(0).fill(email)

            try:
                page.locator('input[placeholder*="Password"]').fill(password)
            except:
                try:
                    page.locator('input[name*="password"]').fill(password)
                except:
                    page.locator('input[type="password"]').fill(password)

            # Birthday dropdowns
            try:
                page.locator('select').filter(has_text="Month").first.select_option(label=str(random.randint(1,12)))
                page.locator('select').filter(has_text="Day").first.select_option(label=str(random.randint(1,28)))
                page.locator('select').filter(has_text="Year").first.select_option(label=str(random.randint(1998,2006)))
            except:
                pass

            # Full name
            try:
                page.locator('input[placeholder*="Full name"]').fill(full_name)
            except:
                try:
                    page.locator('input[placeholder*="Name"]').fill(full_name)
                except:
                    page.locator('input[type="text"]').nth(1).fill(full_name)

            # Username
            username = generate_username(first, last)
            try:
                page.locator('input[placeholder*="Username"]').fill(username)
            except:
                try:
                    page.locator('input[name*="username"]').fill(username)
                except:
                    page.locator('input[type="text"]').nth(2).fill(username)

            # Submit
            try:
                page.get_by_role("button", name="Sign up").click()
            except:
                try:
                    page.locator('button[type="submit"]').click()
                except:
                    page.locator('button').filter(has_text="Sign up").click()

            print(f"Form submitted for {full_name}")
            print(f"Email    : {email}")
            print(f"Username : {username}")
            print(f"Password : {password}")
            print("-" * 80)

            input("Check your temp mail for OTP, complete it in the browser, then press Enter here... ")

            accounts.append([datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), full_name, username, password, "Submitted"])

            if i < len(names):
                time.sleep(10)

        browser.close()

    filename = f"instagram_accounts_{datetime.datetime.now().strftime('%Y%m%d_%H%M')}.csv"
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Timestamp", "Full Name", "Username", "Password", "Status"])
        writer.writerows(accounts)

    print(f"\nAll done! Results saved to {filename}")

if __name__ == "__main__":
    main()

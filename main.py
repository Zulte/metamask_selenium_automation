from browser import Browser


if __name__ == "__main__":
    browser = Browser()
    words = browser.metamask.register_new_wallet()
    print(words)
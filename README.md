# Reddit-Bot-Account-Maker

Reddit Bot Account Maker Documentation by WZCoding

NOTE:
*This is a basic bot. Expect it to do basic things. Please don't abuse it*

This bot creates a random username and password, verifies the email, and views the inbox

REQUIREMENTS:

Linux (Ubuntu)

Python3 (Ubuntu has Python3 preinstalled)

Firefox (Ubuntu has Firefox preinstalled)

2captcha API key (must manually input in code)

Various Libraries (These need to be manually installed)
1. Selenium CMD: pip3 install selenium
2. Tor CMD: sudo apt install tor
3. Requests CMD: pip3 install requests
4. Names CMD: pip3 install names

USAGE:

CMD: python code.py

TROUBLESHOOTING:

Error: Service error
Note: This has to do with the current state of the API that solves captcha. It might be down or very slow.

Error: Unknown error
Note: This can be a variety of things. After all, the web is a changing place and this code doesn't change to account for it.
Most Likely: Could not find captcha. Manually enter user/pass and try again later.
Other Possibility: The code for either old.reddit.com, reddit.com, or getnada.com has changed.
Other Possibility: Actual unknown error.

ADDITIONAL NOTES:

There are set delays in the code that make it sleep. You can change it to be faster/slower, depends on your requirements.
Don't run this in a VM. It won't work as tor won't actually get you a new IP. You must run this on a native Linux computer.

Please visit my Fiverr page if you'd like me to code for you.
https://www.fiverr.com/wzcoding

This project enables automating of Instacart ordering via Playwright in python. It was generally speaking created with vibe coding, with small human input.
It has two files for user to configure(MaxItemsAllowed needs to be configured only once or rarely):
  ItemsQuantity.txt -- Number of items I have at home
  MaxItemsAllowed.txt -- Max number of items allowed for me to have at any point

CommandToStartGoogleChromeAtPort9222.bat file needs to be executed once and then login to Instacart using your own credentials. Playwright can then use that browser instance instead of running automation in isolation where authentication 
could be an issue.
Order.py is the file user needs to execute using python or python3 command: python Order.py


Here’s a step-by-step guide to run your own Telegram bot — perfect for your Gopher Explore Bot project 👇


---

🧭 Step 1 — Create a Telegram Bot

1. Open Telegram and search for @BotFather


2. Type /start


3. Then type /newbot


4. Follow the prompts to:

Give your bot a name

Choose a username (must end with bot, e.g. GopherExploreBot)



5. BotFather will then give you a Bot Token, which looks like this:

1234567890:ABCDefGhIJKlmNoPQRstuVWxyz1234567

> ⚠️ Keep this token private, it gives full access to your bot.






---

🧩 Step 2 — Install Python & Libraries

If you’re using Termux, VSCode, or your PC terminal, run these commands:

# Make sure Python is installed
python --version

# Then install the required packages
pip install python-telegram-bot requests


---

⚙️ Step 3 — Create Your Bot File

Create a new file called bot.py and paste this basic working example:


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

import logging
import os
import json
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('bot.log')
    ]
)
logger = logging.getLogger(__name__)

# Set httpx and telegram logging to WARNING to reduce noise
logging.getLogger('httpx').setLevel(logging.WARNING)
logging.getLogger('telegram').setLevel(logging.WARNING)

# Bot Token - Replace with your bot token
BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "8457913630:AAGHtn4JXN0en9AeDvdRrrvSBCSeB4EVqf8")

# Gopher AI API Configuration
GOPHER_API_TOKEN = os.environ.get("GOPHER_API_TOKEN", "UYfNr7tVRR3u6QrpgNF4lYD5Sf5kfBFXAKU1fGDSfSO0GKjN")
GOPHER_API_BASE = "https://data.gopher-ai.com/api/v1"

# Store user search state
search_states = {}

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handler for /start command"""
    await update.message.reply_text(
        "🔍 Welcome to Gopher Explore Bot! 🔍\n\n"
        "Your AI-powered companion for exploring digital content across platforms.\n\n"
        "I can analyze:\n"
        "🔐 Social media accounts and profiles\n"
        "🔑 Keywords and trends\n"
        "🌐 Web content and websites\n"
        "🎵 TikTok videos and hashtags\n"
        "💬 Reddit posts and discussions\n\n"
        "⚡ Powered by Gopher AI\n"
        "📊 https://data.gopher-ai.com\n\n"
        "🛠️ Commands: /start • /help • /info • /search\n\n"
        "💡 Simply send me usernames, keywords, or URLs to begin exploring!\n\n"
        "🚀 Your digital discovery journey starts here!"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handler for /help command"""
    help_text = (
        "🤖 **Telegram Bot Help**\n\n"
        "Available commands:\n\n"
        "• `/start` - Start bot and display welcome message\n"
        "• `/help` - Show this help message\n"
        "• `/info` - Display bot information\n\n"
        "Bot features:\n"
        "✅ Responds to text messages\n"
        "✅ Echo sent messages\n"
        "✅ Basic text formatting\n\n"
        "This is a basic template that can be further developed."
    )
    await update.message.reply_text(help_text, parse_mode='Markdown')

async def info_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handler for /info command"""
    user = update.effective_user
    chat_info = f"""
📊 **Bot Information**

**Chat Info:**
• Chat ID: {update.effective_chat.id}
• Chat Type: {update.effective_chat.type}
• Chat Name: {update.effective_chat.title or 'Private Chat'}

**User Info:**
• Name: {user.first_name} {user.last_name or ''}
• Username: @{user.username}
• User ID: {user.id}

**Bot Info:**
• Status: 🟢 Online
• Version: 1.0.0
• Framework: python-telegram-bot
    """
    await update.message.reply_text(chat_info, parse_mode='Markdown')

async def search_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handler for /search command"""
    user_id = update.effective_user.id
    
    # Store search state for this user
    search_states[user_id] = {
        'step': 'type_selection',
        'platform': 'twitter'
    }
    
    # Create inline keyboard with search type options
    keyboard = [
        [InlineKeyboardButton("🔍 Search by Query", callback_data="searchbyquery")],
        [InlineKeyboardButton("👤 Search by Profile", callback_data="searchbyprofile")],
        [InlineKeyboardButton("📚 Full Archive Search", callback_data="searchbyfullarchive")],
        [InlineKeyboardButton("🆔 Get by ID", callback_data="getbyid")],
        [InlineKeyboardButton("💬 Get Replies", callback_data="getreplies")],
        [InlineKeyboardButton("🔄 Get Retweeters", callback_data="getretweeters")],
        [InlineKeyboardButton("📝 Get Tweets", callback_data="gettweets")],
        [InlineKeyboardButton("🎬 Get Media", callback_data="getmedia")],
        [InlineKeyboardButton("👥 Get Profile by ID", callback_data="getprofilebyid")],
        [InlineKeyboardButton("📈 Get Trends", callback_data="gettrends")],
        [InlineKeyboardButton("➕ Get Following", callback_data="getfollowing")],
        [InlineKeyboardButton("👨‍👩‍👧‍👦 Get Followers", callback_data="getfollowers")],
        [InlineKeyboardButton("🎙️ Get Space", callback_data="getspace")],
        [InlineKeyboardButton("📋 Get Profile", callback_data="getprofile")]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "🔍 Choose search type:\n\n"
        "Select one of the options below:",
        reply_markup=reply_markup
    )

async def search_type_button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle button callback for search type selection"""
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    search_type = query.data
    
    logger.info(f"User {user_id} selected search type: {search_type}")
    
    # Check if user has an active search state
    if user_id not in search_states:
        logger.warning(f"User {user_id} has no active search state")
        await query.edit_message_text("❌ Search session expired. Please use /search to start again.")
        return
    
    # Update search state
    search_states[user_id]['search_type'] = search_type
    search_states[user_id]['step'] = 'query_input'
    
    logger.info(f"User {user_id} state updated: {search_states[user_id]}")
    
    # Show query input prompt
    examples = "Examples: 'from:gopher_ai', 'python tutorial', '#web3', 'Elon Musk'"
    
    await query.edit_message_text(
        f"✅ Search type set to: {search_type}\n\n"
        f"💬 What do you want to search for?\n\n"
        f"{examples}\n\n"
        f"📝 Reply with your search query:"
    )

async def handle_search_step(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle interactive search steps"""
    user_id = update.effective_user.id
    user_message = update.message.text.strip()
    
    logger.info(f"User {user_id} sent message: {user_message[:100]}")
    
    # Check if user is in search process
    if user_id not in search_states:
        logger.info(f"User {user_id} not in search state, ignoring")
        return
    
    state = search_states[user_id]
    logger.info(f"User {user_id} current state: {state}")
    
    # Handle query input
    if state['step'] == 'query_input':
        # Store query and execute search
        state['query'] = user_message
        state['step'] = 'searching'
        
        logger.info(f"User {user_id} starting search with query: {user_message}")
        
        await update.message.reply_text("🔄 Starting search... Please wait a moment.")
        
        # Execute search
        await execute_gopher_search(update, state)

async def execute_gopher_search(update: Update, state: dict) -> None:
    """Execute search using Gopher AI API"""
    import time
    import asyncio
    
    user_id = update.effective_user.id
    
    try:
        # First request - start search
        search_data = {
            "type": state['platform'],
            "arguments": {
                "type": state['search_type'],
                "query": state['query'],
                "max_results": 5
            }
        }
        
        headers = {
            "Authorization": f"Bearer {GOPHER_API_TOKEN}",
            "Content-Type": "application/json"
        }
        
        logger.info(f"Starting search for user {user_id}")
        logger.info(f"Request URL: {GOPHER_API_BASE}/search/live")
        logger.info(f"Request data: {json.dumps(search_data, indent=2)}")
        
        # Start search
        response = requests.post(
            f"{GOPHER_API_BASE}/search/live",
            headers=headers,
            json=search_data,
            timeout=30
        )
        
        logger.info(f"Search start response status: {response.status_code}")
        logger.info(f"Search start response: {response.text}")
        
        if response.status_code != 200:
            error_msg = f"❌ API ERROR {response.status_code}\n\n"
            try:
                error_data = response.json()
                error_msg += f"Error: {json.dumps(error_data, indent=2)}"
            except:
                error_msg += f"Response: {response.text[:500]}"
            
            await update.message.reply_text(error_msg)
            del search_states[user_id]
            return
        
        search_result = response.json()
        logger.info(f"Search result response: {json.dumps(search_result, indent=2)}")
        
        # Check for error in response
        if 'error' in search_result and search_result['error']:
            logger.error(f"API returned error: {search_result['error']}")
            await update.message.reply_text(
                f"❌ API Error\n\n"
                f"Error: {search_result['error']}\n\n"
                f"Please try again or contact support."
            )
            del search_states[user_id]
            return
        
        # Extract UUID
        if 'uuid' not in search_result:
            logger.error(f"No UUID in response: {search_result}")
            await update.message.reply_text(
                f"❌ Invalid API response (no UUID)\n\n"
                f"Response: {json.dumps(search_result, indent=2)[:500]}"
            )
            del search_states[user_id]
            return
        
        uuid = search_result['uuid']
        logger.info(f"✓ Search UUID received: {uuid}")
        await update.message.reply_text(
            f"⏳ Search initiated successfully!\n\n"
            f"🆔 Search ID: {uuid[:8]}...\n\n"
            f"Fetching results..."
        )
        
        # Poll for results with retry logic
        max_retries = 10
        retry_delay = 2  # seconds
        
        for attempt in range(max_retries):
            logger.info(f"Fetching results, attempt {attempt + 1}/{max_retries}")
            
            result_url = f"{GOPHER_API_BASE}/search/live/result/{uuid}"
            logger.info(f"Requesting endpoint 2: {result_url}")
            logger.info(f"Using UUID: {uuid}")
            
            result_response = requests.get(
                result_url,
                headers=headers,
                timeout=30
            )
            
            logger.info(f"Result fetch status: {result_response.status_code}")
            logger.info(f"Result fetch response: {result_response.text[:500]}")
            
            if result_response.status_code != 200:
                if attempt < max_retries - 1:
                    logger.warning(f"Retry {attempt + 1}, status: {result_response.status_code}")
                    await asyncio.sleep(retry_delay)
                    continue
                else:
                    error_msg = f"❌ Failed to get results after {max_retries} attempts\n\n"
                    error_msg += f"Status: {result_response.status_code}\n"
                    try:
                        error_data = result_response.json()
                        error_msg += f"Response: {json.dumps(error_data, indent=2)[:500]}"
                    except:
                        error_msg += f"Response: {result_response.text[:500]}"
                    
                    await update.message.reply_text(error_msg)
                    del search_states[user_id]
                    return
            
            results = result_response.json()
            logger.info(f"Results type: {type(results)}, length: {len(results) if isinstance(results, (list, dict)) else 'N/A'}")
            
            # Case 1: Results is a list (actual data)
            if isinstance(results, list):
                if len(results) > 0:
                    # Results ready!
                    logger.info(f"✓ Results ready, found {len(results)} items")
                    await display_search_results(update, state, results)
                    break
                else:
                    # Empty list means results not ready yet
                    if attempt < max_retries - 1:
                        logger.info("Results not ready yet (empty list), retrying...")
                        await update.message.reply_text(f"⏳ Processing... ({attempt + 1}/{max_retries})")
                        await asyncio.sleep(retry_delay)
                        continue
                    else:
                        logger.warning("Results not ready after max retries")
                        await update.message.reply_text(
                            f"⚠️ Search is taking longer than expected.\n\n"
                            f"🆔 UUID: {uuid}\n\n"
                            f"The search may still be processing. Please try again in a few moments."
                        )
                        del search_states[user_id]
                        return
            
            # Case 2: Results is a dict (could be error or wrapped data)
            elif isinstance(results, dict):
                # Check for error
                if 'error' in results and results['error']:
                    error_detail = results['error']
                    logger.error(f"Search failed with error: {error_detail}")
                    await update.message.reply_text(
                        f"❌ Search Failed\n\n"
                        f"Error: {error_detail}\n\n"
                        f"Please try again or use different search parameters."
                    )
                    del search_states[user_id]
                    return
                
                # Check for data field (wrapped response)
                elif 'data' in results:
                    logger.info("Results wrapped in 'data' field")
                    await display_search_results(update, state, results)
                    break
                
                # Check for status field (legacy format)
                elif 'status' in results:
                    status = results.get('status', 'unknown')
                    logger.info(f"Result status: {status}")
                    
                    # Normalize status (replace spaces with underscores, lowercase)
                    status_normalized = status.lower().replace(' ', '_')
                    
                    if status_normalized in ['in_progress', 'pending', 'processing']:
                        if attempt < max_retries - 1:
                            logger.info(f"Status '{status}' indicates not ready, retrying...")
                            await update.message.reply_text(f"⏳ Processing... ({attempt + 1}/{max_retries})")
                            await asyncio.sleep(retry_delay)
                            continue
                        else:
                            logger.warning(f"Max retries reached, status still: {status}")
                            await update.message.reply_text(
                                f"⚠️ Search timeout\n\n"
                                f"Status: {status}\n"
                                f"UUID: {uuid}\n\n"
                                f"The search is taking longer than expected. Please try again later."
                            )
                            del search_states[user_id]
                            return
                    
                    elif status_normalized in ['completed', 'success', 'done', 'finished']:
                        logger.info("Results ready (status completed)")
                        await display_search_results(update, state, results)
                        break
                    
                    elif status_normalized in ['failed', 'error', 'cancelled']:
                        error_detail = results.get('error', results.get('message', 'Unknown error'))
                        if not error_detail or error_detail == "":
                            error_detail = f"Search status: {status}"
                        logger.error(f"Search failed: {error_detail}")
                        await update.message.reply_text(
                            f"❌ Search failed\n\n"
                            f"Error: {error_detail}"
                        )
                        del search_states[user_id]
                        return
                    
                    else:
                        # Unknown status - treat as not ready and retry
                        logger.warning(f"Unknown status '{status}', treating as in_progress")
                        if attempt < max_retries - 1:
                            await update.message.reply_text(f"⏳ Processing... ({attempt + 1}/{max_retries})")
                            await asyncio.sleep(retry_delay)
                            continue
                        else:
                            await update.message.reply_text(
                                f"⚠️ Unknown status: {status}\n\n"
                                f"UUID: {uuid}\n\n"
                                f"Please try again later."
                            )
                            del search_states[user_id]
                            return
                
                # Unknown dict format, try to display
                else:
                    logger.warning(f"Unknown dict format, displaying as-is")
                    await display_search_results(update, state, results)
                    break
            
            # Case 3: Unexpected format
            else:
                logger.error(f"Unexpected results type: {type(results)}")
                await update.message.reply_text(
                    f"❌ Unexpected response format\n\n"
                    f"Type: {type(results)}\n"
                    f"Please contact support."
                )
                del search_states[user_id]
                return
        
        # Clean up state
        if user_id in search_states:
            del search_states[user_id]
        
    except requests.exceptions.Timeout:
        logger.error("Request timeout")
        await update.message.reply_text("❌ Request timeout. API took too long to respond.")
        if user_id in search_states:
            del search_states[user_id]
    
    except requests.exceptions.RequestException as e:
        logger.error(f"Request error: {str(e)}")
        await update.message.reply_text(f"❌ Network error: {str(e)}")
        if user_id in search_states:
            del search_states[user_id]
    
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}", exc_info=True)
        await update.message.reply_text(
            f"❌ Unexpected error: {str(e)}\n\n"
            f"Please try again or contact support."
        )
        if user_id in search_states:
            del search_states[user_id]

async def display_search_results(update: Update, state: dict, results) -> None:
    """Display search results"""
    logger.info(f"Displaying results type: {type(results)}")
    logger.info(f"Results preview: {json.dumps(results, indent=2)[:1000] if not isinstance(results, str) else results[:1000]}")
    
    result_text = (
        f"✅ SEARCH COMPLETED\n\n"
        f"🎯 Type: {state['search_type']}\n"
        f"📝 Query: {state['query']}\n"
        f"🌐 Platform: {state['platform']}\n\n"
    )
    
    # Handle results based on type
    data_list = None
    
    # Case 1: Results is a dict with 'data' key
    if isinstance(results, dict):
        if 'status' in results:
            status = results.get('status', 'unknown')
            result_text += f"📈 Status: {status}\n\n"
        
        if 'data' in results:
            data_list = results['data']
    
    # Case 2: Results is directly a list (like your example)
    elif isinstance(results, list):
        data_list = results
    
    # Process data list
    if data_list and isinstance(data_list, list) and len(data_list) > 0:
        result_text += f"📊 Found {len(data_list)} results:\n\n"
        result_text += "=" * 40 + "\n\n"
        
        for i, item in enumerate(data_list[:10], 1):  # Show up to 10 results
            if not isinstance(item, dict):
                continue
            
            # Extract content/text
            content = item.get('content') or item.get('text', '')
            tweet_id = item.get('id', '')
            source = item.get('source', 'unknown')
            
            # Get metadata
            metadata = item.get('metadata', {})
            
            # Display content
            if content:
                # Truncate long content
                display_content = content[:300] + "..." if len(content) > 300 else content
                result_text += f"[{i}] {display_content}\n\n"
            else:
                result_text += f"[{i}] (No content)\n\n"
            
            # Display metadata
            if metadata:
                # Username
                username = metadata.get('username', '')
                if username:
                    result_text += f"   👤 @{username}\n"
                
                # Created date
                created_at = metadata.get('created_at', '')
                if created_at:
                    # Format date nicely
                    try:
                        from datetime import datetime
                        dt = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
                        formatted_date = dt.strftime('%Y-%m-%d %H:%M')
                        result_text += f"   📅 {formatted_date} UTC\n"
                    except:
                        result_text += f"   📅 {created_at}\n"
                
                # Public metrics
                public_metrics = metadata.get('public_metrics', {})
                if public_metrics:
                    likes = public_metrics.get('like_count', 0)
                    retweets = public_metrics.get('retweet_count', 0)
                    replies = public_metrics.get('reply_count', 0)
                    quotes = public_metrics.get('quote_count', 0)
                    
                    if likes > 0 or retweets > 0 or replies > 0:
                        result_text += f"   📊 "
                        metrics = []
                        if likes > 0:
                            metrics.append(f"❤️ {likes}")
                        if retweets > 0:
                            metrics.append(f"🔄 {retweets}")
                        if replies > 0:
                            metrics.append(f"💬 {replies}")
                        if quotes > 0:
                            metrics.append(f"📝 {quotes}")
                        result_text += " | ".join(metrics) + "\n"
                
                # Tweet/Post ID and link
                tweet_id_meta = metadata.get('tweet_id') or metadata.get('id')
                if tweet_id_meta and username:
                    result_text += f"   🔗 https://twitter.com/{username}/status/{tweet_id_meta}\n"
                elif tweet_id:
                    result_text += f"   🆔 ID: {tweet_id}\n"
            
            result_text += "\n" + "-" * 40 + "\n\n"
        
        # Show if there are more results
        if len(data_list) > 10:
            result_text += f"... and {len(data_list) - 10} more results\n"
    
    elif data_list and isinstance(data_list, dict):
        # Single result as dict
        result_text += f"📊 Single Result:\n\n"
        data_str = json.dumps(data_list, indent=2)[:1000]
        result_text += f"{data_str}\n"
    
    elif data_list is not None and len(data_list) == 0:
        result_text += "📊 No results found.\n\n"
        result_text += "Try:\n"
        result_text += "• Different keywords\n"
        result_text += "• Broader search terms\n"
        result_text += "• Different search type\n"
    
    elif isinstance(results, dict) and 'error' in results:
        result_text += f"❌ Error: {results['error']}\n"
    
    else:
        # Fallback: display raw results
        result_text += f"📊 Raw Results:\n\n"
        try:
            results_str = json.dumps(results, indent=2)[:800] if not isinstance(results, str) else str(results)[:800]
            result_text += f"{results_str}\n"
        except:
            result_text += f"{str(results)[:800]}\n"
    
    # Split message if too long
    if len(result_text) > 4000:
        # Split into chunks
        chunks = [result_text[i:i+4000] for i in range(0, len(result_text), 4000)]
        for idx, chunk in enumerate(chunks):
            if idx > 0:
                import asyncio
                await asyncio.sleep(0.5)  # Small delay between chunks
            await update.message.reply_text(chunk)
    else:
        await update.message.reply_text(result_text)

async def echo_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handler for regular text messages (echo)"""
    user_id = update.effective_user.id
    
    # Check if user is in search process
    if user_id in search_states:
        await handle_search_step(update, context)
        return
    
    # Regular echo for other messages
    user_message = update.message.text
    response = f"💬 You wrote:\n\n_{user_message}_\n\n✅ Message received successfully!"
    await update.message.reply_text(response, parse_mode='Markdown')

async def unknown_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handler for unknown commands"""
    await update.message.reply_text(
        "❌ Unknown command. Type /help to see available commands."
    )

def main() -> None:
    """Main function to run the bot"""
    # Validate token
    if BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
        print("❌ Error: BOT TOKEN not set!")
        print("Please set the TELEGRAM_BOT_TOKEN environment variable")
        print("or replace the BOT_TOKEN variable in main.py")
        return
    
    # Create the Application
    application = Application.builder().token(BOT_TOKEN).build()

    # Command handlers
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("info", info_command))
    application.add_handler(CommandHandler("search", search_command))
    
    # Callback query handler for button interactions
    application.add_handler(CallbackQueryHandler(search_type_button_callback))
    
    # Message handler for text messages
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo_message))
    
    # Unknown command handler
    application.add_handler(MessageHandler(filters.COMMAND, unknown_command))

    # Run the bot
    print("🤖 Bot is starting...")
    print(f"📱 Bot Token: {BOT_TOKEN[:10]}...")
    
    application.run_polling()
    print("🔄 Bot is running with polling...")

if __name__ == "__main__":
    main()



🚀 Step 4 — Run the Bot

Run this command in your terminal:

python bot.py

If everything is good, you’ll see:

🤖 Bot is starting...
📱 Bot Token: 1234567890...
🔄 Bot is running with polling...

Then open your bot in Telegram → type /start.


---

💡 Step 5 — Test Commands

Your bot will support these commands:

/start — greet user
/help — show available commands
/info — show bot information
/search — begin Gopher data search

⚙️ Technologies Used
Python (🐍)
python-telegram-bot (💬)
Requests (🌐)
Gopher AI API (🧠)
Logging System (🪵)

🧠 About Gopher AI
Gopher AI is a data & AI platform that provides real-time access to social analysis, trends, and digital content via API.

👨‍💻 Developer
Created by the Gopher AI Community.
Inspired to democratize access to digital data through AI.
💡 Contribute & Explore with us!

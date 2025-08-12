from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.exceptions import TelegramAPIError
from service.planner import MCPPlanner
from core.loader import load_config_tools
from core.router import execute_toolcall_chain
from service.response import generate_final_reply
from utils.common import get_resource_path
from dotenv import load_dotenv, set_key
from utils.common import detect_language
from config.settings import settings
import httpx
import os

API_URL = settings.TG_API_URL
BOT_TOKEN = ""
WHITE_LIST = set()

bot: Bot = None
dp: Dispatcher = None

planner = MCPPlanner()
tool_registry = load_config_tools()

ENV_PATH = get_resource_path(".env")

def ensure_openai_api_key() -> str:
    load_dotenv(dotenv_path=ENV_PATH, override=False)
    key = os.getenv("OPENAI_API_KEY", "").strip()

    if not key:
        print("🔐 Missing OpenAI API Key. | 请输入你的 OpenAI API Key（sk-xxxx 开头）：")
        while True:
            key = input(" > ").strip()
            if key.startswith("sk-"):
                set_key(str(ENV_PATH), "OPENAI_API_KEY", key)
                print("✅ OPENAI_API_KEY has been saved. | 已保存OPENAI API KEY。")
                break
            else:
                print("❗️Format error. It must start with sk-. Please re-enter: | 格式错误，必须以 sk- 开头。请重新输入：")

    load_dotenv(dotenv_path=ENV_PATH, override=True)

def is_valid_token(token: str) -> bool:
    url = f"{API_URL}{token}/getMe"
    try:
        response = httpx.get(url)
        return response.status_code == 200 and response.json().get("ok")
    except Exception:
        return False

async def start_bot():
    global bot, dp, BOT_TOKEN

    ensure_openai_api_key()

    BOT_TOKEN = input("🤖 Please enter your Bot Token ｜ 请输入你的 Bot Token：").strip()
    if not is_valid_token(BOT_TOKEN):
        print("❌ Invalid token. Please check and try again. ｜ Token 无效，请检查后重试。")
        return

    print("✅ Token verification successful. Please add a whitelist user ID.")
    print("🛡️ 你必须输入一个白名单用户 ID，否则无法启动。")

    while True:
        whitelist_input = input("📝 Enter user ID (数字)：").strip()
        if whitelist_input.isdigit():
            WHITE_LIST.add(int(whitelist_input))
            print(f"✅ Added user ID {whitelist_input} to whitelist.")
            break
        else:
            print("❗ 请输入有效的数字用户 ID，不能为空，也不能跳过。")

    try:
        bot = Bot(token=BOT_TOKEN)
        await bot.delete_webhook(drop_pending_updates=True)
        dp = Dispatcher()

        print("🚀 Telegram Bot is starting and listening for messages...")
        register_handlers()
        await dp.start_polling(bot)

    except TelegramAPIError as e:
        print(f"❌ Telegram API error: {e}")
    except Exception as e:
        print(f"❌ Unexpected error occurred: {e}")
    finally:
        if bot:
            await bot.session.close()

def register_handlers():
    @dp.message(Command(commands=["help"]))
    async def help_command(message: Message):
        await process_mcp(message)

    @dp.message()
    async def generic_handler(message: Message):
        uid = message.from_user.id
        if WHITE_LIST and uid in WHITE_LIST:
            return await white_process_mcp(message)
        else:
            await message.reply("🤖 You are currently in restricted mode. Please use /help to initiate a request.")

async def process_mcp(message: Message):
    user_input = message.text.replace("/help", "").strip()
    if not user_input:
        toolcall = planner.plan(user_input)
        results = await execute_toolcall_chain(toolcall, registry=tool_registry)
        reply = generate_final_reply(user_input, results, lang="unknown")
        await message.reply(reply)
        return

    reply = f"🤖 MCP is processing your request: {user_input}\n(The actual response will be returned here)"
    await message.reply(reply)

async def white_process_mcp(message: Message):
    user_input = message.text
    if user_input == "/start":
        intro_text = (
            "👋 Hi, I’m your dedicated Web3 assistant — Coreon MCP Execution Engine. \n\n"
            "Just give me a natural language command, and I’ll automatically help you handle various on-chain tasks: \n"
            "• 📊 Technical analysis (candlestick charts, indicators) \n"
            "• 🧠 Sentiment monitoring (Twitter, news, LunarCrush) \n"
            "• 🕵️ Risk scanning (honeypot detection, holding concentration) \n"
            "• 🔍 Project intelligence analysis (launch date, liquidity, trading volume) \n\n"
            "You can ask me things like: \n"
            "Help me check the trend of ... \n"
            "Analyze if there’s anything unusual with this address recently \n"
    
            "🚀 I’ll automatically gather data from multiple sources and use intelligent reasoning to deliver results. ✅ \n\n"
            "📌 More powerful features are coming soon, including alert systems, watchlist assistants, and batch analysis. \n\n"
            "🎯 I’m ready — feel free to chat with me anytime! "
        )
        await message.answer(intro_text)
        return

    # lang = detect_language(user_input)
    toolcall = planner.plan(user_input)

    results = await execute_toolcall_chain(toolcall, registry=tool_registry)
    reply = generate_final_reply(user_input, results, lang=settings.MCP_LANG)
    await message.reply(reply)

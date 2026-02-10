from pyrogram import Client, filters, enums
from RishuMusic import app
import shutil
from typing import List
import asyncio
import re
import config
import random
import aiohttp  # Added for API requests
from motor.motor_asyncio import AsyncIOMotorClient as MongoCli
from pyrogram.errors import MessageEmpty, ChatAdminRequired, UserIsBlocked, ChatWriteForbidden, FloodWait, RPCError
from pyrogram.enums import ChatAction, ChatMemberStatus as CMS
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery, VideoChatScheduled, ChatMemberUpdated

# =========================
# MISTRAL CONFIG
# =========================
MISTRAL_URL = "https://api.mistral.ai/v1/chat/completions"
# WARNING: Keep your API Key safe. Ideally, put this in your config.py
MISTRAL_API_KEY = "pbNojPS9lRrEfUoFOzFzISyz0Cgg4Zjn" 
MODEL = "mistral-small-latest"

# =========================
# DATABASE SETUP
# =========================
mongodb = MongoCli(config.MONGO_DB_URI)
db = mongodb.Anonymous
sticker_db = db.stickers.sticker
lang_db = db.ChatLangDb.LangCollection
status_db = db.chatbot_status_db.status

CHAT_STORAGE = [
    "mongodb+srv://chatbot1:a@cluster0.pxbu0.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0",
    "mongodb+srv://chatbot2:b@cluster0.9i8as.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0",
    "mongodb+srv://chatbot3:c@cluster0.0ak9k.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0",
    "mongodb+srv://chatbot4:d@cluster0.4i428.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0",
    "mongodb+srv://chatbot5:e@cluster0.pmaap.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0",
    "mongodb+srv://chatbot6:f@cluster0.u63li.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0",
    "mongodb+srv://chatbot7:g@cluster0.mhzef.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0",
    "mongodb+srv://chatbot8:h@cluster0.okxao.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0",
    "mongodb+srv://chatbot9:i@cluster0.yausb.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0",
    "mongodb+srv://chatbot10:j@cluster0.9esnn.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0",
]

VIPBOY = MongoCli(random.choice(CHAT_STORAGE))
chatdb = VIPBOY.Anonymous
chatai = chatdb.Word.WordDb
storeai = VIPBOY.Anonymous.Word.NewWordDb

reply = []
status_cache = []
sticker = []
LOAD = "FALSE"

# =========================
# CACHE FUNCTIONS
# =========================

async def load_caches():
    global reply, sticker, LOAD, status_cache
    if LOAD == "TRUE":
        return
    LOAD = "TRUE"
    reply.clear()
    sticker.clear()

    print("All cache cleaned ✅")  
    await asyncio.sleep(1)  
    try:  
        print("Loading All Caches...")  
        
        reply = await chatai.find().to_list(length=10000)  
        print("Replies Loaded ✅")  
        await asyncio.sleep(1)  
        
        status_cache = await status_db.find().to_list(length=None)  
        print("Status Loaded ✅")  
        
        sticker = await sticker_db.find().to_list(length=None)  
        if not sticker:  
            sticker_id = "CAACAgUAAxkBAAENzH5nsI3qB-eJNDAUZQL9v3SQl_m-DAACigYAAuT1GFUScU-uCJCWAjYE"  
            await sticker_db.insert_one({"sticker_id": sticker_id})  
        print("Sticker Loaded ✅")  
        print("All caches loaded 👍 ✅")  
        LOAD = "FALSE"  
    except Exception as e:  
        print(f"Error loading caches: {e}")  
        LOAD = "FALSE"  
    return

async def get_chat_status_from_cache(chat_id, bot_id):
    global status_cache
    for entry in status_cache:
        if entry["chat_id"] == chat_id and entry["bot_id"] == bot_id:
            return entry.get("status", "enabled")
    return "enabled"

# =========================
# MISTRAL AI FUNCTION
# =========================

async def ask_mistral(query):
    """Fetches response from Mistral AI."""
    headers = {
        "Authorization": f"Bearer {MISTRAL_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": MODEL,
        "messages": [{"role": "user", "content": query}],
        "max_tokens": 200  # Limit tokens to prevent huge messages
    }
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(MISTRAL_URL, json=data, headers=headers) as resp:
                if resp.status == 200:
                    result = await resp.json()
                    return result['choices'][0]['message']['content']
                else:
                    print(f"Mistral API Error: {resp.status} - {await resp.text()}")
                    return None
    except Exception as e:
        print(f"Mistral Request Failed: {e}")
        return None

async def get_reply(message_text: str):
    global reply
    # First check for exact match in DB
    matched_replies = [reply_data for reply_data in reply if reply_data["word"] == message_text]
    
    if matched_replies:
        return random.choice(matched_replies)
    
    # If no DB match, return None (So we can trigger Mistral later)
    return None 

# =========================
# HANDLERS
# =========================

@app.on_message(filters.command("chatbot", prefixes=[".", "/"]))
async def chatbot_command(client: Client, message: Message):
    command = message.text.split()
    if len(command) > 1:
        flag = command[1].lower()
        chat_id = message.chat.id
        bot_id = client.me.id

        if flag in ["on", "enable"]:  
            await status_db.update_one(  
                {"chat_id": chat_id, "bot_id": bot_id},  
                {"$set": {"status": "enabled"}},  
                upsert=True  
            )  
            await message.reply_text(f"Chatbot has been **enabled** for this chat ✅.")  
            await load_caches()  
        elif flag in ["off", "disable"]:  
            await status_db.update_one(  
                {"chat_id": chat_id, "bot_id": bot_id},  
                {"$set": {"status": "disabled"}},  
                upsert=True  
            )  
            await message.reply_text(f"Chatbot has been **disabled** for this chat ❌.")  
            await load_caches()  
        else:  
            await message.reply_text("Invalid option! Use `/chatbot on` or `/chatbot off`.")  
    else:  
        await message.reply_text(  
            "Please specify an option to enable or disable the chatbot.\n\n"  
            "Example: `/chatbot on` or `/chatbot off`"  
        )

async def save_reply(original_message: Message, reply_message: Message):
    global reply
    try:
        reply_data = {
            "word": original_message.text.lower(), # Save as lower case for better matching
            "text": None,
            "check": "none",
        }

        if reply_message.sticker:  
            reply_data["text"] = reply_message.sticker.file_id  
            reply_data["check"] = "sticker"  
        elif reply_message.photo:  
            reply_data["text"] = reply_message.photo.file_id  
            reply_data["check"] = "photo"  
        elif reply_message.video:  
            reply_data["text"] = reply_message.video.file_id  
            reply_data["check"] = "video"  
        elif reply_message.audio:  
            reply_data["text"] = reply_message.audio.file_id  
            reply_data["check"] = "audio"  
        elif reply_message.animation:  
            reply_data["text"] = reply_message.animation.file_id  
            reply_data["check"] = "gif"  
        elif reply_message.voice:  
            reply_data["text"] = reply_message.voice.file_id  
            reply_data["check"] = "voice"  
        elif reply_message.text:  
            reply_text = reply_message.text  
            reply_data["text"] = reply_text  
            reply_data["check"] = "none"  

        is_chat = await chatai.find_one(reply_data)  
        if not is_chat:  
            await chatai.insert_one(reply_data)  
            reply.append(reply_data)  

    except Exception as e:  
        print(f"Error in save_reply: {e}")

async def reply_message(client, chat_id, bot_id, message_text, message):
    try:
        # 1. Try to get response from MongoDB Database
        reply_data = await get_reply(message_text)
        
        if reply_data:
            # === DATABASE REPLY FOUND ===
            response_text = reply_data["text"]
            if reply_data["check"] == "sticker":  
                await message.reply_sticker(reply_data["text"])  
            elif reply_data["check"] == "photo":  
                await message.reply_photo(reply_data["text"])  
            elif reply_data["check"] == "video":  
                await message.reply_video(reply_data["text"])  
            elif reply_data["check"] == "audio":  
                await message.reply_audio(reply_data["text"])  
            elif reply_data["check"] == "gif":  
                await message.reply_animation(reply_data["text"])  
            elif reply_data["check"] == "voice":  
                await message.reply_voice(reply_data["text"])  
            else:  
                await message.reply_text(response_text, disable_web_page_preview=True)  
        
        else:
            # === NO DATABASE REPLY? ASK MISTRAL AI ===
            await client.send_chat_action(chat_id, ChatAction.TYPING)
            ai_response = await ask_mistral(message_text)
            
            if ai_response:
                await message.reply_text(ai_response)
            else:
                # Fallback: If AI fails and DB fails, pick a random DB reply (Old behavior)
                if reply:
                    random_reply = random.choice(reply)
                    if random_reply["check"] == "none":
                        await message.reply_text(random_reply["text"])

    except (ChatAdminRequired, UserIsBlocked, ChatWriteForbidden, RPCError) as e:  
        return  
    except Exception as e:  
        print(f"Error in reply_message:- {e}")  
        return

@app.on_message(filters.incoming, group=1)
async def chatbot(client: Client, message: Message):
    global sticker
    bot_id = client.me.id
    if not sticker:
        await load_caches()
        # Don't return here, attempt to reply even if cache is loading first time
        
    if not message.from_user or message.from_user.is_bot:  
        return  
    
    # Ignore messages that are likely commands
    if message.text and any(message.text.startswith(prefix) for prefix in ["!", "/", "@", ".", "?", "#"]):  
        return  
        
    user_id = message.from_user.id if message.from_user else message.chat.id  
    chat_id = message.chat.id  
    
    try:  
        # Only reply if replying to bot OR if it's a general message in the group (depending on your logic)
        # Your logic: If replying to bot OR not replying to anyone
        if (message.reply_to_message and message.reply_to_message.from_user.id == bot_id) or (not message.reply_to_message):  
            
            chat_status = await get_chat_status_from_cache(chat_id, bot_id)  
            if chat_status == "disabled":  
                return  
            
            if message.text:  
                message_text = message.text.lower()  
                
                # Hardcoded quick replies
                if "gn" in message_text or "good night" in message_text:  
                    return await message.reply_text(f"Good Night! Sweet dreams {message.from_user.mention} 🌙✨")  
    
                elif "gm" in message_text or "good morning" in message_text:  
                    return await message.reply_text(f"Good Morning ji! {message.from_user.mention} 🙈")  
    
                elif "hello" in message_text or "hii" in message_text or "hey" in message_text:  
                    return await message.reply_text(f"Hi {message.from_user.mention} 😁 kaise ho??")  
    
                elif "bye" in message_text or "goodbye" in message_text:  
                    return await message.reply_text(f"Goodbye! Take care! {message.from_user.mention} 👋😏")  
    
                elif "thanks" in message_text or "thank you" in message_text:  
                    return await message.reply_text("hehe welcome! 😜")  

                else:  
                    # Main Logic: DB -> AI
                    await reply_message(client, chat_id, bot_id, message_text, message)  
                    return  
        
        # Learning Mode: Save replies
        if message.reply_to_message:  
            await save_reply(message.reply_to_message, message)  
            
    except (ChatAdminRequired, UserIsBlocked, ChatWriteForbidden, RPCError) as e:  
        return  
    except Exception as e:  
        print(f"Error in chatbot handler: {e}")
        return

import asyncio
import nest_asyncio
from pyrogram import Client, filters
from pytgcalls import PyTgCalls
from pytgcalls.types import AudioPiped
import yt_dlp
import os

nest_asyncio.apply()

# Environment Variables မှတစ်ဆင့် Credentials များယူခြင်း
API_ID = int(os.environ.get("API_ID", "33196640"))
API_HASH = os.environ.get("API_HASH", "8ddbd35a990cab7dff1e8267a0cb7053")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "8875152304:AAG-N4oYaiOMMOsE2PRxFLyoeejVuIbSHtM")

app = Client("KgeeMusicBot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
call_py = PyTgCalls(app)

def get_audio_url(youtube_url):
    ydl_opts = {'format': 'bestaudio', 'noplaylist': True}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(youtube_url, download=False)
        return info['url']

@app.on_message(filters.command("play") & filters.group)
async def play_song(client, message):
    if len(message.command) < 2:
        await message.reply("ကျေးဇူးပြု၍ YouTube လင့်ခ် ထည့်ပေးပါ (ဥပမာ - `/play Link`)")
        return
    youtube_url = message.command[1]
    chat_id = message.chat.id
    status_msg = await message.reply("🎶 သီချင်းကို ရှာဖွေနေပါပြီ...")
    try:
        audio_stream_url = get_audio_url(youtube_url)
        await call_py.join_group_call(chat_id, AudioPiped(audio_stream_url))
        await status_msg.edit_text("▶️ သီချင်းစတင် ဖွင့်နေပါပြီ...")
    except Exception as e:
        await status_msg.edit_text(f"❌ အမှား: {str(e)}")

@app.on_message(filters.command("stop") & filters.group)
async def stop_song(client, message):
    try:
        await call_py.leave_group_call(message.chat.id)
        await message.reply("⏹️ သီချင်းရပ်တန့်လိုက်ပါပြီ။")
    except Exception as e:
        await message.reply(f"❌ အမှား: {str(e)}")

async def main():
    print("Bot စတင်နေပါပြီ...")
    await app.start()
    await call_py.start()
    print("✅ Bot အလုပ်လုပ်နေပါပြီ။")
    while True:
        await asyncio.sleep(1)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

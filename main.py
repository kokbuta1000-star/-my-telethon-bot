import asyncio
import http.server
import socketserver
import threading
from telethon import TelegramClient, events
from telethon.sessions import StringSession

# --- 1. حل مشكلة الـ Event Loop ومنع الخمول على سيرفر Render ---
try:
    asyncio.set_event_loop(asyncio.new_event_loop())
except Exception:
    pass

def keep_alive():
    class HeartbeatHandler(http.server.SimpleHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b"Regn UserBot is running perfectly!")

    # تشغيل منفذ وهمي (Port 10000) متوافق مع إعدادات الـ Web Service المجانية لـ Render
    with socketserver.TCPServer(("", 10000), HeartbeatHandler) as httpd:
        httpd.serve_forever()

threading.Thread(target=keep_alive, daemon=True).start()
# -------------------------------------------------------------

# --- 2. إعدادات بيانات حسابك وجلستك الجديدة ---
API_ID = 30655981
API_HASH = "bed0bded4e3a82c8169dfd409a48e423"
SESSION_STRING = "1BVtsOMEBu4XFMIqhIUYruXEC96WXaJlu-8-rtDDcUtkaHtgiDJ2JkVQzlhno_YJNXfSCLwkEb8-V8o2PAevrXv9QjzFGKVyFDi5AxtbhpQpyEGT86w5d31xBBBYl2UselbwdhwJbqaEaEyg4VZqn6W3hdjaWXWEDRL0ls_jgGByYy6ckNP8nyPG4Z6RmDvfyecMdETnoK5OZRUJDl0aO8HWl4wUNfX5Jl5Dq8KcK_ayKfMMHfmxM0WxsFet-A9L8RvtkZxWrNbOyp-WnuNu5p6Iyw1CPqIMHCXEMCW-272aaUomRm05c4cE0DUL6Z3AxwkVzJy3u4Yl_rdZwFvvSGEUZZvzjDkw="

# إنشاء عميل التليثون باستخدام الجلسة النصية الصحيحة
client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)

# --- 3. أوامر اليوزر بوت (UserBot Commands) ---

# أمر الفحص الذاتي للتأكد من تشغيل البوت
@client.on(events.NewMessage(pattern=r'\.فحص', outgoing=True))
async def check_bot(event):
    await event.edit("**🤖 يوزر بوت Regn يعمل بنجاح وكفاءة عالية الآن على سيرفر Render مدمجاً بـ الـ Keep-Alive!**")

# --- 4. إطلاق تشغيل الحساب بصفة دائمة ---
print("Connecting and starting the UserBot...")
client.start()
client.run_until_disconnected()

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

# --- 2. إعدادات بيانات حسابك وجلستك ---
# تنبيه: تذكر استبدال النص بـ كود الجلسة (String Session) الخاص بك لتفادي توقف السكربت (Status 1)
API_ID = 26889392
API_HASH = "b043ec11b5186b865cbef91b947c92b2"
SESSION_STRING = "ضع_كود_الجلسة_هنا_بالكامل" 

# إنشاء عميل التليثون باستخدام الجلسة النصية المستخرجة
client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)

# --- 3. أوامر اليوزر بوت (UserBot Commands) ---

# أمر الفحص الذاتي للتأكد من تشغيل البوت
@client.on(events.NewMessage(pattern=r'\.فحص', outgoing=True))
async def check_bot(event):
    await event.edit("**🤖 يوزر بوت Regn يعمل بنجاح وكفاءة عالية الآن على سيرفر Render مدمجاً بـ الـ Keep-Alive!**")

# هنا يمكنك إضافة أي وظائف أو ملفات حماية وتنظيف للمجموعات مستقبلاً...

# --- 4. إطلاق تشغيل الحساب بصفة دائمة ---
print("Connecting and starting the UserBot...")
client.start()
client.run_until_disconnected()

import asyncio
import http.server
import socketserver
import threading
from telethon import TelegramClient, events

# --- حل مشكلة تشغيل السيرفر ومنع الخمول على Render ---
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
            self.wfile.write(b"Bot is alive and running!")

    # تشغيل منفذ وهمي لاستقبال اتصالات التنشيط من السيرفر
    with socketserver.TCPServer(("", 10000), HeartbeatHandler) as httpd:
        httpd.serve_forever()

threading.Thread(target=keep_alive, daemon=True).start()
# --------------------------------------------------

# --- إعدادات بيانات التليجرام وكود الجلسة (Session) ---
API_ID = 26889392  # تم جلبها بدقة من لقطة الشاشة الخاصة بك
API_HASH = "b043ec11b5186b865cbef91b947c92b2"  # ضع الـ API Hash الخاص بحسابك هنا بين علامتي التنصيص
SESSION_STRING = "ضع_كود_الجلسة_هنا_بالكامل"  # الصق نص الجلسة الطويل (Telethon String Session) هنا

# تشغيل العميل باستخدام الجلسة النصية المستخرجة
from telethon.sessions import StringSession
client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)

# --- أوامر اليوزر بوت (UserBot) ---

# أمر الفحص (.فحص)
@client.on(events.NewMessage(pattern=r'\.فحص', outgoing=True))
async def check_bot(event):
    await event.edit("**🤖 يوزر بوت Regn يعمل بنجاح وكفاءة عالية الآن على سيرفر Render!**")

# يمكنك إضافة أي أوامر تلقائية أخرى هنا مستقبلاً...

# إطلاق تشغيل الحساب بصفة دائمة
print("Connecting and starting the UserBot...")
client.start()
client.run_until_disconnected()

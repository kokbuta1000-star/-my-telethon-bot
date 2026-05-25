import asyncio
import http.server
import socketserver
import threading
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from telethon.tl.functions.channels import EditBannedRequest
from telethon.tl.types import ChatBannedRights

# --- 1. منع خمول السيرفر (Keep-Alive) ---
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
            self.wfile.write(b"Regn Security Bot is Active!")
    with socketserver.TCPServer(("", 10000), HeartbeatHandler) as httpd:
        httpd.serve_forever()

threading.Thread(target=keep_alive, daemon=True).start()

# --- 2. بيانات الاتصال بالجلسة ---
API_ID = 30655981
API_HASH = "bed0bded4e3a82c8169dfd409a48e423"
SESSION_STRING = "1BVtsOMEBu4XFMIqhIUYruXEC96WXaJlu-8-rtDDcUtkaHtgiDJ2JkVQzlhno_YJNXfSCLwkEb8-V8o2PAevrXv9QjzFGKVyFDi5AxtbhpQpyEGT86w5d31xBBBYl2UselbwdhwJbqaEaEyg4VZqn6W3hdjaWXWEDRL0ls_jgGByYy6ckNP8nyPG4Z6RmDvfyecMdETnoK5OZRUJDl0aO8HWl4wUNfX5Jl5Dq8KcK_ayKfMMHfmxM0WxsFet-A9L8RvtkZxWrNbOyp-WnuNu5p6Iyw1CPqIMHCXEMCW-272aaUomRm05c4cE0DUL6Z3AxwkVzJy3u4Yl_rdZwFvvSGEUZZvzjDkw="

client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)

PROTECTION_MODE = True  # وضع الحماية التلقائي (شغال افتراضياً)

# --- 3. قسم الأوامر الشاملة ---

# [1] أمر عرض لوحة التحكم
@client.on(events.NewMessage(pattern=r'\.الاوامر', outgoing=True))
async def show_menu(event):
    menu = """
🛡️ **لوحة تحكم سورس Regn لحماية المجموعات:**

• `.فحص` ➜ للتأكد من استجابة الحساب وسرعته.
• `.كتم` ➜ لكتم العضو تماماً داخل المجموعة (بالرد).
• `.حظر` ➜ لحظر عضو واحد وطره (بالرد).
• `.الغاء` ➜ لإلغاء الحظر أو الكتم عن الشخص (بالرد).
• `.تنظيف + العدد` ➜ لمسح رسائل الشات بسرعة (مثال: `.تنظيف 50`).
• `.تفعيل الحماية` ➜ تشغيل الحذف التلقائي للإعلانات والروابط.
• `.تعطيل الحماية` ➜ إيقاف الحذف التلقائي للروابط.

⚡ **أمر التطهير السريع والمجنون:**
• `.تفليش` ➜ طرد وتفليش جميع أعضاء المجموعة أو القناة فوراً بسرعة البرق.
"""
    await event.edit(menu)

# [2] أمر الفحص الذاتي
@client.on(events.NewMessage(pattern=r'\.فحص', outgoing=True))
async def check_bot(event):
    await event.edit("**🤖 سورس Regn يعمل بنجاح وبأقصى سرعة اتصال متوفرة!**")

# [3] أمر الكتم (بالرد)
@client.on(events.NewMessage(pattern=r'\.كتم', outgoing=True))
async def mute_user(event):
    if not event.is_reply: return await event.edit("**⚠️ رد على رسالة الشخص أولاً!**")
    reply = await event.get_reply_message()
    try:
        await client(EditBannedRequest(event.chat_id, reply.sender_id, ChatBannedRights(until_date=None, send_messages=True)))
        await event.edit("**🔇 تم كتم العضو ومنعه من إرسال الرسائل.**")
    except Exception as e: await event.edit(f"**⚠️ خطأ في الصلاحيات:** {e}")

# [4] أمر الحظر الفردي (بالرد)
@client.on(events.NewMessage(pattern=r'\.حظر', outgoing=True))
async def ban_user(event):
    if not event.is_reply: return await event.edit("**⚠️ رد على رسالة الشخص أولاً!**")
    reply = await event.get_reply_message()
    try:
        await client(EditBannedRequest(event.chat_id, reply.sender_id, ChatBannedRights(until_date=None, view_messages=True)))
        await event.edit("**⚡️ تم حظر العضو وطره بنجاح.**")
    except Exception as e: await event.edit(f"**⚠️ خطأ:** {e}")

# [5] أمر إلغاء القيود (بالرد)
@client.on(events.NewMessage(pattern=r'\.الغاء', outgoing=True))
async def unmute_user(event):
    if not event.is_reply: return await event.edit("**⚠️ رد على الشخص لإلغاء القيود!**")
    reply = await event.get_reply_message()
    try:
        await client(EditBannedRequest(event.chat_id, reply.sender_id, ChatBannedRights(until_date=None)))
        await event.edit("**🔓 تم فك الحظر/الكتم عن العضو بنجاح.**")
    except Exception as e: await event.edit(f"**⚠️ خطأ:** {e}")

# [6] أمر تنظيف الشات
@client.on(events.NewMessage(pattern=r'\.تنظيف (\d+)', outgoing=True))
async def clear_chat(event):
    num = int(event.pattern_match.group(1))
    await event.delete()
    async for msg in client.iter_messages(event.chat_id, limit=num):
        try: await msg.delete()
        except Exception: pass

# [7] التحكم بنظام الحماية التلقائي
@client.on(events.NewMessage(pattern=r'\.تفعيل الحماية', outgoing=True))
async def anti_on(event):
    global PROTECTION_MODE
    PROTECTION_MODE = True
    await event.edit("**🛡️ تم تشغيل الحماية الذكية (حذف الروابط تلقائياً).**")

@client.on(events.NewMessage(pattern=r'\.تعطيل الحماية', outgoing=True))
async def anti_off(event):
    global PROTECTION_MODE
    PROTECTION_MODE = False
    await event.edit("**⚠️ تم إيقاف نظام حماية المجموعة.**")

# [8] فحص الروابط والمخالفات التلقائي للقروب
@client.on(events.NewMessage(incoming=True))
async def watch_ads(event):
    if event.is_private or not PROTECTION_MODE: return
    if event.text and ("t.me/" in event.text or "http" in event.text):
        try: await event.delete()
        except Exception: pass

# =================================================================
# [9] ⚡️ أمر التفليش الخارق (السرعة المجنونة للحظر الجماعي) ⚡️
# =================================================================
@client.on(events.NewMessage(pattern=r'\.تفليش', outgoing=True))
async def mass_ban(event):
    chat_id = event.chat_id
    await event.edit("**⚡️ جاري سحب قائمة الأعضاء وبدء التفليش الخارق...**")
    
    # جلب جميع أعضاء المجموعة أو القناة
    try:
        members = await client.get_participants(chat_id)
    except Exception as e:
        return await event.edit(f"**⚠️ لا يمكن جلب الأعضاء، تأكد من صلاحياتك: {e}**")
    
    tasks = []
    rights = ChatBannedRights(until_date=None, view_messages=True)
    
    # تجميع طلبات الحظر في مصفوفة مهام ليتم إرسالها دفعة واحدة (توازي كامل)
    for user in members:
        if user.deleted or user.is_self: 
            continue # تخطي الحسابات المحذوفة وتخطي حسابك الشخصي منعاً لطرد نفسك
        
        # إضافة طلب الحظر لقائمة المهام
        tasks.append(client(EditBannedRequest(chat_id, user.id, rights)))
    
    if not tasks:
        return await event.edit("**⚠️ لم يتم العثور على أعضاء قابلين للحظر!**")
    
    await event.edit(f"**🔥 جاري حظر وطرد {len(tasks)} عضو في نفس اللحظة بـ السرعة القصوى...**")
    
    # تنفيذ كل عمليات الحظر بالتوازي الكامل وجزء من الثانية
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    # حساب عدد العمليات الناجحة
    success_count = sum(1 for res in results if not isinstance(res, Exception))
    
    await event.respond(f"**💥 تم انتهاء التفليش بنجاح!**\n• تم تدمير وحظر: `{success_count}` عضو من الشات بنجاح.")

# --- 4. تشغيل الحساب بصفة دائمة ---
print("Regn Security Source is running with maximum speed features...")
client.start()
client.run_until_disconnected()

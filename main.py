import os
import asyncio
import time
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from telethon.errors import FloodWaitError

# --- إعدادات الحساب والاتصال الآمن ---
API_ID = 30655981
API_HASH = "bed0bded4e3a82c8169dfd409a48e423"
SESSION_STRING = "1BVtsOMEBu4XFMIqhIUYruXEC96WXaJlu-8-rtDDcUtkaHtgiDJ2JkVQzlhno_YJNXfSCLwkEb8-V8o2PAevrXv9QjzFGKVyFDi5AxtbhpQpyEGT86w5d31xBBBYl2UselbwdhwJbqaEaEyg4VZqn6W3hdjaWXWEDRL0ls_jgGByYy6ckNP8nyPG4Z6RmDvfyecMdETnoK5OZRUJDl0aO8HWl4wUNfX5Jl5Dq8KcK_ayKfMMHfmxM0WxsFet-A9L8RvtkZxWrNbOyp-WnuNu5p6Iyw1CPqIMHCXEMCW-272aaUomRm05c4cE0DUL6Z3AxwkVzJy3u4Yl_rdZwFvvSGEUZZvzjDkw="

start_time = time.time()

# بدء تشغيل العميل مع معالجة الأخطاء التلقائية
try:
    client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)
except Exception as e:
    print(f"خطأ في تهيئة الجلسة: {e}")

# --- قسم الأوامر المتقدمة المضافة للملف ---

# 1. أمر الفحص المطور مع حساب سرعة الاستجابة ووقت التشغيل
@client.on(events.NewMessage(outgoing=True, pattern=r"\.فحص"))
async def ping(event):
    start = time.time()
    await event.edit("**⏳ جاري الفحص...**")
    end = time.time()
    
    # حساب وقت التشغيل (Uptime) بالدقائق
    uptime = round((time.time() - start_time) / 60, 2)
    ping_time = round((end - start) * 1000, 2)
    
    status_text = (
        f"**⚡️ سورس يوزر بوت يعمل بنجاح!**\n\n"
        f"• **سرعة الاستجابة (Ping):** `{ping_time}ms`\n"
        f"• **مدة التشغيل:** `{uptime} دقيقة`\n"
        f"• **البيئة:** `Render Cloud 🚀`"
    )
    await event.edit(status_text)

# 2. أمر التعديل الذكي الذاتي
@client.on(events.NewMessage(outgoing=True, pattern=r"\.تعديل (.*)"))
async def modify_text(event):
    new_text = event.pattern_match.group(1)
    await event.edit(new_text)

# 3. أمر إظهار كود الأوامر (المساعدة) لسهولة الاستخدام
@client.on(events.NewMessage(outgoing=True, pattern=r"\.الاوامر"))
async def help_commands(event):
    help_text = (
        "**📚 قائمة أوامر اليوزر بوت المطور:**\n\n"
        "• `.فحص` - لعرض حالة السورس وسرعة الاستجابة.\n"
        "• `.تعديل [النص]` - لتعديل الرسالة التي كتبت فيها الأمر فوراً.\n"
        "• `.حذف` - لحذف الرسالة التي ترد عليها بشكل سريع.\n"
        "• `.تكرار [العدد] [النص]` - لتكرار إرسال نص معين بعدد محدد.\n"
        "• `.معلوماتي` - لجلب معلومات حسابك الشخصي بسرعة.\n"
        "• `.كتم` - (ترد بها على شخص) لحظر رسائله من لفت انتباهك."
    )
    await event.edit(help_text)

# 4. أمر الحذف السريع (ترد به على رسالتك لحذفها لمسح تلميحات الأوامر)
@client.on(events.NewMessage(outgoing=True, pattern=r"\.حذف"))
async def delete_message(event):
    if event.is_reply:
        reply_msg = await event.get_reply_message()
        await reply_msg.delete()
    await event.delete()

# 5. أمر التكرار السريع والمحمي ضد الحظر المتتالي (Spam)
@client.on(events.NewMessage(outgoing=True, pattern=r"\.تكرار (\d+) (.*)"))
async def spammer(event):
    counter = int(event.pattern_match.group(1))
    spam_text = event.pattern_match.group(2)
    await event.delete()
    
    # حد أقصى للتكرار لحماية الحساب من الباند التلقائي
    if counter > 50:
        counter = 50 
        
    for _ in range(counter):
        try:
            await event.respond(spam_text)
            await asyncio.sleep(0.4) # تأخير زمني بسيط لتجنب فلود التليجرام
        except FloodWaitError as e:
            await asyncio.sleep(e.seconds) # الانتظار التلقائي إذا طلب التليجرام الهدوء

# 6. أمر جلب معلومات حسابك (معلوماتي)
@client.on(events.NewMessage(outgoing=True, pattern=r"\.معلوماتي"))
async def get_info(event):
    me = await client.get_me()
    info = (
        f"**👤 معلومات الحساب المشغل للسورس:**\n\n"
        f"• **الاسم:** {me.first_name}\n"
        f"• **الآيدي (ID):** `{me.id}`\n"
        f"• **اليوزر نيم:** @{me.username if me.username else 'لا يوجد'}\n"
        f"• **الحسابPremium:** {'نعم' if me.premium else 'لا'}"
    )
    await event.edit(info)

# --- تشغيل البوت ومعالجة أحداث السيرفر المستمرة ---
async def main():
    print("✨ جاري بدء تشغيل السورس المطور...")
    await client.start()
    print("✅ السورس المطور يعمل الآن بنجاح في الخلفية على السيرفر!")
    await client.run_until_disconnected()

if __name__ == "__main__":
    # تشغيل الحلقة البرمجية بدون مشاكل توافقية مع سيرفرات الويب
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

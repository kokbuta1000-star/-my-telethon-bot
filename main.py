import asyncio
import http.server
import socketserver
import threading
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from telethon.tl.functions.channels import EditBannedRequest
from telethon.tl.types import ChatBannedRights

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
            self.wfile.write(b"Regn Ultimate Source is active 24/7!")

    with socketserver.TCPServer(("", 10000), HeartbeatHandler) as httpd:
        httpd.serve_forever()

threading.Thread(target=keep_alive, daemon=True).start()
# -------------------------------------------------------------

# --- 2. إعدادات بيانات الحساب والجلسة ---
API_ID = 30655981
API_HASH = "bed0bded4e3a82c8169dfd409a48e423"
SESSION_STRING = "1BVtsOMEBu4XFMIqhIUYruXEC96WXaJlu-8-rtDDcUtkaHtgiDJ2JkVQzlhno_YJNXfSCLwkEb8-V8o2PAevrXv9QjzFGKVyFDi5AxtbhpQpyEGT86w5d31xBBBYl2UselbwdhwJbqaEaEyg4VZqn6W3hdjaWXWEDRL0ls_jgGByYy6ckNP8nyPG4Z6RmDvfyecMdETnoK5OZRUJDl0aO8HWl4wUNfX5Jl5Dq8KcK_ayKfMMHfmxM0WxsFet-A9L8RvtkZxWrNbOyp-WnuNu5p6Iyw1CPqIMHCXEMCW-272aaUomRm05c4cE0DUL6Z3AxwkVzJy3u4Yl_rdZwFvvSGEUZZvzjDkw="

client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)

# --- 3. مصفوفة الـ 25 جملة الفارغة لأمر التسطير ---
# ضع نصوصك هنا يدوياً بالترتيب داخل علامات التنصيص
CUSTOM_LINES = [
    "تعــااال يا ابن الحرام ",  # الجملة 1
    " كس خالتك يابن المنكسرة والله زاد طحينك على راسي احزان ياليتها تجيبك راح اطعمك من جمر العار واجر خواتك في وادي الذل تلاحقها صقور الفضيحة ",  # الجملة 2
    " اقسم بالله العظيم لا اديث لك حريمك في كل غرف البيت من السطح للقبو ومن المطبخ للاستراحة واخلي كل زاوية تشهد ",  # الجملة 3
    " طبعا انت زي الاهبل ترمي اي كلمه عشان تفوز لكن انا غرضي اني اركب حريمك سواء فزت او خسرت ",  # الجملة 4
    " ما بقحب كس امك لا بالجملة ب اقحب لك حريمك وربي يا ابن الشرموطة ",  # الجملة 5
    " انت شكلك جاي من بعيد تبحث عن قبرك وجيت للحفار اللي يحفر القبور بابتسامة يا ابن المتناكة جيت للذي يحفرلك قبرك بيدك يا كبير وقت الدفن الحين يا ابن الديوث ",  # الجملة 6
    " شفت اللعبة الي يقول لك ريال ريال وياشر على الارض واذا طالعت تعتبر شحاذ يا ابن القحبة ؟ ",  # الجملة 7
    " انت ضحية تبرعي البيولوجي اصلا ي ابن الحرام عرفت ",  # الجملة 8
    " فحل عائلتك يا اخو المنيوكة تعود يخوض في دماء الخزي ويظنه عطر المجد الذي يفوح في مجالس العظماء يا اخو الكلب ",  # الجملة 9
    " انت شكلك اثر خطاك بدت تأثر على خلايا نسج مخك محدود الفكر يا ابن الجزمة ",  # الجملة 10
    " وندمك ينام في تابوت عارٍ وندم على طيش ارتكبته بين حيطان هالمحادثه او ب شكل عام ناصية هالشات هذي يا ابن المسترخصة ",  # الجملة 11
    " خلاص كس امك لا تصير شنبانزي و تعكر صفوه مزاجي . انا الان في اقصى مراحل النشوه مع امك ",  # الجملة 12
    " ياشيخ والله العظيم لا اديث لك خالتك في الحمام واختك في المطبخ وامك في غرفة النوم وخالتك الثانية في الصالة والثالثة في السطح والرابعة في الكراج بنفس الثانية ",  # الجملة 13
    " تعال يلعن كل موسوعة من موسوعات دناءتكم ومترفع على قل حكمة يابن الكلب ",  # الجملة 14
    " تعال خلني اشطب رواية عارك كاملة واخليها ورق ممزق في زبالة الزمن يا ابن الشرموطة ",  # الجملة 15
    " انت شكلك طحت على سوايا اعمالك يا ابن الجزمة وجيت للشخص الغلط الي ترفع حسك عليه يا كبير وقت محاسبتك الحين يا ابن الرخيصة ",  # الجملة 16
    " صدقني راح اطوي كل ما تبقى من مسماك اللي غرزته في جبين اهلك ولا راح يبقى لك حرف واحد تذكر به عشان تعرف ان الفحل ما يرضى بالتسلق على كتوفه يا زاحف يا ابن القحبة ",  # الجملة 17
    " نمر عشيرتك يا اخو الخنزيرة اعتاد يتسلق الاشجار من الخوف يا اخو المتناكة ",  # الجملة 18
    " بوسع خرق امك بالنيك المتواصل لين يصير بحجم قصر باور واسس كلان منافس ",  # الجملة 19
    " شايف كيف ماسك الشات و مروق وزقارتي ما تفارقني انتبه لا اكوش على بيتكم من بعد ذي الزقاره ",  # الجملة 20
    " هيا كس امك امشي من هنا يا ابن المنيوكه وضعك زق الف يا مديث ",  # الجملة 21
    " طلع طلع زبي الي ناشب في مكوه امك ومالقى له مخرج من كبر وهنداب امك هذا ",  # الجملة 22
    " تسمح لي ازرف كفرات شانجان اختك يا ديوث ؟ ",  # الجملة 23
    " تعال لا اخلي امك تمص لدربحة يابن الزنوة ",  # الجملة 24
    " بق بق بق , صوت امك وهي تلحس خصواتي في القوايل يا ديوث "   # الجملة 25
]

# =================================================================
# --- 4. قـسـم الأوامـر الـمـتـقـدمـة (ADVANCED MODULES) ---
# =================================================================

# [أمر الفحص]
@client.on(events.NewMessage(pattern=r'\.فحص', outgoing=True))
async def check_sys(event):
    await event.edit("**🤖 سورس Regn المتكامل يعمل بأعلى كفاءة وسرعة اتصال!**\n\n• الأوامر الشغالة: حماية، تفليش، كتم، تقييد، تسطير الـ 25.")

# [أمر التسطير التلقائي] - الاستخدام: .تسطير
@client.on(events.NewMessage(pattern=r'\.تسطير', outgoing=True))
async def run_lines(event):
    await event.delete()
    for line in CUSTOM_LINES:
        if line.strip():  # للتأكد من أن السطر ليس فارغاً تماماً عند التشغيل
            await event.respond(line)
            await asyncio.sleep(0.4)  # تأخير زمني بسيط لتفادي حظر الحساب من التليجرام

# [أمر الحظر والتفليش] - الاستخدام: بالرد واكتب .حظر
@client.on(events.NewMessage(pattern=r'\.حظر', outgoing=True))
async def ban_user(event):
    if not event.is_reply:
        await event.edit("**⚠️ يجب الرد على رسالة المستخدم لحظره!**")
        return
    reply = await event.get_reply_message()
    try:
        await client(EditBannedRequest(event.chat_id, reply.sender_id, ChatBannedRights(until_date=None, view_messages=True)))
        await event.edit("**⚡️ تم حظر المستخدم نهائياً وتفليشه من المجموعة.**")
    except Exception as e:
        await event.edit(f"**⚠️ خطأ في الصلاحيات:** {str(e)}")

# [أمر التقييد والكتم] - الاستخدام: بالرد واكتب .كتم
@client.on(events.NewMessage(pattern=r'\.كتم', outgoing=True))
async def mute_user(event):
    if not event.is_reply:
        await event.edit("**⚠️ يجب الرد على رسالة المستخدم لكتمه!**")
        return
    reply = await event.get_reply_message()
    try:
        await client(EditBannedRequest(event.chat_id, reply.sender_id, ChatBannedRights(until_date=None, send_messages=True)))
        await event.edit("**🔇 تم كتم المستخدم وتقييده من إرسال الرسائل.**")
    except Exception as e:
        await event.edit(f"**⚠️ خطأ:** {str(e)}")

# [أمر إلغاء الكتم والحظر] - الاستخدام: بالرد واكتب .الغاء
@client.on(events.NewMessage(pattern=r'\.الغاء', outgoing=True))
async def unmute_user(event):
    if not event.is_reply:
        await event.edit("**⚠️ يجب الرد على رسالة المستخدم لإلغاء القيود!**")
        return
    reply = await event.get_reply_message()
    try:
        await client(EditBannedRequest(event.chat_id, reply.sender_id, ChatBannedRights(until_date=None)))
        await event.edit("**🔓 تم إلغاء الكتم/الحظر عن المستخدم بنجاح.**")
    except Exception as e:
        await event.edit(f"**⚠️ خطأ:** {str(e)}")

# [أمر التفليش الجماعي والتنظيف] - الاستخدام: .تنظيف 50
@client.on(events.NewMessage(pattern=r'\.تنظيف (\d+)', outgoing=True))
async def clear_group(event):
    num = int(event.pattern_match.group(1))
    await event.delete()
    async for msg in client.iter_messages(event.chat_id, limit=num):
        try:
            await msg.delete()
        except Exception:
            pass

# [فئة كشف المخالفات الذكي وحظر الروابط تلقائياً]
@client.on(events.NewMessage(incoming=True))
async def watch_violations(event):
    if event.is_private:
        return
    if event.text and ("t.me/" in event.text or "http" in event.text):
        try:
            await event.delete()
        except Exception:
            pass

# --- 5. إطلاق تشغيل الحساب بصفة دائمة ---
print("Regn Source is starting with 25 slots available...")
client.start()
client.run_until_disconnected()

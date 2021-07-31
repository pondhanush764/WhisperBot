from telethon import events, TelegramClient, Button
import logging
from telethon.tl.functions.users import GetFullUserRequest as us
import os


logging.basicConfig(level=logging.INFO)

TOKEN = os.environ.get("TOKEN", None)

bot = TelegramClient(
        "Whisper",
        api_id=6,
        api_hash="eb06d4abfb49dc3eeb1aeb98ae0f581e"
        ).start(
                bot_token=TOKEN
                )
db = {}

@bot.on(events.NewMessage(pattern="^[!?/]start$"))
async def stsrt(event):
    await event.reply(
            "**வணக்கம், நான் ரகசிய போட்🤫. கீழே உள்ள buttonகளைக் கிளிக் செய்து என்னை முயற்சிக்கவும்😝!**",
            buttons=[
                [Button.switch_inline("Go Inline", query="")],
                [InlineKeyboardButton(text="Support🥰", url="t.me/kittysupport")]
                ]
            )


@bot.on(events.InlineQuery())
async def die(event):
    if len(event.text) != 0:
        return
    me = (await bot.get_me()).username
    dn = event.builder.article(
            title="It's a Secret bot!",
            description="It's a Secret Bot!\n(c) Reeshuxd",
            text=f"**It's a Secret bot**\n`@{me} wspr UserID|Message`\n**(c) Reeshuxd**",
            buttons=[
                [Button.switch_inline(" Go Inline ", query="wspr ")]
                ]
            )
    await event.answer([dn])
    
@bot.on(events.InlineQuery(pattern="wspr"))
async def inline(event):
    me = (await bot.get_me()).username
    try:
        inp = event.text.split(None, 1)[1]
        user, msg = inp.split("|")
    except IndexError:
        await event.answer(
                [], 
                switch_pm=f"@{me} [UserID]|[Message]",
                switch_pm_param="start"
                )
    except ValueError:
        await event.answer(
                [],
                switch_pm=f"Give a message too!",
                switch_pm_param="start"
                )
    try:
        ui = await bot(us(user))
    except BaseException:
        await event.answer(
                [],
                switch_pm="Invalid User ID/Username",
                switch_pm_param="start"
                )
        return
    db.update({"user_id": ui.user.id, "msg": msg, "self": event.sender.id})
    text = f"""
A Ragasiya message Has Been Sent
To [{ui.user.first_name}](tg://user?id={ui.user.id}) 🤣!
 செய்தியைப் பார்க்க கீழே உள்ள Button ஐ கிளிக் செய்யவும்😒!
**Note:** __Only {ui.user.first_name} can open this!__
    """
    dn = event.builder.article(
            title="Its a secret message! Sssh",
            description="It's a secret message! Sssh!",
            text=text,
            buttons=[
                [Button.inline("Ragasiya message🤫! ", data="wspr")]
                ]
            )
    await event.answer(
            [dn],
            switch_pm="It's a secret message! Sssh",
            switch_pm_param="start"
            )


@bot.on(events.CallbackQuery(data="wspr"))
async def ws(event):
    user = int(db["user_id"])
    lol = [int(db["self"])]
    lol.append(user)
    if event.sender.id not in lol:
        await event.answer("ஏய் 😡, இந்த செய்தி உங்களுக்காக அல்ல🤣 மற்றவர்களின் செயல்பாட்டில் உங்கள் மூக்கை நுலைக்காதீற்கள்!", alert=True)
        return
    msg = db["msg"]
    if msg == []:
        await event.anwswer(
                "Oops!\nIt's looks like message got deleted from my server!", alert=True)
        return
    await event.answer(msg, alert=True)

print("Succesfully Started Bot!")
bot.run_until_disconnected()

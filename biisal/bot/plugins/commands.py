# (c) @biisal @adarsh

from biisal.bot import StreamBot
from biisal.vars import Var
import logging
logger = logging.getLogger(__name__)
from biisal.bot.plugins.stream import MY_PASS
from biisal.utils.human_readable import humanbytes
from biisal.utils.database import Database
from pyrogram import filters, enums
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import UserNotParticipant
from biisal.utils.file_properties import get_name, get_hash, get_media_file_size
db = Database(Var.DATABASE_URL, Var.name)
from pyrogram.types import ReplyKeyboardMarkup
from biisal.vars import bot_name , bisal_channel , bisal_grp
btns = InlineKeyboardButton
btns2 = InlineKeyboardMarkup

SRT_TXT = """<b>Hey {}!,
I ᴀᴍ Fɪʟᴇ ᴛᴏ Lɪɴᴋ Gᴇɴᴇʀᴀᴛᴏʀ Bᴏᴛ ᴡɪᴛʜ Cʜᴀɴɴᴇʟ sᴜᴘᴘᴏʀᴛ.

Sᴇɴᴅ ᴍᴇ ᴀɴʏ ғɪʟᴇ ᴀɴᴅ ɢᴇᴛ ᴀ ᴅɪʀᴇᴄᴛ ᴅᴏᴡɴʟᴏᴀᴅ ʟɪɴᴋ ᴀɴᴅ sᴛʀᴇᴀᴍᴀʙʟᴇ ʟɪɴᴋ.!
ᴍᴀɪɴᴛᴀɪɴᴇᴅ ʙʏ : <a href='https://t.me/sahid_malik'>Sahid malik</a></b>"""

@StreamBot.on_message(filters.command("start") & filters.private )
async def start(b, m):
    if not await db.is_user_exist(m.from_user.id):
        await db.add_user(m.from_user.id)
        await b.send_message(
            Var.NEW_USER_LOG,
            f"**Nᴇᴡ Usᴇʀ Jᴏɪɴᴇᴅ:** \n\n__Mʏ Nᴇᴡ Fʀɪᴇɴᴅ__ [{m.from_user.first_name}](tg://user?id={m.from_user.id}) __Sᴛᴀʀᴛᴇᴅ Yᴏᴜʀ Bᴏᴛ !!__"
        )
    if Var.UPDATES_CHANNEL != "None":
        try:
            user = await b.get_chat_member(Var.UPDATES_CHANNEL, m.chat.id)
            if user.status == "kicked":
                await b.send_message(
                    chat_id=m.chat.id,
                    text="__𝓢𝓞𝓡𝓡𝓨, 𝓨𝓞𝓤 𝓐𝓡𝓔 𝓐𝓡𝓔 𝓑𝓐𝓝𝓝𝓔𝓓 𝓕𝓡𝓞𝓜 𝓤𝓢𝓘𝓝𝓖 𝓜𝓔. 𝓒ᴏɴᴛᴀᴄᴛ ᴛʜᴇ 𝓓ᴇᴠᴇʟᴏᴘᴇʀ__\n\n  **𝙃𝙚 𝙬𝙞𝙡𝙡 𝙝𝙚𝙡𝙥 𝙮𝙤𝙪**",
                    disable_web_page_preview=True
                )
                return
        except UserNotParticipant:
             await StreamBot.send_photo(
                chat_id=m.chat.id,
                photo="https://telegra.ph/file/5eb253f28ed7ed68cb4e6.png",
                caption=""""<b>Hᴇʏ ᴛʜᴇʀᴇ!\n\nPʟᴇᴀsᴇ ᴊᴏɪɴ ᴏᴜʀ ᴜᴘᴅᴀᴛᴇs ᴄʜᴀɴɴᴇʟ ᴛᴏ ᴜsᴇ ᴍᴇ ! 😊\n\nDᴜᴇ ᴛᴏ sᴇʀᴠᴇʀ ᴏᴠᴇʀʟᴏᴀᴅ, ᴏɴʟʏ ᴏᴜʀ ᴄʜᴀɴɴᴇʟ sᴜʙsᴄʀɪʙᴇʀs ᴄᴀɴ ᴜsᴇ ᴛʜɪs ʙᴏᴛ !</b>""",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton("Jᴏɪɴ ɴᴏᴡ 🚩", url=f"https://t.me/{Var.UPDATES_CHANNEL}")
                        ]
                    ]
                ),
                
            )
             return
        except Exception:
            await b.send_message(
                chat_id=m.chat.id,
                text="<b>sᴏᴍᴇᴛʜɪɴɢ ᴡᴇɴᴛ ᴡʀᴏɴɢ.ᴘʟᴇᴀsᴇ <a href='https://t.me/sahid_malik'>ᴄʟɪᴄᴋ ʜᴇʀᴇ ғᴏʀ sᴜᴘᴘᴏʀᴛ</a></b>",
                
                disable_web_page_preview=True)
            return
    await m.reply_text(
    #chat_id=m.chat.id,
    #photo="https://telegra.ph/file/d813fe75a3ac675ef34b7.jpg",
    text = SRT_TXT.format(m.from_user.mention), 
    disable_web_page_preview=True,
    reply_markup=InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("ᴜᴘᴅᴀᴛᴇ ᴄʜᴀɴɴᴇʟ 🤡", url="https://t.me/m_house786")],
            [
                 InlineKeyboardButton("ᴀʙᴏᴜᴛ 😎", callback_data="about"),
                 InlineKeyboardButton("ʜᴇʟᴘ 😅", callback_data="help")
            ],
            [InlineKeyboardButton("ᴏᴜʀ ɢʀᴏᴜᴘ 🚩", url=bisal_grp)],

            [
                 InlineKeyboardButton("ᴅɪsᴄʟᴀɪᴍᴇʀ 🔻", url=f"https://www.google.com"),
                 InlineKeyboardButton("ᴅᴇᴠ 😊", callback_data="aboutDev")
            ]
        ]
    ) 
)
@StreamBot.on_message(filters.command("help") & filters.private )
async def help_cd(b, m):
    if not await db.is_user_exist(m.from_user.id):
        await db.add_user(m.from_user.id)
        await b.send_message(
            Var.NEW_USER_LOG,
            f"**Nᴇᴡ Usᴇʀ Jᴏɪɴᴇᴅ:** \n\n__Mʏ Nᴇᴡ Fʀɪᴇɴᴅ__ [{m.from_user.first_name}](tg://user?id={m.from_user.id}) __Sᴛᴀʀᴛᴇᴅ Yᴏᴜʀ Bᴏᴛ !!__"
        )
    if Var.UPDATES_CHANNEL != "None":
        try:
            user = await b.get_chat_member(Var.UPDATES_CHANNEL, m.chat.id)
            if user.status == "kicked":
                await b.send_message(
                    chat_id=m.chat.id,
                    text="__𝓢𝓞𝓡𝓡𝓨, 𝓨𝓞𝓤 𝓐𝓡𝓔 𝓐𝓡𝓔 𝓑𝓐𝓝𝓝𝓔𝓓 𝓕𝓡𝓞𝓜 𝓤𝓢𝓘𝓝𝓖 𝓜𝓔. 𝓒ᴏɴᴛᴀᴄᴛ ᴛʜᴇ 𝓓ᴇᴠᴇʟᴏᴘᴇʀ__\n\n  **𝙃𝙚 𝙬𝙞𝙡𝙡 𝙝𝙚𝙡𝙥 𝙮𝙤𝙪**",
                    disable_web_page_preview=True
                )
                return
        except UserNotParticipant:
             await StreamBot.send_photo(
                chat_id=m.chat.id,
                photo="https://telegra.ph/file/5eb253f28ed7ed68cb4e6.png",
                caption=""""<b>Hᴇʏ ᴛʜᴇʀᴇ!\n\nPʟᴇᴀsᴇ ᴊᴏɪɴ ᴏᴜʀ ᴜᴘᴅᴀᴛᴇs ᴄʜᴀɴɴᴇʟ ᴛᴏ ᴜsᴇ ᴍᴇ ! 😊\n\nDᴜᴇ ᴛᴏ sᴇʀᴠᴇʀ ᴏᴠᴇʀʟᴏᴀᴅ, ᴏɴʟʏ ᴏᴜʀ ᴄʜᴀɴɴᴇʟ sᴜʙsᴄʀɪʙᴇʀs ᴄᴀɴ ᴜsᴇ ᴛʜɪs ʙᴏᴛ !</b>""",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton("Jᴏɪɴ ɴᴏᴡ 🚩", url=f"https://t.me/{Var.UPDATES_CHANNEL}")
                        ]
                    ]
                ),
                
            )
             return
        except Exception:
            await b.send_message(
                chat_id=m.chat.id,
                text="<b>sᴏᴍᴇᴛʜɪɴɢ ᴡᴇɴᴛ ᴡʀᴏɴɢ.ᴘʟᴇᴀsᴇ <a href='https://t.me/biisal_bot'>ᴄʟɪᴄᴋ ʜᴇʀᴇ ғᴏʀ sᴜᴘᴘᴏʀᴛ</a></b>",
                
                disable_web_page_preview=True)
            return
    await StreamBot.send_photo(
    chat_id=m.chat.id,
    photo="https://telegra.ph/file/d813fe75a3ac675ef34b7.jpg",
    caption=f"<b>ᴡᴇ ᴅᴏɴᴛ ɴᴇᴇᴅ ᴍᴀɴʏ <a href='https://t.me/sahid_malik'>ᴄᴏᴍᴍᴀɴᴅs</a> ᴛᴏ ᴜsᴇ ᴛʜɪs ʙᴏᴛ 🤩.\n\nᴊᴜsᴛ sᴇɴᴅ ᴍᴇ <a href='https://t.me/sahid_malik'>ᴠɪᴅᴇᴏ ғɪʟᴇs</a> ᴀɴᴅ ɪ ᴡɪʟʟ ɢɪᴠᴇ ʏᴏᴜ <a href='https://t.me/sahid_malik'>ᴅɪʀᴇᴄᴛ ᴅᴏᴡɴʟᴏᴀᴅ & sᴛʀᴇᴀᴍᴀʙʟᴇ</a> ʟɪɴᴋ.\n\nᴏʀ ʏᴏᴜ ᴄᴀɴ ᴜsᴇ ᴍᴇ ɪɴ <a href='https://t.me/sahid_malik'>ʏᴏᴜʀ ᴄʜᴀɴɴᴇʟ</a>..ᴊᴜsᴛ ᴀᴅᴅ ᴍᴇ ᴀɴᴅ ᴍᴀᴋᴇ ᴍᴇ ᴀᴅᴍɪɴ ᴀɴᴅ sᴇᴇ ᴍʏ ᴍᴀɢɪᴄ 😎</b>",
    reply_markup=InlineKeyboardMarkup(
        [
            [   
                InlineKeyboardButton("ᴜᴘᴅᴀᴛᴇ ᴄʜᴀɴɴᴇʟ 🤡", url=bisal_channel)
            ],
            [
                InlineKeyboardButton("ᴅɪsᴄʟᴀɪᴍᴇʀ 🔻", url=f"https://www.google.com"),
                InlineKeyboardButton("ᴏᴜʀ ɢʀᴏᴜᴘ 🚩", url=bisal_grp),

            ],
            [
                InlineKeyboardButton("ʜᴏᴍᴇ", callback_data="start"),

            ]

        ]
    )
)
@StreamBot.on_message(filters.command('ban') & filters.user(Var.OWNER_ID))
async def do_ban(bot ,  message):
    userid = message.text.split(" ", 2)[1] if len(message.text.split(" ", 1)) > 1 else None
    reason = message.text.split(" ", 2)[2] if len(message.text.split(" ", 2)) > 2 else None
    if not userid:
        return await message.reply('<b>ᴘʟᴇᴀsᴇ ᴀᴅᴅ ᴀ ᴠᴀʟɪᴅ ᴜsᴇʀ/ᴄʜᴀɴɴᴇʟ ɪᴅ ᴡɪᴛʜ ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ\n\nᴇx : /ban (user/channel_id) (banning reason[Optional]) \nʀᴇᴀʟ ᴇx : <code>/ban 1234567899</code>\nᴡɪᴛʜ ʀᴇᴀsᴏɴ ᴇx:<code>/ban 1234567899 seding adult links to bot</code>\nᴛᴏ ʙᴀɴ ᴀ ᴄʜᴀɴɴᴇʟ :\n<code>/ban CHANEL_ID</code>\nᴇx : <code>/ban -1001234567899</code></b>')
    text = await message.reply("<b>ʟᴇᴛ ᴍᴇ ᴄʜᴇᴄᴋ 👀</b>")
    banSts = await db.ban_user(userid)
    if banSts == True:
        await text.edit(
    text=f"<b><code>{userid}</code> ʜᴀs ʙᴇᴇɴ ʙᴀɴɴᴇᴅ sᴜᴄᴄᴇssғᴜʟʟʏ\n\nSʜᴏᴜʟᴅ I sᴇɴᴅ ᴀɴ ᴀʟᴇʀᴛ ᴛᴏ ᴛʜᴇ ʙᴀɴɴᴇᴅ ᴜsᴇʀ?</b>",
    reply_markup=InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("ʏᴇs ✅", callback_data=f"sendAlert_{userid}_{reason if reason else 'no reason provided'}"),
                InlineKeyboardButton("ɴᴏ ❌", callback_data=f"noAlert_{userid}"),
            ],
        ]
    ),
)
    else:
        await text.edit(f"<b>Cᴏɴᴛʀᴏʟʟ ʏᴏᴜʀ ᴀɴɢᴇʀ ʙʀᴏ...\n<code>{userid}</code> ɪs ᴀʟʀᴇᴀᴅʏ ʙᴀɴɴᴇᴅ !!</b>")
    return


@StreamBot.on_message(filters.command('unban') & filters.user(Var.OWNER_ID))
async def do_unban(bot ,  message):
    userid = message.text.split(" ", 2)[1] if len(message.text.split(" ", 1)) > 1 else None
    if not userid:
        return await message.reply('ɢɪᴠᴇ ᴍᴇ ᴀɴ ɪᴅ\nᴇx : <code>/unban 1234567899<code>')
    text = await message.reply("<b>ʟᴇᴛ ᴍᴇ ᴄʜᴇᴄᴋ 🥱</b>")
    unban_chk = await db.is_unbanned(userid)
    if  unban_chk == True:
        await text.edit(text=f'<b><code>{userid}</code> ɪs ᴜɴʙᴀɴɴᴇᴅ\nSʜᴏᴜʟᴅ I sᴇɴᴅ ᴛʜᴇ ʜᴀᴘᴘʏ ɴᴇᴡs ᴀʟᴇʀᴛ ᴛᴏ ᴛʜᴇ ᴜɴʙᴀɴɴᴇᴅ ᴜsᴇʀ?</b>',
        reply_markup=InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("ʏᴇs ✅", callback_data=f"sendUnbanAlert_{userid}"),
                InlineKeyboardButton("ɴᴏ ❌", callback_data=f"NoUnbanAlert_{userid}"),
            ],
        ]
    ),
)

    elif unban_chk==False:
        await text.edit('<b>ᴜsᴇʀ ɪs ɴᴏᴛ ʙᴀɴɴᴇᴅ ʏᴇᴛ.</b>')
    else :
        await text.edit(f"<b>ғᴀɪʟᴇᴅ ᴛᴏ ᴜɴʙᴀɴ ᴜsᴇʀ/ᴄʜᴀɴɴᴇʟ.\nʀᴇᴀsᴏɴ : {unban_chk}</b>")



@StreamBot.on_callback_query()
async def cb_handler(client, query):
    data = query.data
    if data == "close_data":
        await query.message.delete()


    if data == "start":
        btn = [[InlineKeyboardButton("ᴜᴘᴅᴀᴛᴇ ᴄʜᴀɴɴᴇʟ 🤡", url="https://t.me/m_house786"),
           ],[
           InlineKeyboardButton("ᴀʙᴏᴜᴛ 😎", callback_data="about"),
           InlineKeyboardButton("ʜᴇʟᴘ 😅", callback_data="help")
           ],[
           InlineKeyboardButton("ᴏᴜʀ ɢʀᴏᴜᴘ 🚩", url=bisal_grp),
           InlineKeyboardButton("ᴅɪsᴄʟᴀɪᴍᴇʀ 🔻", url=f"https://telegra.ph/Disclaimer-11-07-37"),
           ],[
           InlineKeyboardButton("ᴅᴇᴠ 😊", callback_data="aboutDev")
           ]] 
        msg_txt = SRT_TXT.format(query.from_user.mention)
        await query.message.edit_text(msg_txt, disable_web_page_preview=True, reply_markup=InlineKeyboardMarkup(btn)) #reply_markup=reply_markup,parse_mode=enums.ParseMode.HTML))
    
    elif data == "about":
        btn = [[
            btns("ʜᴏᴍᴇ", callback_data="start"),
            btns("ᴄʟᴏsᴇ ‼️", callback_data="close_data")
        ]]
        await query.message.edit_text(text=f"<b>Mʏ ɴᴀᴍᴇ :<a href='https://t.me/filetolink65bot'>{bot_name}</a>\nAᴅᴍɪɴ : <a href='https://t.me/sahid_malik'>Sahid malik</a>\nʜᴏsᴛᴇᴅ ᴏɴ : ʜᴇʀᴏᴋᴜ\nᴅᴀᴛᴀʙᴀsᴇ : ᴍᴏɴɢᴏ ᴅʙ\nʟᴀɴɢᴜᴀɢᴇ : ᴘʏᴛʜᴏɴ 3</b>", disable_web_page_preview=True, reply_markup=btns2(btn))
    elif data == "help":
        btn=[[
            btns("ʜᴏᴍᴇ", callback_data="start"),
            btns("ᴄʟᴏsᴇ ‼️", callback_data="close_data") 
        ]]
        await query.message.edit_text(text=f"<b>ᴡᴇ ᴅᴏɴᴛ ɴᴇᴇᴅ ᴍᴀɴʏ ᴄᴏᴍᴍᴀɴᴅs ᴛᴏ ᴜsᴇ ᴛʜɪs ʙᴏᴛ 🤩.\n\nᴊᴜsᴛ sᴇɴᴅ ᴍᴇ ᴠɪᴅᴇᴏ ғɪʟᴇs ᴀɴᴅ ɪ ᴡɪʟʟ ɢɪᴠᴇ ʏᴏᴜ ᴅɪʀᴇᴄᴛ ᴅᴏᴡɴʟᴏᴀᴅ & sᴛʀᴇᴀᴍᴀʙʟᴇ</a> ʟɪɴᴋ.\n\nᴏʀ ʏᴏᴜ ᴄᴀɴ ᴜsᴇ ᴍᴇ ɪɴ <a href='https://t.me/m_admins'>ʏᴏᴜʀ ᴄʜᴀɴɴᴇʟ</a>..ᴊᴜsᴛ ᴀᴅᴅ ᴍᴇ ᴀɴᴅ ᴍᴀᴋᴇ ᴍᴇ ᴀᴅᴍɪɴ ᴀɴᴅ sᴇᴇ ᴍʏ ᴍᴀɢɪᴄ 😎</b>", disable_web_page_preview=True, reply_markup=btns2(btn))
            

            
    elif data == "aboutDev":
        # please don't steal credit
        btn=[[
            btns("ʜᴏᴍᴇ", callback_data="start"),
            btns("ᴄʟᴏsᴇ ‼️", callback_data="close_data") 
        ]]
        await query.message.edit_text(text=f"<b>ɪᴍ <a href='https://t.me/sahid_malik'>Sahid malik</a>\nɪ ᴀᴍ ᴛʜᴇ ᴀᴅᴍɪɴ ᴏғ ᴛʜɪs ʙᴏᴛ..ᴀɴᴅ ɪ ᴍᴀᴅᴇ ᴛʜᴇ  ʙᴏᴛ ʙʏ ʜᴇʟᴘ ᴏғ <a href='https://github.com/adarsh-goel'>ᴀᴅᴀʀsʜ</a> ʙʀᴏ..</b>", disable_web_page_preview=True, reply_markup=btns2(btn))

    
    elif data.startswith("sendAlert"):
        user_id =(data.split("_")[1])
        user_id = int(user_id.replace(' ' , ''))
        if len(str(user_id)) == 10:
            reason = str(data.split("_")[2])
            try:
                await client.send_message(user_id , f'<b>ʏᴏᴜ ᴀʀᴇ ʙᴀɴɴᴇᴅ ʙʏ ᴀᴅᴍɪɴ.\nRᴇᴀsᴏɴ : {reason}</b>')
                await query.message.edit(f"<b>Aʟᴇʀᴛ sᴇɴᴛ ᴛᴏ <code>{user_id}</code>\nRᴇᴀsᴏɴ : {reason}</b>")
            except Exception as e:
                await query.message.edit(f"<b>sʀʏ ɪ ɢᴏᴛ ᴛʜɪs ᴇʀʀᴏʀ : {e}</b>")
        else:
            await query.message.edit(f"<b>Tʜᴇ ᴘʀᴏᴄᴇss ᴡᴀs ɴᴏᴛ ᴄᴏᴍᴘʟᴇᴛᴇᴅ ʙᴇᴄᴀᴜsᴇ ᴛʜᴇ ᴜsᴇʀ ɪᴅ ᴡᴀs ɴᴏᴛ ᴠᴀʟɪᴅ, ᴏʀ ᴘᴇʀʜᴀᴘs ɪᴛ ᴡᴀs ᴀ ᴄʜᴀɴɴᴇʟ ɪᴅ</b>")

    elif data.startswith('noAlert'):
        user_id =(data.split("_")[1])
        user_id = int(user_id.replace(' ' , ''))
        await query.message.edit(f"<b>Tʜᴇ ʙᴀɴ ᴏɴ <code>{user_id}</code> ᴡᴀs ᴇxᴇᴄᴜᴛᴇᴅ sɪʟᴇɴᴛʟʏ.</b>")

    elif data.startswith('sendUnbanAlert'):
        user_id =(data.split("_")[1])
        user_id = int(user_id.replace(' ' , ''))
        if len(str(user_id)) == 10:
            try:
                unban_text = '<b>ʜᴜʀʀᴀʏ..ʏᴏᴜ ᴀʀᴇ ᴜɴʙᴀɴɴᴇᴅ ʙʏ ᴀᴅᴍɪɴ.</b>'
                await client.send_message(user_id , unban_text)
                await query.message.edit(f"<b>Uɴʙᴀɴɴᴇᴅ Aʟᴇʀᴛ sᴇɴᴛ ᴛᴏ <code>{user_id}</code>\nᴀʟᴇʀᴛ ᴛᴇxᴛ : {unban_text}</b>")
            except Exception as e:
                await query.message.edit(f"<b>sʀʏ ɪ ɢᴏᴛ ᴛʜɪs ᴇʀʀᴏʀ : {e}</b>")
        else:
            await query.message.edit(f"<b>Tʜᴇ ᴘʀᴏᴄᴇss ᴡᴀs ɴᴏᴛ ᴄᴏᴍᴘʟᴇᴛᴇᴅ ʙᴇᴄᴀᴜsᴇ ᴛʜᴇ ᴜsᴇʀ ɪᴅ ᴡᴀs ɴᴏᴛ ᴠᴀʟɪᴅ, ᴏʀ ᴘᴇʀʜᴀᴘs ɪᴛ ᴡᴀs ᴀ ᴄʜᴀɴɴᴇʟ ɪᴅ</b>")   
    elif data.startswith('NoUnbanAlert'):
        user_id =(data.split("_")[1])
        user_id = int(user_id.replace(' ' , ''))
        await query.message.edit(f"Tʜᴇ ᴜɴʙᴀɴ ᴏɴ <code>{user_id}</code> ᴡᴀs ᴇxᴇᴄᴜᴛᴇᴅ sɪʟᴇɴᴛʟʏ.")

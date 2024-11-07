import asyncio
from FileStream.bot import FileStream, multi_clients
from FileStream.utils.bot_utils import (
    is_user_banned,
    is_user_exist,
    is_user_joined,
    gen_link,
    is_channel_banned,
    is_channel_exist,
    is_user_authorized
)
from FileStream.utils.database import Database
from FileStream.utils.file_properties import get_file_ids, get_file_info
from FileStream.config import Telegram
from pyrogram import filters, Client
from pyrogram.errors import FloodWait
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.enums.parse_mode import ParseMode

db = Database(Telegram.DATABASE_URL, Telegram.SESSION_NAME)

@FileStream.on_message(
    filters.private
    & (
        filters.document
        | filters.video
        | filters.video_note
        | filters.audio
        | filters.voice
        | filters.animation
        | filters.photo
    ),
    group=4,
)
async def private_receive_handler(bot: Client, message: Message):
    if not await is_user_authorized(message):
        return
    if await is_user_banned(message):
        return

    await is_user_exist(bot, message)
    if Telegram.FORCE_SUB:
        if not await is_user_joined(bot, message):
            return
    try:
        inserted_id = await db.add_file(get_file_info(message))
        print(f"File added with ID: {inserted_id}")
        await get_file_ids(False, inserted_id, multi_clients, message)
        reply_markup, stream_text = await gen_link(_id=inserted_id)
        print(f"replyMarkuop: {reply_markup} \n\n stream Text: {stream_text}")
        await message.reply_text(
            text=stream_text,
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=True,
            reply_markup=reply_markup,
            quote=True
        )
    except FloodWait as e:
        print(f"Sleeping for {str(e.value)}s")
        await asyncio.sleep(e.value)
        await bot.send_message(
            chat_id=Telegram.ULOG_CHANNEL,
            text=(
                f"Gᴏᴛ FʟᴏᴏᴅWᴀɪᴛ ᴏғ {str(e.value)}s ғʀᴏᴍ "
                f"[{message.from_user.first_name}](tg://user?id={message.from_user.id})\n\n"
                f"**ᴜsᴇʀ ɪᴅ :** `{str(message.from_user.id)}`"
            ),
            disable_web_page_preview=True,
            parse_mode=ParseMode.MARKDOWN
        )

@FileStream.on_message(
    filters.channel
    & ~filters.forwarded
    & ~filters.media_group
    & (
        filters.document
        | filters.video
        | filters.video_note
        | filters.audio
        | filters.voice
        | filters.photo
    )
)
async def channel_receive_handler(bot: Client, message: Message):
    if await is_channel_banned(bot, message):
        return
    await is_channel_exist(bot, message)

    try:
        inserted_id = await db.add_file(get_file_info(message))
        print(f"File added with ID: {inserted_id}")
        await get_file_ids(False, inserted_id, multi_clients, message)
        reply_markup, stream_link = await gen_link(_id=inserted_id)
        print(f"replyMarkuop: {reply_markup} \n\n stream Text: {stream_link}")
        await bot.edit_message_reply_markup(
            chat_id=message.chat.id,
            message_id=message.id,
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton(
                    "Dᴏᴡɴʟᴏᴀᴅ ʟɪɴᴋ 📥",
                    url=f"https://t.me/{FileStream.username}?start=stream_{str(inserted_id)}"
                )]]
            )
        )

    except FloodWait as w:
        print(f"Sleeping for {str(w.x)}s")
        await asyncio.sleep(w.x)
        await bot.send_message(
            chat_id=Telegram.ULOG_CHANNEL,
            text=(
                f"ɢᴏᴛ ғʟᴏᴏᴅᴡᴀɪᴛ ᴏғ {str(w.x)}s ғʀᴏᴍ {message.chat.title}\n\n"
                f"**ᴄʜᴀɴɴᴇʟ ɪᴅ :** `{str(message.chat.id)}`"
            ),
            disable_web_page_preview=True
        )
    except Exception as e:
        await bot.send_message(
            chat_id=Telegram.ULOG_CHANNEL,
            text=f"**#EʀʀᴏʀTʀᴀᴄᴋᴇʙᴀᴄᴋ:** `{e}`",
            disable_web_page_preview=True
        )
        print(
            f"Cᴀɴ'ᴛ Eᴅɪᴛ Bʀᴏᴀᴅᴄᴀsᴛ Mᴇssᴀɢᴇ!\n"
            f"Eʀʀᴏʀ:  **Gɪᴠᴇ ᴍᴇ ᴇᴅɪᴛ ᴘᴇʀᴍɪssɪᴏɴ ɪɴ ᴜᴘᴅᴀᴛᴇs ᴀɴᴅ ʙɪɴ Cʜᴀɴɴᴇʟ!{e}**"
        )

@FileStream.on_message(filters.command(["link"]))
async def link_command_handler(bot: Client, message: Message):
    replied_message = message.reply_to_message

    # User Authorization and Existence Checks
    if not await is_user_authorized(message):
        return
    if await is_user_banned(message):
        return
    await is_user_exist(bot, message)

    try:
        if not replied_message or not replied_message.media:
            await message.reply_text(
                text="Please reply to a message containing media to generate a link.",
                quote=True
            )
            return

        # Add the file information to the database
        inserted_id = await db.add_file(get_file_info(replied_message))
        print(f"File added with ID: {inserted_id}")
        # Generate the file IDs and the link
        await get_file_ids(False, inserted_id, multi_clients, replied_message)

        # Generate the link
        reply_markup, stream_text = await gen_link(_id=inserted_id)
        print(f"replyMarkuop: {reply_markup} \n\n stream Text: {stream_text}")

        # Send the link back to the user
        await message.reply_text(
            text=stream_text,
            quote=True,
            disable_web_page_preview=True,
            reply_markup=reply_markup
        )

    except FloodWait as e:
        print(f"Sleeping for {str(e.value)}s")
        await asyncio.sleep(e.value)
        await bot.send_message(
            chat_id=Telegram.ULOG_CHANNEL,
            text=(
                f"Gᴏᴛ FʟᴏᴏᴅWᴀɪᴛ ᴏғ {str(e.value)}s ғʀᴏᴍ "
                f"[{message.from_user.first_name}](tg://user?id={message.from_user.id})\n\n"
                f"**ᴜsᴇʀ ɪᴅ :** `{str(message.from_user.id)}`"
            ),
            disable_web_page_preview=True,
            parse_mode=ParseMode.MARKDOWN
        )
    except Exception as e:
        await bot.send_message(
            chat_id=Telegram.ULOG_CHANNEL,
            text=f"**#EʀʀᴏʀTʀᴀᴄᴋᴇʙᴀᴄᴋ:** `{e}`",
            disable_web_page_preview=True
        )
        print(
            f"An error occurred in /link command:\n"
            f"Eʀʀᴏʀ: **{e}**"
        )

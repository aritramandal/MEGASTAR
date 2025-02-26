"""@telegraph Utilities
Available Commands:
.tele media as reply to a media
.tele text as reply to a large text"""
import os
from datetime import datetime

from PIL import Image
from telegraph import Telegraph, exceptions, upload_file

from userbot.utils import admin_cmd

from . import CMD_HELP

telegraph = Telegraph()
r = telegraph.create_account(short_name=config.TELEGRAPH_SHORT_NAME)
auth_url = r["auth_url"]


@borg.on(admin_cmd("tele (media|text) ?(.*)"))
async def _(event):
    if event.fwd_from:
        return
    if config.PRIVATE_GROUP_ID is None:
        await event.edit(
            "Please set the required environment variable `PLUGIN_CHANNEL` for this plugin to work"
        )
        return
    if not os.path.isdir(config.TMP_DOWNLOAD_DIRECTORY):
        os.makedirs(config.TMP_DOWNLOAD_DIRECTORY)
    await borg.send_message(
        config.PRIVATE_GROUP_ID,
        "Created New Telegraph account {} for the current session. \n**Do not give this url to anyone, even if they say they are from Telegram!**".format(
            auth_url
        ),
    )
    optional_title = event.pattern_match.group(2)
    if event.reply_to_msg_id:
        start = datetime.now()
        r_message = await event.get_reply_message()
        input_str = event.pattern_match.group(1)
        if input_str == "media":
            downloaded_file_name = await borg.download_media(
                r_message, config.TMP_DOWNLOAD_DIRECTORY
            )
            end = datetime.now()
            ms = (end - start).seconds
            await event.edit(
                "Downloaded to {} in {} seconds.".format(downloaded_file_name, ms)
            )
            if downloaded_file_name.endswith((".webp")):
                resize_image(downloaded_file_name)
            try:
                start = datetime.now()
                media_urls = upload_file(downloaded_file_name)
            except exceptions.TelegraphException as exc:
                await event.edit("ERROR: " + str(exc))
                os.remove(downloaded_file_name)
            else:
                end = datetime.now()
                ms_two = (end - start).seconds
                os.remove(downloaded_file_name)
                await event.edit(
                    "File uploaded ser By MEGASTAR USERBOT https://telegra.ph{} ".format(
                        media_urls[0], (ms + ms_two)
                    ),
                    link_preview=True,
                )
        elif input_str == "text":
            user_object = await borg.get_entity(r_message.from_id)
            title_of_page = user_object.first_name  # + " " + user_object.last_name
            # apparently, all Users do not have last_name field
            if optional_title:
                title_of_page = optional_title
            page_content = r_message.message
            if r_message.media:
                if page_content != "":
                    title_of_page = page_content
                downloaded_file_name = await borg.download_media(
                    r_message, config.TMP_DOWNLOAD_DIRECTORY
                )
                m_list = None
                with open(downloaded_file_name, "rb") as fd:
                    m_list = fd.readlines()
                for m in m_list:
                    page_content += m.decode("UTF-8") + "\n"
                os.remove(downloaded_file_name)
            page_content = page_content.replace("\n", "<br>")
            response = telegraph.create_page(title_of_page, html_content=page_content)
            end = datetime.now()
            ms = (end - start).seconds
            await event.edit(
                "Pasted ser https://telegra.ph/{} in {} seconds.".format(
                    response["path"], ms
                ),
                link_preview=True,
            )
    else:
        await event.edit(
            "Reply to a message to get a permanent telegra.ph link. (Inspired by @ControllerBot)"
        )


def resize_image(image):
    im = Image.open(image)
    im.save(image, "PNG")


CMD_HELP.update(
    {
        "telegraph": "**Plugin :**`telegraph`\
     \n\n**Syntax :** `.tele media`\
     \n**Usage :** Reply to any image or video to upload it to telegraph (video must be less than 5mb)\
     \n\n**Syntax :** `.tele text`\
     \n**Usage :** reply to any text file or any message to paste it to telegraph\
    "
    }
)

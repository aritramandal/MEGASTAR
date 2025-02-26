import asyncio
import os
import time
from datetime import datetime

from ..utils import admin_cmd, edit_or_reply
from . import CMD_HELP

thumb_image_path = config.TMP_DOWNLOAD_DIRECTORY + "thumb_image.jpg"


@borg.on(admin_cmd(pattern="rename (.*)"))
async def _(event):
    if event.fwd_from:
        return
    event = await edit_or_reply(
        event,
        "`Renaming in process 🙄🙇‍♂️🙇‍♂️🙇‍♀️ It might take some time if file size is big`",
    )
    input_str = event.pattern_match.group(1)
    if not os.path.isdir(config.TMP_DOWNLOAD_DIRECTORY):
        os.makedirs(config.TMP_DOWNLOAD_DIRECTORY)
    if event.reply_to_msg_id:
        start = datetime.now()
        file_name = input_str
        reply_message = await event.get_reply_message()
        c_time = time.time()
        to_download_directory = config.TMP_DOWNLOAD_DIRECTORY
        downloaded_file_name = os.path.join(to_download_directory, file_name)
        downloaded_file_name = await event.client.download_media(
            reply_message,
            downloaded_file_name,
            progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                progress(d, t, event, c_time, "trying to download", file_name)
            ),
        )
        end = datetime.now()
        ms = (end - start).seconds
        if os.path.exists(downloaded_file_name):
            await event.edit(
                f"**File Downloaded in {ms} seconds.**\n**File location : **`{downloaded_file_name}`"
            )
        else:
            await event.edit("Error Occurred\n {}".format(input_str))
    else:
        await event.edit(
            "**Syntax : ** `.rename file.name` as reply to a Telegram media"
        )


@borg.on(admin_cmd(pattern="rnup (.*)"))
async def _(event):
    if event.fwd_from:
        return
    thumb = None
    if os.path.exists(thumb_image_path):
        thumb = thumb_image_path
    event = await edit_or_reply(
        event,
        "`Rename & Upload in process 🙄🙇‍♂️🙇‍♂️🙇‍♀️ It might take some time if file size is big`",
    )
    input_str = event.pattern_match.group(1)
    if not os.path.isdir(config.TMP_DOWNLOAD_DIRECTORY):
        os.makedirs(config.TMP_DOWNLOAD_DIRECTORY)
    if event.reply_to_msg_id:
        start = datetime.now()
        file_name = input_str
        reply_message = await event.get_reply_message()
        c_time = time.time()
        to_download_directory = config.TMP_DOWNLOAD_DIRECTORY
        downloaded_file_name = os.path.join(to_download_directory, file_name)
        downloaded_file_name = await event.client.download_media(
            reply_message,
            downloaded_file_name,
            progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                progress(d, t, event, c_time, "trying to download", file_name)
            ),
        )
        end = datetime.now()
        ms_one = (end - start).seconds
        try:
            thumb = await reply_message.download_media(thumb=-1)
        except Exception:
            thumb = thumb
        if os.path.exists(downloaded_file_name):
            c_time = time.time()
            caat = await event.client.send_file(
                event.chat_id,
                downloaded_file_name,
                force_document=False,
                supports_streaming=True,
                allow_cache=False,
                reply_to=event.message.id,
                thumb=thumb,
                progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                    progress(
                        d, t, event, c_time, "trying to upload", downloaded_file_name
                    )
                ),
            )
            end_two = datetime.now()
            os.remove(downloaded_file_name)
            ms_two = (end_two - end).seconds
            await event.edit(
                f"`Downloaded file in {ms_one} seconds.`\n`Uploaded in {ms_two} seconds.`"
            )
            await asyncio.sleep(3)
            await event.delete()
        else:
            await event.edit("File Not Found {}".format(input_str))
    else:
        await event.edit(
            "**Syntax : **`.rnupload file.name` as reply to a Telegram media"
        )


CMD_HELP.update(
    {
        "rename": "**Plugin : **`rename`\
    \n\n**Syntax : **`.rename filename`\
    \n**Function : **__Reply to media with above command to save in your server with that given filename__\
    \n\n**Syntax : **`.rnup filename`\
    \n**Function : **__Reply to media with above command to rename and upload the file with given name__\
    "
    }
)

# ported from paperplaneExtended by avinashreddy3108 for media support


from ..utils import admin_cmd, edit_or_reply
from . import BOTLOG_CHATID, CMD_HELP
from .sql_helper.snip_sql import add_note, get_note, get_notes, rm_note


@borg.on(admin_cmd(pattern=r"snips (\w*)"))
async def add_snip(fltr):
    keyword = fltr.pattern_match.group(1)
    string = fltr.text.partition(keyword)[2]
    msg = await fltr.get_reply_message()
    msg_id = None
    if msg and msg.media and not string:
        if BOTLOG_CHATID:
            await bot.send_message(
                BOTLOG_CHATID,
                f"#NOTE\
                  \nKEYWORD: `#{keyword}`\
                  \n\nThe following message is saved as the snip in your bot , do NOT delete it !!",
            )
            msg_o = await bot.forward_messages(
                entity=BOTLOG_CHATID, messages=msg, from_peer=fltr.chat_id, silent=True
            )
            msg_id = msg_o.id
        else:
            await edit_or_reply(
                fltr,
                "Saving media as data for the note requires the `PRIVATE_GROUP_BOT_API_ID` to be set.",
            )
            return
    elif fltr.reply_to_msg_id and not string:
        rep_msg = await fltr.get_reply_message()
        string = rep_msg.text
    success = "Note {}  is successfully saved. Use` #{} `to get it"
    if add_note(keyword, string, msg_id) is False:
        rm_note(keyword)
        if add_note(keyword, string, msg_id) is False:
            return await edit_or_reply(
                fltr, f"Error in saving the given snip {keyword}"
            )
        return await edit_or_reply(fltr, success.format("updated", keyword))
    return await edit_or_reply(fltr, success.format("added", keyword))


@borg.on(admin_cmd(pattern="snipl$"))
async def on_snip_list(event):
    message = "There are no saved notes in this chat"
    notes = get_notes()
    for note in notes:
        if message == "There are no saved notes in this chat":
            message = "Notes saved in this chat:\n"
        message += "👉 `#{}`\n".format(note.keyword)
    if len(message) > Config.MAX_MESSAGE_SIZE_LIMIT:
        with io.BytesIO(str.encode(message)) as out_file:
            out_file.name = "snips.text"
            await bot.send_file(
                event.chat_id,
                out_file,
                force_document=True,
                allow_cache=False,
                caption="Available Snips",
                reply_to=event,
            )
            await event.delete()
    else:
        await edit_or_reply(event, message)


@borg.on(admin_cmd(pattern=r"snipd (\S+)"))
async def on_snip_delete(event):
    name = event.pattern_match.group(1)
    snip = get_note(name)
    if snip:
        rm_note(name)
    else:
        return await edit_or_reply(
            event, f"Are you sure that #{name} is saved as snip?"
        )
    await edit_or_reply(event, "snip #{} deleted successfully".format(name))


CMD_HELP.update(
    {
        "snip": "**Plugin :** `snip`\
\n\n**Syntax :** #<snipname>\
\n**Usage :** Gets the specified note.\
\n\n**Syntax :** `.snips: reply to a message with .snips <notename>`\
\n**Usage :** Saves the replied message as a note with the notename. (Works with pics, docs, and stickers too!)\
\n\n**Syntax :** `.snipl`\
\n**Usage :** Gets all saved notes in a chat.\
\n\n**Syntax :** `.snipd <notename>`\
\n**Usage :** Deletes the specified note.\
"
    }
)

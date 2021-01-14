from math import ceil
from re import compile

from telethon.events import InlineQuery, callbackquery
from telethon.sync import custom
from telethon.tl.functions.channels import JoinChannelRequest

from userbot import *
from userbot.utils import *

def button(page, modules):
    Row = config.NO_OF_BUTTONS_DISPLAYED_IN_H_ME_CMD
    Column = config.NO_OF_COLOUMS_DISPLAYED_IN_H_ME_CMD

    modules = sorted([modul for modul in modules if not modul.startswith("◉‿◉")])
    pairs = list(map(list, zip(modules[::2], modules[1::2])))
    if len(modules) % 2 == 1:
        pairs.append([modules[-1]])
    max_pages = ceil(len(pairs) / Row)
    pairs = [pairs[i : i + Row] for i in range(0, len(pairs), Row)]
    buttons = []
    for pairs in pairs[page]:
        buttons.append(
            [
                custom.Button.inline("✰ " + pair, data=f"Information[{page}]({pair})")
                for pair in pairs
            ]
        )

    buttons.append(
        [
            custom.Button.inline(
                "☜," data=f"page({(max_pages - 1) if page == 0 else (page - 1)})"
            ),
            custom.Button.inline(
              "⌧", data="close"
            ),
            custom.Button.inline(
                "☞", data=f"page({0 if page == (max_pages - 1) else page + 1})"
            ),
        ]
    )
    return [max_pages, buttons]
    
    modules = CMD_HELP
if Var.TG_BOT_USER_NAME_BF_HER is not None and tgbot is not None:
    @tgbot.on(InlineQuery)  # pylint:disable=E0602
    async def inline_handler(event):
        builder = event.builder
        result = None
        query = event.text
        if event.query.user_id == bot.uid and query == "@MEGASTAR_USERBOT":
            rev_text = query[::-1]
            veriler = button(0, sorted(CMD_HELP))
            result = await builder.article(
                f"Hey! Only use .help please",
                text=f"**Megastar Helper to reveal all the commands 🥳\nDo** `.help plugin_name` **for commands, in case popup doesn't appear.🌹\n @MEGASTAR_SUPPORT\nCurrently Loaded Plugins**:`{len(CMD_HELP)}`\n**page:** 1/{veriler[0]}",
                buttons=veriler[1],
                link_preview=False,
            )
        elif query.startswith("http"):
            part = query.split(" ")
            result = builder.article(
                "File uploaded",
                text=f"**File uploaded successfully to {part[2]} site.\n\nUpload Time : {part[1][:3]} second\n[‏‏‎ ‎]({part[0]})",
                buttons=[[custom.Button.url("URL", part[0])]],
                link_preview=True,
            )
        else:
            result = builder.article(
                "@MEGASTAR_USERBOT",
                text="""**Hey! This is [🄼🄴🄶🄰🅂🅃🄰🅁](https://t.me/MEGASTAR_USERBOT) \nYou can know more about me from the links given below 👇**""",
                buttons=[
                    [
                        custom.Button.url(" 𝙲𝚑𝚊𝚗𝚗𝚎𝚕 ", "https://t.me/MEGASTAR_USERBOT"),
                        custom.Button.url(
                            "𝙶𝚛𝚘𝚞𝚙 ", "https://t.me/ /MEGASTAR_SUPPORT"
                        ),
                    ],
                    [
                        custom.Button.url(
                            "𝚁𝚎𝚙𝚘𝚜𝚒𝚝𝚘𝚛𝚢 ", "https://github.com/Bristi-OP/MEGASTAR"),
                        custom.Button.url
                    (
                            " 𝚃𝚞𝚝𝚘𝚛𝚒𝚊𝚕", "http://youtu.be/bzk16hwJVr0"
                    )
                    ],
                ],
                link_preview=False,
            )
        await event.answer([result] if result else None)

    @tgbot.on(callbackquery.CallbackQuery(data=compile(b"page\((.+?)\)")))
    async def page(event):
        if not event.query.user_id == bot.uid:
            return await event.answer(
                "Please Deploy your own Megastar userbot.. don't try to use mine😕",
                cache_time=0,
                alert=True,
            )
        page = int(event.data_match.group(1).decode("UTF-8"))
        veriler = button(page, CMD_HELP)
        await event.edit(
            f"**Megastar Helper to reveal all the commands 🥳\nDo** `.help plugin_name` **for commands, in case popup doesn't appear.🌹\n @MEGASTAR_SUPPORT\nCurrently Loaded Plugins:** `{len(CMD_HELP)}`\n**page:** {page + 1}/{veriler[0]}",
            buttons=veriler[1],
            link_preview=False,
        )
        
    @tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"close")))
    async def on_plug_in_callback_query_handler(event):
        if event.query.user_id == bot.uid:
            await event.edit(
                "✞ Megastar help menu closed ✞"
            )
          
    @tgbot.on(
        callbackquery.CallbackQuery(data=compile(b"Information\[(\d*)\]\((.*)\)"))
    )
    async def Information(event):
        if not event.query.user_id == bot.uid:
            return await event.answer(
                "Please deploy your own Megastar userbot and don't try to use mine😕",
                cache_time=0,
                alert=True,
            )

        page = int(event.data_match.group(1).decode("UTF-8"))
        commands = event.data_match.group(2).decode("UTF-8")
        try:
            buttons = [
                custom.Button.inline(
                    "🔹 " + cmd[0], data=f"commands[{commands}[{page}]]({cmd[0]})"
                )
                for cmd in CMD_HELP_BOT[commands]["commands"].items()
            ]
        except KeyError:
            return await event.answer(
                "No Description is written for this plugin", cache_time=0, alert=True
            )

        buttons = [buttons[i : i + 2] for i in range(0, len(buttons), 2)]
        buttons.append([custom.Button.inline("☜", data=f"page({page})")])
        await event.edit(
            f"**Plugin Name ☞:** `{commands}`\n** Number of commands found ☞:** `{len(CMD_HELP_BOT[commands]['commands'])}`",
            buttons=buttons,
            link_preview=False,
        )

    @tgbot.on(
        callbackquery.CallbackQuery(data=compile(b"commands\[(.*)\[(\d*)\]\]\((.*)\)"))
    )
    async def commands(event):
        if not event.query.user_id == bot.uid:
            return await event.answer(
                "Please Deploy your own Megastar userbot and don't try to use mine😕",
                cache_time=0,
                alert=True,
            )

        cmd = event.data_match.group(1).decode("UTF-8")
        page = int(event.data_match.group(2).decode("UTF-8"))
        commands = event.data_match.group(3).decode("UTF-8")

        result = f"**Plugin Name ☞:** `{cmd}`\n"
        if CMD_HELP_BOT[cmd]["info"]["info"] == "":
            if not CMD_HELP_BOT[cmd]["info"]["warning"] == "":
                result += f"**⬇️ Official:** {'✅' if CMD_HELP_BOT[cmd]['info']['official'] else '❌'}\n"
                result += f"**⚠️ Warning :** {CMD_HELP_BOT[cmd]['info']['warning']}\n\n"
            else:
                result += f"**⬇️ Official:** {'✅' if CMD_HELP_BOT[cmd]['info']['official'] else '❌'}\n\n"
        else:
            result += f"**⬇️ Official:** {'✅' if CMD_HELP_BOT[cmd]['info']['official'] else '❌'}\n"
            if not CMD_HELP_BOT[cmd]["info"]["warning"] == "":
                result += f"**⚠️ Warning:** {CMD_HELP_BOT[cmd]['info']['warning']}\n"
            result += f"**ℹ️ Info:** {CMD_HELP_BOT[cmd]['info']['info']}\n\n"

        command = CMD_HELP_BOT[cmd]["commands"][commands]
        if command["params"] is None:
            result += f"**❀ commands:** `{COMMAND_HAND_LER[:1]}{command['command']}`\n"
        else:
            result += f"**❀ commands:** `{COMMAND_HAND_LER[:1]}{command['command']} {command['params']}`\n"

        if command["example"] is None:
            result += f"**✞ Explanation:** `{command['usage']}`\n\n"
        else:
            result += f"**✞ Explanation:** `{command['usage']}`\n"
            result += f"**⌨ For Example:** `{COMMAND_HAND_LER[:1]}{command['example']}`\n\n"

        await event.edit(
            result,
            buttons=[
                custom.Button.inline("☜", data=f"Information[{page}]({cmd})")
            ],
            link_preview=False,
        )


# Idea from Hellbot


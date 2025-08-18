from telegram import Update, ChatMember, ChatPermissions
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from filter import filter
from spam import spam
import json
import time

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_type = update.message.chat.type
    if chat_type == "private":
        await update.message.reply_text(
            '👋 Welcome to Messages Filter Bot!\n'
            "I'm powered by GPT-5 and designed to intelligently detect and censor inappropriate messages based on the context of the conversation."
        )
        await update.message.reply_text('Add me to you group and grant admin rights to get started')
        await update.message.reply_text(
            "🔧 *Admin Commands:* \n\n"
            "/passivemode – Silently delete inappropriate messages\n"
            "/activemode – Delete inappropriate messages and notify the group\n"
            "/censormode – Delete inappropriate messages and post a censored version\n"
            "/messagerate <rate>  – Set how many messages a user can send per minute\n"
            "/muteduration <duration> – Set how long (in minutes) a user is muted for spamming",
            parse_mode="Markdown"
        )
        await update.message.reply_text("Send me a message to see how the censoring feature works!")

async def activemode(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_type = update.message.chat.type
    user = update.effective_user
    chat = update.effective_chat
    chat_id = str(chat.id)
    member = await context.bot.get_chat_member(chat.id, user.id)
    if chat_type == "private" or member.status not in ['administrator', 'creator']:
        return
    with open('groups/settings.json', 'r') as f:
        data = json.load(f)
    if chat_id not in data:
        data[f'{chat.id}']['message_rate'] = 15
        data[f'{chat.id}']['mute_duration'] = 60
        data[chat_id] = {}
    data[f'{chat.id}']['mode'] = 'active'
    with open('groups/settings.json', 'w') as f:
        json.dump(data,f,indent=4)
    await update.message.reply_text('Active mode is now enabled')

async def passivemode(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_type = update.message.chat.type
    user = update.effective_user
    chat = update.effective_chat
    chat_id = str(chat.id)
    member = await context.bot.get_chat_member(chat.id, user.id)
    if chat_type == "private" or member.status not in ['administrator', 'creator']:
        return
    with open('groups/settings.json', 'r') as f:
        data = json.load(f)
    if chat_id not in data:
        data[f'{chat.id}']['message_rate'] = 15
        data[f'{chat.id}']['mute_duration'] = 60
        data[chat_id] = {}
    data[f'{chat.id}']['mode'] = 'passive'
    with open('groups/settings.json', 'w') as f:
        json.dump(data,f,indent=4)
    await update.message.reply_text('Passive mode is now enabled')

async def censormode(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_type = update.message.chat.type
    user = update.effective_user
    chat = update.effective_chat
    chat_id = str(chat.id)
    member = await context.bot.get_chat_member(chat.id, user.id)
    if chat_type == "private" or member.status not in ['administrator', 'creator']:
        return
    with open('groups/settings.json', 'r') as f:
        data = json.load(f)
    if chat_id not in data:
        data[f'{chat.id}']['message_rate'] = 15
        data[f'{chat.id}']['mute_duration'] = 60
        data[chat_id] = {}
    data[f'{chat.id}']['mode'] = 'censor'
    with open('groups/settings.json', 'w') as f:
        json.dump(data,f,indent=4)
    await update.message.reply_text('Censor mode is now enabled')

async def messagerate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_type = update.message.chat.type
    user = update.effective_user
    chat = update.effective_chat
    chat_id = str(chat.id)
    member = await context.bot.get_chat_member(chat.id, user.id)
    if chat_type == "private" or member.status not in ['administrator', 'creator']:
        return
    if len(context.args) != 1:
        await update.message.reply_text('Use the format /messagerate [rate]')
        return
    with open('groups/settings.json', 'r') as f:
        data = json.load(f)
    if chat_id not in data:
        data[f'{chat.id}']['message_rate'] = 15
        data[f'{chat.id}']['mute_duration'] = 60
        data[chat_id] = {}
    data[f'{chat.id}']['message_rate'] = int(context.args[0])
    with open('groups/settings.json', 'w') as f:
        json.dump(data,f,indent=4)
    await update.message.reply_text(f"Message rate is now set to {data[str(chat.id)]['message_rate']} messages per minute")

async def muteduration(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_type = update.message.chat.type
    user = update.effective_user
    chat = update.effective_chat
    chat_id = str(chat.id)
    member = await context.bot.get_chat_member(chat.id, user.id)
    if chat_type == "private" or member.status not in ['administrator', 'creator']:
        return
    if len(context.args) != 1:
        await update.message.reply_text('Use the format /muteduration [duration]')
        return
    with open('groups/settings.json', 'r') as f:
        data = json.load(f)
    if chat_id not in data:
        data[f'{chat.id}']['message_rate'] = 15
        data[f'{chat.id}']['mute_duration'] = 60
        data[chat_id] = {}
    data[f'{chat.id}']['mute_duration'] = int(context.args[0]) * 60
    with open('groups/settings.json', 'w') as f:
        json.dump(data,f,indent=4)
    await update.message.reply_text(f'Mute duration is now set to {int(context.args[0])} minutes')

async def message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_type = update.message.chat.type
    if chat_type == "private":
        output = filter(3, update.message.text)
        await update.message.reply_text(output)
        return
    user = update.effective_user
    chat = update.effective_chat
    chat_id = str(chat.id)
    username = user.username
    bot_id = (await context.bot.get_me()).id
    bot_member = await context.bot.get_chat_member(chat_id, bot_id)
    if bot_member.status not in ["administrator", "creator"]:
        return
    with open('groups/settings.json', 'r') as f:
        data = json.load(f)
    if chat_id not in data:
        data[chat_id] = {}
        data[f'{chat.id}']['message_rate'] = 15
        data[f'{chat.id}']['mute_duration'] = 60
        data[f'{chat.id}']['mode'] = 'passive'
        with open('groups/settings.json', 'w') as f:
            json.dump(data,f,indent=4)
    with open('groups/settings.json', 'r') as f:
        data = json.load(f)
    type = data[f'{chat.id}']['mode']
    is_spam = spam(user.id,chat.id,data[f'{chat.id}']['message_rate'])
    member = await context.bot.get_chat_member(chat_id, user.id)
    if type == 'passive':
        if is_spam:
            if member.status == "restricted" and not getattr(member, "can_send_messages", True):
                return
            try:
                await context.bot.restrict_chat_member(chat_id=chat_id, user_id=user.id, permissions=ChatPermissions(can_send_messages=False), until_date=int(time.time())+data[f'{chat.id}']['mute_duration'])
            except:
                print(f"Failed to mute user: @{username}")
            return
        output = filter(1, update.message.text)
        if output == '1':
            await update.message.delete()
    elif type == 'active':
        if is_spam:
            if member.status == "restricted" and not getattr(member, "can_send_messages", True):
                return
            try:
                await context.bot.restrict_chat_member(chat_id=chat_id, user_id=user.id, permissions=ChatPermissions(can_send_messages=False), until_date=int(time.time())+data[f'{chat.id}']['mute_duration'])
                await context.bot.send_message(chat_id=chat_id, text=f"@{username} was muted.\nReason: Spam")
            except:
                await context.bot.send_message(chat_id=chat_id, text=f"Failed to mute user: @{username}")
            return
        output = filter(2, update.message.text)
        if output == '1':
            await update.message.delete()
            await context.bot.send_message(chat_id=chat_id, text=f"@{username}'s message was deleted.\nReason: Inappropriate language")
    else:
        if is_spam:
            if member.status == "restricted" and not getattr(member, "can_send_messages", True):
                return
            try:
                await context.bot.restrict_chat_member(chat_id=chat_id, user_id=user.id, permissions=ChatPermissions(can_send_messages=False), until_date=int(time.time())+data[f'{chat.id}']['mute_duration'])
                await context.bot.send_message(chat_id=chat_id, text=f"@{username} was muted.\nReason: Spam")
            except:
                await context.bot.send_message(chat_id=chat_id, text=f"Failed to mute user: @{username}")
            return
        output = filter(3, update.message.text)
        if output != update.message.text:
            await update.message.delete()
            await context.bot.send_message(chat_id=chat_id, text=f"@{username} sent:\n{output}")
    
if __name__ == '__main__':
    with open('config/config.json','r') as f:
        data = json.load(f)
    app = ApplicationBuilder().token(data["Telegram_Token"]).build()
    app.add_handler(CommandHandler("start",start))
    app.add_handler(CommandHandler("activemode",activemode))
    app.add_handler(CommandHandler("passivemode",passivemode))
    app.add_handler(CommandHandler("censormode",censormode))
    app.add_handler(CommandHandler("messagerate",messagerate))
    app.add_handler(CommandHandler("muteduration",muteduration))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message))
    app.run_polling()
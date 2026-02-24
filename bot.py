import os
import json
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = os.environ.get("TOKEN")
OWNER_ID = int(os.environ.get("OWNER_ID"))

def load_staff():
    with open("staff.json", "r", encoding="utf-8") as f:
        return json.load(f)

def save_staff(data):
    with open("staff.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def is_owner(update: Update):
    return update.effective_user.id == OWNER_ID

async def staff(update: Update, context: ContextTypes.DEFAULT_TYPE):
    s = load_staff()
    msg = (
        "👑 STAFF OFICIAL — MRX | HYPER V PE 🇵🇪\n\n"
        "👑 Fundador\n"
        f"└ @{s['fundador'][0]} » 𝗙𝘂𝗻𝗱𝗮𝗱𝗼𝗿\n\n"
        "⚜ Cofundadores\n"
    )

    for u in s["cofundadores"]:
        msg += f"├ @{u}\n"

    msg += "\n👮‍♂️ Administradores\n"
    for u in s["admins"]:
        msg += f"├ @{u} » 𝗔𝗱𝗺𝗶𝗻\n"

    msg += "\n✅ Certificados\n"
    for u in s["certificados"]:
        msg += f"└ @{u} » 𝗖𝗲𝗿𝘁𝗶𝗳𝗶𝗰𝗮𝗱𝗼\n"

    msg += (
        "\n────────────────────\n"
        "🔔 IMPORTANTE — COMPRA SEGURA\n"
        "⚠️ Los administradores DEV MRX o La CHAMA\n"
        "❌ NUNCA escriben por privado para vender.\n\n"
        "👉 https://t.me/Dev_MRX00"
    )

    await update.message.reply_text(msg)

async def add_role(update, context, role):
    if not is_owner(update):
        await update.message.reply_text("⛔ Sin permisos")
        return

    if not context.args:
        await update.message.reply_text("⚠️ Usa el comando con @usuario")
        return

    user = context.args[0].replace("@", "")
    data = load_staff()

    if user not in data[role]:
        data[role].append(user)
        save_staff(data)
        await update.message.reply_text(f"✅ @{user} agregado a {role}")
    else:
        await update.message.reply_text("ℹ️ Ya existe")

async def reload_cmd(update, context):
    if not is_owner(update):
        await update.message.reply_text("⛔ Sin permisos")
        return
    load_staff()
    await update.message.reply_text("🔄 Staff recargado correctamente")

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("staff", staff))
app.add_handler(CommandHandler("addadmin", lambda u,c: add_role(u,c,"admins")))
app.add_handler(CommandHandler("addcertificado", lambda u,c: add_role(u,c,"certificados")))
app.add_handler(CommandHandler("addcofundador", lambda u,c: add_role(u,c,"cofundadores")))
app.add_handler(CommandHandler("reload", reload_cmd))

app.run_polling()

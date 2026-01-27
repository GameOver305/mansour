import discord
from discord.ext import commands
from discord.ui import View, Button
import json, os

# ───────── إعداد الملفات ─────────
DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)

BADGE_FILE = os.path.join(DATA_DIR, "badges.json")
RANK_FILE = os.path.join(DATA_DIR, "ranks.json")

def load_json(path, default):
    if not os.path.exists(path):
        with open(path, "w", encoding="utf-8") as f:
            json.dump(default, f, ensure_ascii=False, indent=4)
        return default
    with open(path, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except:
            with open(path, "w", encoding="utf-8") as fw:
                json.dump(default, fw, ensure_ascii=False, indent=4)
            return default

def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def load_badges(): return load_json(BADGE_FILE, {"badges": {}})
def save_badges(data): save_json(BADGE_FILE, data)
def load_ranks(): return load_json(RANK_FILE, {"ranks": {}})
def save_ranks(data): save_json(RANK_FILE, data)

# ───────── الشارات ─────────
BADGE_OPTIONS = {
    "bomb_heart": "💣❤️ قنبلة حب",
    "bread": "🍞 خبزة أسطورية",
    "jelly_crown": "👑 جيلي ملكي",
    "judge": "⚖️ قاضي السيرفر",
    "fire_demon": "🔥 شيطان النار",
    "helm": "🛡️ خوذة أسطورية",
    "red_bomb": "💣 قنبلة حمراء",
    "pink_gem": "💎 جوهرة وردية",
    "fire_fox": "🦊 ثعلب النار",
    "purple_cube": "🧊 مكعب غامض",
    "goblet": "🍷 كأس أسطوري",
    "blue_bird": "🐦 طائر أزرق",
    "green_bird": "🐦 طائر أخضر",
    "meat": "🍖 قطعة لحم",
    "dark_cake": "🎂 كعكة مظلمة",
    "pumpkin": "🎃 يقطينة",
    "bee_honey": "🐝 خلية عسل",
    "red_gem": "💎 جوهرة حمراء",
    "green_pumpkin": "🎃 يقطينة خضراء",
    "toxic_cube": "🧪 مكعب سام",
    "gold_ghost": "🪙 شبح ذهبي",
    "fire_cube": "🔥 مكعب ناري",
    "red_bird": "🐦 طائر أحمر",
    "blue_bomb": "💣 قنبلة زرقاء",
    "magic_gift": "🎁 هدية سحرية",
    "electric_mug": "⚡ كوب كهربائي",
    "royal_beast": "👑 مخلوق ملكي",
}

# ───────── View الشارات (صفحات) ─────────
class BadgeSelectView(View):
    def __init__(self, page: int = 0):
        super().__init__(timeout=None)
        self.page = page

        badges = list(BADGE_OPTIONS.items())
        per_page = 20
        start = page * per_page
        end = start + per_page
        current = badges[start:end]

        for key, label in current:
            self.add_item(Button(label=label, style=discord.ButtonStyle.secondary, custom_id=f"badge_{key}"))

        if end < len(badges):
            self.add_item(Button(label="التالي ➡️", style=discord.ButtonStyle.primary, custom_id=f"next_{page}"))

        if page > 0:
            self.add_item(Button(label="⬅️ السابق", style=discord.ButtonStyle.primary, custom_id=f"prev_{page}"))

# ───────── لوحة الترحيب ─────────
class WelcomeButtons(View):
    def __init__(self):
        super().__init__(timeout=None)

        ranks = ["R5", "R4", "R3", "R2", "R1"]
        for r in ranks:
            self.add_item(Button(label=r, style=discord.ButtonStyle.primary, custom_id=f"rank_{r}"))

        self.add_item(Button(label="⭐ اختر شارتك", style=discord.ButtonStyle.success, custom_id="choose_badge"))

        self.add_item(Button(label="ℹ️ معلومات التحالف", style=discord.ButtonStyle.secondary, custom_id="info"))
        self.add_item(Button(label="📘 القوانين", style=discord.ButtonStyle.secondary, custom_id="rules"))
        self.add_item(Button(label="📝 تعليمات البداية", style=discord.ButtonStyle.secondary, custom_id="guide"))

# ───────── البوت ─────────
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    await bot.tree.sync()
    print("Bot is online")

# ───────── /dang ─────────
@bot.tree.command(name="dang")
async def dang(interaction: discord.Interaction):
    embed = discord.Embed(title="🎉 مرحبًا بك", description="اختر إعداداتك:", color=0x3498db)
    await interaction.response.send_message(embed=embed, view=WelcomeButtons())

# ───────── /profile ─────────
@bot.tree.command(name="profile")
async def profile(interaction: discord.Interaction):
    uid = str(interaction.user.id)
    badges = load_badges()
    ranks = load_ranks()

    badge = badges["badges"].get(uid, "لا توجد شارة")
    rank = ranks["ranks"].get(uid, "لا توجد رتبة")

    embed = discord.Embed(title=f"ملف {interaction.user.display_name}", color=0x2ecc71)
    embed.add_field(name="الرتبة", value=rank, inline=False)
    embed.add_field(name="الشارة", value=badge, inline=False)

    await interaction.response.send_message(embed=embed, ephemeral=True)

# ───────── تفاعل الأزرار ─────────
@bot.event
async def on_interaction(interaction: discord.Interaction):

    if interaction.type != discord.InteractionType.component:
        return

    cid = interaction.data["custom_id"]
    uid = str(interaction.user.id)

    # فتح قائمة الشارات (رسالة عادية)
    if cid == "choose_badge":
        await interaction.response.send_message("اختر شارتك:", view=BadgeSelectView(0))
        return

    # التالي
    if cid.startswith("next_"):
        page = int(cid.replace("next_", "")) + 1
        await interaction.response.edit_message(content="اختر شارتك:", view=BadgeSelectView(page))
        return

    # السابق
    if cid.startswith("prev_"):
        page = int(cid.replace("prev_", "")) - 1
        await interaction.response.edit_message(content="اختر شارتك:", view=BadgeSelectView(page))
        return

    # اختيار شارة
    if cid.startswith("badge_"):
        key = cid.replace("badge_", "")
        label = BADGE_OPTIONS.get(key, "شارة")

        badges = load_badges()
        badges["badges"][uid] = label
        save_badges(badges)

        await interaction.response.send_message(f"✔️ تم اختيار شارتك: {label}", ephemeral=True)
        return

    # اختيار رتبة
    if cid.startswith("rank_"):
        rank = cid.replace("rank_", "")
        ranks = load_ranks()
        ranks["ranks"][uid] = rank
        save_ranks(ranks)

        await interaction.response.send_message(f"✔️ تم تعيين رتبتك: {rank}", ephemeral=True)
        return

    # معلومات
    if cid == "info":
        await interaction.response.send_message("ℹ️ معلومات التحالف هنا", ephemeral=True)
        return

    if cid == "rules":
        await interaction.response.send_message("📘 القوانين هنا", ephemeral=True)
        return

    if cid == "guide":
        await interaction.response.send_message("📝 تعليمات البداية هنا", ephemeral=True)
        return

# ───────── تشغيل البوت ─────────
if __name__ == "__main__":
    TOKEN = os.getenv("MTQ2NTcyODgxOTE1NDUxODA0OQ.GyV9hK.74xSM6EIUTYkgdhT1YXMsgEm0S2gB6S6bFsj5Q")

    bot.run(TOKEN)

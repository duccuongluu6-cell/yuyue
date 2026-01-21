import streamlit as st
from datetime import datetime, date, timedelta

# 1. 页面配置
st.set_page_config(page_title="女生贴心助手", page_icon="🌸", layout="wide")

# 2. 核心知识库：四个时期的详细数据
PHASE_DICT = {
    "月经期": {
        "range": (1, 5),
        "icon": "🩸", "color": "#FFC0CB", "bg": "#FFF0F5",
        "change": "子宫内膜脱落，激素降至最低。你可能会感到痛经、腰酸、乏力，皮肤也变得干燥敏感。",
        "do": ["暖宝宝热敷小腹", "早睡早起，保证8小时睡眠", "淋浴，保持身体清洁"],
        "no": ["忌生冷冰凉（冷饮、冰淇淋）", "忌剧烈运动、游泳、盆浴", "忌洗头不吹干、受凉"],
        "eat": "🥣 建议：红糖姜茶、黑米粥、牛肉、红枣、暖性水果。"
    },
    "卵泡期": {
        "range": (6, 12),
        "icon": "🌱", "color": "#ADD8E6", "bg": "#F0F8FF",
        "change": "雌激素开始回升，卵泡发育。你会发现自己精力变充沛了，心情变好，皮肤也开始透亮。",
        "do": ["高效学习工作，这是你的黄金期", "尝试新技能或社交活动", "可以开始力量训练"],
        "no": ["忌过度熬夜（浪费了身体修复的最佳期）", "忌盲目节食"],
        "eat": "🥗 建议：鱼虾等优质蛋白、豆浆、新鲜蔬果。"
    },
    "排卵期": {
        "range": (13, 16),
        "icon": "🥚", "color": "#90EE90", "bg": "#F5FFF5",
        "change": "雌激素达到顶峰。身体分泌物增加，体温略微升高，心情最轻盈，自信心爆棚。",
        "do": ["保持身体干爽清洁", "多做户外运动、慢跑", "适合拍照、约会"],
        "no": ["忌吃太甜（此时激素波动容易长排卵痘）", "忌久坐不动"],
        "eat": "💧 建议：多喝水、全谷物、高纤维食物。"
    },
    "黄体期": {
        "range": (17, 28),
        "icon": "🍂", "color": "#FFFACD", "bg": "#FFFFF0",
        "change": "孕激素占主导。你可能会感到胸部胀痛、身体浮肿，容易焦虑、易怒或无故想哭。",
        "do": ["睡前热水泡脚", "做冥想或听舒缓音乐放松", "适当减少社交，多独处"],
        "no": ["忌吃太咸（会加重浮肿）", "忌喝咖啡（会加重焦虑）", "忌做重大决策"],
        "eat": "🍌 建议：香蕉（补镁）、全麦面包、坚果、黑巧克力。"
    }
}

# 3. 首页问候与核心交互
st.title("🌸 专属生理期智能顾问")
st.write("---")

# 交互中心：提问
st.subheader("👋 亲爱的，先告诉我你的进度：")
col_q1, col_q2 = st.columns([1, 1])

with col_q1:
    day_input = st.number_input("今天是月经来的第几天？", min_value=1, max_value=35, value=1, step=1)

# 4. 核心逻辑：根据天数判定时期
def get_current_phase(day):
    if 1 <= day <= 5: return "月经期"
    elif 6 <= day <= 12: return "卵泡期"
    elif 13 <= day <= 16: return "排卵期"
    else: return "黄体期"

current_phase = get_current_phase(day_input)
data = PHASE_DICT[current_phase]

# 5. 结果显示：一眼看穿当前状态
st.write("")
st.markdown(f"""
<div style="background-color: {data['bg']}; padding: 30px; border-radius: 20px; border-left: 15px solid {data['color']};">
    <h1 style="margin:0; color: #333;">{data['icon']} 当前处于：{current_phase}</h1>
    <h3 style="color: #666; margin-top: 5px;">第 {day_input} 天</h3>
    <hr style="border: 0.5px solid {data['color']}55;">
    <p style="font-size: 1.2em; color: #333;"><b>🧬 身体变化：</b>{data['change']}</p>
</div>
""", unsafe_allow_html=True)

# 6. 宜忌卡片
st.write("")
c1, c2, c3 = st.columns(3)

with c1:
    st.success("✅ **你应该做**")
    for item in data['do']:
        st.write(f"· {item}")

with c2:
    st.error("❌ **你要忌讳**")
    for item in data['no']:
        st.write(f"· {item}")

with c3:
    st.warning("🍱 **饮食贴士**")
    st.write(data['eat'])

# 7. 全周期概览（小图示）
st.write("---")
st.caption("📍 全周期概览：月经期(1-5天) | 卵泡期(6-12天) | 排卵期(13-16天) | 黄体期(17-28天)")

# 8. 紧急关怀按钮
if st.button("🚨 我现在很不舒服"):
    st.toast("摸摸头，请尝试热敷或休息，严重请务必就医。")
    st.info("建议：月经期请注意保暖，黄体期请尽量放松心态。")

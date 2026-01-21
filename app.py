import streamlit as st
from datetime import datetime, date
import matplotlib.pyplot as plt
import numpy as np
from logic import get_period_phase

# 设置页面配置
st.set_page_config(page_title="女生贴心助手", page_icon="🌙", layout="wide")

# 1. 建议数据库与配置
ADVICE_DATA = {
    "月经期": {
        "eat_yes": "🩸 补血温热：红糖姜茶、黑豆、菠菜、桂圆。",
        "eat_no": "🧊 严禁生冷：冰淇淋、冷饮、螃蟹、绿茶。",
        "do": "🛌 多休息，可以用暖宝宝热敷，避免剧烈运动和受凉。",
        "status": "当前处于身体排毒期，请务必保暖。",
        "color": "#FFC0CB",
        "icon": "🩸"
    },
    "卵泡期": {
        "eat_yes": "🥗 优质蛋白：豆制品、鱼类、大量新鲜蔬果。",
        "eat_no": "🍔 正常饮食，避免过量油腻。",
        "do": "💪 状态最好！适合健身、学习，效率极高。",
        "status": "荷尔蒙分泌增加，皮肤状态和心情都会变好哦！",
        "color": "#ADD8E6",
        "icon": "🌱"
    },
    "排卵期": {
        "eat_yes": "💧 多喝水：多吃谷物和含纤维素高的食物。",
        "eat_no": "🍩 控糖：此时容易长痘，少吃甜食。",
        "do": "🚶‍♀️ 保持运动，注意个人清洁。",
        "status": "此时精力旺盛，是身体最轻盈的时候。",
        "color": "#90EE90",
        "icon": "🥚"
    },
    "黄体期": {
        "eat_yes": "🍌 缓解焦虑：香蕉（含镁）、全麦面包、坚果。",
        "eat_no": "🧂 控盐：防止经前水肿；少喝咖啡防止焦虑。",
        "do": "🧘 适合冥想、听轻音乐，保证充足睡眠。",
        "status": "可能会有经前综合征（PMS），心情烦躁是正常的，抱抱你。",
        "color": "#FFFACD",
        "icon": "🍂"
    }
}

st.title("🌙 您的生理期贴心指南")

# 2. 侧边栏设置
with st.sidebar:
    st.header("⚙️ 个人设置")
    # 默认日期设置为今天
    last_date = st.date_input("上次月经开始日期", date.today())
    avg_c = st.number_input("平均周期天数", value=28, min_value=20, max_value=45)
    st.info("数据仅存于浏览器，保护隐私。")

# 3. 计算逻辑
phase, day_num = get_period_phase(last_date, avg_c)

# 4. 核心指标展示
col_m1, col_m2 = st.columns(2)
with col_m1:
    st.metric("当前阶段", f"{ADVICE_DATA[phase]['icon']} {phase}")
with col_m2:
    st.metric("周期天数", f"第 {day_num} 天")

# --- 5. 一眼看状态 (大卡片) ---
# 使用 HTML 增加背景颜色和边框，强化视觉
st.markdown(f"""
<div style="background-color: {ADVICE_DATA[phase]['color']}44; padding: 20px; border-radius: 10px; border-left: 10px solid {ADVICE_DATA[phase]['color']}; margin-bottom: 25px;">
    <h3 style="margin:0; color: #333;">📍 身体信号：</h3>
    <p style="font-size: 1.2em; color: #444; margin-top: 10px;">{ADVICE_DATA[phase]['status']}</p>
</div>
""", unsafe_allow_html=True)

# 6. 建议板块
c1, c2, c3 = st.columns(3)
with c1:
    st.success("✅ **建议吃**")
    st.write(ADVICE_DATA[phase]['eat_yes'])
with c2:
    st.error("❌ **忌口**")
    st.write(ADVICE_DATA[phase]['eat_no'])
with c3:
    st.warning("🧘 **该做什么**")
    st.write(ADVICE_DATA[phase]['do'])

# --- 7. 视觉强化进度图 ---
st.divider()
st.subheader("🗓️ 周期阶段进度")

fig, ax = plt.subplots(figsize=(10, 2))
boundaries = [0, 5, 12, 16, avg_c]
names = ["月经期", "卵泡期", "排卵期", "黄体期"]

for i in range(len(names)):
    # 逻辑：只有当前阶段是高亮的，其他阶段变淡
    is_current = (phase == names[i])
    alpha_val = 0.9 if is_current else 0.15
    
    # 绘制色块
    ax.barh(0, boundaries[i+1]-boundaries[i], left=boundaries[i], 
            color=ADVICE_DATA[names[i]]['color'], alpha=alpha_val, edgecolor='white', linewidth=1)
    
    # 标注图标（避免文字乱码）
    icon_text = ADVICE_DATA[names[i]]['icon']
    ax.text(boundaries[i] + (boundaries[i+1]-boundaries[i])/2, 0, icon_text, 
            va='center', ha='center', fontsize=16)

# 标记“今天”的位置
ax.plot(day_num, 0, marker='o', markersize=12, color='red', markeredgecolor='white')
ax.annotate("YOU", xy=(day_num, 0.2), xytext=(day_num, 0.8),
            arrowprops=dict(facecolor='black', shrink=0.05, width=1, headwidth=5),
            ha='center', fontweight='bold', color='red')

ax.set_xlim(0, avg_c)
ax.set_ylim(-1, 1)
ax.axis('off') # 隐藏坐标轴
st.pyplot(fig)

# 8. 紧急对策
st.divider()
if st.toggle("🚨 我现在很不舒服 (痛经)"):
    st.error("### 🚑 紧急缓解方案：\n1. 喝热水/姜汤 \n2. 腹部热敷 \n3. 婴儿式侧卧 \n4. 必要时咨询医生使用药物")

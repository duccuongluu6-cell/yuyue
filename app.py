import streamlit as st
from datetime import datetime, date
import matplotlib.pyplot as plt
import numpy as np
from logic import get_period_phase

# 设置页面配置
st.set_page_config(page_title="女生贴心助手", page_icon="🌙", layout="wide")

# 1. 建议数据库
ADVICE_DATA = {
    "月经期": {
        "eat_yes": "🩸 补血温热：红糖姜茶、黑豆、菠菜、桂圆。",
        "eat_no": "🧊 严禁生冷：冰淇淋、冷饮、螃蟹、绿茶。",
        "do": "🛌 多休息，可以用暖宝宝热敷，避免剧烈运动和受凉。",
        "status": "当前处于身体排毒期，请务必保暖。",
        "color": "#FFC0CB" 
    },
    "卵泡期": {
        "eat_yes": "🥗 优质蛋白：豆制品、鱼类、大量新鲜蔬果。",
        "eat_no": "🍔 正常饮食，避免过量油腻。",
        "do": "💪 状态最好！适合健身、学习，效率极高。",
        "status": "荷尔蒙分泌增加，皮肤状态和心情都会变好哦！",
        "color": "#ADD8E6"
    },
    "排卵期": {
        "eat_yes": "💧 多喝水：多吃谷物和含纤维素高的食物。",
        "eat_no": "🍩 控糖：此时容易长痘，少吃甜食。",
        "do": "🚶‍♀️ 保持运动，注意个人清洁。",
        "status": "此时精力旺盛，是身体最轻盈的时候。",
        "color": "#90EE90"
    },
    "黄体期": {
        "eat_yes": "🍌 缓解焦虑：香蕉（含镁）、全麦面包、坚果。",
        "eat_no": "🧂 控盐：防止水肿；少喝咖啡防止焦虑。",
        "do": "🧘 适合冥想、听轻音乐，保证充足睡眠。",
        "status": "可能会有经前综合征（PMS），心情烦躁是正常的，抱抱你。",
        "color": "#FFFACD"
    }
}

st.title("🌙 您的生理期贴心指南")

# 2. 侧边栏设置
with st.sidebar:
    st.header("⚙️ 个人设置")
    last_date = st.date_input("上次月经开始日期", date.today())
    avg_c = st.number_input("平均周期天数", value=28, min_value=20, max_value=45)
    st.info("数据仅存于本地浏览器缓存，不会上传服务器。")

# 3. 计算逻辑
phase, day_num = get_period_phase(last_date, avg_c)

# 4. 核心指标展示
col_m1, col_m2 = st.columns(2)
col_m1.metric("当前阶段", phase)
col_m2.metric("周期天数", f"第 {day_num} 天")

st.info(f"💡 **状态提醒：** {ADVICE_DATA[phase]['status']}")

# 5. 建议板块
st.divider()
c1, c2, c3 = st.columns(3)
with c1:
    st.success("✅ **建议吃**")
    st.write(ADVICE_DATA[phase]['eat_yes'])
with c2:
    st.error("❌ **忌口**")
    st.write(ADVICE_DATA[phase]['eat_no'])
with c3:
    st.warning("🧘 **应该做**")
    st.write(ADVICE_DATA[phase]['do'])

# 6. 图表展示
st.divider()
st.subheader("🗓️ 周期进度视觉化")

fig, ax = plt.subplots(figsize=(10, 2))
# 绘制背景条
boundaries = [0, 5, 12, 16, avg_c]
colors = [ADVICE_DATA["月经期"]["color"], ADVICE_DATA["卵泡期"]["color"], 
          ADVICE_DATA["排卵期"]["color"], ADVICE_DATA["黄体期"]["color"]]
names = ["月经期", "卵泡期", "排卵期", "黄体期"]

for i in range(len(colors)):
    ax.barh(0, boundaries[i+1]-boundaries[i], left=boundaries[i], color=colors[i], alpha=0.6)
    ax.text(boundaries[i] + (boundaries[i+1]-boundaries[i])/2, 0, names[i], va='center', ha='center', fontsize=9)

# 标记当前位置
ax.plot(day_num, 0, marker='v', markersize=15, color='red')
ax.text(day_num, 0.6, "今天", color='red', ha='center', fontweight='bold')

ax.set_xlim(0, avg_c)
ax.set_ylim(-1, 1)
ax.axis('off') # 隐藏坐标轴让界面更干净
st.pyplot(fig)

# 7. 紧急对策
st.divider()
if st.toggle("🚨 我现在很不舒服 (痛经)"):
    st.error("### 🚑 紧急缓解方案：\n1. 喝热水/姜汤 \n2. 腹部热敷 \n3. 婴儿式侧卧 \n4. 必要时咨询医生使用药物")
import streamlit as st
from datetime import datetime, date, timedelta
import matplotlib.pyplot as plt
from logic import get_period_phase

# 1. 页面配置与视觉样式
st.set_page_config(page_title="女生贴心助手", page_icon="🌙", layout="wide")

PHASE_INFO = {
    "月经期": {"icon": "🩸", "color": "#FFC0CB", "bg": "#FFF0F5", "tips": "身体排毒中，请务必保暖。"},
    "卵泡期": {"icon": "🌱", "color": "#ADD8E6", "bg": "#F0F8FF", "tips": "荷尔蒙回升，状态越来越好！"},
    "排卵期": {"icon": "🥚", "color": "#90EE90", "bg": "#F5FFF5", "tips": "精力最旺盛，心情最轻盈。"},
    "黄体期": {"icon": "🍂", "color": "#FFFACD", "bg": "#FFFFF0", "tips": "可能情绪波动，记得抱抱自己。"}
}

st.title("🌙 专属生理期智能助手")

# 2. 侧边栏：基础数据记录
with st.sidebar:
    st.header("⚙️ 个人历史档案")
    history_date = st.date_input("记录：上次月经开始日", date.today() - timedelta(days=28))
    avg_cycle = st.number_input("平均周期长度 (天)", value=28)
    st.divider()
    st.caption("数据仅保存在您的本地设备")

# 3. 核心交互区：智能状态确认
st.subheader("👋 亲爱的，今天感觉怎么样？")

# 创建交互按钮
col_btn1, col_btn2 = st.columns([1, 1])
with col_btn1:
    is_period_now = st.toggle("🩸 我现在正处于经期", value=False)

# 智能天数推算逻辑
if is_period_now:
    phase = "月经期"
    with col_btn2:
        # 增加智能询问：来了几天了？
        days_already = st.select_slider("已经来了几天了？", options=range(1, 8), value=1)
    day_num = days_already
    
    # 动态问候语
    if day_num == 1:
        greeting = "今天是第一天，记得准备好暖宝宝，不要碰凉水哦。"
    elif day_num <= 3:
        greeting = f"已经是第 {day_num} 天了，最难受的时候快过去啦，加油！"
    else:
        greeting = f"第 {day_num} 天，身体正在慢慢恢复活力呢。"
else:
    # 自动推算逻辑
    phase, day_num = get_period_phase(history_date, avg_cycle)
    greeting = f"根据记录推算，你现在正处于{phase}。"

# 4. 智能状态大卡片
st.markdown(f"""
<div style="background-color: {PHASE_INFO[phase]['bg']}; padding: 25px; border-radius: 15px; border-left: 10px solid {PHASE_INFO[phase]['color']};">
    <h1 style="margin:0; color: #333;">{PHASE_INFO[phase]['icon']} {phase} <span style="font-size: 0.5em; color: #666;">第 {day_num} 天</span></h1>
    <p style="font-size: 1.3em; color: #d63384; margin-top: 10px; font-weight: bold;">{greeting}</p>
    <p style="font-size: 1.1em; color: #555;">💡 温馨提示：{PHASE_INFO[phase]['tips']}</p>
</div>
""", unsafe_allow_html=True)

# 5. 饮食与生活建议
st.write("")
st.subheader("🍱 今日生活指南")
c1, c2, c3 = st.columns(3)

# 这里的建议会随 phase 自动变化（复用你之前的 ADVICE_DETAIL 逻辑）
ADVICE_DETAIL = {
    "月经期": {"yes": "红糖姜茶、桂圆、菠菜", "no": "冰淇淋、冷饮、浓茶", "do": "小腹热敷、充足睡眠"},
    "卵泡期": {"yes": "豆制品、鱼类、新鲜蔬果", "no": "避免过度节食", "do": "高效工作、尝试新运动"},
    "排卵期": {"yes": "多喝水、全谷物", "no": "高糖甜食、油炸食品", "do": "注意皮肤清洁、规律作息"},
    "黄体期": {"yes": "香蕉、坚果、燕麦", "no": "高盐食物、酒精", "do": "冥想放松、睡前足浴"}
}

with c1:
    st.success(f"✅ **推荐：** {ADVICE_DETAIL[phase]['yes']}")
with c2:
    st.error(f"❌ **忌口：** {ADVICE_DETAIL[phase]['no']}")
with c3:
    st.warning(f"🧘 **行动：** {ADVICE_DETAIL[phase]['do']}")

# 6. 视觉化进度（带当前阶段高亮）
st.divider()
st.subheader("📊 周期进度图")

fig, ax = plt.subplots(figsize=(10, 1.2))
boundaries = [0, 5, 12, 16, avg_cycle]
p_names = ["月经期", "卵泡期", "排卵期", "黄体期"]

for i in range(len(p_names)):
    active = (phase == p_names[i])
    ax.barh(0, boundaries[i+1]-boundaries[i], left=boundaries[i], 
            color=PHASE_INFO[p_names[i]]['color'], 
            alpha=0.9 if active else 0.1, 
            edgecolor='white', linewidth=2)
    ax.text(boundaries[i] + (boundaries[i+1]-boundaries[i])/2, 0, 
            PHASE_INFO[p_names[i]]['icon'], va='center', ha='center', fontsize=18)

# 标记用户具体位置
ax.plot(day_num, 0, marker='o', markersize=15, color='#d63384', markeredgecolor='white')
ax.axis('off')
st.pyplot(fig)

# 7. 智能贴心小工具
if st.button("🩸 经血量异常/不舒服？"):
    with st.expander("点击查看对策"):
        st.write("- **量多、有大血块：** 可能是受凉或劳累，多喝温水休息，若持续请咨询医生。")
        st.write("- **痛经严重：** 试试婴儿式卧位，或者用暖宝宝。")

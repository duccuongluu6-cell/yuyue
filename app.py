import streamlit as st
from datetime import datetime, date, timedelta
import matplotlib.pyplot as plt
from logic import get_period_phase

# 页面配置
st.set_page_config(page_title="女生贴心助手", page_icon="🌙", layout="wide")

# 1. 完善的阶段配置
PHASE_INFO = {
    "月经期": {"icon": "🩸", "color": "#FFC0CB", "bg": "#FFF0F5", "status": "身体排毒中，请务必保暖。"},
    "卵泡期": {"icon": "🌱", "color": "#ADD8E6", "bg": "#F0F8FF", "status": "荷尔蒙回升，皮肤和心情都在变好！"},
    "排卵期": {"icon": "🥚", "color": "#90EE90", "bg": "#F5FFF5", "status": "精力最旺盛，身体最轻盈的时候。"},
    "黄体期": {"icon": "🍂", "color": "#FFFACD", "bg": "#FFFFF0", "status": "可能伴随经前不适，记得抱抱自己。"}
}

ADVICE_DETAIL = {
    "月经期": {"eat_yes": "红糖姜茶、黑豆、补铁食物", "eat_no": "冷饮、生冷海鲜、浓茶", "do": "热敷小腹、早睡、避免洗头受凉"},
    "卵泡期": {"eat_yes": "鱼虾蛋白、新鲜蔬果", "eat_no": "无特殊忌口，均衡为主", "do": "适合高强度健身、高效工作"},
    "排卵期": {"eat_yes": "多喝水、高纤维食物", "eat_no": "甜食、高油高糖", "do": "户外活动、注意皮肤清洁"},
    "黄体期": {"eat_yes": "香蕉(补镁)、全麦面包", "eat_no": "高盐食物(防浮肿)、咖啡", "do": "冥想、听轻音乐、保证睡眠"}
}

st.title("🌙 生理期智慧指南")

# 2. 侧边栏：基础数据
with st.sidebar:
    st.header("⚙️ 基础设置")
    history_date = st.date_input("记录：上次月经开始日", date.today() - timedelta(days=14))
    avg_cycle = st.number_input("周期长度 (天)", value=28)
    st.divider()
    st.caption("数据仅保存在您的浏览器中")

# 3. 核心交互区：用户主动指明状态
st.subheader("📢 实时状态确认")
col_btn1, col_btn2 = st.columns([1, 2])

# 用户手动点击按钮
is_period_now = col_btn1.toggle("🩸 我现在正处于经期", value=False)

if is_period_now:
    # 如果用户点选“是”，强制锁定为月经期
    phase = "月经期"
    day_num = 1
    st.toast("已切换至经期模式，请注意休息！")
else:
    # 否则按逻辑推算
    phase, day_num = get_period_phase(history_date, avg_cycle)

# 4. 视觉卡片：一眼看状态
st.markdown(f"""
<div style="background-color: {PHASE_INFO[phase]['bg']}; padding: 25px; border-radius: 15px; border-left: 10px solid {PHASE_INFO[phase]['color']};">
    <h1 style="margin:0; color: #333;">{PHASE_INFO[phase]['icon']} {phase} <span style="font-size: 0.6em; color: #666;">· 第 {day_num} 天</span></h1>
    <p style="font-size: 1.3em; color: #444; margin-top: 10px;"><b>身体信号：</b>{PHASE_INFO[phase]['status']}</p>
</div>
""", unsafe_allow_html=True)

# 5. 建议板块
st.write("")
c1, c2, c3 = st.columns(3)
with c1:
    st.success(f"✅ **建议吃**\n\n{ADVICE_DETAIL[phase]['eat_yes']}")
with c2:
    st.error(f"❌ **忌口**\n\n{ADVICE_DETAIL[phase]['eat_no']}")
with c3:
    st.warning(f"🧘 **应该做**\n\n{ADVICE_DETAIL[phase]['do']}")

# 6. 视觉化进度条（高亮当前）
st.divider()
st.subheader("🗓️ 周期进度视觉化")

fig, ax = plt.subplots(figsize=(10, 1.5))
boundaries = [0, 5, 12, 16, avg_cycle]
p_names = ["月经期", "卵泡期", "排卵期", "黄体期"]

for i in range(len(p_names)):
    # 聚光灯效果：只有当前阶段是彩色的
    is_active = (phase == p_names[i])
    ax.barh(0, boundaries[i+1]-boundaries[i], left=boundaries[i], 
            color=PHASE_INFO[p_names[i]]['color'], 
            alpha=0.9 if is_active else 0.1, 
            edgecolor='white', linewidth=2)
    # 用图标代表阶段
    ax.text(boundaries[i] + (boundaries[i+1]-boundaries[i])/2, 0, 
            PHASE_INFO[p_names[i]]['icon'], va='center', ha='center', fontsize=18)

# 标注用户位置
ax.plot(day_num, 0, marker='o', markersize=15, color='red', markeredgecolor='white')
ax.set_xlim(0, avg_cycle)
ax.axis('off')
st.pyplot(fig)

# 7. 痛经紧急求助
if st.button("🚨 我现在很痛，该怎么办？"):
    st.error("### 🚑 痛经紧急对策：\n1. 喝热姜茶 / 敷暖宝宝 \n2. 婴儿式侧卧放松腹部 \n3. 严重时请咨询医生并按医嘱使用止痛药")

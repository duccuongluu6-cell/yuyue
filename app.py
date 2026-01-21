import streamlit as st
from datetime import datetime, date, timedelta
import matplotlib.pyplot as plt
from logic import get_period_phase

# 1. 页面配置
st.set_page_config(page_title="女生生理期顾问", page_icon="🌸", layout="wide")

# 2. 时期核心数据库
PHASE_DATA = {
    "月经期": {
        "range": "第1-5天",
        "icon": "🩸", "color": "#FFC0CB", "bg": "#FFF0F5",
        "intro": "内膜脱落期，身体免疫力最低，容易疲劳和畏寒。",
        "do": "✅ 睡足8小时、小腹热敷、淋浴、轻柔拉伸",
        "no": "❌ 剧烈运动、盆浴、洗头受凉、过度劳累",
        "eat_yes": "🥣 红糖姜茶、黑豆汤、牛肉、暖性水果",
        "eat_no": "🧊 冰淇淋、冷饮、生鱼片、浓茶、螃蟹"
    },
    "卵泡期": {
        "range": "第6-12天",
        "icon": "🌱", "color": "#ADD8E6", "bg": "#F0F8FF",
        "intro": "卵泡发育期，雌激素回升，是身体状态最好的“黄金期”。",
        "do": "✅ 高效工作、尝试新技能、加强力量训练",
        "no": "❌ 熬夜（浪费了修复皮肤的好时机）",
        "eat_yes": "🥗 鱼虾蛋白、豆制品、五谷杂粮",
        "eat_no": "🍔 尽量少吃高油腻食物"
    },
    "排卵期": {
        "range": "第13-16天",
        "icon": "🥚", "color": "#90EE90", "bg": "#F5FFF5",
        "intro": "排卵期，精力最旺盛，代谢最快，但也容易心情波动。",
        "do": "✅ 户外运动、保持私处干爽、记录白带变化",
        "no": "❌ 忽略避孕（若无备孕计划）、久坐不动",
        "eat_yes": "💧 多喝水、多吃蔬菜、高纤维食物",
        "eat_no": "🍩 控糖！此时容易长痘"
    },
    "黄体期": {
        "range": "第17-28天",
        "icon": "🍂", "color": "#FFFACD", "bg": "#FFFFF0",
        "intro": "经前准备期，孕激素升高，容易出现浮肿和情绪波动。",
        "do": "✅ 早睡、睡前足浴、冥想放松心情",
        "no": "❌ 剧烈运动、做重大决策（情绪易不稳定）",
        "eat_yes": "🍌 香蕉、坚果、全麦面包、黑巧克力",
        "eat_no": "🧂 控盐防止浮肿、咖啡因防止焦虑"
    }
}

st.title("🌸 女生生理期智能顾问")

# 3. 核心交互：用户输入
with st.sidebar:
    st.header("⚙️ 基础设定")
    avg_cycle = st.number_input("平均周期天数", value=28)
    st.divider()
    st.caption("建议将此页面添加到手机主屏幕使用")

# --- 交互核心：来了几天 ---
st.subheader("👋 亲爱的，今天进度如何？")
is_period = st.toggle("🩸 我现在正处于经期", value=True)

if is_period:
    # 如果处于经期，用户直接选天数
    day_num = st.select_slider("月经已经来了几天了？", options=range(1, 8), value=1)
    phase = "月经期"
else:
    # 如果没在经期，让用户输入上次来的日期进行智能推算
    last_date = st.date_input("上次月经开始的日期", date.today() - timedelta(days=15))
    phase, day_num = get_period_phase(last_date, avg_cycle)

# 4. 时期指示灯（一眼看到所有时期）
st.write("### 📍 周期位置定位")
cols = st.columns(4)
p_list = ["月经期", "卵泡期", "排卵期", "黄体期"]

for i, p_name in enumerate(p_list):
    with cols[i]:
        is_active = (phase == p_name)
        # 高亮逻辑：当前阶段用深色边框和实色，其他阶段灰色
        box_style = f"""
            background-color: {PHASE_DATA[p_name]['bg']};
            padding: 15px;
            border-radius: 10px;
            border: { '3px solid ' + PHASE_DATA[p_name]['color'] if is_active else '1px solid #ddd'};
            opacity: { '1.0' if is_active else '0.4'};
            text-align: center;
        """
        st.markdown(f"""
            <div style="{box_style}">
                <h2 style="margin:0;">{PHASE_DATA[p_name]['icon']}</h2>
                <b style="color:#333;">{p_name}</b><br>
                <small style="color:#666;">{PHASE_DATA[p_name]['range']}</small>
            </div>
        """, unsafe_allow_html=True)
        if is_active:
            st.markdown("<p style='text-align:center; color:red;'>▲ 您在这里</p>", unsafe_allow_html=True)

# 5. 详细攻略展示
st.divider()
st.subheader(f"📖 {phase} · 详细指南 (第 {day_num} 天)")

# 核心看板
st.info(f"**时期特征：** {PHASE_DATA[phase]['intro']}")

c1, c2 = st.columns(2)
with c1:
    st.success("🍱 **饮食建议**")
    st.write(f"**推荐吃：** {PHASE_DATA[phase]['eat_yes']}")
    st.write(f"**忌讳吃：** {PHASE_DATA[phase]['eat_no']}")

with c2:
    st.warning("🧘 **生活宜忌**")
    st.write(f"**应该做：** {PHASE_DATA[phase]['do']}")
    st.write(f"**忌讳做：** {PHASE_DATA[phase]['no']}")

# 6. 动态温馨语
st.markdown(f"""
<div style="background-color: {PHASE_DATA[phase]['color']}22; padding: 20px; border-radius: 10px; border-top: 5px solid {PHASE_DATA[phase]['color']};">
    <p style="font-size: 1.1em; color: #555; font-style: italic;">
        “ 亲爱的，目前是{phase}的第 {day_num} 天，身体正在进行自然的循环。{'请多爱自己一点。' if phase == '月经期' else '现在是状态最好的时候，去发光吧！'} ”
    </p>
</div>
""", unsafe_allow_html=True)

import streamlit as st
from datetime import datetime, date, timedelta
import matplotlib.pyplot as plt
from logic import get_period_phase

# 1. 页面配置与主题风格
st.set_page_config(page_title="女生贴心助手", page_icon="🌙", layout="wide")

# 2. 超详细的周期知识库
PHASE_CONFIG = {
    "月经期": {
        "icon": "🩸", "color": "#FFC0CB", "bg": "#FFF0F5",
        "intro": "子宫内膜脱落，激素处于低水平。身体最虚弱，免疫力较低。",
        "status": "痛经、腰酸、乏力、畏寒、皮肤敏感。",
        "eat": ["✅ 红糖姜茶、黑豆、牛肉、暖性水果（苹果、桂圆）", "❌ 冰激凌、冷饮、生鱼片、浓茶、浓咖啡"],
        "do": ["🧘 轻柔拉伸、冥想、充足睡眠", "🚿 淋浴而非盆浴、避免剧烈运动"],
        "skin": "肤色暗沉，油脂分泌减少，重点在于**补水保湿和防晒**。"
    },
    "卵泡期": {
        "icon": "🌱", "color": "#ADD8E6", "bg": "#F0F8FF",
        "intro": "雌激素开始回升，卵泡逐渐发育。身体代谢加快，精力最旺盛。",
        "status": "心情愉悦、自信心增强、身体轻盈、皮肤透亮。",
        "eat": ["✅ 优质蛋白（鱼、蛋）、豆制品、大量新鲜蔬菜", "❌ 无特殊禁忌，但应避免暴饮暴食"],
        "do": ["💪 力量训练、有氧运动、高效学习/工作", "🌟 尝试挑战新事物、社交、拍照"],
        "skin": "皮肤屏障最强，状态最佳。适合**高功能性护肤**或尝试新产品。"
    },
    "排卵期": {
        "icon": "🥚", "color": "#90EE90", "bg": "#F5FFF5",
        "intro": "雌激素达到顶峰。身体分泌物增加，处于易孕期。",
        "status": "精力极佳、体温略微升高、性欲增强。",
        "eat": ["✅ 保持水分（多喝水）、高纤维食物（全谷物）", "❌ 控糖：此时激素波动可能导致长痘，少吃甜品"],
        "do": ["🚶‍♀️ 户外运动、瑜伽、保持身体清洁", "💓 重点关注身体微小变化"],
        "skin": "油脂分泌开始增加，注意**清洁和控油**，预防排卵痘。"
    },
    "黄体期": {
        "icon": "🍂", "color": "#FFFACD", "bg": "#FFFFF0",
        "intro": "孕激素占主导地位。若未受孕，激素水平将骤降，引发PMS。",
        "status": "经前综合征（乳房胀痛、浮肿、焦虑、易怒）、食欲大增。",
        "eat": ["✅ 补镁食物（香蕉、黑巧克力、核桃）、复合碳水", "❌ 控盐：防止水肿；少喝咖啡：防止情绪焦虑"],
        "do": ["🛁 泡脚缓解压力、早睡、做简单的家务分散注意力", "🫂 接受自己的负面情绪，避免做重大决策"],
        "skin": "皮脂腺极其活跃。加强**深层清洁**，防止毛孔堵塞，停用高浓度酸类。"
    }
}

st.title("🌙 女生生理期全维度智能顾问")

# 3. 侧边栏：基础数据
with st.sidebar:
    st.header("⚙️ 个人历史档案")
    history_date = st.date_input("记录：上次月经开始日", date.today() - timedelta(days=28))
    avg_cycle = st.number_input("平均周期长度 (天)", value=28)
    st.divider()
    st.caption("隐私说明：所有数据仅保留在您的浏览器中。")

# 4. 核心交互区
st.subheader("👋 实时状态同步")
col_btn, col_slider = st.columns([1, 1.5])

with col_btn:
    is_period_now = st.toggle("🩸 我现在正处于经期", value=False)

if is_period_now:
    phase = "月经期"
    with col_slider:
        day_num = st.select_slider("已经来了几天了？", options=range(1, 8), value=1)
    greeting = f"今天是经期第 {day_num} 天，照顾好自己，哪怕只是多休息一分钟。"
else:
    phase, day_num = get_period_phase(history_date, avg_cycle)
    greeting = f"当前处于 {phase} 第 {day_num} 天，身体正在有条不紊地运行。"

# 5. 沉浸式状态大卡片
cfg = PHASE_CONFIG[phase]
st.markdown(f"""
<div style="background-color: {cfg['bg']}; padding: 30px; border-radius: 20px; border-left: 12px solid {cfg['color']}; margin-bottom: 25px;">
    <h1 style="margin:0; color: #333;">{cfg['icon']} {phase} <span style="font-size: 0.5em; color: #666;">第 {day_num} 天</span></h1>
    <p style="font-size: 1.2em; color: #d63384; margin-top: 15px; font-weight: bold;">{greeting}</p>
    <p style="font-size: 1.1em; color: #444; margin-top: 10px;"><b>时期特征：</b>{cfg['intro']}</p>
    <p style="font-size: 1.1em; color: #444;"><b>常见表现：</b>{cfg['status']}</p>
</div>
""", unsafe_allow_html=True)

# 6. 四维注意事项 (使用 Columns 展示更清晰)
st.subheader("📝 本阶段全方位指南")
c1, c2 = st.columns(2)
with c1:
    with st.expander("🍱 饮食方案", expanded=True):
        for item in cfg['eat']: st.write(item)
    with st.expander("💄 护肤要点", expanded=True):
        st.write(cfg['skin'])

with c2:
    with st.expander("🧘 生活与运动", expanded=True):
        for item in cfg['do']: st.write(item)
    with st.expander("💖 心情寄语", expanded=True):
        st.info(f"在这个阶段，{greeting.split('，')[-1]}")

# 7. 动态进度图
st.divider()
st.subheader("📊 周期运行轨迹")

fig, ax = plt.subplots(figsize=(10, 1.5))
boundaries = [0, 5, 12, 16, avg_cycle]
p_names = list(PHASE_CONFIG.keys())

for i in range(len(p_names)):
    active = (phase == p_names[i])
    ax.barh(0, boundaries[i+1]-boundaries[i], left=boundaries[i], 
            color=PHASE_CONFIG[p_names[i]]['color'], 
            alpha=0.9 if active else 0.1, 
            edgecolor='white', linewidth=2)
    ax.text(boundaries[i] + (boundaries[i+1]-boundaries[i])/2, 0, 
            PHASE_CONFIG[p_names[i]]['icon'], va='center', ha='center', fontsize=20)

# 标记红点位置
ax.plot(day_num, 0, marker='o', markersize=16, color='#d63384', markeredgecolor='white', markeredgewidth=2)
ax.axis('off')
st.pyplot(fig)

# 8. 智能求助
if st.button("🚨 感到很不舒服？点击求助"):
    st.warning("### 贴心对策：\n1. **痛经：** 暖宝宝贴在气海穴/关元穴，或侧卧蜷缩。\n2. **心情烦躁：** 试试4-7-8呼吸法，或者允许自己哭一场放松压力。\n3. **身体浮肿：** 晚上8点后少喝水，垫高双脚睡觉。")

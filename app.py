import streamlit as st
from datetime import datetime, date, timedelta
import numpy as np

# 1. 页面配置
st.set_page_config(page_title="女生生理期全能管家", page_icon="🌸", layout="wide")

# 2. 核心知识库 (详细到饮食与宜忌)
PHASE_DATA = {
    "月经期": {
        "icon": "🩸", "color": "#FFC0CB", "bg": "#FFF0F5",
        "change": "内膜脱落，激素降至最低。身体最虚弱，容易畏寒、腰酸、痛经。",
        "do": "✅ 睡够8小时、小腹热敷、淋浴、轻拉伸",
        "no": "❌ 剧烈运动、盆浴、洗头不吹干、熬夜",
        "eat_yes": "🥣 红糖姜茶、黑豆、牛肉、红枣、暖性水果",
        "eat_no": "🧊 冰激凌、生鱼片、浓茶、浓咖啡、螃蟹"
    },
    "卵泡期": {
        "icon": "🌱", "color": "#ADD8E6", "bg": "#F0F8FF",
        "change": "雌激素回升，卵泡发育。精力最旺盛，皮肤状态和心情最好的“黄金期”。",
        "do": "✅ 高效工作、尝试挑战、高强度健身、社交",
        "no": "❌ 盲目节食（此时代谢快，需补充营养）",
        "eat_yes": "🥗 鱼虾蛋白、豆浆、大量鲜蔬、五谷杂粮",
        "eat_no": "🍔 尽量少吃深加工的油腻食品"
    },
    "排卵期": {
        "icon": "🥚", "color": "#90EE90", "bg": "#F5FFF5",
        "change": "雌激素达到顶峰。身体轻盈，自信心强，是受孕几率最高的时期。",
        "do": "✅ 户外运动、保持私处清洁、约会拍照",
        "no": "❌ 忽视避孕（若无备孕计划）、久坐不动",
        "eat_yes": "💧 多喝水、高纤维蔬菜、水果",
        "eat_no": "🍩 控糖！此时激素波动易长排卵痘"
    },
    "黄体期": {
        "icon": "🍂", "color": "#FFFACD", "bg": "#FFFFF0",
        "change": "孕激素占主导。易出现PMS（经前综合征），如乳房胀痛、浮肿、焦虑。",
        "do": "✅ 泡脚、冥想、早睡、写日记放松",
        "no": "❌ 做重大决策、剧烈运动、过度社交",
        "eat_yes": "🍌 香蕉、坚果、黑巧克力、全麦面包",
        "eat_no": "🧂 控盐防止浮肿、控酒精、少咖啡因"
    }
}

# 3. 智能进化系统 (侧边栏)
if 'cycle_history' not in st.session_state:
    st.session_state.cycle_history = [28]

with st.sidebar:
    st.header("🧠 智能进化中")
    new_record = st.number_input("记录一次实际周期(天):", 20, 50, 28)
    if st.button("➕ 确认记录"):
        st.session_state.cycle_history.append(new_record)
        st.success("记录成功！")
    
    avg_cycle = int(np.mean(st.session_state.cycle_history))
    st.metric("计算出的平均周期", f"{avg_cycle} 天")
    st.caption("记录越多，预警越准。")

# 4. 核心交互区
st.title("🌸 私人生理期智能顾问")
st.write("---")

st.subheader("👋 亲爱的，今天状态如何？")
col_q1, col_q2 = st.columns(2)
with col_q1:
    day_input = st.number_input("月经开始后的第几天？", 1, avg_cycle, 1)

# 判定逻辑
def get_phase(day, cycle):
    if 1 <= day <= 5: return "月经期"
    elif day <= (cycle - 14 - 2): return "卵泡期"
    elif day <= (cycle - 14 + 2): return "排卵期"
    else: return "黄体期"

current_p = get_phase(day_input, avg_cycle)
data = PHASE_DATA[current_p]

# 日历预警
today = date.today()
next_date = today + timedelta(days=(avg_cycle - day_input + 1))

# 5. 状态看板
st.markdown(f"""
<div style="background-color: {data['bg']}; padding: 25px; border-radius: 15px; border-left: 15px solid {data['color']};">
    <h1 style="margin:0;">{data['icon']} {current_p} <span style="font-size:0.5em; color:gray;">(第 {day_input} 天)</span></h1>
    <p style="font-size: 1.1em; color: #333; margin-top: 10px;"><b>🧬 身体变化：</b>{data['change']}</p>
    <p style="font-size: 1.1em; color: #d63384;"><b>📅 预警：</b>预计下一次将在 <b>{next_date.strftime('%Y年%m月%d日')}</b> 左右到来。</p>
</div>
""", unsafe_allow_html=True)

# 6. 详细建议板块
st.write("")
st.subheader("📝 本阶段专属指南")
c1, c2 = st.columns(2)

with c1:
    with st.expander("🧘 生活宜忌", expanded=True):
        st.write(data['do'])
        st.write(data['no'])
with c2:
    with st.expander("🍱 饮食方案", expanded=True):
        st.write(f"**建议吃：** {data['eat_yes']}")
        st.write(f"**忌讳吃：** {data['eat_no']}")

# 7. 意外情况处理 (智能交互)
st.write("---")
st.subheader("🚨 身体求助站")
st.write("如果现在感到不舒服，请选择具体情况：")

issue = st.selectbox("我现在感觉...", ["我很好，一切正常", "痛经难忍", "经血量异常(过多/过少)", "情绪极度焦虑/想哭", "身体严重浮肿"])

if issue == "痛经难忍":
    st.warning("### 🚑 痛经对策：\n1. **物理缓解**：暖宝宝贴在小腹或后腰（气海穴）。\n2. **体位放松**：尝试‘婴儿式’侧卧蜷缩。\n3. **饮食**：喝一杯浓郁的热红糖姜茶。\n4. **就医**：若痛到无法站立且药物无效，请务必及时就医。")
elif issue == "经血量异常(过多/过少)":
    st.info("### 📋 量多/量少建议：\n- **量多**：避免剧烈运动，多吃红肉补铁。若一小时需更换一次卫生巾且持续，请咨询医生。\n- **量少**：注意保暖，避免寒凉食物，观察是否因压力过大或节食引起。")
elif issue == "情绪极度焦虑/想哭":
    st.info("### 🫂 情绪抱抱：\n- 这是体内激素骤降（尤其是黄体期）的正常反应，不是你的错。\n- 允许自己哭出来，或者吃一块黑巧克力缓解压力。\n- 尝试4-7-8呼吸法，暂停处理重大决策。")
elif issue == "身体严重浮肿":
    st.info("### 💧 消肿指南：\n1. **控盐**：减少晚餐食盐摄入。\n2. **运动**：散步15分钟促进循环。\n3. **姿势**：睡觉时在脚下垫一个枕头，帮助血液回流。")

# 8. 进度视觉化
st.write("---")
progress = day_input / avg_cycle
st.caption(f"周期进度：{int(progress*100)}%")
st.progress(progress)

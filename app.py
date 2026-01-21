import streamlit as st
from datetime import datetime, date, timedelta
import numpy as np

# 1. 页面配置
st.set_page_config(page_title="智能生理期进化助手", page_icon="🌙", layout="wide")

# 2. 初始化智能数据库 (如果浏览器没刷新，它会一直记得)
if 'cycle_history' not in st.session_state:
    st.session_state.cycle_history = [28] # 默认初始值为28天

# 3. 核心知识库
PHASE_DICT = {
    "月经期": {"icon": "🩸", "color": "#FFC0CB", "bg": "#FFF0F5", "change": "内膜脱落，身体虚弱。建议：热敷、保暖、补铁。"},
    "卵泡期": {"icon": "🌱", "color": "#ADD8E6", "bg": "#F0F8FF", "change": "雌激素回升。建议：高效工作、尝试新运动。"},
    "排卵期": {"icon": "🥚", "color": "#90EE90", "bg": "#F5FFF5", "change": "精力最旺盛。建议：多喝水、保持心情愉快。"},
    "黄体期": {"icon": "🍂", "color": "#FFFACD", "bg": "#FFFFF0", "change": "经前综合征。建议：控盐、控咖啡因、冥想。"}
}

st.title("🌙 生理期智能顾问 (进化中...)")

# --- 侧边栏：智能进化区 ---
with st.sidebar:
    st.header("🧠 智能进化系统")
    st.write("App 会根据您的历史记录自动计算平均值。")
    
    # 手动输入历史记录（模拟用久了的情况）
    new_record = st.number_input("添加一次历史周期天数 (如30):", min_value=20, max_value=45, value=28)
    if st.button("➕ 记录这次周期"):
        st.session_state.cycle_history.append(new_record)
        st.success("记录成功！")

    # 计算平均值
    avg_cycle = int(np.mean(st.session_state.cycle_history))
    st.metric("您的平均周期", f"{avg_cycle} 天", delta=f"{avg_cycle - 28} (vs 初始值)")
    
    if st.button("🗑️ 清空历史"):
        st.session_state.cycle_history = [28]
        st.rerun()

# --- 主交互区 ---
st.subheader("👋 亲爱的，今天进度如何？")

# 交互输入
day_input = st.number_input("今天是月经开始后的第几天？", min_value=1, max_value=avg_cycle, value=1)

# 判定时期逻辑 (根据平均周期动态调整比例)
def get_current_phase(day, cycle):
    if day <= 5: return "月经期"
    elif day <= (cycle - 14 - 2): return "卵泡期" # 排卵前
    elif day <= (cycle - 14 + 2): return "排卵期" # 排卵前后4天
    else: return "黄体期"

current_phase = get_current_phase(day_input, avg_cycle)
data = PHASE_DICT[current_phase]

# 计算现实日历预警
today = date.today()
start_of_this_period = today - timedelta(days=day_input - 1)
next_period_date = start_of_this_period + timedelta(days=avg_cycle)
days_until_next = (next_period_date - today).days

# 4. 显示大卡片
st.markdown(f"""
<div style="background-color: {data['bg']}; padding: 25px; border-radius: 15px; border-left: 15px solid {data['color']};">
    <h1 style="margin:0;">{data['icon']} 当前：{current_phase}</h1>
    <h3 style="color: #666;">第 {day_input} 天 (基于平均周期 {avg_cycle} 天)</h3>
    <p style="font-size: 1.1em; margin-top:10px;"><b>🧬 身体状态：</b>{data['change']}</p>
</div>
""", unsafe_allow_html=True)

# 5. 日历预警
st.write("")
col1, col2 = st.columns(2)
with col1:
    st.info(f"### 📅 下次预警：\n## {next_period_date.strftime('%Y-%m-%d')}")
    st.write(f"距离下一次还有 **{days_until_next}** 天")

with col2:
    if days_until_next <= 3:
        st.error("🚨 **高能预警：姨妈即将到达战场！**\n请备好物资，减少凉食。")
    else:
        progress = (day_input / avg_cycle)
        st.write("⚙️ **周期进度**")
        st.progress(progress)

# 6. 生活指南
st.divider()
st.subheader("💡 今天的专属宜忌")
c1, c2 = st.columns(2)
# 简单的宜忌数据
advice = {
    "月经期": {"do": "早睡、热敷、喝姜茶", "no": "剧烈运动、冰淇淋、盆浴"},
    "卵泡期": {"do": "高强度工作、健身、社交", "no": "过度节食"},
    "排卵期": {"do": "多喝水、记录分泌物", "no": "熬夜、吃太甜"},
    "黄体期": {"do": "泡脚、听轻音乐、吃黑巧", "no": "咖啡、高盐饮食、大决策"}
}

with c1:
    st.success(f"✅ **推荐做：** {advice[current_phase]['do']}")
with c2:
    st.error(f"❌ **忌讳做：** {advice[current_phase]['no']}")

st.caption("注：随着您记录的次数增多，左侧侧边栏的‘平均周期’会越来越准，预警也会随之自动修正。")

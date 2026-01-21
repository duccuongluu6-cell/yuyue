from datetime import datetime

def get_period_phase(last_start_date, avg_cycle=28):
    """
    根据上次开始日期，判断今天处于哪个阶段
    """
    today = datetime.now().date()
    # 计算从开始那天到今天过了几天
    delta_days = (today - last_start_date).days
    
    # 取模运算，得到在当前周期内的第几天
    day_in_cycle = (delta_days % avg_cycle) + 1
    
    # 定义阶段范围
    if 1 <= day_in_cycle <= 5:
        return "月经期", day_in_cycle
    elif 6 <= day_in_cycle <= 12:
        return "卵泡期", day_in_cycle
    elif 13 <= day_in_cycle <= 16:
        return "排卵期", day_in_cycle
    else:
        return "黄体期", day_in_cycle
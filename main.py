# 初始手牌
init_hand_cards = [
    ("2", "♠", 2), ("2", "♣", 2), ("2", "♦", 2), ("2", "♥", 2),
    ("3", "♠", 3), ("3", "♣", 3), ("3", "♦", 3), ("3", "♥", 3),
    ("4", "♠", 4), ("4", "♣", 4), ("4", "♦", 4), ("4", "♥", 4),
    ("5", "♠", 5), ("5", "♣", 5), ("5", "♦", 5), ("5", "♥", 5),
    ("6", "♠", 6), ("6", "♣", 6), ("6", "♦", 6), ("6", "♥", 6),
    ("7", "♠", 7), ("7", "♣", 7), ("7", "♦", 7), ("7", "♥", 7),
    ("8", "♠", 8), ("8", "♣", 8), ("8", "♦", 8), ("8", "♥", 8),
    ("9", "♠", 9), ("9", "♣", 9), ("9", "♦", 9), ("9", "♥", 9),
    ("10", "♠", 10), ("10", "♣", 10), ("10", "♦", 10), ("10", "♥", 10),
    ("J", "♠", 10), ("J", "♣", 10), ("J", "♦", 10), ("J", "♥", 10),
    ("Q", "♠", 10), ("Q", "♣", 10), ("Q", "♦", 10), ("Q", "♥", 10),
    ("K", "♠", 10), ("K", "♣", 10), ("K", "♦", 10), ("K", "♥", 10),
    ("A", "♠", 11), ("A", "♣", 11), ("A", "♦", 11), ("A", "♥", 11),
]

# 初始筹码和倍率
init_card_type_score = {
    "gaopai": {
        "score": 5,
        "rate": 1
    },
    "duizi": {
        "score": 10,
        "rate": 2
    },
    "liangdui": {
        "score": 20,
        "rate": 2
    },
    "santiao": {
        "score": 30,
        "rate": 3
    },
    "shunzi": {
        "score": 30,
        "rate": 4
    },
    "tonghua": {
        "score": 35,
        "rate": 4
    },
    "hulu": {
        "score": 40,
        "rate": 4
    },
    "sitiao": {
        "score": 60,
        "rate": 7
    },
    "tonghuashun": {
        "score": 100,
        "rate": 8
    }
}

values = {
    "A": 14,
    "K": 13,
    "Q": 12,
    "J": 11,
    "10": 10,
    "9": 9,
    "8": 8,
    "7": 7,
    "6": 6,
    "5": 5,
    "4": 4,
    "3": 3,
    "2": 2,
}

import itertools
from functools import lru_cache
from collections import Counter
import concurrent.futures
import threading
import time

@lru_cache(maxsize=1024)
def count_cards(cards):
    """缓存卡牌计数结果"""
    return Counter(card[0] for card in cards)

@lru_cache(maxsize=1024)
def check_tonghua(cards):
    """检查是否是同花"""
    if len(cards) != 5:
        return False
    return all(card[1] == cards[0][1] for card in cards[1:])

@lru_cache(maxsize=1024)
def check_shunzi(cards, allow_recycle=False):
    """检查是否是顺子"""
    if len(cards) < 5:
        return False
    
    # 转换为值列表并排序
    cards_values = sorted(values[card[0]] for card in cards)
    
    # 检查是否是特殊顺子（A2345）
    if allow_recycle and cards_values == [2, 3, 4, 5, 14]:
        return True
        
    # 检查普通顺子
    return all(cards_values[i+1] - cards_values[i] == 1 for i in range(4))

@lru_cache(maxsize=1024)
def check_sitiao(cards):
    """检查是否是四条"""
    if len(cards) < 4:
        return False, None
    
    counter = count_cards(cards)
    for value, count in counter.items():
        if count == 4:
            return True, values[value]
    return False, None

@lru_cache(maxsize=1024)
def check_hulu(cards):
    """检查是否是葫芦"""
    if len(cards) != 5:
        return False
    
    counter = count_cards(cards)
    return len(counter) == 2 and 3 in counter.values()

@lru_cache(maxsize=1024)
def check_santiao(cards):
    """检查三条"""
    if len(cards) < 3:
        return False
    
    counter = count_cards(cards)
    return 3 in counter.values()

@lru_cache(maxsize=1024)
def check_liangdui(cards):
    """检查两对"""
    if len(cards) < 4:
        return False
    
    counter = count_cards(cards)
    pairs = sum(1 for count in counter.values() if count == 2)
    return pairs == 2

@lru_cache(maxsize=1024)
def check_duizi(cards):
    """检查对子"""
    if len(cards) < 2:
        return False
    
    counter = count_cards(cards)
    return 2 in counter.values()

@lru_cache(maxsize=1024)
def check_tonghuashun(cards):
    """检查是否是同花顺"""
    return check_tonghua(cards) and check_shunzi(cards)

def get_card_string(cards):
    card_string = ""
    for card in cards:
        card_string += card[0]
    return card_string

def get_tonghuashun_score(cards):
    """计算同花顺的分数"""

    # 获得基础筹码
    score = init_card_type_score["tonghuashun"]["score"]
    # 获得倍率
    rate = init_card_type_score["tonghuashun"]["rate"]

    # 计算最终分数
    # 同花顺的分数 = 基础筹码 + (五张牌的筹码总和) * 倍率
    for card in cards:
        score += card[2]

    return score * rate

def get_sitiao_score(cards):
    """计算四条的分数"""
    # 获得基础筹码
    score = init_card_type_score["sitiao"]["score"]
    # 获得倍率
    rate = init_card_type_score["sitiao"]["rate"]

    # 找到四条的牌，然后计算最终分数
    sitiao_card_value = 0
    for card in cards:
        count = len([c for c in cards if c[0] == card[0]])
        if count == 4:
            sitiao_card_value = values[card[0]]
            break

    # 计算最终分数
    # 四条的分数 = 基础筹码 + (四张牌的筹码总和) * 倍率
    for card in cards:
        if values[card[0]] == sitiao_card_value:
            score += card[2]

    return score * rate

def get_hulu_score(cards):
    """计算葫芦的分数"""
    # 获得基础筹码
    score = init_card_type_score["hulu"]["score"]
    # 获得倍率
    rate = init_card_type_score["hulu"]["rate"]

    # 葫芦的每张牌都参数计算分数
    for card in cards:
        score += card[2]

    return score * rate

def get_tonghua_score(cards):
    """计算同花的分数"""
    # 获得基础筹码
    score = init_card_type_score["tonghua"]["score"]
    # 获得倍率
    rate = init_card_type_score["tonghua"]["rate"]

    # 同花的每张牌都参数计算分数
    for card in cards:
        score += card[2]

    return score * rate

def get_shunzi_score(cards):
    """计算顺子的分数"""
    # 获得基础筹码
    score = init_card_type_score["shunzi"]["score"]
    # 获得倍率
    rate = init_card_type_score["shunzi"]["rate"]

    # 顺子的每张牌都参数计算分数
    for card in cards:
        score += card[2]

    return score * rate

def get_santiao_score(cards):
    """计算三条的分数"""
    # 获得基础筹码
    score = init_card_type_score["santiao"]["score"]
    # 获得倍率
    rate = init_card_type_score["santiao"]["rate"]

    # 找到三条的牌，然后计算最终分数
    santiao_card_value = 0
    for card in cards:
        count = len([c for c in cards if c[0] == card[0]])
        if count == 3:
            santiao_card_value = values[card[0]]
            break

    # 计算最终分数
    # 三条的分数 = 基础筹码 + (三张牌的筹码总和) * 倍率
    for card in cards:
        if values[card[0]] == santiao_card_value:
            score += card[2]

    return score * rate

def get_liangdui_score(cards):
    """计算两对的分数"""
    # 获得基础筹码
    score = init_card_type_score["liangdui"]["score"]
    # 获得倍率
    rate = init_card_type_score["liangdui"]["rate"]

    # 找到两对的牌，然后计算最终分数
    liangdui_card_values = []
    for card in cards:
        count = len([c for c in cards if c[0] == card[0]])
        if count == 2:
            liangdui_card_values.append(values[card[0]])

    # 计算最终分数
    # 两对的分数 = 基础筹码 + (两对牌的筹码总和) * 倍率
    for card in cards:
        if values[card[0]] in liangdui_card_values:
            score += card[2]

    return score * rate

def get_duizi_score(cards):
    """计算对子的分数"""
    # 获得基础筹码
    score = init_card_type_score["duizi"]["score"]
    # 获得倍率
    rate = init_card_type_score["duizi"]["rate"]

    # 找到对子的牌，然后计算最终分数
    duizi_card_value = 0
    for card in cards:
        count = len([c for c in cards if c[0] == card[0]])
        if count == 2:
            duizi_card_value = values[card[0]]
            break

    # 计算最终分数
    # 对子的分数 = 基础筹码 + (两张牌的筹码总和) * 倍率
    for card in cards:
        if values[card[0]] == duizi_card_value:
            score += card[2]

    return score * rate

def get_gaopai_score(cards):
    """计算高牌的分数"""
    # 获得基础筹码
    score = init_card_type_score["gaopai"]["score"]
    # 获得倍率
    rate = init_card_type_score["gaopai"]["rate"]

    # 高牌的分数 = [基础筹码 + (最大的一张牌的筹码)] * 倍率
    score += cards[-1][2]

    return score * rate

@lru_cache(maxsize=1024)
def get_cards_type_and_score(cards):
    """
    获得牌型，还有最终的分数
    允许出1~5张牌
    """
    # 先对牌进行排序并转换为元组以支持缓存
    cards = tuple(sorted(cards, key=lambda x: values[x[0]]))

    if check_tonghuashun(cards):
        return "tonghuashun", get_tonghuashun_score(cards)

    is_sitiao, sitiao_value = check_sitiao(cards)
    if is_sitiao:
        return "sitiao", get_sitiao_score(cards)

    is_hulu = check_hulu(cards)
    if is_hulu:
        return "hulu", get_hulu_score(cards)

    is_tonghua = check_tonghua(cards)
    if is_tonghua:
        return "tonghua", get_tonghua_score(cards)

    is_shunzi = check_shunzi(cards)
    if is_shunzi:
        return "shunzi", get_shunzi_score(cards)

    is_santiao = check_santiao(cards)
    if is_santiao:
        return "santiao", get_santiao_score(cards)

    is_liangdui = check_liangdui(cards)
    if is_liangdui:
        return "liangdui", get_liangdui_score(cards)

    is_duizi = check_duizi(cards)
    if is_duizi:
        return "duizi", get_duizi_score(cards)

    return "gaopai", get_gaopai_score(cards)

def get_max_cards_type_and_score(hand_cards):
    """
    从N张牌中抽取5张牌，获取最大的牌型和分数
    使用生成器优化内存使用
    """
    max_score = 0
    max_card_type = ""
    
    # 使用生成器而不是一次性生成所有组合
    for five_cards in itertools.combinations(hand_cards, 5):
        cur_card_type, cur_card_score = get_cards_type_and_score(five_cards)
        if cur_card_score > max_score:
            max_score = cur_card_score
            max_card_type = cur_card_type
            
            # 如果已经是最大牌型，可以提前结束
            if cur_card_type == "tonghuashun":
                break
    
    return max_card_type, max_score

def process_combination(cards):
    """处理单个组合"""
    card_type, card_score = get_max_cards_type_and_score(cards)
    return card_score >= 300, card_score

def calculate_probabilities():
    """计算概率统计，使用多线程处理"""
    score = 0
    can_pass = 0
    total = 0
    
    # 创建线程锁用于更新计数器
    counter_lock = threading.Lock()
    progress_counter = {'processed': 0}
    
    # 计算总组合数
    total_combinations = sum(1 for _ in itertools.combinations(init_hand_cards, 8))
    start_time = time.time()
    
    def process_batch(batch):
        batch_score = 0
        batch_pass = 0
        batch_total = 0
        
        for cards in batch:
            is_pass, card_score = process_combination(cards)
            if is_pass:
                batch_pass += 1
            batch_score += card_score
            batch_total += 1
            
            # 更新进度
            with counter_lock:
                progress_counter['processed'] += 1
                if progress_counter['processed'] % 1000 == 0:  # 每处理1000个组合更新一次
                    elapsed_time = time.time() - start_time
                    progress = progress_counter['processed'] / total_combinations * 100
                    remaining_time = (elapsed_time / progress_counter['processed'] * 
                                   (total_combinations - progress_counter['processed']))
                    print(f"进度: {progress:.2f}% ({progress_counter['processed']}/{total_combinations})")
                    print(f"预计剩余时间: {remaining_time:.2f}秒")
                    print(f"当前平均分数: {batch_score/batch_total:.2f}")
                    print(f"当前通过率: {batch_pass/batch_total:.2%}\n")
        
        return batch_pass, batch_score, batch_total
    
    # 将组合分成多个批次
    batch_size = 10000  # 每个批次的大小
    combinations = list(itertools.combinations(init_hand_cards, 8))
    batches = [combinations[i:i + batch_size] for i in range(0, len(combinations), batch_size)]
    
    print(f"总组合数: {total_combinations}")
    print(f"批次数: {len(batches)}")
    print("开始计算...\n")
    
    # 使用线程池处理批次
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
        futures = [executor.submit(process_batch, batch) for batch in batches]
        
        # 收集结果
        for future in concurrent.futures.as_completed(futures):
            batch_pass, batch_score, batch_total = future.result()
            can_pass += batch_pass
            score += batch_score
            total += batch_total
    
    # 计算最终结果
    avg_score = score / total if total > 0 else 0
    pass_rate = can_pass / total if total > 0 else 0
    
    # 输出总用时
    total_time = time.time() - start_time
    print(f"\n计算完成！总用时: {total_time:.2f}秒")
    
    return avg_score, pass_rate

# 测试第一轮的概率情况
print("开始计算概率...")
score, pass_rate = calculate_probabilities()
print(f"\n最终结果:")
print(f"平均分数：{score:.2f}")
print(f"通过概率：{pass_rate:.2%}")

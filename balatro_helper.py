# 小丑牌计算帮助类

def get_hand_max_score(hand_cards, score_types):
    """
    计算当前手牌可以拿到的最大分数

    参数:
    hand_cards (list): 当前手牌，每张牌由 (点数, 花色, 分数) 组成的元组表示
    score_types (dict): 不同牌型的得分规则，包含基础分数和倍率

    返回:
    tuple: 包含最大可能得分和对应的牌型
    """
    max_score = 0
    best_type = ""

    # 遍历所有可能的5张牌组合
    for combo in itertools.combinations(hand_cards, 5):
        score, card_type = get_hand_score(combo, score_types)
        if score > max_score:
            max_score = score
            best_type = card_type

    return max_score, best_type

def get_hand_score(cards, score_types):
    # 判断牌型并计算分数
    if is_royal_flush(cards):
        return calculate_score(cards, score_types["royal_flush"]), "Royal Flush"
    elif is_straight_flush(cards):
        return calculate_score(cards, score_types["straight_flush"]), "Straight Flush"
    elif is_four_of_a_kind(cards):
        return calculate_score(cards, score_types["four_of_a_kind"]), "Four of a Kind"
    # ... 其他牌型判断 ...
    else:
        return calculate_score(cards, score_types["high_card"]), "High Card"

def calculate_score(cards, score_rule):
    base_score = score_rule["score"]
    rate = score_rule["rate"]
    return base_score + sum(card[2] for card in cards) * rate

# 当前手牌
# 当前牌堆
# 如果弃牌的话，弃牌之后的手牌得分概率
def cal_probabilities(hand_cards, left_cards, score_types, balatro_cards):
    """
    计算当前手牌可以拿到的最大分数

    参数:
    hand_cards (list): 当前手牌，每张牌由 (点数, 花色, 分数) 组成的元组表示
    left_cards (list): 当前牌堆中剩余的牌，格式同 hand_cards
    balatro_cards (list): 当前手中的小丑牌
    score_types (dict): 不同牌型的得分规则，包含基础分数和倍率

    返回:
    tuple: 包含最大可能得分和对应的牌型
    """

    
    # 计算当前手牌可以拿到的最大分数
    cur_max_score = 

    pass
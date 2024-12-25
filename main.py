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


# 牌型：
# 1. 高牌
# 2. 对子
# 3. 两对
# 4. 三条
# 5. 顺子
# 6. 同花
# 7. 葫芦
# 8. 四条
# 9. 同花顺

def check_tonghua(cards):
    """
    检查是否是同花
    """
    if len(cards) != 5:
        return False

    for i in range(1, len(cards)):
        if cards[i][2] != cards[0][2]:
            return False

    return True


def get_card_string(cards):
    card_string = ""
    for card in cards:
        card_string += card[0]
    return card_string


def check_shunzi_without_recycle(cards):
    if len(cards) != 5:
        return False

    cards.sort(key=lambda x: values[x[0]])

    for i in range(4):  # 检查前四张牌，因为第五张牌必然与第四张牌连续
        if values[cards[i + 1][0]] - values[cards[i][0]] != 1:
            return False
    return True


def check_shunzi(cards, allow_recycle=False):
    """
    检查是否是顺子
    @param allow_recycle: 是否允许循环，例如 K A 2 3 4
    """
    if len(cards) < 5:
        return False

    cards.sort(key=lambda x: values[x[0]])

    if allow_recycle:
        # 循环检查
        cards_string = get_card_string(cards)
        allowed_recycle_shunzi = ["2JQKA", "23QKA", "234KA", "2345A"]
        return check_shunzi_without_recycle(cards) or cards_string in allowed_recycle_shunzi
    else:
        for i in range(4):  # 检查前四张牌，因为第五张牌必然与第四张牌连续
            if values[cards[i + 1][0]] - values[cards[i][0]] != 1:
                return False
        return True


def check_tonghuashun(cards):
    """
    检查是否是同花顺
    """
    if len(cards) != 5:
        return False

    return check_tonghua(cards) and check_shunzi(cards)


def check_sitiao(cards):
    """
    检查是否是四条
    """
    if len(cards) < 4:
        return False, None

    cards.sort(key=lambda x: values[x[0]])

    if cards[0][0] == cards[1][0] == cards[2][0] == cards[3][0]:
        return True, values[cards[0][0]]
    if cards[1][0] == cards[2][0] == cards[3][0] == cards[4][0]:
        return True, values[cards[1][0]]

    return False, None


def check_hulu(cards):
    """
    检查是否是葫芦
    """
    if len(cards) != 5:
        return False

    cards.sort(key=lambda x: values[x[0]])

    if cards[0][0] == cards[1][0] == cards[2][0] and cards[3][0] == cards[4][0]:
        return True
    if cards[0][0] == cards[1][0] and cards[2][0] == cards[3][0] == cards[4][0]:
        return True
    return False


def check_santiao(cards):
    """检查三条"""
    if len(cards) < 3:
        return False

    cards.sort(key=lambda x: values[x[0]])

    if cards[0][0] == cards[1][0] == cards[2][0]:
        return True
    if cards[1][0] == cards[2][0] == cards[3][0]:
        return True
    if cards[2][0] == cards[3][0] == cards[4][0]:
        return True
    return False


def check_liangdui(cards):
    """检查两对"""
    if len(cards) < 4:
        return False

    cards.sort(key=lambda x: values[x[0]])

    if cards[0][0] == cards[1][0] and cards[2][0] == cards[3][0]:
        return True
    if cards[0][0] == cards[1][0] and cards[3][0] == cards[4][0]:
        return True
    if cards[1][0] == cards[2][0] and cards[3][0] == cards[4][0]:
        return True
    return False


def check_duizi(cards):
    """检查对子"""
    if len(cards) < 2:
        return False

    cards.sort(key=lambda x: values[x[0]])

    if cards[0][0] == cards[1][0]:
        return True
    if cards[1][0] == cards[2][0]:
        return True
    if cards[2][0] == cards[3][0]:
        return True
    if cards[3][0] == cards[4][0]:
        return True
    return False


def check_gaopai(cards):
    """检查高牌"""
    return True


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


def get_cards_type_and_score(cards):
    """
    获得牌型，还有最终的分数
    允许出1~5张牌
    """
    # 先对牌进行排序
    cards.sort(key=lambda x: values[x[0]])

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


# 从N张牌中抽取5张牌，获取最大的牌型和分数
def get_max_cards_type_and_score(hand_cards):
    """
    从N张牌中抽取5张牌，获取最大的牌型和分数
    """
    all_hand_cards_combines = list(itertools.combinations(hand_cards, 5))

    max_score = 0
    max_card_type = ""

    for five_cards in all_hand_cards_combines:
        cur_card_type, cur_card_score = get_cards_type_and_score(list(five_cards))
        if cur_card_score > max_score:
            max_score = cur_card_score
            max_card_type = cur_card_type

    return max_card_type, max_score


# 测试第一轮的概率情况
# 总共有52张牌，第一轮抽选5张牌

import copy

init_cards = copy.deepcopy(init_hand_cards)
# 从52张牌中抽取5张牌
import itertools

all_cards = list(itertools.combinations(init_cards, 8))

print(len(all_cards))

score = 0
can_pass = 0

for cards in all_cards:
    card_type, card_score = get_max_cards_type_and_score(list(cards))
    if card_score >= 300:
        all_cards.remove(cards)

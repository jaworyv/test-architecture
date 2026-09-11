# 1. Дана строка s. Нужно вернуть индекс первого символа,
# который встречается в строке ровно один раз.
# Если такого символа нет — вернуть -1.
#first_unique_char("leetcode")
# 0
# 'l' встречается один раз
#first_unique_char("loveleetcode")
# 2
# первый уникальный символ — 'v'
#first_unique_char("aabb")
# -1
#first_unique_char("aabbc")
# 4
from rstr import lowercase


def first_uniq_index(s: str) -> int:
    answer = {}
    for c in s:
        if c not in answer:
            answer[c] = 1
        else:
            answer[c] += 1
    for k, v in answer.items():
        if v == 1:
            uniq_item = k
    return s.find(uniq_item)


print(first_uniq_index("leetcode"))



import math
from matplotlib import pyplot as plt

def visual_key_concept_statistics(json_dic, n_col_limit=3, linewidth=2, markersize=5):
    num = len(json_dic.keys()) - 1
    if num<=n_col_limit:
        row = 1
        col = num
    else:
        row = math.ceil(num/n_col_limit)
        col = n_col_limit
    for i, (k, v) in enumerate(json_dic.items()):
        if k!="empty_concepts":
            x = [i["lemma"] for i in v]
            y = [i["count"] for i in v]
            plt.subplot(row, col, i)
            plt.plot(x, y, "o", linewidth=linewidth, markersize=markersize)
            plt.title(k)

from holoviews import output
from holoviews.operation import operation


def get_min_step(steps):
    """
    缩进代码:通过多次操作，最终实现对每一行的缩进长度要求。一次操作是缩进一个TAB长度。注：这里缩进仅指从左往右，不能回退。
    一次操作可选择一行或连续多行同时缩进。
    :param steps: n 个整数，依次表示第 1~n 行的最终缩进长度要求，取值范围：[0, 1000000]。
    :return: 所需的最少操作次数
    """
    # 问题：区间增量最小次数问题；形象为往一形状不规则的仓库中注水，一次注一个单位高度，求注满水的最小次数。
    # 求解思路：对注满每个位置需要进行的注水操作次数求和。当前高度小于等于前一高度时，前一位置的水高蔓延到当前位置，当前位置不需要进行注水操作；
    # 当前高度大于前一高度时，需进行高度差次的注水操作。
    operations = steps[0]
    for i in range(1, len(steps)):
        if steps[i] > steps[i - 1]:
            operations += steps[i] - steps[i - 1]
    return operations

if __name__ == '__main__':
    step1, step2 = [1, 2, 3, 2, 1], [0, 1, 2, 0, 2, 4, 2, 1, 0]
    target1, target2 = 3, 6
    print(f"预测值：{get_min_step(step1)}, {get_min_step(step2)}")
    print(f"目标值：{target1}, {target2}")

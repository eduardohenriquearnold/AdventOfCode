import numpy as np

inp = """30373
25512
65332
33549
35390"""


def parse_input(input):
    arr = np.array([int(i) for i in input.replace("\n", "")], copy=False)
    shape = int(len(arr) ** 0.5)
    arr = arr.reshape(shape, shape)
    return arr


def visible_trees(heights):
    visible = np.zeros_like(heights, dtype=bool)

    # borders are visible
    visible[:, 0] = visible[:, -1] = visible[0, :] = visible[-1, :] = True

    # compute visibility for remaining trees
    for i in range(1, visible.shape[0] - 1):
        max_height_top = heights[:i, :].max(axis=0)
        visible[i, :] += max_height_top < heights[i, :]

        max_height_bottom = heights[i + 1 :, :].max(axis=0)
        visible[i, :] += max_height_bottom < heights[i, :]

        max_height_left = heights[:, :i].max(axis=1)
        visible[:, i] += max_height_left < heights[:, i]

        max_height_right = heights[:, i + 1 :].max(axis=1)
        visible[:, i] += max_height_right < heights[:, i]

    return visible


def score_trees(heights):
    score_top = np.zeros_like(heights, dtype=np.int32)
    score_bottom = np.zeros_like(heights, dtype=np.int32)
    score_left = np.zeros_like(heights, dtype=np.int32)
    score_right = np.zeros_like(heights, dtype=np.int32)
    ones = np.ones(heights.shape[0], dtype=np.int32)

    # score non-edge trees
    for i in range(1, heights.shape[0] - 1):
        score_top[i, :] += np.where(heights[i, :] > heights[i - 1, :], score_top[i - 1, :] + 1, ones)
        score_bottom[-i - 1, :] += np.where(heights[-i - 1, :] > heights[-i, :], score_bottom[-i, :] + 1, ones)
        score_left[:, i] += np.where(heights[:, i] > heights[:, i - 1], score_left[:, i - 1] + 1, ones)
        score_right[:, -i - 1] += np.where(heights[:, -i - 1] > heights[:, -i], score_right[:, -i] + 1, ones)

    print("top")
    print(score_top)
    print("bottom")
    print(score_bottom)
    print("left")
    print(score_left)
    print("right")
    print(score_right)

    score = score_top * score_bottom * score_left * score_right
    return score


# heights = parse_input(open("inputs/8.txt", "r").read())
heights = parse_input(inp)
vis = visible_trees(heights=heights)
score = score_trees(heights=heights)
print(vis.sum())
print(score.max())
print(score)

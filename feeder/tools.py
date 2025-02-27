import math
import torch
import random
import numpy as np
import torch.nn as nn
import torch.nn.functional as F
from math import sin, cos


transform_order = {
    'ntu': [0, 1, 2, 3, 8, 9, 10, 11, 4, 5, 6, 7, 16, 17, 18, 19, 12, 13, 14, 15, 20, 23, 24, 21, 22]
}


def drop_joint(data, drop_num=3, p=0.5):
    if random.random() < p:
        rng = np.random.default_rng()
        joint_num = data.shape[2]
        zeros = rng.choice(joint_num, drop_num, replace=False)
        tran = data.copy()
        tran[:, zeros] = 0
        return tran
    else:
        return data


def part_reverse(data, frame):
    C, T, V, M = data.shape
    trunk = [1, 2, 21, 3, 4]
    left_arm = [9, 10, 11, 12, 24, 25]
    right_arm = [5, 6, 7, 8, 22, 23]
    left_leg = [17, 18, 19, 20]
    right_leg = [13, 14, 15, 16]
    bodys = [trunk, left_arm, right_arm, left_leg, right_leg]

    reverse_order = np.flip(np.arange(frame), axis=0)
    # reverse_order = np.arange(frame)
    # np.random.shuffle(reverse_order)

    assert frame <= T, ' given frame length is smaller than tha data has :('

    # an evaluate function
    # using variance
    # max_change_score = -1
    # chosen_part_id = -1
    # data_s = np.sum(data, axis=3)
    # for part_id, part in enumerate(bodys):
    #     # change_score = sum(sum([np.var(data_s[:, :, joint - 1], axis=0) for joint in part]))
    #     change_score = sum([np.var(np.sum(data_s[:, :, joint - 1], axis=0), axis=0) for joint in part])
    #     # print(change_score)
    #     if change_score > max_change_score:
    #         # chosen_part = part
    #         chosen_part_id = part_id
    #         max_change_score = change_score
    #
    # # chosen_part_id = random.randint(0, 4)
    # # chosen_part_id = 1
    # assert chosen_part_id >= 0
    # chosen_part = bodys[chosen_part_id]
    chosen_part_id = random.randint(0, 4)
    chosen_part = bodys[chosen_part_id]

    trans = data.copy()
    chosen_part = [part - 1 for part in chosen_part]
    shuffle_frames = np.arange(T)
    shuffle_frames[:len(reverse_order)] = reverse_order
    for joint in chosen_part:
        trans[:, :, joint] = data[:, shuffle_frames, joint]
        # trans[:, :, joint] = 0

    return trans

def random_zero(data, frame):
    C, T, V, M = data.shape

    joints = [i for i in range(1, 26)]
    chosen_part = random.sample(joints, 5)
    trans = data.copy()

    assert frame <= T, ' given frame length is smaller than tha data has :('

    for joint in chosen_part:
        # trans[:, :, joint] = data[:, shuffle_frames, joint]
        trans[:, :, joint - 1] = 0

    return trans

def part_zero(data, frame):
    C, T, V, M = data.shape
    trunk = [1, 2, 21, 3, 4]
    left_arm = [9, 10, 11, 12, 24, 25]
    right_arm = [5, 6, 7, 8, 22, 23]
    left_leg = [17, 18, 19, 20]
    right_leg = [13, 14, 15, 16]
    bodys = [trunk, left_arm, right_arm, left_leg, right_leg]

    # reverse_order = np.flip(np.arange(frame), axis=0)
    # reverse_order = np.arange(frame)
    # np.random.shuffle(reverse_order)

    assert frame <= T, ' given frame length is smaller than tha data has :('

    # an evaluate function
    # using variance
    # max_change_score = -1
    # chosen_part_id = -1
    # data_s = np.sum(data, axis=3)
    # for part_id, part in enumerate(bodys):
    #     # change_score = sum(sum([np.var(data_s[:, :, joint - 1], axis=0) for joint in part]))
    #     change_score = sum([np.var(np.sum(data_s[:, :, joint - 1], axis=0), axis=0) for joint in part])
    #     # print(change_score)
    #     if change_score > max_change_score:
    #         # chosen_part = part
    #         chosen_part_id = part_id
    #         max_change_score = change_score
    #
    # # chosen_part_id = random.randint(0, 4)
    # # chosen_part_id = 1
    # assert chosen_part_id >= 0
    # chosen_part = bodys[chosen_part_id]
    chosen_part_id = random.randint(0, 4)
    chosen_part = bodys[chosen_part_id]

    trans = data.copy()
    chosen_part = [part - 1 for part in chosen_part]
    # shuffle_frames = np.arange(T)
    # shuffle_frames[:len(reverse_order)] = reverse_order
    for joint in chosen_part:
        # trans[:, :, joint] = data[:, shuffle_frames, joint]
        trans[:, :, joint] = 0

    return trans


def part_reverse_p(data, frame, p=0.5):
    if random.random() < p:
        C, T, V, M = data.shape
        trunk = [1, 2, 21, 3, 4]
        left_arm = [9, 10, 11, 12, 24, 25]
        right_arm = [5, 6, 7, 8, 22, 23]
        left_leg = [17, 18, 19, 20]
        right_leg = [13, 14, 15, 16]
        bodys = [trunk, left_arm, right_arm, left_leg, right_leg]

        reverse_order = np.flip(np.arange(frame), axis=0)
        # reverse_order = np.arange(frame)
        # np.random.shuffle(reverse_order)

        assert frame <= T, ' given frame length is smaller than tha data has :('

        # an evaluate function
        # using variance
        # max_change_score = -1
        # chosen_part_id = -1
        # data_s = np.sum(data, axis=3)
        # for part_id, part in enumerate(bodys):
        #     # change_score = sum(sum([np.var(data_s[:, :, joint - 1], axis=0) for joint in part]))
        #     change_score = sum([np.var(np.sum(data_s[:, :, joint - 1], axis=0), axis=0) for joint in part])
        #     # print(change_score)
        #     if change_score > max_change_score:
        #         # chosen_part = part
        #         chosen_part_id = part_id
        #         max_change_score = change_score
        #
        # # chosen_part_id = random.randint(0, 4)
        # # chosen_part_id = 1
        # assert chosen_part_id >= 0
        # chosen_part = bodys[chosen_part_id]
        chosen_part_id = random.randint(0, 4)
        chosen_part = bodys[chosen_part_id]

        trans = data.copy()
        chosen_part = [part - 1 for part in chosen_part]
        shuffle_frames = np.arange(T)
        shuffle_frames[:len(reverse_order)] = reverse_order
        for joint in chosen_part:
            trans[:, :, joint] = data[:, shuffle_frames, joint]
            # trans[:, :, joint] = 0

        return trans
    else:
        return data


def part_reverse_120(data, frame, p=0.5):
    if random.random() < p:
        C, T, V, M = data.shape
        trunk = [1, 2, 21, 3, 4]
        left_arm = [9, 10, 11, 12, 24, 25]
        right_arm = [5, 6, 7, 8, 22, 23]
        left_leg = [17, 18, 19, 20]
        right_leg = [13, 14, 15, 16]
        bodys = [trunk, left_arm, right_arm, left_leg, right_leg]

        # reverse_order = np.flip(np.arange(frame), axis=0)
        # reverse_order = np.arange(frame)
        # np.random.shuffle(reverse_order)

        assert frame <= T, ' given frame length is smaller than tha data has :('

        # an evaluate function
        # using variance
        # max_change_score = -1
        # chosen_part_id = -1
        # data_s = np.sum(data, axis=3)
        # for part_id, part in enumerate(bodys):
        #     # change_score = sum(sum([np.var(data_s[:, :, joint - 1], axis=0) for joint in part]))
        #     change_score = sum([np.var(np.sum(data_s[:, :, joint - 1], axis=0), axis=0) for joint in part])
        #     # print(change_score)
        #     if change_score > max_change_score:
        #         # chosen_part = part
        #         chosen_part_id = part_id
        #         max_change_score = change_score
        #
        # # chosen_part_id = random.randint(0, 4)
        # # chosen_part_id = 1
        # assert chosen_part_id >= 0
        # chosen_part = bodys[chosen_part_id]
        chosen_part_id = random.randint(0, 4)
        chosen_part = bodys[chosen_part_id]

        trans = data.copy()
        chosen_part = [part - 1 for part in chosen_part]
        # shuffle_frames = np.arange(T)
        # shuffle_frames[:len(reverse_order)] = reverse_order
        for joint in chosen_part:
            # trans[:, :, joint] = data[:, shuffle_frames, joint]
            trans[:, :, joint] = 0

        return trans
    else:
        return data


def part_reverse_p_l(data, frame, p=0.5):
    C, T, V, M = data.shape
    trunk = [1, 2, 21, 3, 4]
    left_arm = [9, 10, 11, 12, 24, 25]
    right_arm = [5, 6, 7, 8, 22, 23]
    left_leg = [17, 18, 19, 20]
    right_leg = [13, 14, 15, 16]
    bodys = [trunk, left_arm, right_arm, left_leg, right_leg]

    reverse_order = np.flip(np.arange(frame), axis=0)

    assert frame <= T, ' given frame length is smaller than tha data has :('

    chosen_part_id = random.randint(0, 4)
    chosen_part = bodys[chosen_part_id]

    trans = data.copy()
    chosen_part = [part - 1 for part in chosen_part]
    shuffle_frames = np.arange(T)
    shuffle_frames[:len(reverse_order)] = reverse_order
    for joint in chosen_part:
        trans[:, :, joint] = data[:, shuffle_frames, joint]

    return trans, chosen_part_id

def shear(data_numpy, r=0.5):
    s1_list = [random.uniform(-r, r), random.uniform(-r, r), random.uniform(-r, r)]
    s2_list = [random.uniform(-r, r), random.uniform(-r, r), random.uniform(-r, r)]

    R = np.array([[1,          s1_list[0], s2_list[0]],
                  [s1_list[1], 1,          s2_list[1]],
                  [s1_list[2], s2_list[2], 1        ]])

    R = R.transpose()
    data_numpy = np.dot(data_numpy.transpose([1, 2, 3, 0]), R)
    data_numpy = data_numpy.transpose(3, 0, 1, 2)
    return data_numpy


def temperal_crop(data_numpy, temperal_padding_ratio=6):
    C, T, V, M = data_numpy.shape
    padding_len = T // temperal_padding_ratio
    frame_start = np.random.randint(0, padding_len * 2 + 1)
    data_numpy = np.concatenate((data_numpy[:, :padding_len][:, ::-1],
                                 data_numpy,
                                 data_numpy[:, -padding_len:][:, ::-1]),
                                axis=1)
    data_numpy = data_numpy[:, frame_start:frame_start + T]
    return data_numpy


def random_spatial_flip(seq, p=0.5):
    if random.random() < p:
        # Do the left-right transform C,T,V,M
        index = transform_order['ntu']
        trans_seq = seq[:, :, index, :]
        return trans_seq
    else:
        return seq


def random_time_flip(seq, p=0.5):
    T = seq.shape[1]
    if random.random() < p:
        time_range_order = [i for i in range(T)]
        time_range_reverse = list(reversed(time_range_order))
        return seq[:, time_range_reverse, :, :]
    else:
        return seq


def random_rotate(seq):
    def rotate(seq, axis, angle):
        # x
        if axis == 0:
            R = np.array([[1, 0, 0],
                              [0, cos(angle), sin(angle)],
                              [0, -sin(angle), cos(angle)]])
        # y
        if axis == 1:
            R = np.array([[cos(angle), 0, -sin(angle)],
                              [0, 1, 0],
                              [sin(angle), 0, cos(angle)]])

        # z
        if axis == 2:
            R = np.array([[cos(angle), sin(angle), 0],
                              [-sin(angle), cos(angle), 0],
                              [0, 0, 1]])
        R = R.T
        temp = np.matmul(seq, R)
        return temp

    new_seq = seq.copy()
    # C, T, V, M -> T, V, M, C
    new_seq = np.transpose(new_seq, (1, 2, 3, 0))
    total_axis = [0, 1, 2]
    main_axis = random.randint(0, 2)
    for axis in total_axis:
        if axis == main_axis:
            rotate_angle = random.uniform(0, 30)
            rotate_angle = math.radians(rotate_angle)
            new_seq = rotate(new_seq, axis, rotate_angle)
        else:
            rotate_angle = random.uniform(0, 1)
            rotate_angle = math.radians(rotate_angle)
            new_seq = rotate(new_seq, axis, rotate_angle)

    new_seq = np.transpose(new_seq, (3, 0, 1, 2))

    return new_seq


def gaus_noise(data_numpy, mean= 0, std=0.01, p=0.5):
    if random.random() < p:
        temp = data_numpy.copy()
        C, T, V, M = data_numpy.shape
        noise = np.random.normal(mean, std, size=(C, T, V, M))
        return temp + noise
    else:
        return data_numpy


def gaus_filter(data_numpy):
    g = GaussianBlurConv(3)
    return g(data_numpy)


class GaussianBlurConv(nn.Module):
    def __init__(self, channels=3, kernel = 15, sigma = [0.1, 2]):
        super(GaussianBlurConv, self).__init__()
        self.channels = channels
        self.kernel = kernel
        self.min_max_sigma = sigma
        radius = int(kernel / 2)
        self.kernel_index = np.arange(-radius, radius + 1)

    def __call__(self, x):
        sigma = random.uniform(self.min_max_sigma[0], self.min_max_sigma[1])
        blur_flter = np.exp(-np.power(self.kernel_index, 2.0) / (2.0 * np.power(sigma, 2.0)))
        kernel = torch.from_numpy(blur_flter).unsqueeze(0).unsqueeze(0)
        # kernel =  kernel.float()
        kernel = kernel.double()
        kernel = kernel.repeat(self.channels, 1, 1, 1) # (3,1,1,5)
        self.weight = nn.Parameter(data=kernel, requires_grad=False)

        prob = np.random.random_sample()
        x = torch.from_numpy(x)
        if prob < 0.5:
            x = x.permute(3,0,2,1) # M,C,V,T
            x = F.conv2d(x, self.weight, padding=(0, int((self.kernel - 1) / 2 )),   groups=self.channels)
            x = x.permute(1,-1,-2, 0) #C,T,V,M

        return x.numpy()

class Zero_out_axis(object):
    def __init__(self, axis = None):
        self.first_axis = axis


    def __call__(self, data_numpy):
        if self.first_axis != None:
            axis_next = self.first_axis
        else:
            axis_next = random.randint(0,2)

        temp = data_numpy.copy()
        C, T, V, M = data_numpy.shape
        x_new = np.zeros((T, V, M))
        temp[axis_next] = x_new
        return temp

def axis_mask(data_numpy, p=0.5):
    am = Zero_out_axis()
    if random.random() < p:
        return am(data_numpy)
    else:
        return data_numpy

if __name__ == '__main__':
    data_seq = np.ndarray((1, 5, 5, 2))
    print(data_seq)
    data_seq = temperal_crop(data_seq, temperal_padding_ratio=2)
    print(data_seq)

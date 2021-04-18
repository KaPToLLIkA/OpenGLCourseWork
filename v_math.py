from math import *


def normalize_vec3f(vec):
    x = sqrt(vec[0] * vec[0] + vec[1] * vec[1] + vec[2] * vec[2])
    vec1 = [vec[0] / x, vec[1] / x, vec[2] / x]
    return vec1


def mul_vec_3f(vec1, num):
    vec3 = [vec1[0] * num, vec1[1] * num, vec1[2] * num]
    return vec3


def add_vec_3f(vec1, vec2):
    vec3 = [vec1[0] + vec2[0], vec1[1] + vec2[1], vec1[2] + vec2[2]]
    return vec3


def sub_vec_3f(vec1, vec2):
    vec3 = [vec1[0] - vec2[0], vec1[1] - vec2[1], vec1[2] - vec2[2]]
    return vec3


def cross_vec3f(vec1, vec2):
    vec3 = [
        vec1[1] * vec2[2] - vec1[2] * vec2[1],
        vec1[2] * vec2[0] - vec1[0] * vec2[2],
        vec1[0] * vec2[1] - vec1[1] * vec2[0],
    ]
    return vec3

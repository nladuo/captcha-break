# -*- coding:utf-8 -*-
#!/usr/bin/env python3

"""

"""
from collections import namedtuple

Point = namedtuple('Point', ['x', 'y'])

import numpy as np

def has_tranversed_the_point(x, y, tranversed_points:list):
    for point in tranversed_points:
        if x == point.x and y == point.y:
            return True

    return False

def find_connection_area(now_point, image:np.array, area:list, tranversed_points:list):

    if now_point.x < 0 or now_point.x >= image.shape[1]\
        or now_point.y < 0 or now_point.y >= image.shape[0]:
        return

    if image[now_point.y][now_point.x] != 0: return

    if has_tranversed_the_point(now_point.x, now_point.y, tranversed_points):return

    area.append(now_point)
    tranversed_points.append(now_point)

    find_connection_area(Point(now_point.x, now_point.y-1), image, area, tranversed_points)  #上
    find_connection_area(Point(now_point.x, now_point.y+1), image, area, tranversed_points)   #下
    find_connection_area(Point(now_point.x-1, now_point.y), image, area, tranversed_points)   #左
    find_connection_area(Point(now_point.x+1, now_point.y), image, area, tranversed_points)   #右
    find_connection_area(Point(now_point.x-1, now_point.y-1), image, area, tranversed_points) #左上
    find_connection_area(Point(now_point.x-1, now_point.y+1), image, area, tranversed_points) #左下
    find_connection_area(Point(now_point.x+1, now_point.y-1), image, area, tranversed_points) #右上
    find_connection_area(Point(now_point.x+1, now_point.y+1), image, area, tranversed_points) #右下

class CaptchaUtils:

    def __init__(self):
        pass

    @classmethod
    def clear_peper_noise(self, image, max_adhesion_count):
        areas = []
        tranversed_points = []
        for i in range(image.shape[1]):
            for j in range(image.shape[0]):
                if image[j][i] == 0 and not has_tranversed_the_point(i, j, tranversed_points):
                    area = []
                    find_connection_area(Point(i, j), image, area, tranversed_points)
                    areas.append(area)

        # clean the noises
        for area in areas:
            if(len(area) <= max_adhesion_count):
                for point in area:
                    image[point.y][point.x] = 255

    @classmethod
    def vertical_project(self, image:np.array, splits:list):
        project = []
        for i in range(image.shape[1]):
            count = 0
            for j in range(1, image.shape[0]-1):
                if image[j][i] == 0:count += 1

            project.append(count)

        index = 0
        i = 1
        threshold = 1
        while index < 8 and i < 100:
            if (project[i] > threshold and project[i-1] <= threshold) \
                    or (project[i] <= threshold and project[i-1] > threshold):
                if(index % 2 == 1 and (i - splits[index-1]) <= 8 ):
                    i += 1
                    continue
                splits[index] = i
                index += 1

            i += 1

















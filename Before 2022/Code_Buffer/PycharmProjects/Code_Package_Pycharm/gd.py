# _*_ encoding:utf-8 _*_
__author__ = 'lifan'
__date__ = '23/01/2018 13:00'


# Grient descent -- python
# y = mx + b
# m is slope, b is y-intercept


def computeErrorForGivenPoints(b, m, points):
    totalError = 0
    for i in range(0, len(points)):
        totalError += (points[i].y - (m * points[i].x + b)) ** 2
    return totalError / float(len(points))


def stepGradient(b_current, m_current, points, leanringRate):
    b_gradient = 0
    m_gradient = 0
    N = float(len(points))
    for i in range(0, len(points)):
        b_gradient = -(2 / N) * (points[i].y - ((m_current * points[i].x) + b_current))
        m_gradient = -(2 / N) * (points[i].y - ((m_current * points[i].x) + b_current)) * points[i].x
    new_b = b_current - leanringRate * b_gradient
    new_m = m_current - leanringRate * m_gradient
    return [new_b, new_m]

# _*_ encoding:utf-8 _*_
__author__ = 'lifan'
__date__ = '29/09/2017 18:52'


def solve(n, i):
    if (i == 1):
        return (n + 7 - 1) % n
    else:
        return (solve(n - 1, i - 1) + 7) % n


if __name__ == '__main__':
    for i in range(1, 11):
        print(solve(10, i) + 1)

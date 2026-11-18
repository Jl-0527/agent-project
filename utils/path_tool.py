# encoding:utf-8
"""
为整个工程提供统一的绝对路径
"""

import os


def get_project_root() -> str:
    """
    获取工程所在的根目录
    :return: 字符串跟目录
    """
    # 当前文件的绝对路径
    current_file = os.path.abspath(__file__)
    # 当前文件的文件夹路径
    current_dir = os.path.dirname(current_file)
    # 工程根目录
    project_root = os.path.dirname(current_dir)

    return project_root


def get_abs_path(relative_path: str) -> str:
    project_root = get_project_root()
    # 相对路径，拼接项目绝对根路径
    return os.path.join(project_root, relative_path)


if __name__ == '__main__':
    print(get_abs_path("config/config.txt"))
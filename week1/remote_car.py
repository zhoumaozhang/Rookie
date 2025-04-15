


def remote_car(commands):
    """
    :param commands:字符串表示的一批遥控指令，仅由字符 G、L、R组成，长度范围[1,100]
    :return:小车最终所处位置的坐标
    """
    x_center = 0
    y_center = 0
    index = 0
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # 北 东 南 西
    for command in commands:
        if command == 'G':
            index = index % 4
            x_center += directions[index][0]
            y_center += directions[index][1]
        elif command == 'L':
            index -= 1
        elif command == 'R':
            index += 1
    return x_center, y_center

if __name__ == '__main__':
    commands = 'GG'
    print(remote_car(commands))
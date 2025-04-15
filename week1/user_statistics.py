

def user_statistics(logs):
    """
    :param logs: 首行一个正整数 num ，表示日志行数，范围为 [1,50000]。接下来 num 行字符串，每行字符串表示一条日志内容，每行字符串长度
    不超过150。 yyyy-mm-dd|client_ip|url|result
    :return:32个整数，以单空格分隔。第1个整数表示月活数，第 2-32 个整数分别表示当月1-31天的日活数。
    """
    # 定义ip规范化函数
    def normalize_ip(ip):
        return ".".join(str(int(part)) for part in ip.split("."))  # str转换成int去除前置0
    # 统计每天的有效ip
    ips_day = [set() for _ in range(31)]
    for log in logs:
        date, client_ip, url, result = log.split("|")
        # 筛选有效信息
        if url == "/login.do" and result == "success":
            day = int(date.split("-")[2]) - 1
            client_ip = normalize_ip(client_ip)
            ips_day[day].add(client_ip)
    # 汇总月有效ip
    ips_month = set().union(*ips_day)  # union合并多个集合, *为解包操作符
    return [len(ips_month)] + [len(ips_day[i]) for i in range(31)]


if __name__ == '__main__':
    logs = ['2020-02-01|192.168.218.218|/login.do|success', '2020-02-01|192.168.218.218|/login.do|success',
            '2020-02-01|192.168.210.210|/login.do|fail', '2020-02-02|192.168.210.210|/login.do|success',
            '2020-02-02|192.168.218.218|/login.do|success']
    print(user_statistics(logs))
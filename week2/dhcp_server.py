class Solution:
    """
    DHCP服务器的功能是为每一个MAC地址分配唯一的IP地址。现假设：分配的IP地址范围从 192.168.0.0 到 192.168.0.255共 256个可用地址。

    """
    def __init__(self):
        self.mac_to_ip = {}  # 当前活跃 MAC->IP
        self.ip_to_mac = {}  # 当前活跃 IP->MAC
        self.mac_history = {}  # 历史记录 MAC->IP
        self.released_ips = []  # 按升序维护的释放池
        self.next_ip = 0  # 下一个未使用IP (0~255)

    def print_ip(self, ip_num):
        print(f"192.168.0.{ip_num}")

    # 给mac分配ip
    def assign_ip(self, mac, ip):
        self.mac_to_ip[mac] = ip
        self.ip_to_mac[ip] = mac
        self.mac_history[mac] = ip

    def insert_sorted_released(self, ip):
        # 插入已释放 IP，保持升序
        idx = 0
        while idx < len(self.released_ips) and self.released_ips[idx] < ip:
            idx += 1
        self.released_ips.insert(idx, ip)

    def dhcp_server(self, mac_list):
        data_list = list()
        for value in mac_list:
            d_tmp = value.split('=')
            data_list.append({'action': d_tmp[0], 'mac_list': d_tmp[1]})
        for data in data_list:
            if data['action'] == "REQUEST":
                self.request(data['mac_list'])
            elif data['action'] == "RELEASE":
                self.release(data['mac_list'])

    def request(self, mac):
        """
        根据输入的MAC地址分配IP地址池中的IP地址
        :param mac:
        :return:
        1.IP已分配并未释放，直接返回对应已分配的IP地址。
        2.IP未分配并已释放，优先分配最近一次曾经为其分配过的IP地址。
        3.IP未分配并未曾释放，先在未使用过的IP中升序分配。
        4.IP未分配并未曾释放，且当前IP全部被使用过。升序分配已释放出来的IP地址。
        5.无法分配成功，则返回 NA。
        """
        # 1. 已经分配过
        if mac in self.mac_to_ip:
            self.print_ip(self.mac_to_ip[mac])
            return

        # 2. 优先尝试历史 IP
        if mac in self.mac_history:
            old_ip = self.mac_history[mac]
            # 曾分配过的ip当前未被使用则分配该ip
            if old_ip not in self.ip_to_mac:
                self.assign_ip(mac, old_ip)
                self.print_ip(old_ip)
                return

        # 3. 尝试分配未使用过的IP
        if self.next_ip < 256:
            ip = self.next_ip
            self.next_ip += 1
            self.assign_ip(mac, ip)
            self.print_ip(ip)
            return

        # 4. 尝试从释放池分配
        for i in range(len(self.released_ips)):
            ip = self.released_ips[i]
            # 跳过池子中正被使用的ip
            if ip not in self.ip_to_mac:
                self.assign_ip(mac, ip)
                self.print_ip(ip)
                self.released_ips.pop(i)
                return

        # 5. 所有IP都被占用
        print("NA")

    def release(self, mac):
        """
        根据输入的MAC地址释放已分配的IP地址
        :param mac:
        :return:如果申请释放的对应的IP地址已分配，则释放此IP地址。否则跳过。
        """
        if mac in self.mac_to_ip:
            ip = self.mac_to_ip.pop(mac)
            self.ip_to_mac.pop(ip)
            self.mac_history[mac] = ip
            if ip not in self.released_ips:
                self.insert_sorted_released(ip)
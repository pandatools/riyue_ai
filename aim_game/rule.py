import copy
import pprint


class NumberObj:
    def __init__(self):
        self.lists = None
        self.statistics = None
        self.max_tou = 5  #骰子的个数
        self.max_tou_number = 6  #骰子的最大面数
        self.tou_number_list = [i for i in range(1, self.max_tou_number + 1)]

    def init_statistics(self):
        '''
        {
            5: 0,
            4:0,
            3:0,
            2:0,
            1:0

        }
        '''
        tmp = {
        }
        for i in range(1, self.max_tou_number + 1):
            tmp[i] = 0
        return tmp

    @property
    def one_counts(self):
        return self.statistics[1]

    @property
    def two_counts(self):
        return self.statistics[2]

    @property
    def three_counts(self):
        return self.statistics[3]

    @property
    def four_counts(self):
        return self.statistics[4]

    @property
    def five_counts(self):
        return self.statistics[5]

    @property
    def six_counts(self):
        return self.statistics[6]

    @property
    def kuai_ting(self):
        """快艇"""
        if self.one_counts == 5 or self.two_counts == 5 \
                or self.three_counts == 5 or self.four_counts == 5 or self.five_counts == 5:
            return 1
        return 0

    @property
    def si_shai(self):
        """四骰同花"""
        if self.one_counts == 4 or self.two_counts == 4 \
                or self.three_counts == 4 or self.four_counts == 4 or self.five_counts == 4:
            return self.all_togather
        return 0

    @property
    def da_shun(self):
        """大顺"""
        if self.two_counts == 1 and self.three_counts == 1 and self.four_counts == 1 and self.five_counts == 1:
            return 1
        return 0

    @property
    def xiao_shun(self):
        """小顺"""
        if (self.three_counts >= 1 and self.four_counts >= 1) and \
                (
                        (self.one_counts >= 1 and self.two_counts >= 1) or \
                        (self.two_counts >= 1 and self.five_counts >= 1) or \
                        (self.five_counts >= 1 and self.six_counts >= 1)
                ):
            return 1
        return 0

    @property
    def three_two(self):
        """ 3+2 """
        is_three = 0
        is_two = 0
        if self.one_counts == 3 or self.two_counts == 3 or self.three_counts == 3 or self.four_counts == 3 or self.five_counts == 3 or self.six_counts == 3:
            is_three = 1
        if self.one_counts == 2 or self.two_counts == 2 or self.three_counts == 2 or self.four_counts == 2 or self.five_counts == 2 or self.six_counts == 2:
            is_two = 1
        return is_three * is_two * self.all_togather

    @property
    def all_togather(self):
        return sum(self.lists)
    def update_lists(self, lists):
        self.statistics = self.init_statistics()
        self.lists = copy.deepcopy(lists)
        for i in self.lists:
            if i not in self.tou_number_list:
                raise Exception('不符合规定')
            self.statistics[i] += 1

    def details(self):
        useful_info = {
            "1的个数": self.one_counts,
            "2的个数": self.two_counts,
            "3的个数": self.three_counts,
            "4的个数": self.four_counts,
            "5的个数": self.five_counts,
            "6的个数": self.six_counts,
            "四骰同花": self.si_shai,
            "3+2": self.three_two,
            "大顺": self.da_shun,
            "小顺": self.xiao_shun,
            "快艇": self.kuai_ting
        }
        pprint.pprint(useful_info)
        return useful_info


# info = NumberObj()
# tou = [1]
# info.update_lists(tou)
# info.details()

import random



class game:
    def __init__(self):
        self.temp = 0  #当前局数
        self.ways_sort = ['one_counts', 'two_counts', 'three_counts',
                     'four_counts', 'five_counts', 'six_counts',
                     'all_togather', 'kuai_ting', 'three_two',
                     'da_shun', 'xiao_shun', 'si_shai']
        self.ways = {}
        self.score_dicts = {
            'one_counts': 1,
            'two_counts': 2,
            'three_counts': 3,
            'four_counts': 4,
            'five_counts': 5,
            'six_counts': 6,
            'all_togather': 1,
            'kuai_ting': 50,
            'three_two': 1,
            'da_shun': 30,
            'xiao_shun': 15,
            'si_shai': 1
        }
        self.history = None


    def game_init(self):
        self.history = []
        self.ways = {key:None for key in self.ways_sort}
        self.temp = 0
    @property
    def running(self):
        "是否继续游戏"
        if self.temp >= 12:
            return False
        else:
            return True

    def start_a_round(self):
        self.temp += 1

    def roll(self, number):
        return [random.randint(1, 6) for _ in range(number)]

    def best_score(self,obj,tou_list):
        """ obj  rule对象 """
        obj.update_lists(tou_list)
        best_way = None

        max_score = -1
        for key,value in self.ways.items():
            if value != None:
                continue
            count_value = getattr(obj, key) * self.score_dicts[key]
            if count_value > max_score:
                max_score = count_value
                best_way = key
        self.ways[best_way] = max_score
        return max_score,best_way

    def apply_action(self,tou_list,way,obj):
        obj.update_lists(tou_list)
        count_value = getattr(obj, way) * self.score_dicts[way]
        self.ways[way] = count_value
        self.temp += 1
        return count_value
    def store(self,best_way,max_score,touzi):
        self.history.append(tuple([best_way, max_score, touzi]))

    @property
    def total_score(self):
        all_sums = 0
        number_sums = 0
        for way,score,_ in self.history:
            all_sums += score
            if 'counts' in way:
                number_sums += score
        if number_sums >= 63:
            all_sums += 35
        return all_sums

    @property
    def remain_rounds(self):
        return 12-self.temp

    @property
    def game_state(self):
        res = []
        for w in self.ways_sort:
            value = self.ways[w] or 0
            res.append(value)
        return res




if __name__ == '__main__':
    from aim_game.rule import NumberObj
    import time
    p = game()
    start =time.time()
    for i in range(10000):
        obj = NumberObj()
        # print(p.best_score(obj,[1,2,1,2,1]))
    print(time.time() - start)

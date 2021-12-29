import collections


class OpponentModel:
    def __init__(self, factor, n):
        self.bidHistory = list()
        self.frequency = list()
        self.weights = [1/n]*n
        self.factor = factor

    def initial_Frequency(self):
        self.frequency = list()
        map1 = collections.defaultdict(int)
        for i in range(-100, 101):
            map1[i] = 1
        self.frequency.append(map1)
        map2 = collections.defaultdict(int)
        for i in range(100):
            map2[i] = 1
        self.frequency.append(map2)


    def update_Model(self, offer):
        self.update_Frequency(offer)
        self.update_weight(offer)
        self.bidHistory.append(offer)

    def update_Frequency(self,offer):
        for i in range(len(offer)):
            self.frequency[i][offer[i]] += 1

    def update_weight(self, offer):
        if not self.bidHistory:
            return
        pre_offer = self.bidHistory[-1]
        total_weight = 1
        for i in range(len(offer)):
            if pre_offer[i] == offer[i]:
                self.weights[i] += self.factor
                total_weight += self.factor
        self.weights = [w/total_weight for w in self.weights]

    def calculate(self, offer):
        sum = 0

        for i in range(len(offer)):
            max = self.findMax(i)
            sum += self.frequency[i][offer[i]] / max * self.weights[i]
        return sum

    def findMax(self, i):
        max = 0
        for key in self.frequency[i]:
            if self.frequency[i][key] > max:
                max = self.frequency[i][key]
        return max

o = OpponentModel(1, 2)
o.initial_Frequency()
o.update_Model((50, 50))
# print(o.weights)
o.update_Model((50, 51))
# print(o.weights)
# print(o.calculate((50, 49)))




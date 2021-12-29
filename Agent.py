import random
from collections import defaultdict
from Offer import Offer
from Opponent import OpponentModel
class Agent:
    def __init__(self, w1, w2, id, reservation, capacity, efficiency , window, volume=0, time=0):
        self.space = list()
        self.space_utility = defaultdict(float)
        self.w1 = w1
        self.w2 = w2
        self.id = id
        self.volume = volume
        self.time = time
        self.aspirational_utility = 0
        self.reservation = reservation
        self.capacity = capacity
        self.efficiency = efficiency
        if self.id == 2:
            self.volume = -volume
        self.load_dem = list()
        self.load_dem_res = [0]*100
        self.x = [0]*100
        self.pb = [0]*100
        self.exchange = defaultdict(list)
        self.opponent = OpponentModel(1, 2)
        self.opponent.initial_Frequency()
        self.window = window
        return

    def generate_contract_space(self, domain, t):
        self.space = list()
        self.space_utility = defaultdict(float)
        for (o1,o2) in domain:
            offer = (o1, o2)
            utility = self.calculate_utility(offer, t)
            self.space.append((utility, offer))
            self.space_utility[offer] = utility
        print(self.space)
        self.space.sort()
        print(self.space)
        return

    def make_offer(self, t):
        utility, offer  = self.space.pop()
        if utility < self.aspirational_utility:
            return None
        return offer

    def make_offer_opponent(self, t):
        _, offer = self.space[-1]
        max_o_u = self.opponent.calculate(offer)
        max_i = len(self.space)-1
        for i in range(len(self.space)-2, max(0, len(self.space)-self.window-1),-1):
            _, offer_iter = self.space[i]
            ut = self.opponent.calculate(offer_iter)
            if ut > max_o_u:
                max_o_u = ut
                max_i = i
        self.space[-1], self.space[max_i] = self.space[max_i], self.space[-1]
        utility, offer = self.space.pop()
        if utility < self.aspirational_utility:
            return None
        return offer


    def accept_offer(self, offer, t):
        u = self.space_utility[offer]
        response = False
        if u> self.aspirational_utility:
            response = True
        return response

    def accept_offer_opponent(self, offer, t):
        self.opponent.update_Model(offer)
        u = self.space_utility[offer]
        response = False
        if u> self.aspirational_utility:
            response = True
        return response

    def implement_agreed_contract(self, offer, t):
        return

    def implement_reserve_plan(self, t):
        return

    def calculate_utility(self, offer, t):
        load = self.get_predicted_load(t)
        scenarios = self.generate_scenarios(load, t)
        scenarios_with_offer = self.amend_scenarios(scenarios, offer, t)
        e1 = self.evalC1(scenarios_with_offer)
        e2 = self.evalC2(scenarios_with_offer)
        utilities= self.w1*e1 + self.w2*e2
        return utilities

    def get_predicted_load(self, t):
        return

    def generate_scenarios(self, load, t):
        return []

    def amend_scenarios(self, scenarios, offer, t):
        return []

    def evalC1(self, s_offer):
        return 1.0

    def evalC2(self, s_offer):
        return 1.0

    def generate_contract_space_2(self, domain):
        self.space = list()
        self.space_utility = defaultdict(float)
        for (o1, o2) in domain:
            offer = (o1, o2)
            utility = self.calculate_utility_2(offer)
            self.space.append((utility, offer))
            self.space_utility[offer] = utility
        self.space.sort()
        #print(self.space)
        leng = len(self.space)
        index = int(0.8*leng)
        self.aspirational_utility = self.space[index][0]
        #print(self.aspirational_utility)

    def calculate_utility_2(self, offer):
        e1 = self.evalC1_2(offer)
        e2 = self.evalC2_2(offer)
        return self.w1*e1 + self.w2*e2

    def evalC1_2(self, offer):
        v = offer[0]
        # print("1")
        # print(1/(abs(v-self.volume)+1))
        return 100/(abs(v-self.volume)+100)

    def evalC2_2(self, offer):
        t = offer[1]
        # print("2")
        # print(1/(abs(t-self.time)+1))
        return 100/(abs(t-self.time)+100)

    def generate_net_demand(self):
        self.load_dem = list()
        rang = [i/10 for i in range(-15, 10)]
        for i in range(100):
            self.load_dem.append(random.choice(rang))



class Buyer:
    def __init__(self, wc, wq, requires, minQ, minP, cg, epsi, fis, pt):
        self.wc = wc
        self.wq = wq
        self.requires = requires
        self.minQ = minQ
        self.minP = minP
        self.cg = cg
        self.epsi = epsi
        self.fis = fis
        self.space = list()
        self.threshold = 0
        self.pt = pt

    def generate_contract_space(self, domain):
        self.space = list()
        for offer in domain:
            u = self.utilities(offer)
            self.space.append((u, offer))
        self.space.sort(key=lambda x: x[0])
        self.threshold = min(self.utilities(Offer([0]*4,[self.pt]*4)),
                             self.utilities(Offer(self.requires,[self.pt]*4)))



    def make_offer(self):
        if not self.space:
            return None
        _, o = self.space.pop()
        return o

    def accept(self,offer):
        if self.utilities(offer) >= self.threshold:
            return True
        return False

    def utilities(self, offer):
        c = self.total_cost(offer)
        f = self.quantities(offer)
        return self.wc*c + self.wq*f

    def total_cost(self, offer):
        sum1 = 0
        sum2 = 0
        for i in range(4):
            # print(offer.qs)
            # print(offer.ps)
            sum1 += self.requires[i] * self.cg[i] - offer.qs[i] * offer.ps[i]
            sum2 += self.requires[i] * self.cg[i] - self.minP[i] * self.minQ[i]
        return sum1/sum2

    def quantities(self, offer):
        wNs = list()
        for i in range(4):
            wN = self.requires[i]/max(self.requires) + 0
            wNs.append(wN)
        f = 0
        for i in range(4):
            fq = 0
            if offer.qs[i] <= self.requires[i] + self.fis[i]:
                fq = (min(offer.qs[i], self.requires[i]) + self.epsi)/(self.requires[i]+self.epsi)
            wN = wNs[i]/sum(wNs)
            f += fq*wN
        return f

class Seller:
    def __init__(self, require, mc, pt, der):
        self.require = require
        self.der = der
        self.available = [x-y for (x,y) in zip(der,require)]
        self.mc = mc
        self.feasible = list()
        self.space = list()
        self.threshold = 0
        self.pt = pt

    def make_offer(self):
        if not self.space:
            return None
        _, o = self.space.pop()
        return o

    def accept(self, offer):
        u = self.utility(offer)
        if u >= self.threshold:
            return True
        return False

    def generate_contract_space(self):
        print("generate_contract_space")
        print(len(self.feasible))
        self.space = list()
        i = 0
        for offer in self.feasible:
            print(i)
            i += 1
            u = self.utility(offer)
            self.space.append((u, offer))
        self.space.sort(key=lambda x: x[0])
        self.threshold = self.utility(Offer([0]*4, [self.pt]*4))

    def utility(self, offer):
        if offer not in self.feasible:
            return -1
        maxqa = float('-inf')
        minqn = float('inf')
        for offer in self.feasible:
            sum1 = 0
            sum2 = 0
            for i in range(4):
                sum1 += offer.qs[i] * offer.ps[i]
                sum2 += offer.qs[i] * self.mc[i]
            maxqa = max(maxqa, sum1)
            minqn = min(minqn, sum2)
        maxci = maxqa - minqn
        r = 0
        for i in range(4):
            r+= offer.qs[i] * offer.ps[i] - offer.qs[i]*self.mc[i]
        return r/maxci

    def removeUnfeasible(self,all_offers,soc_max, soc_init, g_max):
        print("feasiable")
        self.feasible = list()
        for offer in all_offers:
            soc = soc_init
            flag = True
            for i in range(4):
                soc = min(soc+self.der[i]+g_max-self.require[i], soc_max)
                if soc < offer.qs[i]:
                    flag = False
                    break
            if flag:
                self.feasible.append(offer)







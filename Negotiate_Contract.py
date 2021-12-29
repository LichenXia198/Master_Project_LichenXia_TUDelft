from Agent import Agent
import csv
import time

class NegotiateContract:
    def __init__(self):
        return

    def negotiate(self, deadline, windowSize):
        domain = self.generate_domain()
        agent1 = Agent(0.5, 0.5, 1, 0, 0, 0, windowSize ,volume= 40, time=40)
        agent2 = Agent(0.5, 0.5, 2, 0, 0, 0, windowSize ,volume=-70, time=70)
        agent1.generate_contract_space_2(domain)
        agent2.generate_contract_space_2(domain)
        r = 1
        offeraccepted = False

        result = list()
        while r < deadline:
            d = dict()
            d['round'] = r
            if r%2 == 0:
                d['agent1'] = 1
                d['agent2'] = 0
                offer = agent1.make_offer_opponent(0)
                if offer:
                    #print(offer)
                    offeraccepted = agent2.accept_offer_opponent(offer, 0)
                    if offeraccepted:
                        break
            else:
                d['agent1'] = 0
                d['agent2'] = 1
                offer = agent2.make_offer_opponent(0)
                if offer:
                    #print(offer)
                    offeraccepted = agent1.accept_offer_opponent(offer, 0)
                    if offeraccepted:
                        break
            if offer:
                d['utility1'] = agent1.calculate_utility_2(offer)
                d['utility2'] = agent2.calculate_utility_2(offer)
            result.append(d)
            r+=1
        print(r)
        maxo = domain[0]
        maxu = agent1.calculate_utility_2(maxo)*agent2.calculate_utility_2(maxo)
        for i_offer in domain:
            u = agent1.calculate_utility_2(i_offer)*agent2.calculate_utility_2(i_offer)
            if u > maxu:
                maxu = u
                maxo = i_offer
        print(maxu)
        print(maxo)
        distance = 0
        finalnashProduct = 0
        u1 = 0
        u2 = 0

        if offeraccepted:
            print("accepted")
            u1 = agent1.calculate_utility_2(offer)
            u2 = agent2.calculate_utility_2(offer)
            finalnashProduct = u1*u2
            distance = abs(maxu-finalnashProduct)
            print(finalnashProduct)
            print(offer)
            agent1.implement_agreed_contract(offer,0)
            agent2.implement_agreed_contract(offer,0)
        else:
            agent1.implement_reserve_plan(0)
            agent2.implement_reserve_plan(0)
        # with open('negotiation_O_w_0.5_0.5_0.5_0.5_window1000_40_40_-70_70.csv', mode='w') as negotiation:
        #     fieldnames = ['round', 'utility1', 'utility2','agent1', 'agent2']
        #     writer = csv.DictWriter(negotiation, fieldnames=fieldnames)
        #     writer.writeheader()
        #     for row in result:
        #         writer.writerow(row)
        return offeraccepted, finalnashProduct,distance,r, u1, u2

    def generate_domain(self):
        vols = [i for i in range(-100, 101)]
        times = [i for i in range(100)]
        domain = list()
        for i in range(len(vols)):
            for j in range(len(times)):
                domain.append((vols[i], times[j]))
        return domain

with open('negotiation_time_with_windowSize_and_nashProduct_little_match_preference(40).csv', mode='w') as negotiation:
    fieldnames = ['windowSize', 'time', 'nashProduct','distance','round','u1','u2']
    writer = csv.DictWriter(negotiation, fieldnames=fieldnames)
    writer.writeheader()
    for w in range(0, 3001, 100):
        d = dict()
        nego = NegotiateContract()
        start = time.time()
        offeraccepted, finalnashProduct,distance, r ,u1, u2= nego.negotiate(5000,w)
        end = time.time()
        d['windowSize'] = w
        d['time'] = end-start
        d['nashProduct'] = finalnashProduct
        d['distance'] = distance
        d['round'] = r
        d['u1'] = u1
        d['u2'] = u2
        writer.writerow(d)
        print(offeraccepted)
# nego = NegotiateContract()
# success = nego.negotiate(5000)
# print(success)



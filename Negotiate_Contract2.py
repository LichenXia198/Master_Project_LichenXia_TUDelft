from Agent import Agent, Buyer, Seller
from Offer import Offer

class NegotiateContract:
    def __init__(self):
        return

    def negotiate(self, deadline):
        domain = self.generate_domain()
        buyer = Buyer( 0.5, 0.5, [0.25,0.25,0,1], [0.01]*4, [0.01]*4, [1.5]*4, 0.0001, [0.1]*4, 1.2)
        seller = Seller([0.65, 0.86, 0.443, 1.4], [0.001]*4, [0.5]*4, [0, 2, 2,5, 0])
        buyer.generate_contract_space(domain)
        seller.removeUnfeasible(domain,2.8,2.8,0)
        seller.generate_contract_space()
        r = 0
        offeraccepted = False
        while r < deadline:
            print(r)
            if r%2 == 0:
                offer = seller.make_offer()
                if offer:
                    #print(offer)
                    offeraccepted = seller.accept(offer)
                    if offeraccepted:
                        break
            else:
                offer = buyer.make_offer()
                if offer:
                    #print(offer)
                    offeraccepted = buyer.accept(offer, 0)
                    if offeraccepted:
                        break
            r+=1
        print(r)
        return offeraccepted

    def generate_domain(self):
        quantities = [i/100 for i in range(1, 100, 10)]
        prices = [i/100 for i in range(1, 100, 5)]
        domain = list()
        for i in range(len(quantities)):
            for j in range(len(quantities)):
                for x in range(len(quantities)):
                    for y in range(len(quantities)):
                        for z in range(len(prices)):
                            domain.append(
                                Offer([quantities[i], quantities[j], quantities[x],quantities[y]],
                            [prices[z]]*4))
        return domain


nego = NegotiateContract()
success = nego.negotiate(500)
print(success)

from .models import MarketInstance



class MarketScheduler(object):

    def __init__(self,market_id):
        self.market_id = market_id
    
    def schedulemarket(self):
        from time import sleep
        sleep(5)
        MarketInstance.objects.filter(id = self.market_id).update(is_active= True)
        MarketInstance.objects.filter(id = self.market_id).update(betaccept= True)
        print( 'Betting Session Begin')
        sleep(10)
        MarketInstance.objects.filter(id = self.market_id).update(betaccept= False)
        print( 'Betting Session Ends')
        print('Wheel Spinning')

        sleep(10)
        print('Wheel Spinning Stop and Outcome presents'

        MarketInstance.objects.filter(id = self.market_id).update(is_active= False)
        MarketInstance.objects.filter(id = self.market_id).update(betaccept= False)


while True:
    m1 = MarketScheduler(1)
    m1.schedulemarket()
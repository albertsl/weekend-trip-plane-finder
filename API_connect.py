class API_connect:
    def __init__(mkt, cur, loc):
        self.market = mkt
        self.currency = cur
        self.locale = loc
        self.API_key = self.get_API_key()

    def get_API_key():
        API_file = open("API.txt",'r')
        API_key = API_file.read()
        API_key = API_key[:-1] #The txt file has a \n at the end.
        return API_key

    def where_to_go(weekend):
        pass

    def when_to_go(airport):
        pass

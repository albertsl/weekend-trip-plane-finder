import urllib2
import json

def getData(url):
    '''Returns the data that the Skyscanner API returns for a given URL'''
    response = urllib2.urlopen(url)
    data = response.read()
    return data

def readData(data):
    '''Returns a dictionary with the parsed data'''
    JSONData = json.loads(data)
    return JSONData

class SkyScannerPlace:
    def __init__(self, PlaceName, CountryId, RegionId, PlaceId, CityId, CountryName):
        self.PlaceName = PlaceName
        self.CountryId = CountryId
        self.RegionId = RegionId
        self.PlaceId = PlaceId
        self.CityId = CityId
        self.CountryName = CountryName
    def printPlace(self):
        print self.PlaceName + ", " + self.CountryName
    def getPlaceId(self):
        return self.PlaceId

class SkyScannerFlight:
    def __init__(self, currency, price, carrierId, originId, destinationId, departureDate, quoteDateTime):
        self.currency = currency
        self.price = price
        self.carrierId = carrierId
        self.originId = originId
        self.destinationId = destinationId
        self.departureDate = departureDate
        self.quoteDateTime = quoteDateTime

class APIconnect:
    def __init__(self, mkt, cur, loc):
        self.market = mkt
        self.currency = cur
        self.locale = loc
        self.API_key = self.getAPIkey()

    def getAPIkey(self):
        API_file = open("API.txt",'r')
        API_key = API_file.read()
        API_key = API_key[:-1] #The txt file has a \n at the end.
        return API_key

    def getListOfPlaces(self, query):
        '''Returns a list of SkyScannerPlace objects for a given query '''
        url = "http://partners.api.skyscanner.net/apiservices/autosuggest/v1.0/{}/{}/{}/?query={}&apiKey={}".format(self.market, self.currency, self.locale, query, self.API_key)
        data = getData(url)
        dataDict = readData(data)

        placeList = []
        for item in dataDict['Places']:
            placeList.append(SkyScannerPlace(item['PlaceName'], item['CountryId'], item['RegionId'], item['PlaceId'], item['CityId'], item['CountryName']))
        return url

    #Still working from here till the end
    def getPlanes(self, origin, destination, departure_date):
        ''' Returns a list of SkyScannerFlight objects for the given trip conditions'''
        url = "http://partners.api.skyscanner.net/apiservices/browsequotes/v1.0/{}/{}/{}/{}/{}/{}/?apiKey={}".format(self.market, self.currency, self.locale, origin, destination, departure_date, self.API_key)
        data = getData(url)
        dataDict = readData(data)

        currency = dataDict['Currencies'][0]['Code']
        quoteList = []
        for item in dataDict['Quotes']:
            if item['Direct'] == True:
                quoteList.append(SkyScannerFlight(currency, item['MinPrice'], item['OutboundLeg']['CarrierIds'][0], item['OutboundLeg']['OriginId'], item['OutboundLeg']['DestinationId'], item['OutboundLeg']['DepartureDate'], item['QuoteDateTime']))
        return quoteList

    def whereToGo(self, origin, departure_date, return_date):
        self.getPlanes(origin, "anywhere", departure_date)
        # For every place on the list, get the return possibilities
        # self.getPlanes("", origin, return_date)
        #
        # url = "http://partners.api.skyscanner.net/apiservices/browsequotes/v1.0/{}/{}/{}/{}/{}/{}/{}?apiKey={}".format(self.market, self.currency, self.locale, origin, "anywhere", departure_date, return_date, self.API_key)
        # data = getData(url)
        # dataDict = readData(data)

        # currency = dataDict['Currencies'][0]['Code']
        # quoteList = []
        # for item in dataDict['Quotes']:
        #     quoteList.append((SkyScannerFlight(currency, ),
        #                         SkyScannerFlight(currency, ))
        # return quoteList

    def whenToGo(self, origin, destination):
        url = "http://partners.api.skyscanner.net/apiservices/browsequotes/v1.0/{}/{}/{}/{}/{}/{}/{}?apiKey={}".format(self.market, self.currency, self.locale, origin, destination, "anytime", "anytime", self.API_key)
        data = getData(url)
        dataDict = readData(data)
        return url

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
    def __init__(self, currency, price, carrierId, originId, destinationId, departureDate, quoteDateTime, direct):
        self.currency = currency
        self.price = price
        self.carrierId = carrierId
        self.originId = originId
        self.destinationId = destinationId
        self.departureDate = departureDate
        self.quoteDateTime = quoteDateTime
        self.direct = direct
    def __str__(self):
        return "goinig to {} for {} {}".format(self.originId, self.price, self.currency)
    def getOrigin(self):
        return self.originId

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

    def getFlights(self, origin, destination, departure_date):
        ''' Returns a list of SkyScannerFlight objects for the given trip conditions'''
        url = "http://partners.api.skyscanner.net/apiservices/browseroutes/v1.0/{}/{}/{}/{}/{}/{}/?apiKey={}".format(self.market, self.currency, self.locale, origin, destination, departure_date, self.API_key)
        data = getData(url)
        dataDict = readData(data)

        currency = dataDict['Currencies'][0]['Code']
        flightList = []
        for item in dataDict['Quotes']:
            flightList.append(SkyScannerFlight(currency, item['MinPrice'], item['OutboundLeg']['CarrierIds'][0], item['OutboundLeg']['OriginId'], item['OutboundLeg']['DestinationId'], item['OutboundLeg']['DepartureDate'], item['QuoteDateTime'], item['Direct']))
        return flightList

    #Still working from here till the end
    def whereToGo(self, origin, departure_date, return_date):
        flightList = self.getFlights(origin, "anywhere", departure_date)
        for flight in flightList:
            print flight
        # For every place on the list, get the return possibilities
        # self.getFlights("", origin, return_date)
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

'''
Browse Routes

Use Browse Routes to retrieve a list of destinations and prices. You can use 'anywhere' to get a list of countries, or you can specify a country or a city (using its Skyscanner code e.g. CDG for Paris Charles-de-Gaulle airport or LOND for London).

http://partners.api.skyscanner.net/apiservices/browseroutes/v1.0/GB/GBP/en-GB/US/anywhere/anytime/anytime?apiKey=<your_api_key>

http://partners.api.skyscanner.net/apiservices/browseroutes/v1.0/GB/GBP/en-GB/US/FR/2017-11/2017-12?apiKey=<your_api_key>



Browse Dates

Use Browse Dates to retrieve the cheapest prices to your selected destination (city or airport) for a given month (e.g. 2017-12) or for the next 12 months (anytime).

http://partners.api.skyscanner.net/apiservices/browsedates/v1.0/GB/GBP/en-GB/US/LHR/SIN/anytime/anytime?apiKey=<your_api_key>

If you want the response to be formatted in a way that is easy to display as a calendar you can use Browse Grid.

http://partners.api.skyscanner.net/apiservices/browsegrid/v1.0/GB/GBP/en-GB/US/LHR/SIN/2017-12/2017-12?apiKey=<your_api_key>



Browse Quotes

Use Browse Quotes if you don't need the Routes or Dates built for you and just need the individual quotes.

http://partners.api.skyscanner.net/apiservices/browsequotes/v1.0/GB/GBP/en-GB/US/CDG/EDI/2017-12-12/2017-12-20?apiKey=<your_api_key>

http://en.business.skyscanner.net/dev-guidelines-api
'''

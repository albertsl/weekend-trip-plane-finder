import urllib2
import json

PRICE_LIMIT = 100

def getData(url):
    '''Returns the data that the Skyscanner API returns for a given URL'''
    response = urllib2.urlopen(url)
    data = response.read()
    return data

def readData(data):
    '''Returns a dictionary with the parsed data'''
    JSONData = json.loads(data)
    return JSONData

def lowCostFlights(flightList):
    '''From a given list of SkyScannerFlight object, gets rid of the ones that don't fit my low cost criteria'''
    newFlightList = []
    for flight in flightList:
        if flight.direct == True and (flight.currency == "EUR" and flight.price < PRICE_LIMIT):
            newFlightList.append(flight)
    return newFlightList

def getSkyScannerCodeFromRnid(dataDict, rnid):
    for place in dataDict['Places']:
        if place['PlaceId'] == rnid:
            return place['SkyscannerCode']

def getCitySkyScannerCodeFromPlaceSkyScannerCode(placeSkyScannerCode, APIconnection):
    '''Given an airport code, it returns the city code'''
    placeList = APIconnection.getListOfPlaces(placeSkyScannerCode)
    for item in placeList:
        if item.getPlaceSkyScannerCode == placeSkyScannerCode:
            return item.getCitySkyScannerCode()

def getPlaceNameFromPlaceSkyScannerCode(placeSkyScannerCode, APIconnection):
    '''Given an airport code, it returns the place name'''
    placeSkyScannerCode = placeSkyScannerCode + '-sky'
    placeList = APIconnection.getListOfPlaces(placeSkyScannerCode)
    for item in placeList:
        if item.getPlaceSkyScannerCode() == placeSkyScannerCode:
            return item.getPlaceName()

def parsePossibilityList(possibilityList):
    '''Given a possibility list with tuples like (city_name, price) returns only the lowest prices'''
    d = {}
    for item in possibilityList:
        if item[0] not in d:
            d[item[0]] = item[1]
        else:
            if d[item[0]] > item[1]:
                d[item[0]] = item[1]
    return d.items()

class SkyScannerPlace:
    def __init__(self, PlaceName, CountryId, RegionId, PlaceId, CityId, CountryName):
        #ToDo: Check if PlaceId is Rnid or SkyScannerCode
        self.placeName = PlaceName
        self.countrySkyScannerCode = CountryId
        self.regionId = RegionId
        self.placeSkyScannerCode = PlaceId
        self.citySkyScannerCode = CityId
        self.countryName = CountryName
    def __str__(self):
        print self.PlaceName + ", " + self.CountryName
    def getPlaceSkyScannerCode(self):
        return self.placeSkyScannerCode
    def getCitySkyScannerCode(self):
        return self.citySkyScannerCode
    def getPlaceName(self):
        return self.placeName

class SkyScannerFlight:
    def __init__(self, currency, price, carrierId, originId, destinationId, originSkyScannerCode, destinationSkyScannerCode, departureDate, quoteDateTime, direct):
        self.currency = currency
        self.price = price
        self.carrierId = carrierId
        self.originId = originId
        self.destinationId = destinationId
        self.originSkyScannerCode = originSkyScannerCode
        self.destinationSkyScannerCode = destinationSkyScannerCode
        self.departureDate = departureDate
        self.quoteDateTime = quoteDateTime
        self.direct = direct
    def __str__(self):
        return "going from {} to {} for {} {}".format(self.getOrigin(), self.getDestination(), self.getPrice(), self.getCurrency())
    def getOrigin(self):
        return self.originSkyScannerCode
    def getDestination(self):
        return self.destinationSkyScannerCode
    def getPrice(self):
        return self.price
    def getCurrency(self):
        return self.currency

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

    def getListOfPlaces(self, query, getUrl=False):
        '''Returns a list of SkyScannerPlace objects for a given query '''
        url = "http://partners.api.skyscanner.net/apiservices/autosuggest/v1.0/{}/{}/{}/?query={}&apiKey={}".format(self.market, self.currency, self.locale, query, self.API_key)
        data = getData(url)
        dataDict = readData(data)

        placeList = []
        for item in dataDict['Places']:
            placeList.append(SkyScannerPlace(item['PlaceName'], item['CountryId'], item['RegionId'], item['PlaceId'], item['CityId'], item['CountryName']))
        if getUrl:
            return placeList, url
        else:
            return placeList

    def getFlights(self, origin, destination, departure_date, getUrl = False):
        ''' Returns a list of SkyScannerFlight objects for the given trip conditions'''
        url = "http://partners.api.skyscanner.net/apiservices/browseroutes/v1.0/{}/{}/{}/{}/{}/{}/?apiKey={}".format(self.market, self.currency, self.locale, origin, destination, departure_date, self.API_key)
        data = getData(url)
        dataDict = readData(data)

        currency = dataDict['Currencies'][0]['Code']
        flightList = []
        for item in dataDict['Quotes']:
            try:
                originId = item['OutboundLeg']['OriginId']
                destinationId = item['OutboundLeg']['DestinationId']
                originSkyScannerCode = getSkyScannerCodeFromRnid(dataDict, originId)
                destinationSkyScannerCode = getSkyScannerCodeFromRnid(dataDict, destinationId)
                flightList.append(SkyScannerFlight(currency, item['MinPrice'], item['OutboundLeg']['CarrierIds'][0], originId, destinationId, originSkyScannerCode, destinationSkyScannerCode, item['OutboundLeg']['DepartureDate'], item['QuoteDateTime'], item['Direct']))
            except:
                print "There was an error in the getFlights function while processing the query:"
                print item
        if getUrl:
            return flightList, url
        else:
            return flightList

    #Still working from here till the end
    def whereToGo(self, origin, departure_date, return_date, low_cost=True):
        possibilities = []

        flightList = self.getFlights(origin, "anywhere", departure_date)
        if low_cost:
            flightList = lowCostFlights(flightList)

        CheckedDestinationsList = []
        for flight in flightList:
            if flight.getDestination() not in CheckedDestinationsList:
                CheckedDestinationsList.append(flight.getDestination())
                flightList2 = self.getFlights(flight.getDestination(), origin, return_date)
                if low_cost:
                    flightList2 = lowCostFlights(flightList2)
                if flightList2 != []:
                    for flight2 in flightList2:
                        price1 = flight.getPrice()
                        price2 = flight2.getPrice()
                        combinedPrice = price1 + price2
                        if combinedPrice < PRICE_LIMIT and flight.getCurrency() == "EUR":
                            possibilities.append((getPlaceNameFromPlaceSkyScannerCode(flight2.getOrigin(), self), combinedPrice))
        return parsePossibilityList(possibilities)

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

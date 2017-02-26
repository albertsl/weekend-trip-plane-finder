import APIconnect

#Then decide from which airports you want to fly and at what times
departure_airport1 = ["BCN-sky","GRO-sky"]
departure_time1 = ["Friday night", "Saturday Morning"]
arrival_airport1 = ["Any"]
arrival_time1 = ["Any"]
departure_airport2 = arrival_airport1
departure_time2 = ["Sunday afternoon or later"]
arrival_airport2 = ["BCN-sky", "GRO-sky"]
arrival_time2 = ["Sunday night"]

APIconnection = APIconnect.APIconnect("ES", "EUR", "es-ES")
# print APIconnection.getListOfPlaces("Mallorca",True)
# print APIconnection.getFlights("BCN-sky", "CRA-sky", "2017-03-11", True)[1]
# print APIconnection.getFlights("CRA-sky", "BCN-sky", "2017-03-12", True)[1]
# print APIconnection.getFlights("CRA-sky", "BCN-sky", "2017-03-12", True)[1]
#print APIconnection.getFlights("BCN-sky", "anywhere", "2017-03-11", True)
# print APIconnection.whereToGo("BCN-sky", "2017-03-11", "2017-03-12")
# print APIconnection.whenToGo("BCN-sky", "LOND-sky")

def planesForTheWeekend(friday, departureCityList):
    APIconnection = APIconnect.APIconnect("ES", "EUR", "es-ES")
    possibilityList = []
    fridaySplit = friday.split("-")
    fridaySplit[-1] = str(int(fridaySplit[-1])+1).zfill(2)
    saturday = '-'.join(fridaySplit)
    fridaySplit[-1] = str(int(fridaySplit[-1])+1).zfill(2)
    sunday = '-'.join(fridaySplit)

    for city in departureCityList:
        possibilityList += APIconnection.whereToGo(city, friday, sunday)
        possibilityList += APIconnection.whereToGo(city, friday, saturday)
        possibilityList += APIconnection.whereToGo(city, saturday, sunday)

    return APIconnect.parsePossibilityList(possibilityList)

print planesForTheWeekend("2017-05-06", ["BCN-sky","GRO-sky"])

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
# print APIconnection.getListOfPlaces("Barce")
print APIconnection.getPlanes("BCN-sky", "LOND-sky", "2017-03-11")
# print APIconnection.whereToGo("BCN-sky", "2017-03-11", "2017-03-12")
# print APIconnection.whenToGo("BCN-sky", "LOND-sky")

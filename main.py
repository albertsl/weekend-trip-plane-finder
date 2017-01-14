#First connect to Skyscanner API
API_file = open("API.txt",'r')
API_key = API_file.read()
API_key = API_key[:-1]

#Then decide from which airports you want to fly and at what times
departure_airport1 = ["BCN","GRO"]
departure_time1 = ["Friday night", "Saturday Morning"]
arrival_airport1 = ["Any"]
arrival_time1 = ["Any"]
departure_airport2 = arrival_airport1
departure_time2 = ["Sunday afternoon or later"]
arrival_airport2 = ["BCN", "GRO"]
arrival_time2 = ["Sunday night"]

#On every request you must specify country and currency and language http://partners.api.skyscanner.net/apiservices/carhire/v2/pricing/{market}/{currency}/{locale}/...

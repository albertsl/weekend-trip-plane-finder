import API_connect

#Then decide from which airports you want to fly and at what times
departure_airport1 = ["BCN","GRO"]
departure_time1 = ["Friday night", "Saturday Morning"]
arrival_airport1 = ["Any"]
arrival_time1 = ["Any"]
departure_airport2 = arrival_airport1
departure_time2 = ["Sunday afternoon or later"]
arrival_airport2 = ["BCN", "GRO"]
arrival_time2 = ["Sunday night"]

API_connect("ES", "EUR", "es-ES")

http://partners.api.skyscanner.net/apiservices/browsequotes/v1.0/ES/EUR/es-ES/{originPlace}/{destinationPlace}/{outboundPartialDate}/{inboundPartialDate}?apiKey={apiKey}

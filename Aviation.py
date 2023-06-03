from flight import *
from airport import *

class Aviation:
    def __init__(self):
        self._allAirports = {}  #container to store all Airports
        self._allFlights = {}  #container to store all Flights
        self._allCountries = {}  #container to store all countries
  
    def getAllAirports(self):
        return self._allAirports
    
    def getAllFlights(self):
        return self._allFlights
    
    def getAllCountries(self):
        return self._allCountries
    
    def setAllAirports(self, airports):
        self._allAirports = airports

    def setAllFlights(self, flights):
        self._allFlights = flights
    
    def setAllCountries(self, countries):
        self._allCountries = countries

    def loadData(self, airportFile, flightFile, countriesFile):
        self.__init__()
        try:
            f = open(countriesFile, "r", encoding='utf8')
            for line in f:
                line = line.strip()
                parts = line.split(',')
                self._allCountries[parts[0].strip()] = parts[1].strip()
            f.close()

            f = open(airportFile, "r", encoding='utf8')
            for line in f:
                if line:
                    line = line.strip()
                    parts = line.split(',')
                    code = parts[0].strip()
                    city = parts[2].strip()
                    country = parts[1].strip()
                    cont = self._allCountries[country]
                    newAirport = Airport(code, city, country, cont)
                    self._allAirports[code] = newAirport
            f.close()

            f = open(flightFile, "r", encoding='utf8')
            for line in f:
                line = line.strip()
                parts = line.split(',')
                flightNo = parts[0].strip()
                orig = self._allAirports[parts[1].strip()]
                dest = self._allAirports[parts[2].strip()]
                newFlight = Flight(flightNo, orig, dest)
                if orig.getCode() in self._allFlights:
                    self._allFlights[orig.getCode()].append(newFlight)
                else:
                    self._allFlights[orig.getCode()] = [newFlight]
            f.close()    
        except Exception as e:
            return False
        return True
        
    def getAirportByCode(self, code):
        for airport in self._allAirports.values():
            if airport.getCode() == code:
                return airport
        return -1

    def findAllCityFlights(self, city):
        flights = []
        for flightList in self._allFlights.values():
            for flight in flightList:
                originAirport = self.getAirportByCode(flight.getOrigin().getCode())
                destinationAirport = self.getAirportByCode(flight.getDestination().getCode())
                if originAirport.getCity() == city or destinationAirport.getCity() == city:
                    flights.append(flight)
        return flights

    def findFlightByNo(self, flightNo):
        for flightList in self._allFlights.values():
            for flight in flightList:
                if flight.getFlightNumber() == flightNo:
                    return flight
        return -1

    def findAllCountryFlights(self, country):
        flights = []
        for flightList in self._allFlights.values():
            for flight in flightList:
                originAirport = self.getAirportByCode(flight.getOrigin().getCode())
                destinationAirport = self.getAirportByCode(flight.getDestination().getCode())
                if originAirport.getCountry() == country or destinationAirport.getCountry() == country:
                    flights.append(flight)
        return flights
    
    def findFlightBetween(self, origAirport, destAirport):
        directFlight = False
        for flight in self._allFlights.get(origAirport.getCode(), []):
            if flight.getDestination().getCode() == destAirport.getCode():
                return f"Direct Flight({flight.getFlightNumber()}): {origAirport.getCode()} to {destAirport.getCode()}"
        for airportCode in self._allFlights.keys():
            if airportCode == origAirport.getCode() or airportCode == destAirport.getCode():
                continue
            for flight1 in self._allFlights[origAirport.getCode()]:
                if flight1.getDestination().getCode() == airportCode:
                    for flight2 in self._allFlights[airportCode]:
                        if flight2.getDestination().getCode() == destAirport.getCode():
                            return set([airportCode])
        return -1
    
    def findReturnFlight(self, firstFlight):
        for flight in self._allFlights.values():
            for f in flight:
                if f.getOrigin() == firstFlight.getDestination() and f.getDestination() == firstFlight.getOrigin():
                    return f
        return -1

    def findFlightsAcross(self, ocean):
    # Create a set to store the flight codes that cross the specified ocean
        flight_codes = set()
        greenZone = ["Canada", "United States", "Mexico", "Brazil", "Argentina", "Colombia"]
        redZone = ["Japan", "China", "South Korea", "Australia", "New Zealand", "India", "Philippines", "Palestine", "United Arab Emirates"]
        blueZone = ["England", "France", "Spain", "Portugal", "Ireland", "South Africa", "Kenya", "Libya", "Italy"]
        # Check if the ocean parameter is valid
        if ocean not in ["Atlantic", "Pacific"]:
            return -1
        
        # Loop through all flights in the airport
        for flights in self._allFlights.values():
            for flight in flights:
                # Check if the flight crosses the specified ocean
                if ocean == "Atlantic":
                    if (flight.getOrigin().getCountry() in greenZone and flight.getDestination().getCountry() in blueZone) or (flight.getDestination().getCountry() in greenZone and flight.getOrigin().getCountry() in blueZone):
                        flight_codes.add(flight.getFlightNumber())
                elif ocean == "Pacific":
                    if (flight.getOrigin().getCountry() in greenZone and flight.getDestination().getCountry() in redZone) or (flight.getDestination().getCountry() in greenZone and flight.getOrigin().getCountry() in redZone):
                        flight_codes.add(flight.getFlightNumber())
        
        # Check if any flight codes were found
        if len(flight_codes) == 0:
            return -1
        else:
            return flight_codes
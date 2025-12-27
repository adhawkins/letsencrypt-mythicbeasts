import requests
import dns.resolver

from pprint import pprint


class MythicBeastsDNS:

    __BASE_URL = "https://api.mythic-beasts.com/dns/v2/"

    def __init__(self, key, secret):
        self.key = key
        self.secret = secret
        zones = self.MakeGetRequest("zones")
        self.zones = zones["zones"]

        answers = dns.resolver.resolve("ns1.mythic-beasts.com", "A")
        self.nameservers = [str(answer) for answer in answers]

    def MakeGetRequest(self, endpoint, data={}):
        r = requests.get(self.__BASE_URL + endpoint,
                         params=data, auth=(self.key, self.secret))
        return r.json()

    def MakePostRequest(self, endpoint, data):
        r = requests.post(self.__BASE_URL + endpoint,
                          json=data, auth=(self.key, self.secret))
        return r.json()

    def MakePutRequest(self, endpoint, data):
        r = requests.put(self.__BASE_URL + endpoint,
                         json=data, auth=(self.key, self.secret))
        return r.json()

    def MakeDeleteRequest(self, endpoint):
        r = requests.delete(self.__BASE_URL + endpoint,
                            auth=(self.key, self.secret))
        return r.json()

    def ParseRecord(self, name):
        thisZone = None
        thisRecord = None

        for zone in self.zones:
            if name.endswith(zone):
                thisZone = zone
                thisRecord = name[:-len(zone)-1]
                break

        return thisZone, thisRecord

    def AddTXTRecord(self, name, text, ttl=300):
        thisZone, thisRecord = self.ParseRecord(name)

        if thisZone and thisRecord:
            print(
                f"Adding TXT record to zone {thisZone}: {thisRecord} -> {text}")

            data = {
                "records": [
                    {
                        "host": thisRecord,
                        "ttl": ttl,
                        "type": "TXT",
                        "data": text,
                    }
                ],
            }

            response = self.MakePostRequest(
                f"zones/{thisZone}/records", data)
            pprint(response)
            return response

    def DeleteTXTRecord(self, name):
        thisZone, thisRecord = self.ParseRecord(name)

        if thisZone and thisRecord:
            print(
                f"Deleting TXT record from zone {thisZone}: {thisRecord}")

            response = self.MakeDeleteRequest(
                f"zones/{thisZone}/records/{thisRecord}/TXT")
            pprint(response)
            return response

    def LookupRecord(self, name, record_type):
        resolver = dns.resolver.Resolver()
        resolver.nameservers = self.nameservers

        try:
            answers = resolver.resolve(name, record_type)
            return [rdata.to_text() for rdata in answers]
        except dns.resolver.NXDOMAIN:
            return None

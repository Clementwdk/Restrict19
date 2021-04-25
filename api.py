import requests

url = "https://covid-19-coronavirus-statistics.p.rapidapi.com/v1/total"
headers = {
    'x-rapidapi-key': "096f9b67edmsh12f5f736f33e54ap13a933jsn5facda559584",
    'x-rapidapi-host': "covid-19-coronavirus-statistics.p.rapidapi.com"}


class InfoC:
    def __init__(self):
        self.death ="",
        self.recovered = "",
        self.confirmed = "",

    def getDeath(self):
        return self.death
    def getRecovered(self):
        return self.recovered
    def getConfirmed(self):
        return self.confirmed


    def reqApi(self,country):
        querystring = {"country": country}
        response = requests.request("GET", url, headers=headers, params=querystring,)
        a = response.json()
        self.death=str(a['data']['deaths'])
        self.recovered=str(a['data']['recovered'])
        self.confirmed=str(a['data']['confirmed'])
        return ''

    def reqApilIST(self,country):
        listInfo = {}
        querystring = {"country": country}
        response = requests.request("GET", url, headers=headers, params=querystring,)
        a = response.json()
        listInfo["death"]=str(a['data']['deaths'])
        listInfo["recovered"]=str(a['data']['recovered'])
        listInfo["confirmed"]=str(a['data']['confirmed'])
        print(a)
        return listInfo


# {
# "error":false
# "statusCode":200
# "message":"OK"
# "data":{
# "recovered":999374
# "deaths":23482
# "confirmed":1104508
# "lastChecked":"2021-04-17T00:24:44+00:00"
# "lastReported":"2021-04-16T04:20:46+00:00"
# "location":"Canada"
# }
# }

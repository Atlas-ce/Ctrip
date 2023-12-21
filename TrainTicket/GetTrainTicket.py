from bs4 import BeautifulSoup
from DrissionPage import WebPage
from time import sleep
from urllib.parse import quote

def TraninPage(departPlace,arrivePlace,departureDate):
    page = WebPage()
    page.get('https://trains.ctrip.com/webapp/train/list?ticketType=0&dStation='+departPlace+'&aStation='+arrivePlace+'&dDate='+departureDate+'&rDate=&trainsType=&hubCityName=&highSpeedOnly=0')
    sleep(1)
    soup=BeautifulSoup(page.html,"html.parser")
    return soup

def GetTrainPage(departPlace,arrivePlace,departureDate):
    return TraninPage(quote(departPlace),quote(arrivePlace),departureDate)

def TrainInfo(TrainDiv):
    return TrainDiv.find_all("div",{"class":"mid"})

def TrainChangeInfo(TrainDiv):
    return TrainDiv.find("div",{"class":"trans"}).text

def FromDiv(TrainDiv):
    return TrainDiv.find("div",{"class":"from"})

def ToDiv(TrainDiv):
    return TrainDiv.find("div",{"class":"to"})

def GetDpTime(TrainDiv):
    return FromDiv(TrainDiv).find("div",{"class":"time"}).text

def GetDpStation(TrainDiv):
    return FromDiv(TrainDiv).find("div",{"class":"station"}).text

def GetArrTime(TrainDiv):
    return ToDiv(TrainDiv).find("div",{"class":"time"}).text

def GetArrStation(TrainDiv):
    return ToDiv(TrainDiv).find("div",{"class":"station"}).text

def GetTicketInformation(TrainDiv):
    return TrainDiv.find("ul",{"class":"surplus-list"}).text

def GetPrice(TrainDiv):
    return TrainDiv.find("div",{"class":"price"}).text

def ReviseResult(TrainDiv,other_info):
    reuslt = {
    'departure_station': 'null',
    'arrival_station': 'null',
    'departure_time': 'null',
    'arrival_time': 'null',
    'other_info': 'null',
    'ticket_information':'null',
    'price': 'null'
    }
    reuslt['departure_station'] = GetDpStation(TrainDiv)
    reuslt['arrival_station'] = GetArrStation(TrainDiv)
    reuslt['departure_time'] = GetDpTime(TrainDiv)
    reuslt['arrival_time'] = GetArrTime(TrainDiv)
    reuslt['other_info'] = other_info
    reuslt['ticket_information']=GetTicketInformation(TrainDiv)
    reuslt['price']=GetPrice(TrainDiv)
    return reuslt

def DataProcessing(TrainDiv):
    if  len(TrainInfo(TrainDiv)) > 0:   
        return ReviseResult(TrainDiv,TrainInfo(TrainDiv)[0].text)
    else:
        return ReviseResult(TrainDiv,TrainChangeInfo(TrainDiv))
        
def AllTrains(allTrainDivs):
    for TrainDiv in allTrainDivs:
        print(DataProcessing(TrainDiv))

AllTrains(GetTrainPage('成都','运城','2023-12-21').find("section",{"role":"product"}).find_all("div",{"class":"list-bd"}))


import csv
import datetime
import re

import requests
from lxml import html


class KnowledgeBase:
    kb_from_station_name = ""
    kb_to_station_name = ""
    kb_from_station_code = ""
    kb_to_station_code = ""
    kb_date = ""
    kb_time = ""
    kb_depart_or_arrive = ""
    kb_ret_date = ""
    kb_ret_time = ""
    kb_ret_depart_or_arrive = ""
    kb_command = ""

    def add_from_station_code(self, from_station_code):
        self.kb_from_station_code = from_station_code

    def add_to_station_code(self, to_station_code):
        self.kb_to_station_code = to_station_code

    def add_command(self, command):
        self.kb_command = command

    def add_from_station(self, from_station):
        self.kb_from_station_name = from_station

    def add_to_station(self, to_station):
        self.kb_to_station_name = to_station

    def add_date(self, date):
        self.kb_date = date

    def add_time(self, time):
        self.kb_time = time

    def add_depart_or_arrive(self, depart_or_arrive):
        self.kb_depart_or_arrive = depart_or_arrive

    def add_return_date(self, ret_date):
        self.kb_ret_date = ret_date

    def add_return_time(self, ret_time):
        self.kb_ret_time = ret_time

    def add_return_depart_or_arrive(self, ret_depart_or_arrive):
        self.kb_ret_depart_or_arrive = ret_depart_or_arrive

    def remove_command(self):
        self.kb_command = ""

    def remove_from_station(self):
        self.kb_from_station_name = ""

    def remove_to_station(self):
        self.kb_to_station_name = ""

    def remove_date(self):
        self.kb_date = ""

    def remove_time(self):
        self.kb_time = ""

    def remove_depart_or_arrive(self):
        self.kb_depart_or_arrive = ""

    def remove_return_date(self):
        self.kb_ret_date = ""

    def remove_return_time(self):
        self.kb_ret_time = ""

    def remove_return_depart_or_arrive(self):
        self.kb_ret_depart_or_arrive = ""

    def remove_from_station_code(self):
        self.kb_from_station_code = ""

    def remove_to_station_code(self):
        self.kb_to_station_code = ""

    def get_command(self):
        return self.kb_command

    def get_from_station(self):
        return self.kb_from_station_name

    def get_to_station(self):
        return self.kb_to_station_name

    def get_date(self):
        return self.kb_date

    def get_time(self):
        return self.kb_time

    def get_depart_or_arrive(self):
        return self.kb_depart_or_arrive

    def get_return_date(self):
        return self.kb_ret_date

    def get_return_time(self):
        return self.kb_ret_time

    def get_return_depart_or_arrive(self):
        return self.kb_ret_depart_or_arrive

    def get_from_station_code(self):
        return self.kb_from_station_code

    def get_to_station_code(self):
        return self.kb_to_station_code


def train_journey(listtest):
    # information = [str, str, int, int, str, int, int, str]
    information = listtest
    journeyKB = KnowledgeBase
    KnowledgeBase.add_from_station(journeyKB, information[0])
    KnowledgeBase.add_to_station(journeyKB, information[1])
    KnowledgeBase.add_date(journeyKB, information[2])
    KnowledgeBase.add_time(journeyKB, information[3])
    KnowledgeBase.add_depart_or_arrive(journeyKB, information[4])
    KnowledgeBase.add_return_date(journeyKB, information[5])
    KnowledgeBase.add_return_time(journeyKB, information[6])
    KnowledgeBase.add_depart_or_arrive(journeyKB, information[7])

    from_station_name = KnowledgeBase.get_from_station(journeyKB)
    to_station_name = KnowledgeBase.get_to_station(journeyKB)
    date = KnowledgeBase.get_date(journeyKB)
    time = KnowledgeBase.get_time(journeyKB)
    depart_or_arrive = KnowledgeBase.get_depart_or_arrive(journeyKB)
    ret_date = KnowledgeBase.get_return_date(journeyKB)
    ret_time = KnowledgeBase.get_return_time(journeyKB)
    ret_depart_or_arrive = KnowledgeBase.get_return_depart_or_arrive(journeyKB)
    from_station = KnowledgeBase.get_from_station_code(journeyKB)
    to_station = KnowledgeBase.get_to_station_code(journeyKB)

    first_time = True
    expecting_date = False
    names_required = True
    confirmed_print = False
    csv_file = csv.reader(open('norfolk_station_codes_with_names.csv', "rt"), delimiter=",")

    while names_required:
        for row in csv_file:
            if (from_station_name in row[0]) or (from_station_name in row[1]):
                from_station_name = row[0]
                from_station = row[1]
            elif (to_station_name in row[0]) or (to_station_name in row[1]):
                to_station_name = row[0]
                to_station = row[1]
        if from_station_name == '' or None:
            print("From station name still required\n")
            break
        if to_station_name == '' or None:
            print("To station name still requited\n")
            break
        if date == '':
            print("Date not given, do you want to travel today?")
            expecting_date = True
        if (from_station_name != '') & (to_station_name != '') & (date != ''):
            names_required = False
    while expecting_date & (date == ''):
        print("Please enter a date, entering no date will set date to today")
        expecting_date = False

    if (from_station != "") & (to_station != ""):
        url = "http://ojp.nationalrail.co.uk/service/timesandfares/" + from_station + "/" + to_station
        if date == "":
            date = "today"
        url = url + "/" + date
        if time == "":
            time = str(datetime.datetime.now().time())
            time = time[0:2] + time[3:5]
        url = url + "/" + time
        if depart_or_arrive == "":
            depart_or_arrive = "dep"
        url = url + "/" + depart_or_arrive
        if ret_date != "":
            url = url + "/" + ret_date
            if ret_time == "":
                url = url + "/" + "0900/first"
            else:
                url = url + "/" + ret_time
                if ret_depart_or_arrive == "":
                    url = url + "/dep"
                else:
                    url = url + "/" + ret_depart_or_arrive
            page = requests.get(url)
            tree = html.fromstring(page.content)
            price = tree.xpath('//*[@id="singleFaresPane"]/strong/text()')
        else:

            page = requests.get(url)
            tree = html.fromstring(page.content)
            price = tree.xpath('//*[@id="fare-switcher"]/div/a/strong/text()')

        price = re.sub(',.*$|[^£\d\.]', '', str(price))

        f_time_dep = re.sub('[^£\d\.:]', '', str(tree.xpath('//*[@id="oft"]/tbody/tr[1]/td[1]/text()')))
        f_time_arr = re.sub('[^£\d\.:]', '', str(tree.xpath('//*[@id="oft"]/tbody/tr[1]/td[4]/text()')))
        f_price = re.sub('[^£\d\.]', '', str(tree.xpath('//*[@id="oft"]/tbody/tr[1]/td[9]/div/label/text()')))
        service = re.sub('[^A-Za-z ]', '', str(tree.xpath('//*[@id="oft"]/tbody/tr[1]/td[8]/div/div/a/text()')))
        ret_dep_time = re.sub('[^£\d\.:]', '', str(tree.xpath('//*[@id="ift"]/tbody/tr[1]/td[1]/text()')))
        ret_arr_time = re.sub('[^£\d\.:]', '', str(tree.xpath('//*[@id="ift"]/tbody/tr[1]/td[4]/text()')))
        ret_f_price = re.sub('[^£\d\.:]', '', str(tree.xpath('//*[@id="ift"]/tbody/tr[1]/td[9]/div[2]/label/text()')))
        if ret_date == "":
            output = "The train closest to your chosen time leaves " + from_station_name + " at " \
                     + f_time_dep + " on "
            if date != 'today':
                output = output + " " + date[:2] + "/" + date[2:4] + "/" + date[4:8]
            else:
                output = output + " on " + date
            output = output + " costing " + f_price

            if price == f_price:
                output = output + ". This is the cheapest fare around those times." \
                                  " This service is currently running: " + service
            else:
                output = output + "\n" + "Cheapest price found from " + from_station_name + " to " + to_station_name \
                         + " for " + price + ". This service is currently running: " + service

        else:
            ret_f_price = re.sub('[^\d]', '', ret_f_price)
            f_price = re.sub('[^\d]', '', f_price)
            total_price = float(f_price) + float(ret_f_price)
            total_price = total_price / 100
            total_price = str("£" + "%.2f" % total_price)
            output = "The train closest to your chosen time leaves " + from_station_name + " at " \
                     + f_time_dep + " and arrives at " + to_station_name + " at " + f_time_arr
            if date != 'today':
                output = output + " " + date[:2] + "/" + date[2:4] + "/" + date[4:8]
            else:
                output = output + " on " + date
            output = output + ".\nYour return journey will leave " + to_station_name + " at " + ret_dep_time \
                     + " and arrives at " + from_station_name + " at " + ret_arr_time
            if ret_date != 'today':
                output = output + " on " + ret_date[:2] + "/" + ret_date[2:4] + "/" + ret_date[4:8]
            else:
                output = output + ret_date
            output = output + ".\nThis journey will cost " + total_price
            if total_price != price:
                output = output + "\nCheaper return journey from " + from_station_name + " to " + to_station_name \
                         + " for " + price + " is available."

                # TODO: ADD 'NEXT TRAIN'
                # TODO: ADD 'FIRST/LAST TRAIN'
                # TODO: COMMENTS
        print(output)
        print(url)


if __name__ == '__main__':
    listtest = ['KLN', 'London', '15012019', '0900', 'dep', '16012019', '0900', 'arr']

    train_journey(listtest)

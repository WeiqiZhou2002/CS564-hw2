
"""
FILE: skeleton_parser.py
------------------
Author: Firas Abuzaid (fabuzaid@stanford.edu)
Author: Perth Charernwattanagul (puch@stanford.edu)
Modified: 04/21/2014

Skeleton parser for CS564 programming project 1. Has useful imports and
functions for parsing, including:

1) Directory handling -- the parser takes a list of eBay json files
and opens each file inside of a loop. You just need to fill in the rest.
2) Dollar value conversions -- the json files store dollar value amounts in
a string like $3,453.23 -- we provide a function to convert it to a string
like XXXXX.xx.
3) Date/time conversions -- the json files store dates/ times in the form
Mon-DD-YY HH:MM:SS -- we wrote a function (transformDttm) that converts to the
for YYYY-MM-DD HH:MM:SS, which will sort chronologically in SQL.

Your job is to implement the parseJson function, which is invoked on each file by
the main function. We create the initial Python dictionary object of items for
you; the rest is up to you!
Happy parsing!
"""

import sys
from json import loads
from re import sub

columnSeparator = "|"

# Dictionary of months used for date transformation
MONTHS = {'Jan':'01','Feb':'02','Mar':'03','Apr':'04','May':'05','Jun':'06',\
        'Jul':'07','Aug':'08','Sep':'09','Oct':'10','Nov':'11','Dec':'12'}

"""
Returns true if a file ends in .json
"""
def isJson(f):
    return len(f) > 5 and f[-5:] == '.json'

"""
Converts month to a number, e.g. 'Dec' to '12'
"""
def transformMonth(mon):
    if mon in MONTHS:
        return MONTHS[mon]
    else:
        return mon

"""
Transforms a timestamp from Mon-DD-YY HH:MM:SS to YYYY-MM-DD HH:MM:SS
"""
def transformDttm(dttm):
    dttm = dttm.strip().split(' ')
    dt = dttm[0].split('-')
    date = '20' + dt[2] + '-'
    date += transformMonth(dt[0]) + '-' + dt[1]
    return date + ' ' + dttm[1]

"""
Transform a dollar value amount from a string like $3,453.23 to XXXXX.xx
"""

def transformDollar(money):
    if money == None or len(money) == 0:
        return money
    return sub(r'[^\d.]', '', money)

"""
Parses a single json file. Currently, there's a loop that iterates over each
item in the data set. Your job is to extend this functionality to create all
of the necessary SQL tables for your database.
"""
def parseJson(json_file):
    with open(json_file, 'r') as f:
        items = loads(f.read())['Items'] # creates a Python dictionary of Items for the supplied json file
        for item in items:
            """
            TODO: traverse the items dictionary to extract information from the
            given `json_file' and generate the necessary .dat files to generate
            the SQL tables based on your relation design
            """

            item_id = item['ItemID']
            name = item['Name']
            categories = item['Category']
            currently = transformDollar(item['Currently'])
            first_bid = transformDollar(item['First_Bid'])
            number_of_bids = item['Number_of_Bids']
            bids = item['Bids']
            
            started = transformDttm(item['Started'])
            ends = transformDttm(item['Ends'])
 
            seller = item['Seller']
            seller_id = seller['UserID']
            seller_rating = seller['Rating']
            item_location = item['Location']
            item_country = item['Country']
            
            description = item['Description']
            
            with open('item.dat', 'a') as outfile:
                outfile.write(f"{item_id}{columnSeparator}{name}{columnSeparator}{seller_id}{columnSeparator}{currently}{columnSeparator}{first_bid}{columnSeparator}{number_of_bids}{columnSeparator}{started}{columnSeparator}{ends}{columnSeparator}{description}\n")
                
            for category in categories:
                with open('category.dat', 'a') as catfile:
                    catfile.write(f"{item['ItemID']}{columnSeparator}\"{category}\"\n")
            
            with open('user.dat', 'a') as f1:
                Bids = item.get("Bids")
                if Bids is not None:
                    for i in range(len(Bids)):
                        bidder = Bids[i]["Bid"]["Bidder"]
                        info = "\"" + sub(r'\"', '\"\"', bidder["UserID"]) + "\"" if bidder.get("UserID") is not None else "NULL"
                        info += "|" + (bidder["Rating"] if bidder.get("Rating") is not None else "NULL")
                        info += "|" + ("\"" + sub(r'\"', '\"\"', bidder["Location"]) + "\"" if "Location" in bidder and bidder["Location"] is not None else "NULL")
                        info += "|" + ("\"" + sub(r'\"', '\"\"', bidder["Country"]) + "\"" if "Country" in bidder and bidder["Country"] is not None else "NULL")
                        info += "\n"
                        f1.write(info)
                    
                Seller = item["Seller"]
                SellerID = "\"" + sub(r'\"', '\"\"', Seller["UserID"]) + "\"" if Seller.get("UserID") is not None else "NULL"
                info = SellerID
                info += "|" + (Seller["Rating"] if Seller.get("Rating") is not None else "NULL")
                info += "|" + ("\"" + sub(r'\"', '\"\"', item["Location"]) + "\"" if item.get("Location") is not None else "NULL")
                info += "|" + ("\"" + sub(r'\"', '\"\"', item["Country"]) + "\"" if item.get("Country") is not None else "NULL")
                info += "\n"
                f1.write(info)
                    
            # if item.get('Bids') is not None and item['Bids'] != "null": 
            #     for bid in item['Bids']:
            #         if 'Bidder' in bid and bid['Bidder'] is not None:
            #             bidder_id = bid['Bidder']['UserID']
            #             bid_time = transformDttm(bid['Time'])
            #             bid_amount = transformDollar(bid['Amount'])
            #             with open('bids_output.txt', 'a') as bidfile:
            #                 bidfile.write(f"{item_id}{columnSeparator}{bidder_id}{columnSeparator}{bid_time}{columnSeparator}{bid_amount}\n")
                            
            with open('bid.dat', 'a') as f2:
                for item in items:
                    ItemID = item["ItemID"]
                    Bids = item.get("Bids")
                    if Bids is not None:
                        for bid in Bids:
                            Bid = bid["Bid"]
                            Bidder = Bid["Bidder"]
                            BidderUserID = Bidder["UserID"]
                            Time = transformDttm(Bid["Time"])
                            Amount = transformDollar(Bid["Amount"])
                            bid_info = f"{ItemID}|\"{BidderUserID}\"|{Time}|{Amount}\n"
                            f2.write(bid_info)
                        
"""
Loops through each json files provided on the command line and passes each file
to the parser
"""
def main(argv):
    if len(argv) < 2:
        print('Usage: python skeleton_json_parser.py <path to json files>')
        sys.exit(1)
    # loops over all .json files in the argument
    for f in argv[1:]:
        if isJson(f):
            parseJson(f)
            print("Success parsing " + f)

if __name__ == '__main__':
    main(sys.argv)

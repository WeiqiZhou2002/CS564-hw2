
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
            ItemID = item["ItemID"]
            Categories = item["Category"]
            Bids = item["Bids"]
            Seller = item["Seller"]
            SellerID = Seller["UserID"]
            
            # Item.dat (Item_ID, Seller_ID, Name, Currently, Buy_Price, First_Bid, Number_of_Bids, Started, Ends, Description)
            with open('Item.dat', 'a') as f1:
                if not item["Name"] == None:
                    Name = sub(r'\"','\"\"',item["Name"])
                else:
                    Name = "NULL"
                if not item["Currently"] == None:
                    Currently =  transformDollar(item["Currently"]) 
                else:
                    Currently = "NULL"
                if "Buy_Price" in item.keys():
                    Buy_Price = transformDollar(item["Buy_Price"])
                else:
                    Buy_Price = "NULL"
                if not item["First_Bid"] == None:
                    First_Bid = transformDollar(item["First_Bid"])
                else:
                    First_Bid = "NULL"
                if not item["Number_of_Bids"] == None:
                    Number_of_Bids = item["Number_of_Bids"]
                else:
                    Number_of_Bids = "NULL"
                if not item["Started"] == None:
                    Started = transformDttm(item["Started"])
                else:
                    Started = "NULL"
                if not item["Ends"] == None:
                    Ends = transformDttm(item["Ends"])
                else:
                    Ends = "NULL"
                if item["Description"] == None:
                    Description = "NULL"
                else:
                    Description = sub(r'\"','\"\"',item["Description"])
                    
                info = ItemID + "|" + '\"' + Name + '\"' + "|" + '\"' + SellerID + '\"' + "|" + Currently + "|" + Buy_Price + "|" + First_Bid + "|" + Number_of_Bids + "|" + '\"' + Started + '\"' + "|" + '\"' + Ends + '\"' + "|" + '\"' + Description + '\"' + "\n"
                f1.write(info)
            
            
            # Category.dat (ItemID, Category)
            with open('Category.dat', 'a') as f2:
                if ItemID == None:
                    ItemID = "NULL"
                for c in Categories:
                    Category = sub(r'\"','\"\"',c);
                    info = ItemID + "|" + '\"' + Category + '\"' + "\n"
                    f2.write(info)
                
            
            # Bid.dat (Bids[Bidder], UserID, Rating, Location, Country, Time, Amount)
            with open('Bid.dat', 'a') as f3:
                if not Bids == None:
                    for i in range(len(Bids)):
                        if not item["ItemID"] == None:
                            itemID = item["ItemID"]
                        else:
                            itemID = "NULL"
                        
                        bidder = Bids[i]["Bid"]
                        if not bidder["Bidder"]["UserID"] == None:
                            bidID = sub(r'\"','\"\"',bidder["Bidder"]["UserID"])
                        else:
                            bidID = "NULL"
                        if not bidder["Time"] == None:
                            time = transformDttm(bidder["Time"])
                        else:
                            time = "NULL"
                        if not bidder["Amount"] == None:
                            amount = transformDollar(bidder["Amount"])
                        else:
                            amount = "NULL"
                            
                        info = itemID + "|" + '\"' + bidID + '\"' + "|" + '\"' + time + '\"' + "|" + amount  + "\n"
                        f3.write(info)
        
        
            # User.dat (SellerID, Rating, Location, Country)
            with open('User.dat', 'a') as f4:
                if SellerID == None:
                    SellerID = "NULL"
                else:
                    SellerID = sub(r'\"','\"\"',SellerID)
                if not Seller["Rating"] == None:
                    rating = Seller["Rating"]
                else:
                    rating = "NULL"
                if not item["Location"] == None:
                    location = sub(r'\"','\"\"',item["Location"])
                else:
                    location = "NULL"
                if not item["Country"] == None:
                    country = sub(r'\"','\"\"',item["Country"])
                else:
                    country = "NULL"
                    
                info = '\"' + SellerID + '\"' + "|" + rating + "|" + '\"' + location + '\"' + "|" + '\"' + country + '\"' + "\n"
                f4.write(info)
                            
            f1.close()
            f2.close()
            f3.close()
            f4.close()
                        
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

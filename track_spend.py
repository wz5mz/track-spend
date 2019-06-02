#! /data/data/com.termux/files/usr/bin/env python3

from oauth2client.service_account import ServiceAccountCredentials
import gspread
import sys
import re

date = sys.argv[1]
amount = sys.argv[2]
card = sys.argv[3]
tag = sys.argv[4]
memo = sys.argv[5]

amount = float(re.search("[$].+\.\d\d", amount).group(0)[1:])

card_dict = {"2006": "AmEx Gold Card",
             "1003": "AmEx Gold Card",
             "1004": "AmEx Gold Card",
             "0000": "Citi Double Cash credit"}
card = card_dict.get(re.search("\d\d\d\d", card).group(0))


def track_spend(date, amount, card, tag, memo):
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        '/data/data/com.termux/files/home/storage/downloads/Track Spend-908a12e5ca6e.json', scope)
#    credentials = ServiceAccountCredentials.from_json_keyfile_name(
#        'c:/users/wade/downloads/Track Spend-908a12e5ca6e.json', scope)
    gc = gspread.authorize(credentials)
    worksheet = gc.open('Wade Zhang\'s Spending from 2016-06-20.xlsx').worksheet('2016-11-17 to')
    last_row = len(worksheet.col_values(2)) + 1
    cell_list = [gspread.models.Cell(last_row, 1, date),
                 gspread.models.Cell(last_row, 2, amount),
                 gspread.models.Cell(last_row, 3, card),
                 gspread.models.Cell(last_row, 4, tag),
                 gspread.models.Cell(last_row, 5, memo)]
    worksheet.update_cells(cell_list)


track_spend(date, amount, card, tag, memo)

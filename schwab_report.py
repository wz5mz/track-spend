#! /data/data/com.termux/files/usr/bin/env python3

import datetime
import ofxtools
import re
import os
from lxml import etree
import keyring


# Include error handling for when signon fails - MAYBE RETURN N/A?

# def schwab_report(dtstart, dtend):

directory = os.path.join(os.path.dirname(os.path.abspath(__file__)),'schwab_statement.xml')

dtstart = datetime.datetime(2019, 1, 1, tzinfo=ofxtools.utils.UTC)
dtend = datetime.datetime(2019, 12, 25, tzinfo=ofxtools.utils.UTC)


username = keyring.get_password('schwab', 'username')
password = keyring.get_password('schwab', 'password')
rothacctno = keyring.get_password('schwab', 'rothacctno')
brokerageacctno = keyring.get_password('schwab', 'brokerageacctno')

client = ofxtools.OFXClient('https://ofx.schwab.com/cgi_dev/ofx_server',
                            userid=username,
                            brokerid='SCHWAB.COM')

def getnetworth():
    networth = 0
    cash = 0
    acctid = [brokerageacctno, rothacctno]
    for acct in acctid:
        statement = ofxtools.Client.InvStmtRq(acctid=acct, dtstart=dtstart, dtend=dtend)
        with client.request_statements(password, statement) as f:
            message = f.read()

        file = open(directory, 'w')
        file.write(message.decode())
        file.close()

        tree = etree.parse(directory)
        root = tree.getroot()

        for element in root.iter():
            if element.tag=='NAME' and element.text=='Total Account Value':
                for sibling in element.getparent():
                    if sibling.tag=='VALUE':
                        networth += float(sibling.text)
            if element.tag=='AVAILCASH':
                cash += float(element.text)
    return networth, cash

print(getnetworth())
os.remove(directory)

# -*- coding: cp949 -*-
from xmlbook import *
from http.client import HTTPConnection
from http.server import BaseHTTPRequestHandler, HTTPServer
from xml.etree import ElementTree


import mimetypes
import mysmtplib
from email.mime.base import MIMEBase
from email.mime.text import MIMEText

##global
conn = None
tree = None
#regKey = 'FzCbn1kMa0%2Ft0TRkotzGekvr0P0sEYnTfnXGzlfdnh0MaOIgzjKXN4zpALLpJ%2Fj3bwpyZ6ORRm87bSvlhigIrw%3D%3D'

# ���̹� OpenAPI ���� ���� information
server = "apis.data.go.kr"

# smtp ����
host = "smtp.gmail.com" # Gmail SMTP ���� �ּ�.
port = "587"

BooksDoc = None


def userURIBuilder(server,**user):
    str = "http://" + server + "/search" + "?"
    for key in user.keys():
        str += key + "=" + user[key] + "&"
    return str

def connectOpenAPIServer():
    global conn, server
    conn = HTTPConnection(server)
        
def getBookDataFromISBN():
    global server, regKey, conn
    if conn == None :
        connectOpenAPIServer()
    #uri = userURIBuilder(server, key=regKey, query='%20', display="1", start="1", target="book_adv", d_isbn=isbn)
    uri = "/1262000/CountryBasicService/getCountryBasicList?ServiceKey=FzCbn1kMa0%2Ft0TRkotzGekvr0P0sEYnTfnXGzlfdnh0MaOIgzjKXN4zpALLpJ%2Fj3bwpyZ6ORRm87bSvlhigIrw%3D%3D&numOfRows=999&pageSize=999&pageNo=1&startPage=FzCbn1kMa0%2Ft0TRkotzGekvr0P0sEYnTfnXGzlfdnh0MaOIgzjKXN4zpALLpJ%2Fj3bwpyZ6ORRm87bSvlhigIrw%3D%3D1"
    conn.request("GET", uri)
    
    req = conn.getresponse()
    print (req.status)
    if int(req.status) == 200 :
        print("Book data downloading complete!")
        return extractBookData(req.read())
    else:
        print ("OpenAPI request has been failed!! please retry")
        return None
        
def extractBookData(strXml):
    global tree
    
    
    tree = ElementTree.fromstring(strXml)
    print (strXml)
    # Book ������Ʈ�� �����ɴϴ�.
    """
    itemElements = tree.getiterator("item")  # return list type
    print(itemElements)
    for item in itemElements:
        strTitle = item.find("countryEnName")
        print (strTitle)
        if len(strTitle.text) > 0 :
           print("countryEnName:", strTitle.text)
    """


def sendMain():
    global host, port
    html = ""
    title = str(input ('Title :'))
    senderAddr = str(input ('sender email address :'))
    recipientAddr = str(input ('recipient email address :'))
    msgtext = str(input ('write message :'))
    passwd = str(input (' input your password of gmail account :'))
    msgtext = str(input ('Do you want to include book data (y/n):'))
    if msgtext == 'y' :
        keyword = str(input ('input keyword to search:'))
        html = MakeHtmlDoc(SearchBookTitle(keyword))
    
    import mysmtplib
    # MIMEMultipart�� MIME�� �����մϴ�.
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    
    #Message container�� �����մϴ�.
    msg = MIMEMultipart('alternative')

    #set message
    msg['Subject'] = title
    msg['From'] = senderAddr
    msg['To'] = recipientAddr
    
    msgPart = MIMEText(msgtext, 'plain')
    bookPart = MIMEText(html, 'html', _charset = 'UTF-8')
    
    # �޼����� ������ MIME ������ ÷���մϴ�.
    msg.attach(msgPart)
    msg.attach(bookPart)
    
    print ("connect smtp server ... ")
    s = mysmtplib.MySMTP(host,port)
    #s.set_debuglevel(1)
    s.ehlo()
    s.starttls()
    s.ehlo()
    s.login(senderAddr, passwd)    # �α��� �մϴ�. 
    s.sendmail(senderAddr , [recipientAddr], msg.as_string())
    s.close()
    
    print ("Mail sending complete!!!")

class MyHandler(BaseHTTPRequestHandler):
    
    def do_GET(self):
        from urllib.parse import urlparse
        import sys
      
        parts = urlparse(self.path)
        keyword, value = parts.query.split('=',1)

        if keyword == "title" :
            html = MakeHtmlDoc(SearchBookTitle(value)) # keyword�� �ش��ϴ� å�� �˻��ؼ� HTML�� ��ȯ�մϴ�.
            ##��� �κ��� �ۼ�.
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(html.encode('utf-8')) #  ����( body ) �κ��� ��� �մϴ�.
        else:
            self.send_error(400,' bad requst : please check the your url') # �� ���� ��û��� ������ �����Ѵ�.
        
def startWebService():
    try:
        server = HTTPServer( ('localhost',8080), MyHandler)
        print("started http server....")
        server.serve_forever()
        
    except KeyboardInterrupt:
        print ("shutdown web server")
        server.socket.close()  # server �����մϴ�.

def checkConnection():
    global conn
    if conn == None:
        print("Error : connection is fail")
        return False
    return True

def PrintAllCountry():
    global tree
    
    itemElements = tree.getiterator("item")
    for item in itemElements:
        strTitle = item.find("countryName")
        #print (strTitle)
        if len(strTitle.text) > 0 :
            print("countryName:", strTitle.text)

def SearchCountry():
    global tree
    real = False
    ctry = str(input ('input country to find : '))
    
    
    itemElements = tree.getiterator("item")
    for item in itemElements:
        strTitle = item.find("countryName")
        if strTitle.text == ctry:
            print(ctry, "is real")
            real = True
            strTitle = item.find("basic")
            print("���� : ", strTitle.text)
            real = True
            break;
    if real == False:    print("Not real")

























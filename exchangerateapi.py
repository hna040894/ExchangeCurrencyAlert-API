import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


URL = "https://wise.com/gb/currency-converter/eur-to-vnd-rate"
page = requests.get(URL)

#print(page.text)
soup = BeautifulSoup(page.content, "html.parser")

results = soup.find(id="calculator")

#Find exchange rate element
now_euro_vnd = results.find("span", class_="text-success")
print(now_euro_vnd)
now_euro_vnd = now_euro_vnd.text
print(type(now_euro_vnd))

#Create a text file to store current exchange rate
with open('filepath\eurotovndconverter.txt', 'r') as eurotovnd:
    last_euro_vnd = eurotovnd.readline()

if now_euro_vnd != last_euro_vnd:
    with open('filepath\eurotovndconverter.txt', 'w') as eurotovnd:
        eurotovnd.write(now_euro_vnd)  

#Create an email alert
def send_email(exchangerate):
    fromaddr = "abc@email.com"
    toaddr = "egh@email.com"
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "Alert: Euro to VND is above 26500  "
    body = "Alert thong bao ti gia euro / vnd da dat : " + exchangerate
    msg.attach(MIMEText(body, 'plain'))
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromaddr, "EmailGeneratecode")
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()


f = open("filepath\eurotovndconverter.txt", "r")
content = f.read()
#print(content)
if float(content) > 26500.00:
    send_email(content)
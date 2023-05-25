#Script to loop thru a list of IP addresses and check each one to
#see if it returns any web content.
#Selenium requires geckodriver from https://github.com/mozilla/geckodriver/releases
import os
import sys
import requests
import ipaddress
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from time import sleep

if len(sys.argv) < 2:
                print("please enter a file with IPs: webpageFinder.py <file with IPs>")
                sys.exit()

with open(sys.argv[1],"r") as f:
                IPs = [ip.strip() for ip in f]
 
def ipRangeToList(start, end):
    import socket, struct
    start = struct.unpack('>I', socket.inet_aton(start))[0]
    end = struct.unpack('>I', socket.inet_aton(end))[0]
    return [socket.inet_ntoa(struct.pack('>I', i)) for i in range(start, end)]

formattedIPs = []

#convert any ip ranges into individual IPs
for ip in IPs:
                #remove any spaces, such as on either side of the - range separator
                ip = ip.replace(" ", "")

                if "-" in ip: #check for IP range
                                dashLoc = ip.index("-")
                                startIP = ip[0:dashLoc]
                                endIP = ip[dashLoc + 1:]
                                extractedIPs = [ipaddress.ip_address(i).exploded for i in range(int(ipaddress.ip_address(startIP)), int(ipaddress.ip_address(endIP)))]
                                formattedIPs = formattedIPs + extractedIPs

                elif "/" in ip: #check for cidr range
                                #first convert to ip range, to get the starting and ending IPs
                                net = ipaddress.ip_network(ip)
                                startIP = net[0]
                                endIP = net[-1]

                                #then get the IPs in the range
                                extractedIPs = [ipaddress.ip_address(i).exploded for i in range(int(ipaddress.ip_address(startIP)), int(ipaddress.ip_address(endIP)))]
                                formattedIPs = formattedIPs + extractedIPs

                else: #assume its a normal IP
                                formattedIPs.append(ip)

screenshotFilePath="seleniumScreenshots\\" #"C:\\Users\\koyoung\\!scripts\\seleniumScreenshots\\"
if not os.path.exists('seleniumScreenshots\\'):
    os.makedirs('seleniumScreenshots\\')
 
counter = 1
outputFile=open('webpageFinder_output.txt','a')
for ip in formattedIPs:
                print("\n" + str(counter))
                counter+=1
                print(ip)

                try:
                                #see if can connect to a web server at the IP
                                print("https")
                                httpsUrl = https:// + ip
                                httpsResp =requests.get(httpsUrl, verify=False, timeout=5);
                                print(httpsResp.text[0:500])
                                print("\n" + ip + " https - " + httpsResp.text[0:500], file=outputFile)
                                print("taking screenshot")
                                browser = webdriver.Firefox()
                                browser.get(httpsUrl)
                                
                                #sleep(1) #wait a bit for the page to load
                                try:
                                                WebDriverWait(browser, 2).until(EC.alert_is_present(),
                                                                'Timed out waiting for http auth popup to appear.')
                                                alert = browser.switch_to.alert
                                                print(alert.text)
                                                print("\n" + ">>>alert box: " + alert.text, file=outputFile)
                                                alert.dismiss()
                                except TimeoutException:
                                                print("no alert found")
                                finally:
                                                browser.get_screenshot_as_file(screenshotFilePath + ip + "_https.png")
                                                browser.close()
                                                browser.quit()
                               
                                print("\n----\n")
                                print("http")

                                httpUrl = http:// + ip
                                httpResp =requests.get(httpUrl, timeout=5);
                                print(httpResp.text[0:500])
                                print("\n" + ip + " http - " + httpResp.text[0:500], file=outputFile)

                                print("taking screenshot")
                                browser = webdriver.Firefox()
                                browser.get(httpUrl)

                                #sleep(1) #wait a bit for the page to load
                                #handle http auth prompt if necessary
                                #if EC.alert_is_present():
                                try:
                                                WebDriverWait(browser, 2).until(EC.alert_is_present(),
                                                                'Timed out waiting for http auth popup to appear.')
                                                alert = browser.switch_to.alert
                                                print(alert.text)
                                                print("\n" + ">>>alert box: " + alert.text, file=outputFile)
                                                alert.dismiss()
                                except TimeoutException:
                                                print("no alert found")
                                finally:
                                                browser.get_screenshot_as_file(screenshotFilePath + ip + "_http.png")
                                                browser.close()
                                                browser.quit()
                except requests.exceptions.RequestException as e:
                                print("could not connect to: " + ip)
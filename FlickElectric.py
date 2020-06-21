import requests
from bs4 import BeautifulSoup
import json



def main():
   
   USERNAME = "your@mail.com"
   PASSWORD = "SuperSecrectPassword"
   LOGIN_URL = "https://id.flickelectric.co.nz/identity/users/sign_in"
   URL = "https://myflick.flickelectric.co.nz/dashboard/snapshot"
   session_requests = requests.session()
   
   # Get login csrf token

   # "access" LOGIN_URL webpage
   result = session_requests.get(LOGIN_URL)
   #print("result.ok=",result.ok)
   #print("result.status_code =",result.status_code )
   
   # Parse LOGIN_URL HTML and save to BeautifulSoup object
   soup0 = BeautifulSoup(result.text, "html.parser")
   #print(soup0.prettify())
   #print(soup0.find("form").find("input"))
   
   # Using  BeautifulSoup grab the authenticity_token
   authenticity_token=soup0.form.input.contents[0].get('value')
   #print("authenticity_token=",authenticity_token)

   #Create payload
   payload = {
               "authenticity_token":authenticity_token,
                      "user[guest]":"FALSE",  
                      "user[email]":USERNAME,         
                   "user[password]":PASSWORD,      
                "user[remember_me]":"1"    
   }
   
   #Perform login
   result1 = session_requests.post(LOGIN_URL, data = payload, headers = dict(referer = LOGIN_URL))
   #print("result1=",result1)
   #print("result1.ok=",result1.ok)
   #print("result1.status_code =",result1.status_code )

   #Parse Snapshot webpage HTML and save to BeautifulSoup object
   soup1 = BeautifulSoup(result1.text, "html.parser")   
   #print(soup1.prettify())
   
   # Using BeautifulSoup grab the KwH value from data-react-class="FlickNeedle"
   FlickNeedle=soup1.main.div.div.contents
   # and store in a json object
   Current_Value= FlickNeedle[3].get('data-react-props')
     
   #jCurrent_Value = json.dumps(Current_Value)
   
   #vDate = jCurrent_Value["asAt"]
   #vkWh = jCurrent_Value["currentPeriod"]["price"]["value"]
   #valuetoFile = vDate+","+vkWh+'\n'
   #print(valuetoFile)
      

   #Writes <DATE> <Kwh> into a file
   with open('flick_workfile.tx', 'a') as f:
      f.write(Current_Value + "\n")
  
   print(Current_Value)

if __name__ == '__main__':
   main()

#pip install fastapi uvicorn jinja2 python-multipart pymongo
import pymongo;
import requests
import re;
from fastapi import FastAPI, Request, Form;
from fastapi.templating import Jinja2Templates;

app = FastAPI()
templates = Jinja2Templates(directory="C:\\Users\\vkostadinov\OneDrive - VMware, Inc\\VMwareCorp\\Documents\\PythonWorkspace\\reminderVinetu\\templates")

@app.get('/')
def read_form():
    return 'Server is running'

@app.get("/register")
def form_post(request: Request):
    result = "Type car number"
    return templates.TemplateResponse('form.html', context={'request': request, 'result': result})

@app.post("/register")
def form_post(request: Request, num: str = Form(...)):
    carNumStr = num
    
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["carNumbers"]
    mycol = mydb["table"]
    
    if re.match(r"^[A-Za-z]{2}[0-9]{4}[A-Za-z]{2}$", carNumStr):
        query = { "carNum": carNumStr }
        checkExisting = mycol.find(query)
        total_count = list(checkExisting)
        if len(total_count) == 0:

            urlStr = "https://check.bgtoll.bg/check/vignette/plate/BG/" + carNumStr
            r = requests.get(url = urlStr)
            data = r.json()
            print(data)
            if(data['vignette']):
                startDate = data['vignette']['validityDateFrom']
                endDate = data['vignette']['validityDateTo']
            
                mydict = { "carNum": carNumStr, "from": startDate, "end": endDate}
                x = mycol.insert_one(mydict)
                return templates.TemplateResponse('form.html', context={'request': request, 'result': 'The number has been saved to the database'})
            else:
                return templates.TemplateResponse('form.html', context={'request': request, 'result': 'The number can be found under toll system'})    
        else:
            return templates.TemplateResponse('form.html', context={'request': request, 'result': 'The number already exist in the database'})
    else:
        return templates.TemplateResponse('form.html', context={'request': request, 'result': 'The car number format is incorrect'})

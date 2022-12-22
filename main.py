#pip install fastapi uvicorn jinja2 python-multipart pymongo
import pymongo;
import requests
import re;
from fastapi import FastAPI, Request, Form;
from fastapi.templating import Jinja2Templates;

app = FastAPI()
templates = Jinja2Templates(directory="C:\\Users\\vkostadinov\OneDrive - VMware, Inc\\VMwareCorp\\Documents\\PythonWorkspace\\reminderVinetu\\templates")

@app.get('/')
async def read_form():
    return 'Server is running'

@app.get("/register")
async def form_post(request: Request):
    result = "Fulfil data and click submit"
    return templates.TemplateResponse('form.html', context={'request': request, 'result': result})

@app.post("/register")
async def form_post(request: Request, num: str = Form(...), email: str = Form(...)):
    carNumStr = num
    emailStr = email
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
            
            if(data['vignette']):
                startDate = data['vignette']['validityDateFrom']
                endDate = data['vignette']['validityDateTo']
            
                mydict = { "carNum": carNumStr, "from": startDate, "end": endDate, "email": emailStr}
                x = mycol.insert_one(mydict)
                return templates.TemplateResponse('form.html', context={'request': request, 'result': '✓ The carplate has been saved to the database'})
            else:
                return templates.TemplateResponse('form.html', context={'request': request, 'result': '⚠ The carplate is not found under toll system'})    
        else:
            return templates.TemplateResponse('form.html', context={'request': request, 'result': '⚠ The carplate already exist in the database'})
    else:
        return templates.TemplateResponse('form.html', context={'request': request, 'result': '⚠ The carplate format is incorrect'})

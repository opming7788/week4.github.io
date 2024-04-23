from fastapi import FastAPI, Request,Form
from fastapi.responses import HTMLResponse,RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi import Depends
from starlette.middleware.sessions import SessionMiddleware

app = FastAPI()

app.add_middleware(SessionMiddleware, secret_key="mySignIn") ##提供一個秘密鍵來簽名 cookie

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    if request.session.get("signed_in"):
        return RedirectResponse(url="/member", status_code=303)
    return templates.TemplateResponse("home.html", {"request": request})

@app.post("/signin",response_class=HTMLResponse)
async def signin(request: Request,username: str = Form(None), password: str = Form(None)):
    if username is None and password is None :
        return RedirectResponse(url="/error?message=帳號，或密碼錯誤", status_code=303)
    elif username is None or password is None:
        return RedirectResponse(url="/error?message=請輸入帳號，密碼", status_code=303)
    elif username == "test" and password == "test":
        request.session["signed_in"] = True  
        return RedirectResponse(url="/member",status_code=303)
    else:
        return RedirectResponse(url="/error?message=帳號，或密碼錯誤",status_code=303)

@app.get("/signout")
async def signout(request: Request):
    
    request.session["signed_in"] = False 
    return RedirectResponse(url="/", status_code=303)  # 重定向到首頁

@app.get("/member", response_class=HTMLResponse)
async def login_success(request: Request):
    if not request.session.get("signed_in"):
        return RedirectResponse(url="/", status_code=303)  # 如果未登入，重定向到首頁
   
    return templates.TemplateResponse("login_success.html", {"request": request})
    

@app.get("/error", response_class=HTMLResponse)
async def login_failure(request: Request= None,message:str= None):
    
    if request.session.get("signed_in"):
        return RedirectResponse(url="/member", status_code=303)

    return templates.TemplateResponse("login_failure.html", {"request": request,"message": message})
    
   


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

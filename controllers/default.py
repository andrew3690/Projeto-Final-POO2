## import de modulos necessarios para funcionamento da aplicaçao
from app import app
from flask import render_template , url_for
from flask_bootstrap import Bootstrap
from app.models.forms import LoginForm  
import threading
import json
import requests
import matplotlib.pyplot as plt
import time
import os


data={'ABEV':None,'VALE':None,'TTWO':None,'WEGE':None}
sma={'ABEV':None,'VALE':None,'TTWO':None,'WEGE':None}

## funçao para atualizaçao do grafico na aplicaçao 

def graph():
    global data
    global sma

    atual=[data['ABEV'].json(),data["VALE"].json(),data['TTWO'].json(),data['WEGE'].json()]
    sma_atual=[sma['ABEV'].json(),sma["VALE"].json(),sma['TTWO'].json(),sma['WEGE'].json()]
            
    #fechamento
    for i  in range(len(atual)):
        timeseries=atual[i]["Time Series (5min)"]
        close= [float(item["4. close"]) for item in timeseries.values()]
        
        ativo=''
        if i==0:
            ativo='ABEV'
        elif i==1:
            ativo="VALE"
        elif i==2:
            ativo="TTWO"
        else:
            ativo="WEGE"

        valores=[]

        for i in range(len(close)):
            valores.append(i)

        plt.plot(valores,close[::-1])
        plt.savefig("C:/Users/Andre Luiz/AppData/Local/Programs/Python/Python37/Scripts/Projeto/venv/Scripts/appstatic/images/"+ativo+'_close'+'.png')
        plt.close()
        
    #volume    
    for i  in range(len(atual)):
        timeseries=atual[i]["Time Series (5min)"]
        close= [float(item["5. volume"]) for item in timeseries.values()]
        
        ativo=''
        if i==0:
            ativo='ABEV'
        elif i==1:
            ativo="VALE"
        elif i==2:
            ativo="TTWO"
        else:
            ativo="WEGE"

        valores=[]

        for i in range(len(close)):
            valores.append(i)
            
        plt.bar(valores,close[::-1])
        plt.savefig("static/images/"+ativo+'_volume'+'.png')
        plt.close()
    #media movel simples
    for i in range(len(sma_atual)):
        timeseries=sma_atual[i]["Technical Analysis: SMA"]
        close= [float(dado["SMA"]) for dado in timeseries.values()]
        
        ativo=''
        if i==0:
            ativo='ABEV'
        elif i==1:
            ativo="VALE"
        elif i==2:
            ativo="TTWO"
        else:
            ativo="WEGE"

        valores=[]

        for i in range(len(close)):
            valores.append(i)
            
        plt.plot(valores,close[::-1])
        plt.savefig("static/images/"+ativo+'_sma'+'.png')
        plt.close()
    
#funçoes que realizam as requisições, executam uma pausa para não passar o limite do alpha vantage
def req_abev():
    global data
    global sma
    data['ABEV']= requests.get("https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=ABEV3.SA&interval=5min&apikey=G6IBSDLXJ0V0KXQW")
    sma["ABEV"]= requests.get("https://www.alphavantage.co/query?function=SMA&symbol=ABEV3.SA&interval=5min&time_period=10&series_type=close&apikey=G6IBSDLXJ0V0KXQW")
    time.sleep(50)
def req_vale():
    global data
    global sma
    data["VALE"]= requests.get("https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=VALE3.SA&interval=5min&apikey=18947984687123")
    sma["VALE"]= requests.get("https://www.alphavantage.co/query?function=SMA&symbol=VALE3.SA&interval=5min&time_period=10&series_type=close&apikey=419874984189541")
    time.sleep(50)
def req_ttwo():
    global data
    global sma
    data["TTWO"]=requests.get("https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=TTWO&interval=5min&apikey=129849840984984984")
    sma["TTWO"]= requests.get("https://www.alphavantage.co/query?function=SMA&symbol=TTWO&interval=5min&time_period=10&series_type=close&apikey=132186498749849")
    time.sleep(50)
def req_wege():
    global data
    global sma
    data["WEGE"]=requests.get("https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=WEGE3.SA&interval=5min&apikey=2321684684818")
    sma["WEGE"]=requests.get("https://www.alphavantage.co/query?function=SMA&symbol=WEGE3.SA&interval=5min&time_period=10&series_type=close&apikey=98098406941965481")
    time.sleep(50)
def Nomebunito():
	while True:
	    req_ttwo()
	    req_vale()
	    req_wege()
	    req_abev()
	    graph()
	    time.sleep(60)#pausa para fechar 5 minutos

## carregamento das paginas 
def Paginas():
	## pagina principal
	@app.route('/selection', methods =['GET'])
	@app.route('/', defaults ={'user':None})
	def selection(user):
		return render_template('selection.html')

	## pagina da Ambev
	@app.route('/Ambev', methods =['GET'])
	def Ambev():
		return render_template('Ambev.html')

	## pagina da Weg
	@app.route('/WEGE3', methods =['GET'])
	def WGE3():
		return render_template('WEGE3.html')

	## pagina da TAKETOW
	@app.route('/Petr4', methods =['GET'])
	def Petr4():
		return render_template('Petr4.html')

	## pagina da Vale
	@app.route('/Vale3', methods =['GET'])
	def Vale3(): 	
		return render_template('Vale3.html')

## thread para carregamneto paralelo da aplicaçao 
t1=threading.Thread(target=Nomebunito)
t1.start()
Paginas()
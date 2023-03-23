import json
import telebot
import os
from datetime import datetime

CHAVE_API = ''
bot_user_name = ""
URL = ""

bot = telebot.TeleBot(CHAVE_API)

data_dic = ['Day','Profit','QtdOpDay','QtdOpWinDay', 'QtdOpLossDay', 'WinPerc',
            'TotalDays','TotalProfit','TotalOp','QtdOpWinTotal','QtdOpLossTotal',
            'TotalWinPerc','PositiveDays','NegativeDays','ProfitAverage/Day','ProfitAverage/Op']

month = ['JAN','FEV','MAR','APR','MAY','JUN','JUL','AUG','SEP','OCT','NOV','DEC']

#func = predicate
#command = mensgem que tenho q mandar
def handleMessage(data): 
    message = data.text
    message = message.replace('# - - - - RESULTADO DIÁRIO - - - - # ', '')
    message = message.replace('# - - - - RESULTADO PERÍODO - - - #', '')
    message = message.replace('# - - - - - - - - - - - - - - - - - - - - - #', '')
    message = message.replace('R$', '')
    message = message.replace('  ', '')
    message = message.replace(': ', ':')
    newData = message.split('\n')
    while("" in newData):
        newData.remove('')
    while(" " in newData):
        newData.remove(' ')
    dictionary = {}
    for i in range(newData.__len__()):
        var = newData[i].split(':')
        dictionary[data_dic[i]] = var[1]

    return dictionary

def writeDown(values):

    date_format = '%d/%m/%Y'
    date_obj = datetime.strptime(values['Day'], date_format)
    monthName = month[date_obj.month-1]

    profit = int(float(values['Profit']))
    opWins = int(values['QtdOpWinDay'])
    opLoss = int(values['QtdOpLossDay'])
    if(opWins > 0 and opLoss> 0):
        percentage = int((opWins / (opWins + opLoss)) * 100)
    else:
        percentage = 0
    thisMonthValue = {
            "month":monthName,
            "Date": str(date_obj),
            "DayProfit": profit,
            "totalProfit": profit,
            "QtdOpWinTotal": opWins,
            "QtdOpLossTotal": opLoss,
            "TotalWinPerc": percentage
        }
    
    jsonString = json.dumps([thisMonthValue], indent=4)
    
    
    
    try:
        with open(monthName+".json", "r") as fileToRead:

            data = json.load(fileToRead)

            obj = data[data.__len__()-1]

            thisMonthValue['totalProfit'] += obj['totalProfit']
            thisMonthValue['QtdOpWinTotal'] += obj['QtdOpWinTotal']
            thisMonthValue['QtdOpLossTotal'] += obj['QtdOpLossTotal']

            percentage = int((thisMonthValue['QtdOpWinTotal'] / (thisMonthValue['QtdOpWinTotal'] + thisMonthValue['QtdOpLossTotal'])) * 100)
            thisMonthValue['TotalWinPerc'] = percentage

            data.append(thisMonthValue)
            jsonString = json.dumps(data, indent=4)

            with open(monthName+".json", "w") as fileToWrite:
                fileToWrite.write(jsonString)
                fileToWrite.close()

    except FileNotFoundError:                   #First time creating month File
        with open(monthName+".json", "w") as file:
            file.write(jsonString)
            file.close()
            
def verificar(mensagem):
    return True

@bot.message_handler(func=verificar)
def responder(message):
    values = handleMessage(message)
    writeDown(values)
    bot.send_message(message.chat.id, 'success')



bot.delete_webhook()
bot.polling()
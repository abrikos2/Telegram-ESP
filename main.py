import logging
import asyncio
import os 
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
import json
import socket
import keyboards
with open(r"C:\Users\danya\Desktop\Python\Rasbery\ESP_BOT_CONTROL\config.json") as f:
    data = json.load(f)
API_TOKEN = data["API_TOKEN"]
dp = Dispatcher()
bot = Bot(API_TOKEN)
data = {}
sockets = {} 
socket.setdefaulttimeout(2)
port = 5055
selectedESP = 0
async def loadSockets():
    with open(r"C:\Users\danya\Desktop\Python\Rasbery\2.0_beta\ESP.json", "r+")as f:
        json_data = json.load(f)["ListofESP"]
        x = 0
        for key in json_data:
            temp = ",".join(key.keys())
            try:
                sockets[temp] = socket.socket()
                sockets[temp].connect((json_data[x][temp]["IP"], port))
            except Exception as e:
                print(e)
                pass
            finally:
                x+=1
    f.close
async def CheckName(message: types.Message):
    with open(r"C:\Users\danya\Desktop\Python\Rasbery\2.0_beta\ESP.json", "r+", encoding="utf-8") as f:
        json_data= json.load(f)["ListofESP"]
        selectedESP = 0
        for key in json_data:
            try:
                if message.text in key[f"ESP{selectedESP}"]["Name"]:
                    return True
                else:
                    selectedESP+=1 
            except Exception as e:
                print(e)
async def CheckFunc(message: types.Message):
    with open(r"C:\Users\danya\Desktop\Python\Rasbery\2.0_beta\ESP.json", "r+", encoding="utf-8") as f:
        json_data= json.load(f)["ListofESP"]
        selectedESP = 0
        for key in json_data:
            try:
                if message.text in key[f"ESP{selectedESP}"]["Funcs"]:
                    return True
                else:
                    selectedESP+=1 
            except Exception as e:
                print(e)
async def FuncstoNumber(message: types.Message):
    with open(r"C:\Users\danya\Desktop\Python\Rasbery\2.0_beta\ESP.json", "r+", encoding="utf-8") as f:
        json_data= json.load(f)["ListofESP"]
        selectedESP = 0
        for key in json_data:
            try:
                if message.text in key[f"ESP{selectedESP}"]["Funcs"]:
                    return f"ESP{selectedESP}"
                else:
                    selectedESP+=1 
            except Exception as e:
                print(e)
async def ChecktoNumber(message: types.Message):
    with open(r"C:\Users\danya\Desktop\Python\Rasbery\2.0_beta\ESP.json", "r+", encoding="utf-8") as f:
        json_data= json.load(f)
        statment = []
        try:
            for i in range(json_data["AmountofESP"]):
                statment.append(await Check(f"ESP{i}"))
                await bot.send_message(message.chat.id, f"{json_data["ListofESP"][i][f"ESP{i}"]["Name"]}:{'❌' if type(statment[i]) == bool else '✅'}")    
        except Exception as e:
            print(e)
async def Send(message: types.Message):
    try:
        msg = message.text + "\n"
        sockets[await FuncstoNumber(message)].send(msg.encode())
        await bot.send_message(message.chat.id, text=f"Отправленно")
    except socket.error:
        await bot.send_message(message.chat.id, text=f"Управление видео не доступно")
async def Check(x):
        Exc = False
        try:
            sockets[x].send("Check".encode())
        except Exception as e:
            print(f"{e} send")
            Exc = True
            return True 
        finally:
            if Exc == True:
                return True
            else:
                while True:
                    msg = sockets["ESP{x}"].recv(1024).decode()
                    if(msg[-1] == "E"): 
                        print(msg)
                        Exc = False
                        return msg
                
                
@dp.message(F.text, Command("start"))
async def startCommand(message: types.Message):
    await bot.send_message(message.chat.id, text = "Hello", reply_markup=keyboards.keyboardMain())
    
@dp.message(F.text, Command("AddName"))
async def AddName(message:types.Message):
    try:
        if message.text[9:] != "":
            data["Name"] =message.text[9:]
            await bot.send_message(message.chat.id, "Успешно добавленно")
        if message.text[9:] == "":
            await bot.send_message(message.chat.id, "Неверный ввод")
    except Exception as e:
        print(e)
        await bot.send_message(message.chat.id, "Возникла ошибка напишите разработчику(контакт в описсании)")
@dp.message(F.text, Command("AddIP"))
async def AddIP(message:types.Message):
    try:
        try:
            socket.inet_aton(message.text[8:])
            data["IP"] = message.text[7:]
            await bot.send_message(message.chat.id, "Успешно добавленно")
        except socket.error:
            await bot.send_message(message.chat.id, "Неверный ввод")
    except Exception as e:
        print(e)
        await bot.send_message(message.chat.id, "Возникла ошибка напишите разработчику(контакт в описсании)")
    
@dp.message(F.text, Command("Compile"))
async def Compile():
    with open(r"C:\Users\danya\Desktop\Python\Rasbery\2.0_beta\ESP.json", "r+", encoding="utf-8")as f:
        json_data = json.load(f)
        json_data["ListofESP"] = *json_data["ListofESP"],{f"ESP{json_data["AmountofESP"]}": {"Name":data["Name"], "IP":data["IP"], "CountFuncs": 0, "Funcs":{}}}
        json_data["AmountofESP"] += 1
        json.dump(json_data, f)                       
    with open(r"C:\Users\danya\Desktop\Python\Rasbery\2.0_beta\ESP.json", "w", encoding="utf-8") as f:
        json.dump(json_data, f, indent=2, ensure_ascii=False)
        
@dp.message(F.text, Command('Create'))
async def CreateNew(message:types.Message):
    await bot.send_message(message.chat.id, "Процесс создания новой ESP происходит следующими командами по порядку с пробелами:\n/AddName Название кнопки\n/AddIP IP в локальной сети\nВ конце необходимо прописать команду /Compile\nдля добавления функиональности введите /SelectESP Название функции, а после /AddFunc")

@dp.message(F.text, Command("SelectESP"))
async def SelectESP(message:types.Message):
    global selectedESP
    with open(r"C:\Users\danya\Desktop\Python\Rasbery\2.0_beta\ESP.json", "r+", encoding="utf-8") as f:
        json_data= json.load(f)["ListofESP"]
        selectedESP = 0
        for key in json_data:
            try:
                if message.text[11:] in key[f"ESP{selectedESP}"]["Name"]:
                    pass
                else:
                    selectedESP+=1 
            except Exception as e:
                print(e)
                
@dp.message(F.text, Command("AddFunc"))
async def AddFunc(message:types.Message):
    global selectedESP
    with open(r"C:\Users\danya\Desktop\Python\Rasbery\2.0_beta\ESP.json", "r+", encoding="utf-8") as f:
        json_data = json.load(f)
        json_data["ListofESP"][selectedESP][f"ESP{selectedESP}"]["CountFuncs"]+=1
        json_data["ListofESP"][selectedESP][f"ESP{selectedESP}"]["Funcs"] = *json_data["ListofESP"][selectedESP][f"ESP{selectedESP}"]["Funcs"], *{message.text[9:]}
        json.dump(json_data, f)                       
    with open(r"C:\Users\danya\Desktop\Python\Rasbery\2.0_beta\ESP.json", "w", encoding="utf-8") as f:
        json.dump(json_data, f, indent=2, ensure_ascii=False)
              
@dp.message(F.text)
async def adminCommands(message: types.Message):
    if(await CheckName(message) == True):
        await bot.send_message(message.chat.id, f"Выбрано {message.text}", reply_markup=keyboards.keyboardFunc(message) )
    if(message.text == "Назад"):
        await bot.send_message(message.chat.id, text = "Hello", reply_markup=keyboards.keyboardMain())
    if(await CheckFunc(message) == True):
        await Send(message)
    if(message.text == "Проверить состояние подключения"):
        await ChecktoNumber(message)
    

async def main():
    logging.basicConfig(level=logging.INFO)
    bot = Bot(token=API_TOKEN)
    await dp.start_polling(bot)
    
    
    
if __name__ == "__main__":
    asyncio.run(loadSockets())
    asyncio.run(main())
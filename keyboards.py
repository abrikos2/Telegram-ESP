from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram import types
import json


def keyboardMain():
    with open(r"C:\Users\danya\Desktop\Python\Rasbery\2.0_beta\ESP.json", "r+", encoding="utf-8") as f:
        json_data = json.load(f)["ListofESP"]
        try:
            builder = ReplyKeyboardBuilder()
            for i, key in enumerate(json_data):
                builder.button(text=key[f"ESP{i}"]["Name"])
            builder.button(text="Проверить состояние подключения")
            builder.adjust(2)
            f.close()   
            return builder.as_markup(resize_keyboard=True, input_field_placeholder="Выберите пункт меню")
        except Exception as e:
                print(e)
def keyboardFunc(message: types.Message):
    with open(r"C:\Users\danya\Desktop\Python\Rasbery\2.0_beta\ESP.json", "r+", encoding="utf-8") as f:
        json_data= json.load(f)["ListofESP"]
        selectedESP = 0
        for key in json_data:
            try:
                if message.text in key[f"ESP{selectedESP}"]["Name"]:
                    builder = ReplyKeyboardBuilder()
                    for i in json_data[selectedESP][f"ESP{selectedESP}"]["Funcs"]:
                        builder.button(text=i)
                        builder.button(text="Назад")
                        builder.adjust(2)
                        f.close()
                        return builder.as_markup(resize_keyboard=True, input_field_placeholder="Выберите пункт меню")
                else:
                    selectedESP+=1 
            except Exception as e:
                print(e)
    
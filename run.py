import conf
from classes import OKXex, Bot




def start():
    Bot().chek_files()  # Проверяем существование файла <trades.json>
    Bot().fill_trades_file()

def trades_bot():
    pass


















if __name__ == '__main__':
    try:
        start()
        while True:
            trades_bot()

    except Exception as e:
        print(e)




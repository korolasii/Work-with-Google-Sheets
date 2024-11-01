import gspread
from google.oauth2.service_account import Credentials
from sendMes import startBot, openJson
from progress.bar import IncrementalBar


#Open sheet which we want
def open_sheet(spreadsheet, name, headers):
    worksheet = spreadsheet.worksheet(name)
    
    data = worksheet.get_all_records(expected_headers=headers)
    return data



#function which take Google Table and orders from Rozetka after this it found same id and paste in sheet name of order
def work_with_pages(nameSeller, workSheetName):
    table = openJson("data.json")
    
    try:
        table[nameSeller]
    except:
        print("Неправильно указано название магазина")
        return call_work_with_pages()
    
    credentials = Credentials.from_service_account_file(
        table[nameSeller]['url'],
        scopes=["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
    )

    gc = gspread.authorize(credentials)
    spreadsheet = gc.open_by_key(table[nameSeller]['id'])

    headers_work = [
        "Дата перерахування",
        "Дата та час платежу",
        "Сума платежу",
        "Сума комісії з отримувача",
        "Сума комісії з платника",
        "Сума перерахованих коштів",
        "Назва проекту",
        "№ замовлення",
        "% Розетки",
        "Доставка",
        "Собівартість",
        "Дохід",
        "Кіл-ть",
        "ціна за одиницю",
    ]

    work_page = open_sheet(spreadsheet, workSheetName, headers_work)
    
    listOrder = []
    
    print('Запросы и сохранение заказов')
    
    barResponse = IncrementalBar('Countdown', max = 20)
    
    for i in range(1, 21):
        response = startBot(nameSeller, i)
        [listOrder.append(item) for item in response]
        barResponse.next()
        
    barResponse.finish()
    
    row = 2
    
    listId = []
    
    for i in work_page:
        id = i['№ замовлення']
        if id == '':
            break
        else:
            listId.append(id)
            
    print('Поиск товаров и внисение изминений в таблице')
    
    barUpdate = IncrementalBar('Countdown', max = len(listId))
    
    for row, i in enumerate(listId):
        for item in listOrder:
            if i == item['id']:
                spreadsheet.worksheet(workSheetName).update(range_name=f"O{row+2}", values=[[item['items_photos'][0]['item_name']]])
                break
        row += 1
        barUpdate.next()
    
    barUpdate.finish()

#call work function
def call_work_with_pages():
    nameSeller = input('Введите название магазина: ')
    work_with_pages(nameSeller, 'Today')
    
if __name__ == "__main__":
    call_work_with_pages()
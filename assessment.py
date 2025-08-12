import requests
from bs4 import BeautifulSoup
import pandas as pd

def AddEmptySpaces(data, max_x, max_y):
    new_rows_to_add = []
    for x in range(max_x + 1):
        for y in range(max_y + 1):
            if not ((data[0] == x) & (data[2] == y)).any():
                new_rows_to_add.append([x, ' ', y])
    data = pd.concat([data, pd.DataFrame(new_rows_to_add)])
    return data

def PrintMessage(data):
    # Col = 'x, symbol, y'
    data.drop(index=0, inplace = True)
    data[0] = data[0].astype(int)
    data[2] = data[2].astype(int)
    max_x = data[0].max()
    max_y = data[2].max()
    data = AddEmptySpaces(data, max_x, max_y)
    # Change ascending to make upside down or reverse
    data = data.sort_values(by=[2, 0], ascending=[True, True])

    message = {}
    start = 0 
    row_count = 0
    for index in range(len(data) - 1):
        if (data.iloc[index, 2] != data.iloc[index + 1, 2]):
            message[row_count] = ''.join(data.iloc[start:index, 1].astype(str))
            start = index + 1
            row_count += 1
    #Account for last row
    message[row_count] = ''.join(data.iloc[start:len(data), 1].astype(str))

    for key, value in message.items():
        print(value)

def GetMessage(link):
    response = requests.get(link)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    table_body = soup.table
    rows = table_body.find_all('tr')
    data = []
    for row in rows:
        cols = row.find_all('span')
        data.append([col.get_text() for col in cols])
    data = pd.DataFrame(data)
    PrintMessage(data)

def main(): 
    link = 'https://docs.google.com/document/d/e/2PACX-1vTER-wL5E8YC9pxDx43gk8eIds59GtUUk4nJo_ZWagbnrH0NFvMXIw6VWFLpf5tWTZIT9P9oLIoFJ6A/pub'
    GetMessage(link)

if __name__ == '__main__':
    main()
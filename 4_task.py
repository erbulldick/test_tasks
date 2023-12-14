import requests
from bs4 import BeautifulSoup

url = 'https://terrikon.com/football/italy/championship/'
response = requests.get(url)

soup = BeautifulSoup(response.text, 'html.parser')

table = soup.find('table', class_='colored')

data = []
for row in table.find_all('tr'):
    columns = row.find_all('td')
    if len(columns) == 6:
        player_rank = columns[0].text.strip()
        player_name = columns[1].text.strip()
        team_name = columns[2].text.strip()
        goals_scored = columns[3].text.strip()
        games_played = columns[4].text.strip()
        average_goals = columns[5].text.strip()
        data.append((player_rank, player_name, team_name, goals_scored, games_played, average_goals))

formatted_data = '<table>'
formatted_data += '<th></th><th>Игрок</th><th>Команда</th><th>Забито</th><th>Игр</th><th>Среднее</th>'
for player in data:
    formatted_data += f'<tr><td>{player[0]}</td><td>{player[1]}</td><td>{player[2]}</td><td>{player[3]}</td><td>{player[4]}</td><td>{player[5]}</td></tr>' + '\n'
formatted_data += '</table>'

print(formatted_data)

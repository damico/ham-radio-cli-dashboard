import curses

from helper import read_json_url


def get_current_observation(pws_id, api_key):
    url = "https://api.weather.com/v2/pws/observations/current?stationId=" + pws_id + "&format=json&units=m&apiKey=" + api_key
    json = read_json_url(url)
    return json


def print_wu_data(win, pws_id, api_key):
    wu_json = get_current_observation(pws_id, api_key)
    win.addstr(2, 5, 'Observation:', curses.A_NORMAL)
    win.addstr(2, 20, str(wu_json['observations'][0]['obsTimeUtc'])[:19] + ' (UTC)', curses.A_NORMAL)
    win.addstr(3, 5, 'Temperature:', curses.A_NORMAL)
    win.addstr(3, 20, str(wu_json['observations'][0]['metric']['temp']) + ' ºC', curses.A_NORMAL)
    win.addstr(4, 5, 'Wind Chill:', curses.A_NORMAL)
    win.addstr(4, 20, str(wu_json['observations'][0]['metric']['windChill']) + ' ºC', curses.A_NORMAL)
    win.addstr(5, 5, 'Wind Speed:', curses.A_NORMAL)
    win.addstr(5, 20, str(wu_json['observations'][0]['metric']['windSpeed']) + ' km/h', curses.A_NORMAL)
    win.addstr(6, 5, 'Wind Dir:', curses.A_NORMAL)
    win.addstr(6, 20, str(wu_json['observations'][0]['winddir']) + ' °', curses.A_NORMAL)
    win.addstr(7, 5, 'Wind Gust:', curses.A_NORMAL)
    win.addstr(7, 20, str(wu_json['observations'][0]['metric']['windGust']) + ' km/h', curses.A_NORMAL)
    win.addstr(8, 5, 'Humidity:', curses.A_NORMAL)
    win.addstr(8, 20, str(wu_json['observations'][0]['humidity']) + ' %', curses.A_NORMAL)
    win.addstr(9, 5, 'Pressure:', curses.A_NORMAL)
    win.addstr(9, 20, str(wu_json['observations'][0]['metric']['pressure']) + ' Hpa', curses.A_NORMAL)
    win.addstr(10, 5, 'UV Index:', curses.A_NORMAL)
    win.addstr(10, 20, str(wu_json['observations'][0]['uv']), curses.A_NORMAL)
    win.addstr(11, 5, 'S. Radiation:', curses.A_NORMAL)
    win.addstr(11, 20, str(wu_json['observations'][0]['solarRadiation']) + ' w/m²', curses.A_NORMAL)
    win.addstr(12, 5, 'Preciptation', curses.A_NORMAL)
    win.addstr(12, 20, str(wu_json['observations'][0]['metric']['precipTotal']) + ' mm', curses.A_NORMAL)
    win.addstr(13, 5, 'Dew Point:', curses.A_NORMAL)
    win.addstr(13, 20, str(wu_json['observations'][0]['metric']['dewpt']) + ' ºC', curses.A_NORMAL)

#!/usr/bin/env python

import requests
import json
from datetime import datetime

# pincodes = ['110001', '110002', '110003', '110004', '110005', '110006', '110007', '110008', '110009', '110010', '110011', '110012', '110013', '110014', '110015', '110016', '110017', '110018', '110019', '110020', '110021', '110022', '110023', '110024', '110025', '110026', '110027', '110028', '110029', '110030', '110031', '110032', '110033', '110034', '110035', '110036', '110037', '110038', '110039', '110040', '110041', '110042', '110043', '110044', '110045', '110046', '110047', '110048', '110049', '110050', '110051', '110052', '110053', '110054', '110055', '110056', '110057', '110058', '110059', '110060', '110061', '110062', '110063', '110064', '110065', '110066', '110067', '110068', '110069', '110070', '110071', '110072', '110073', '110074', '110075', '110076', '110077', '110078', '110079', '110080', '110081', '110082', '110083', '110084', '110085', '110086', '110087', '110088', '110089', '110090', '110091', '110092', '110093', '110094', '110095', '110096', '122001', '121002', '121001', '201009']
pincodes = ["110085", "110052", "110034", "110035", "110009", "110088", "110086", "110026", "110015", "110087", "110027", "110018", "110058"]

bot_token = '1747353255:AAE60l-9UBv4PYfK9NPcvk9fNiyCi1aZFN8'
bot_chatID = '-521153023'


def get_vaccination_centers_list(pincode):
	print("calling cowin api for pincode:", pincode)
	headers = {
		'Accept': 'application/json, text/plain, */*',
		'Accept-Language': 'en-US,en;q=0.5',
		'Connection': 'keep-alive',
		'Origin': 'https://www.cowin.gov.in',
		'Referer': 'https://www.cowin.gov.in/',
		'TE': 'Trailers',
		'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:88.0) Gecko/20100101 Firefox/88.0',
	}
	date = datetime.today().strftime('%d-%m-%Y')
	params = (
		('pincode', pincode),
		('date', date),
	)

	response = requests.get('https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin', headers=headers, params=params)

	return response.json()


def parse_response(res):
	available_centers = []
	for center in res.get('centers',[]):
		for session in center.get('sessions',[]):
			if session.get('min_age_limit')==18 and session.get('available_capacity')>0:
				available_centers.append([center['name'],session['date'],session['vaccine'], str(session['available_capacity'])])

	print("Available Centers for above pincode: ", len(available_centers))

	return available_centers


def send_message(available_centers, pincode):
	print("sending message to telegram")
	bot_message = "PINCODE: " + pincode + '\n'
	for center in available_centers:
		bot_message += ' --- '.join(center)
		bot_message += '\n'

	send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message
	response = requests.get(send_text)


def main():
	print("started fetching vaccination centers at " + str(datetime.today()) + " for pincodes:", ','.join(pincodes))
	for pincode in pincodes:
		res = get_vaccination_centers_list(pincode)
		# This list can be sent to users as email/sms etc to notify about the centers opened at the moment.
		available_centers = parse_response(res)
		if available_centers:
			send_message(available_centers, pincode)


if __name__ == '__main__':
	main()

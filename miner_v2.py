import requests
import datetime
import json
from discord_hooks import Webhook
from twilio.rest import Client
from time import sleep
import os

def tempCheck(temp):
	num = '1231231234'
	twilioNum = '123456456454'
	client = Client("ID", "ID")
	client.api.account.messages.create(
	    to=num,
	    from_=twilioNum,
	    body="MINER IS OVER {}DEGREES, CALL {} TO ALERT ME".format(temp,num))

def start_bot():
	degree_sign= u'\N{DEGREE SIGN}'
	url = 'https://discordapp.com/api/webhooks/123453/12345654'

	link = "http://192.xxx.x.xxx:42000/getstat"
	r = requests.get(url=link)
	data = json.loads(r.text)
	uptime = str(datetime.datetime.now()- datetime.datetime.fromtimestamp(int(data['start_time'])))[:-7]

	gpuTxt = ""
	totalSpeed = 0
	totalWatt = 0
	for gpu in data['result']:
		gpuTxt += "\t{} : {}{}C {}W {}Sol/s\n".format(str(gpu['gpuid']),str(gpu['temperature']),degree_sign,str(gpu['gpu_power_usage']),str(gpu['speed_sps']))
		totalSpeed += gpu['gpu_power_usage']
		totalWatt += gpu['speed_sps']
		if gpu['temperature'] >= 90:
			tempCheck(gpu['temperature'])

	msgTxt = "```\n{}Sol/s {}W\n--------------\nServer: {}\nUptime: {}\nGPU's:\n{}\n```".format(str(totalSpeed),str(totalWatt),data['current_server'],str(uptime),gpuTxt)

	msg = Webhook(url,msg=msgTxt)
	msg.post()


def main():
	print("STARTING BOT....")
	try:
		while True:
			start_bot()
			sleep(900)
	except:
		print("ENDING BOT...")
		os.system('killall -9 python3')

if __name__ == '__main__':
	main()

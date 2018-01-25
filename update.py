import requests
import datetime
import json
from discord_hooks import Webhook
'''
2080SOL/S 579W
--------------
Mining: nyz.minex.
Uptime: start_time - now
GPU's:
	0 : 50* 104W 524 SOL 
	0 : 50* 104W 524 SOL 
	0 : 50* 104W 524 SOL 
	0 : 50* 104W 524 SOL
'''

degree_sign= u'\N{DEGREE SIGN}'
url = 'webhook link'
link = "http://192.168.x.x:42000/getstat" # miner link
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

msgTxt = "```\n{}Sol/s {}W\n--------------\nServer: {}\nUptime: {}\nGPU's:\n{}\n```".format(str(totalSpeed),str(totalWatt),data['current_server'],str(uptime),gpuTxt)

msg = Webhook(url,msg=msgTxt)
msg.post()

import smtplib
from email.message import EmailMessage
from oneday import oneday_table
from oneweek import oneweek_table
from onemonth import onemonth_table

from utils import get_lastDate,cc_path,to_path
from satcli import satcli_uto

from contrat_oneday import tecnow_up
import datetime
from env import config

def emailing(group):
	EMAIL_ADDRESS=config('EMAIL_ADDRESS',default=None)
	EMAIL_PASSWORD=config('EMAIL_PASSWORD',default=None)
	cc= ', '.join(open(cc_path).read().splitlines())
	to=', '.join(open(to_path).read().splitlines())
	#ahmed.lmimouni@kyntus.com
	#benserya.dev@gmail.com

	
	current_date = datetime.date.today()
	current_week_number = current_date.isocalendar()[1]
	if current_date.weekday() == 0:
		current_week_number-=1
	day = current_date.strftime('%d')

	# Get the month (1 to 12)
	month = current_date.strftime('%m')

	date_=get_lastDate()
	html=f"<br><h3 style=''>Bonjour,<br><br>Vous trouverez ci-dessous l’état de la SATCLI {group} au {date_} :<h3>"
	html+=f"<h3 style=''>•	Ci-dessous le résultat de la SATCLI de la S{current_week_number} par journée :<h3>"
	html+= oneday_table(group)

	html+=f"<br><h3 style=''>•	Ci-dessous l’évolution de la SATCLI du mois en cours par semaine :<h3><br>"
	html+=oneweek_table(group)

	html+=f"<br><h3 style=''>•	Ci-dessous l’évolution de la SATCLI par mois:<h3><br>"
	html+=onemonth_table(group)
	msg = EmailMessage()
	msg['Subject'] = f'Rapport quotidien SATCLI {group} du {date_}'#Rapport quotidien SATCLI SAV du 10/07 et récapitulatif de la S27
	msg['From'] = EMAIL_ADDRESS

	msg['To'] =to#'benserya.dev@gmail.com, ahmed.lmimouni@kyntus.com'#'sidi.hamzaoui@kyntus.com, wael.hermi@kyntus.com, romain.carneiro@kyntus.com, bastien.prieur@kyntus.com, ahmed.bougandouf@kyntus.com, junior.okabe@kyntus.com, herve.monnier@kyntus.com, arlety.nsikoto@kyntus.com, sahbi.assadi@kyntus.com, rosly.bernadel@kyntus.com, lionel.simeon@kyntus.com, khalid.lakhal@kyntus.com, riad.lahcene@kyntus.com, taoufiq.hamama@kyntus.com, pascal.fayo@kyntus.com, herve.monnier@kyntus.com, rachid.ouhmimid@kyntus.com, jean-baptiste.audureau@kyntus.com, karim.jolo@kyntus.com, youcef.abdoune@kyntus.com, pacome.yenou@kyntus.com, sofiane.benaceur@kyntus.com, mostafa.el-mrabet@kyntus.com, yassine.baallal@kyntus.com, bastien.prieur@kyntus.com, laila.nafia@kyntus.com'

	msg['Cc'] = cc#'ahmed.lmimouni@kyntus.com, ayoub.moujaoui@kyntus.com, salah.zemmouri@kyntus.com, nadia.tirhanime@kyntus.com, ikram.bouterfas@kyntus.com, lineda.haouas@kyntus.com, quentin.tricheux@kyntus.com, hicham.hiyani@kyntus.com, youcef.ameur@kyntus.com, younes.herras@kyntus.com, support.developpement@kyntus.com'# zhnyassirkpi@gmail.com, saidi.kyntus@gmail.com'
	msg.set_content(html, subtype='html')
	with smtplib.SMTP_SSL("smtp.ionos.fr", 465) as smtp:
		smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
		smtp.send_message(msg)


import time,sys
if __name__ == '__main__':
	#time.sleep(7*60*60)
	today = datetime.date.today()
	#one_day_ago = today - datetime.timedelta(days=1)
	tecnow_up()
	# Check if today is Sunday (where Monday is 0 and Sunday is 6)
	if today.weekday() == 6:
		print("Today is Sunday.")
		#time.sleep(50400)
		sys.exit()
	satcli_uto()

	group='RACC'
	emailing(group)
	group='SAV'
	emailing(group)
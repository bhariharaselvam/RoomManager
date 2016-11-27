import smtplib



from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class Mail_service:
	def __init__(self):
		self.website='smtp.gmail.com'
		self.port='587'
		self.username='selvamsamy2@gmail.com'
		self.password=''


		self.server=None
		self.recievers=[]
		self.message=""
		try:
			self.server = smtplib.SMTP(self.website, int(self.port))
			self.server.ehlo()
			self.server.starttls()
			self.server.ehlo()
			self.server.login(self.username, self.password)
		except Exception:
			pass


	def add_receiver(self, receiver):
		self.recievers=receiver



	def add_message(self, subject, content):
		msg = MIMEMultipart('alternative')
		msg['Subject'] = subject
		msg['From']=self.username
		html="""\
			<html>

		  		<body>
		    		<p>Hi <br>
		       			"""+content+"""
		    		</p>
				<br>
				Thanks <br>
				<u>Wakeup Room Manager</u>
		  		</body>
			</html>
		"""
		part1 = MIMEText(html, 'html')
		msg.attach(part1)
		self.message=msg.as_string()



	def send_mail(self):
		self.server.sendmail(self.username, self.recievers, self.message)
		return "Mail has been successfully sent to "+",".join(self.recievers)
import smtplib
import getpass
website='smtp.gmail.com'
server = smtplib.SMTP(website, 587)
server.ehlo()
server.starttls()
server.ehlo()
username=raw_input('Username:');
pw=getpass.getpass();
password=pw;
server.login(username, password)
print "Hello "+username+"! \n You are connected with the "+website+"\nYou can send your mail\n"
#password=raw_input('enter your password : ');
toaddress=raw_input('To address :');
sub=raw_input('Subject :');
print "Enter the content. Your last line should be as 'end'"
line="";
text="";
while line != "end":
	text+=line+"\n";
	line=raw_input();


message = 'Subject: %s\n\n%s' % (sub, text)
server.sendmail(username, toaddress, message);
print sub+" has been send to "+toaddress
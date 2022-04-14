from bs4 import BeautifulSoup
from datetime import date
import datetime
import pdfkit
import os

TEMPLATE = 'Invoice-Template.html'
INVOICE_FILES_LOCATION = "Receipts"

def invoice(names,txn_list):
	f = open(TEMPLATE)
	soup = BeautifulSoup(f,'html.parser')

	payment_date,payment_mode,invoice,txn_id,course,total_members,amount_per_person,total_amount,amount_paid = txn_list

	strings = [name for name in soup.find_all("font") if name.string]

	count = 0

	for tag in strings:
		text = tag.string

		if 'DATE' in text:
			tag.string = "DATE: "+datetime.date.today().strftime("%d/%m/%Y")

		elif 'INVOICE NO' in text:
			tag.string = "INVOICE NO: "+str(invoice)

		elif 'Payment Mode' in text:
			tag.string = "Payment Mode: "+payment_mode

		elif 'Transaction' in text:
			tag.string = "Transaction ID: "+txn_id

		elif 'Payment Date' in text:
			tag.string = "Payment Date: "+payment_date

		elif 'Course' in text:
			tag.string = course

		elif 'Members' in text:
			tag.string = str(total_members)

		elif 'price per person' in text:
			tag.string = "₹"+str(int(amount_per_person))

		elif 'total price' in text:
			tag.string = "₹"+str(int(total_amount))

		elif 'total rupees' in text:
			tag.string = "₹"+str(int(total_amount))

		elif 'total paid' in text:
			tag.string = "₹"+str(int(amount_paid))

		elif text == 'NAME':
			if count<len(names):
				tag.string = names[count]
				count+=1
			else:
				tag.clear()

	k = open("invoice_writen.html","w")
	k.write(str(soup))

	file_name = str(invoice)+'.pdf'
	file_name = os.path.join(INVOICE_FILES_LOCATION,file_name)

	pdfkit.from_file('invoice_writen.html',file_name)
	print('Created ',file_name)

	return file_name
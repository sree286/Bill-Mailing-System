import cv2
import pytesseract
from datetime import datetime

def get_payment_details(image):

	try:
		img = cv2.imread(image)
		text = pytesseract.image_to_string(img)

		txn_id = None
		date = None
		payment_mode = None
		paid = None

		splitted_text = text.split(" ")
		split_line = text.split("\n")

		if "Google" in text:
			payment_mode = 'Google Pay'
			for index,t in enumerate(splitted_text):
				if "ID" in t and len(t)>13:
					txn_id = "".join([num for num in t if num.isdigit()])

				elif "Completed" in t:
					try:
						date = splitted_text[index+2]+" "+splitted_text[index+3][:3]+" "+"2021"
						date = datetime.strptime(date,"%d %b %Y")
					except:
						date = "".join([num for num in splitted_text[index+3] if num.isdigit()])+" "+splitted_text[index+2]+" "+"2021"
						date = datetime.strptime(date,"%d %b %Y")
					
					date = date.strftime("%d/%m/%Y")

					t = splitted_text[index-1]
					t = t.split("\n")[2][1:6]

					paid = "".join([num for num in t if num.isdigit()])

		elif "paytm" in text:
			payment_mode = "Paytm"
			for index,t in enumerate(splitted_text):
				if "No" in t:
					t = splitted_text[index+1]
					if len(t)>=12:
						txn_id = t[:12]

				elif "2021" in t:
					date = splitted_text[index][:4]+" "+splitted_text[index-1]+" "+splitted_text[index-2][-2:]
					date = datetime.strptime(date,"%Y %b %d")
					date = date.strftime("%d/%m/%Y")

				elif "Received" in t:
					t = splitted_text[index+1]
					paid = t.split("\n")[0]


		else:
			payment_mode = "Phonepe"
			for index,t in enumerate(splitted_text):
				if "ID" in t and len(t)>23:
					t_index = t.index('T')
					txn_id = t[t_index:t_index+23]

				elif "2021" in t:
					date = splitted_text[index][:4]+" "+splitted_text[index-1]+" "+splitted_text[index-2]
					date = datetime.strptime(date,"%Y %b %d")
					date = date.strftime("%d/%m/%Y")

				t = t.split("\n")

				if len(t[0])==6:
					t = t[0][1:]

					t = "".join([num for num in t if num.isdigit()])
					if t:
						paid = t
		
		return payment_mode,date,txn_id,paid
	except:
		return None,None,None,None

#print(get_txn('gpay2.jpg'))
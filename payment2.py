import pandas as pd
import os
from image_recognition import get_payment_details
import numpy as np
import warnings
from invoice import invoice
from mail import send_mail

RegisteredDf = pd.read_csv("Registered.csv")
FinalDf = pd.read_csv("Final List.csv")
ErrorDf = pd.read_csv("Error List.csv")

FinalDfCopy = FinalDf
ErrorDfCopy = ErrorDf

RegisteredDfColumns = RegisteredDf.columns
FinalDfColumns = FinalDf.columns

RegisteredNameColumns = []
RegisteredDfMailColumns = []
DropColumns = []
CourseColumn = ""

ErrorDfNameColumns = [col for col in ErrorDf.columns if col[:4]=='Name']

IMAGE_FILES_LOCATION = "Txn Images"

Files = os.listdir(IMAGE_FILES_LOCATION)
FilesDirectory = list(map(lambda x:os.path.join(IMAGE_FILES_LOCATION,x),Files))

FilesWithoutExtension = list(map(lambda x:os.path.splitext(x)[0].lower(), Files))

FinalDfNameColumnsIndex = [FinalDfColumns.get_loc(col) for col in FinalDfColumns if col[:4]=='Name']

#warnings.simplefilter('error', UserWarning)

for column in RegisteredDfColumns:

	if column[:4]=="Name":
		RegisteredNameColumns.append(column)

	elif column[:4]=="Mail":
		RegisteredDfMailColumns.append(column)

	elif 'Course' in column:
		CourseColumn = column

Rows = RegisteredDf.shape[0]

def check_payment_status(df,row):
	stat = str(df["Payment Status"][row])
	if 'true' in stat.lower() or 'yes' in stat.lower():
		return True

def get_status(df,row):
	return df["Completed"][row]

def get_col_contents(df,row,column_names):
	return list(df[column_names].iloc[row].dropna())

def get_amount(members):
	if members == 1:
		amount = 1699

	else:
		amount = 1499

	return amount

def get_details_of_name(df,name_columns,name,row):
	for col_name in name_columns:
		if df[col_name][row] == name:
			index = df.columns.get_loc(col_name)
			return list(df.loc[row,df.columns[index:index+6]])

def mails(mail_list,invoice):
	for mail in mail_list:
		mail = "gnaneshwarreddy456@gmail.com"
		#send_mail(mail,invoice)

for row in range(Rows):
	if check_payment_status(RegisteredDf,row):
		completed = get_status(RegisteredDf,row)
		if not completed or np.isnan(completed):
			Names = get_col_contents(RegisteredDf,row,RegisteredNameColumns)
			for name in Names:
				name = name.lower()
				if name in FilesWithoutExtension:
					name_index = FilesWithoutExtension.index(name)
					File = FilesDirectory[name_index]
					break
			else:
				warnings.warn('File not found for {}'.format(Names))
				break

			payment_details = get_payment_details(File)
			PaymentMode,PaymentDate,TxnId,AmountPaid = payment_details

			if not all(payment_details):
				warnings.warn('Error occured in reading data of {}\n\n{}'.format(File,payment_details))

				if not payment_details[0]:
					PaymentMode = input('Enter PaymentMode: ')

				if not payment_details[1]:
					PaymentDate = input('Enter PaymentDate (dd/mm/yyyy): ')

				if not payment_details[2]:
					TxnId = input('Enter TxnId: ')

				if not payment_details[3]:
					AmountPaid = input('Enter Amount Paid: ')

			print(PaymentMode,PaymentDate,TxnId,AmountPaid)
			Members = len(Names)
			Amount = get_amount(Members)
			TotalAmount = Amount*Members
			Invoice = int(FinalDf.iloc[-1,0])+1
			Course = RegisteredDf[CourseColumn][row]

			NewRow = {
				"Invoice" : Invoice,
				"Payment Mode" : PaymentMode,
				"Payment Date" : PaymentDate,
				"Txn Id" : TxnId,
				"Paid" : AmountPaid,
				"Amount" : TotalAmount,
				"Course" : Course,
				"Members" : Members
			}

			MailList = get_col_contents(RegisteredDf,row,RegisteredDfMailColumns)

			print("Check the Payment Details\n\n{}\n\n{}\n{}\n".format(NewRow,Names,MailList))
			usr_inp = input("Press 'Enter' to continue, 'q' to skip this data : ")

			for index,name in enumerate(Names):
				Details = get_details_of_name(RegisteredDf,RegisteredNameColumns,name,row)

				cols_index = FinalDfNameColumnsIndex[index]
				cols = FinalDfColumns[cols_index:cols_index+6]

				DetailsDict = dict(zip(cols,Details))
				NewRow.update(DetailsDict)

			if usr_inp.lower() == 'q':
				ErrorDf = ErrorDf.append(NewRow,ignore_index=True)
				continue

			for row1 in range(ErrorDf.shape[0]):
				ErrorDfNames = get_col_contents(ErrorDf,row1,ErrorDfNameColumns)
				if ErrorDfNames==Names:
					#ErrorDf = ErrorDf.drop(index=row1)
					break

			InvoiceList = [
				PaymentDate,
				PaymentMode,
				Invoice,
				TxnId,
				Course,
				Members,
				Amount,
				TotalAmount,
				AmountPaid,
			]

			PdfFile = invoice(Names,InvoiceList)

			try:
				mails(MailList,PdfFile)
				print('Sent Mails to {}'.format(MailList))

			except:
				warnings.warn('Error in sending mails')
				print(Names)
				continue

			FinalDf = FinalDf.append(NewRow,ignore_index = True)
			RegisteredDf.loc[row,'Completed'] = True

			print('Added Data to List\n')

			


if not ErrorDf.equals(ErrorDfCopy):
	ErrorDf.to_csv('Error List.csv',index=False)
	print('Written to Error List')

if not FinalDf.equals(FinalDfCopy):
	FinalDf.to_csv('Final List.csv',index=False)
	RegisteredDf.to_csv('Registered.csv', index=False)
	print('Written to Final List')
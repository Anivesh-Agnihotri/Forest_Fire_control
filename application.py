import smtplib                                                       #simple mail transfer protocol - it will help in sending e-mails
from email.message import EmailMessage
import getpass
import stdiomask
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score

host ='imap.gmail.com'
sender_Email="you email"
sender_Email_pass="password"
stage= 0

def send_email(receiver,subject,message):                               #function to send emails
    server = smtplib.SMTP('smtp.gmail.com',587)
    server.starttls()                                                   #make sure to give app acess in google account
    server.login(sender_Email,sender_Email_pass)
    email = EmailMessage()
    email['From'] = sender_Email
    email['To'] = receiver
    email['Subject'] = subject
    email.set_content(message)
    server.send_message(email)
    print("Your Email is sent")
#this will send the email    

def get_email_info(stage):                                                   #function to gather the information of email to be send
    print("To Whom you want to send email") 
    receiver =input("Enter the reciver email:")        
    subject = "Forest Fire Pridiction"                                
    message = "Probability of forest fire "+ stage+ "\nwe think you will take poper mesasures\n Thank you"
    send_email(receiver,subject,message)                              #call the send_email function
 
df= pd.read_csv(r'C:\Users\anive\Documents\GitHub\Forest_Fire_control\forestfires.csv')

def condition(row):
    if row['area'] >=0 and row['area']<2 :
        return 0
    elif row['area'] >=2 and row['area']<10 :
        return 1
    else:
        return 2
    
def month_cat(month):
    if month == 'oct' or month == 'sep' :
        return 0
    elif month =='nov' or month == 'may':
        return 1
    elif month == 'mar' or month == 'jun':
        return 2
    elif month == 'jul' or month == 'jan':
        return 3
    elif month == 'feb' or month == 'dec':
        return 4
    else : 
        return 5  

def area_cat(are):
    if are == 0 :
        return "NO Damage"
    elif are == 1 :
        return "Damage"
    else:
        return "High Damage"

df['category'] =df.apply(condition, axis=1)
df['month_new'] = df['month'].apply(month_cat)

x= df[['temp','RH','wind','rain','month_new']]
y= df[['category']]

#x_train,x_test,y_train,y_test= train_test_split(x,y,test_size=0.25,random_state=1)

classifier=SVC(kernel="linear")
classifier.fit(x,y)

def testing() :
    print("Enter the detail:")
    lst =[0,0,0,0,0]
    lst[0]=float(input("Temperature : "))
    lst[1]=float(input("RH: "))
    lst[2]=float(input("wind: "))
    lst[3]=float(input("rain: "))
    m=input("Month_name: ")
    mn=month_cat(m)
    lst[4]=int(mn)
    
    lst=[lst]
    nlst=np.array(lst)

    predictions = classifier.predict(nlst)
    stage = area_cat(predictions)
    print("The probability of Forest fire is "+stage)
    print("Do you want to send the report by email?\n if yes type 'y' otherwise type 'n': ")
    take=input()
    if take == 'y':
        #print("Waring: make sure you have given access to less secure app in yoyr google account")
        #sender_Email = input("Enter the ur email:   ")
        #sender_Email_pass =stdiomask.getpass(prompt="Password: ")
        get_email_info(stage)

os.system("cls")  

print("  "*10+ "*-"*30)    
print("  "*15+"\nWelcome to Machine learning Model to predict Forest fire \n")
print("  "*10+"*-"*30) 
print("\n\n")
while True:
    print("Type - 'machine'- for using model\nType- 'exit' -to exit")
    ch=input("Your choice: ")
    if ch=="machine":
        testing()

    elif ch =="exit":
        print("Thanking for using me")
        break

    else:
        print("Wrong input")    

print("  "*10+"*-"*30)


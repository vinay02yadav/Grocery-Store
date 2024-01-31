import csv
from datetime import datetime, timedelta
import json
import smtplib
import ssl
from email.message import EmailMessage

from flask import render_template,current_app
from app.models import Login,db,Product

from app.workers import celery
from celery.schedules import crontab
import os
from bing_image_downloader import downloader

from api.dashboard.checkout import dic

@celery.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):

    sender.add_periodic_task(
        crontab(minute=31, hour=19),
        sendDailyReminderMail.s(),
        name = 'Daily reminder everyday @7PM via mail.',
    )

    sender.add_periodic_task(
        crontab(minute=31, hour=19),
        # crontab(day_of_month=1, month_of_year='*'),
        sendMonthlyMail.s(),
        name = 'Monthly Activity Report @1st of every month via mail.',
    )



# 1. DAILY reminder TASKS [Daily Reminder Jobs]
# -----------------------


@celery.task
def send_email(email):
    print("Sending email...")
    
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login('726ryadav@gmail.com', '')

    em = EmailMessage()
    em['From'] = '726ryadav@gmail.com'
    em['To'] = email
    em['Subject'] = "🌟 Discover Exciting Offers at Urahara's Shop - Limited Time Only! 🌟"
    em.set_content(f"We hope this message finds you well. We are always looking for ways to enhance your shopping experience and provide you with the best offers on quality products.We're excited to invite you to explore our online grocery store, where you can discover a world of convenience and savings.\n\nAs a token of our appreciation, we're offering a special 17% discount on your first online order. Use code: [WELCOME20] at checkout.\nThank you for being a valued customer. We look forward to serving you online and providing you with a delightful shopping experience.\n\nBest regards,\nSoul Society")

    server.send_message(em)
    
    print("Sent")


@celery.task
def sendDailyReminderMail():
    users = Login.query.filter_by(role = 'user').all()

    for user in users:
        # if not user.timestamp or user.timestamp < datetime.now() - timedelta(days=1):
        if not user.timestamp or (datetime.now() - datetime.strptime(user.timestamp, "%Y-%m-%d %H:%M:%S.%f") > timedelta(hours=24)):
            send_email.delay(user.email)

    return 'Daily Reminder sent successfully via MAIL !!'




# 2. MONTHLY mail - tasks [Scheduled Job - Monthly Activity Report]
# -------------------------

@celery.task
def sendMARMail(id, email):
    user = Login.query.filter_by(id=id).first()
    try:
        orders = json.loads(user.previous_order)
    except Exception as e:
        orders = []
        
    message_html = render_template('MAR.html', orders=orders, has_orders=True)
    
    today = datetime.today().strftime('%B-%Y')
    subject = f'Urahara Shop: Monthly Activity Report for ({today})'

    # Create the plain text version of the email (optional)
    message_plain = ""

    # Set up the email message
    em = EmailMessage()
    em['From'] = '726ryadav@gmail.com'
    em['To'] = email
    em['Subject'] = subject
    em.set_content(message_plain)  # Set plain text content
    em.add_alternative(message_html, subtype='html')  # Set HTML content

    # Connect to the SMTP server and send the email
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login('726ryadav@gmail.com', '')
    server.send_message(em)
    server.quit()

    # return f'Monthly review email sent to {email}'



@celery.task
def sendMonthlyMail():
    users = Login.query.filter_by(role = 'user').all()
    print(users)
    for user in users:
        sendMARMail.delay(user.id, user.email)

    return 'Monthly mail has been sent.'






# 3. EXPORT tasks [User Triggered Async Job - Export as CSV]
# ----------------

@celery.task
def export_csv():
    with current_app.app_context():

        # 1. Generating Product CSV
        # -----------------------

        prod_list = ['id', 'product', 'price', 'quantity', 'stock_left', 'stock_sold']
        products = db.session.query(Product).all()
        
        print("'''''''''''")
        print(products)
        print("'''''''''''")
        rows = []
        for product in products:
            print(product.id)
            print(product.name)
            print(product.rate)
            print(product.quantity)
            print(product.stock)
            print(dic)
            try:
                row = [product.id, product.name, product.rate, product.quantity, product.stock, dic[product]]
            except:
                 row = [product.id, product.name, product.rate, product.quantity, product.stock, 0]
            rows.append(row)

        now = datetime.now().strftime("%d-%m-%Y_%H%M")
        product_filename = f'profile_{now}.csv'
        csv_path = os.path.join('templates/CSV exports/', product_filename)
        os.makedirs(os.path.dirname(csv_path), exist_ok=True)
        print('PRODUCTS FILE SAVED!!')
        with open(csv_path, 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            if csvfile.tell() == 0:
                csvwriter.writerow(prod_list)
            csvwriter.writerows(rows)            
        return  {'status': 'success', 'message': 'Post & Profile CSVs - Created Successfully !!', 'csv_path': csv_path}

basedir = os.path.abspath(os.path.dirname(__file__))
basedir = (basedir.replace("\\","/")) 
print(basedir)
basedir = basedir[:-11] + "frontend/public/images"
@celery.task
def gett_img(name):
    with current_app.app_context():
        print("inside images downloader")
        product = Product.query.filter_by(name = name).first()
        # download_images.delay(product.name).wait()
        downloader.download(product.name, limit=1,  output_dir=basedir,adult_filter_off=True, force_replace=False, timeout=30)
        files = os.listdir(basedir + f"/{product.name}")
        product.image_link = f'images/{product.name}/{files[0]}'
        db.session.commit()
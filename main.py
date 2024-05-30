from bs4 import BeautifulSoup
import requests
import smtplib
import os # so we can send email using environmental Variables
from my_vars import *

# We set product link & target price:
product_link = "https://www.amazon.co.uk/RDX-Standing-Pedestal-Freestanding-Kickboxing/dp/B08M4BNDTT/ref=sr_1_6?crid=HWRZ3NRNT7X2&dib=eyJ2IjoiMSJ9.mX4GP146Dmv-kqYZ_2E9HWTSAlPC3US2Qol_iZX7zqwrHYffRv57fDl5ydILHtgzHVR0SWhCt56DK-mvQgZMhlz88kpeWNBshXEnJvGFFGRM0hZgbJ5FoRlPDF2iXXxbUdhIzyoNyeOSlN1i_ZLi2hgWrO5pXmSq5vmOHkR_WZbIDZoS6EDVSHS3WVZBCVVpIWrcHNMT3UzXrfqK49UOZrJU3E7QZqjyAcqAf3NuDkqiXmJiI8y_XuPV_hV9Ab052Xzl4feOMyomYTxtlQIerrka9YANfwiiR6UJxB8AtPE.dgMgfJtmfFIBjMsiIKfHALdUX8YGZEvsMCTzhSSYOjg&dib_tag=se&keywords=standing%2Bboxing%2Bbag&qid=1717094824&sprefix=standing%2Bboxing%2Bbag%2Caps%2C73&sr=8-6&ufe=app_do%3Aamzn1.fos.d7e5a2de-8759-4da3-993c-d11b6e3d217f&th=1&psc=1"
target_price = 180

# We use the requests library to request the HTML page of the Amazon product.
# We need to pass along some headers in order for the request to return the actual website HTML.
# At minimum we need to give our "User-Agent" and "Accept-Language" values in the request header.
# We have to input the headers, otherwise scraping won't work
# We found our "User-Agent" and "Accept-Language" using https://myhttpheader.com/
my_http_header = {
	"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
	"Accept-Language": "en-US,en;q=0.7"
}

response = requests.get(product_link, headers=my_http_header)

# We get hold of the product price using BeautifulSoup:
soup = BeautifulSoup(response.content, "html.parser")

price_value = soup.find("span", class_="a-offscreen")

price = float(price_value.text.strip("£")) if price_value else "Price not found"

# print(price)

# Now we can send email alerts if price is below our target:

my_email = os.environ.get("DEV_EMAIL")
password = os.environ.get("DEV_EMAIL_ACCESS_PASSWORD")
recipient = RECIPIENT_EMAIL

email_content = (f"Hey, \n The product you're chasing on Amazon is on discounted price today, at only £{price}."
				 f"\nCheck it out here: {product_link}")

if price <= target_price:
	with smtplib.SMTP("smtp.gmail.com") as connection:
		connection.starttls()
		connection.login(user=my_email, password=password)
		connection.sendmail(from_addr=my_email, to_addrs=recipient, msg=email_content)
	print("email sent")
else:
	with smtplib.SMTP("smtp.gmail.com") as connection:
		connection.starttls()
		connection.login(user=my_email, password=password)
		connection.sendmail(from_addr=my_email, to_addrs=recipient, msg="Price is still high.")
	print("email sent")
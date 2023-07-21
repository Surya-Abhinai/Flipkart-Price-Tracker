from bs4 import BeautifulSoup
import requests
import tkinter as tk
from tkinter import messagebox
import smtplib


def send_mail():
    connection = smtplib.SMTP("smtp.gmail.com")
    connection.starttls()
    connection.login(user="abhinayj848430@gmail.com", password="ttycewgyalsymlge")

    subject = f"The product you want is below ₹{desired_price}! Now is your chance to buy!"
    if highlights:
        body = f"Hey, This is the moment we have been waiting for, Now is your chance to pick up the product of your dreams. Don't mess it up!\n\n" \
               f"Rating of the product : {rating}/5\n\n" \
               f"Here are some Highlights of the product: \n{highlights}\n\n" \
               f"Product Link here: {URL}"
    else:
        body = f"Hey, This is the moment we have been waiting for, Now is your chance to pick up the product of your dreams. Don't mess it up!\n\n" \
               f"Rating of the product : {rating}/5\n\n" \
               f"Product Link here: {URL}"

    msg = f"Subject: {subject}\n\n{body}"
    msg = msg.encode("utf-8")

    connection.sendmail(from_addr="abhinayj848430@gmail.com", to_addrs=email, msg=msg)
    connection.close()


def execute():
    def fetch_data():
        global email, desired_price, URL , highlights

        email = email_input.get()
        URL = link_input.get()
        if len(email) == 0 or len(price_input.get()) == 0 or len(URL) == 0:
            messagebox.showinfo(title="Oops", message="Don't leave the fields empty.")
            return

        desired_price = int(price_input.get())
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
            "Accept-Encoding": "gzip, deflate",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "DNT": "1", "Connection": "close", "Upgrade-Insecure-Requests": "1"}

        page = requests.get(f"{URL}", headers=headers)

        Soup1 = BeautifulSoup(page.content, "html.parser")
        Soup2 = BeautifulSoup(Soup1.prettify(), "html.parser")
        global highlights
        try:
            highlights = Soup2.find("div", {"class": "_2cM9lP"}).text.strip()
            # Split the text into lines
            lines = highlights.strip().split("\n")
            # Remove empty lines and extra spaces
            highlights = "\n".join(line.strip() for line in lines[1:] if line.strip())

        except:
            pass

        global price
        price = Soup2.find("div", {"class": "_30jeq3 _16Jk6d"}).text.strip()
        global product_name
        product_name = Soup2.find("span", {"class": "B_NuCI"}).text.strip()
        global offers
        offers = Soup2.find("div", {"class": "_3TT44I"}).text.strip()
        global rating
        rating = Soup2.find("div", {"class": "_3LWZlK"}).text.strip()
        if int(price) < desired_price:
            send_mail()

    window = tk.Tk()
    window.title("Flipkart Price Notifier")
    window.minsize(width=400, height=400)

    # Insertion of logo
    canvas = tk.Canvas(width=300, height=180)
    lock = tk.PhotoImage(file="logo.png")
    canvas.create_image(200, 113, image=lock)
    # canvas.create_text(80,250, text="Website:", fill="black", font=("Arial", 12))
    canvas.grid(row=10, column=10)

    # labels
    link_label = tk.Label(text="Paste Your Link:", foreground="black")
    price_label = tk.Label(text="Desired Price:", foreground="black")
    email_label = tk.Label(text="Email Id:", foreground="black")
    link_label.grid(row=12, column=10)
    price_label.grid(row=14, column=10, pady=5)
    email_label.grid(row=16, column=10, pady=2)

    # Inputs
    link_input = tk.Entry(width=30)
    link_input.place(x=200, y=185)
    price_input = tk.Entry(width=15)
    price_input.place(x=200, y=212)
    email_input = tk.Entry(width=25)
    email_input.place(x=195, y=240)

    # Buttons
    enter = tk.Button(text="Proceed", command=fetch_data)
    enter.place(x=170, y=270)

    window.mainloop()


if __name__ == "__main__":
    highlights = None
    execute()

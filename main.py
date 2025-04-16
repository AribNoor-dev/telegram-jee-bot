from flask import Flask
import threading
import requests
from bs4 import BeautifulSoup as bp
import time

app = Flask(__name__)

url = "https://jeemain.nta.nic.in/"
keywords = ["result","score","card","answer","provisional","key"]  

def telegram_msg(message):
    token = '7584740207:AAG47e0hC8ghyuR76vX5wKb78mWh6juG894'
    chat_id = '-4744859301'
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    data = {"chat_id": chat_id, "text": message}
    requests.post(url, data=data)

def Checker():
    try:
        web_data = requests.get(url)
        soup = bp(web_data.text, "html.parser")
        first_div = soup.find("div", class_="vc_tta-panel-body")
        li = first_div.find_all("li")
        latest_li = li[0]
        text = latest_li.text.lower()

        if any(k in text for k in keywords):
            print("Keyword Found")
            telegram_msg("Result is out!")
        else:
            print("Keyword Not Found")

    except Exception as e:
        print("An error occurred:", e)

def run_checker_loop():
    while True:
        Checker()
        print("Refreshing every 5 minutes...")
        time.sleep(300)

# Start the checker loop in the background
threading.Thread(target=run_checker_loop, daemon=True).start()

@app.route('/')
def home():
    return "Bot is running and checking every 5 minutes."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)

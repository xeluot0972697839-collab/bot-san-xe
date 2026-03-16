import requests
import time

TOKEN = "8797822371:AAEv02DpqqSYvFCoXI142EeA48y5J_AP0n8"
CHAT_ID = "8658034567"

url = "https://gateway.chotot.com/v1/public/ad-listing?cg=2010&limit=20&region=13000"

headers = {
"User-Agent": "Mozilla/5.0",
"Accept": "application/json"
}

sent_ids = set()

def send_telegram(msg):
    telegram_url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    
    requests.post(telegram_url,data={
        "chat_id": CHAT_ID,
        "text": msg
    })


def check_ads():

    res = requests.get(url,headers=headers).json()

    ads = res["ads"]

    for ad in ads:

        ad_id = ad["ad_id"]
        title = ad["subject"].lower()

        if ad_id in sent_ids:
            continue

        # lọc xe Mitsubishi
        if not any(x in title for x in [
            "xpander",
            "xpander cross",
            "attrage",
            "triton"
        ]):
            continue

        area = ad.get("area_name","")
        region = ad.get("region_name","")

        # lọc khu vực
        if not any(x in region.lower() for x in [
            "hồ chí minh",
            "đồng nai"
        ]):
            continue

        price = ad.get("price",0)

        link = f"https://www.chotot.com/mua-ban-oto/{ad_id}.htm"

        msg = f"""
🚗 {ad['subject']}

💰 Giá: {price:,} đ
📍 Khu vực: {area} - {region}

🔗 Link
{link}
"""

        send_telegram(msg)

        sent_ids.add(ad_id)



while True:

    try:

        check_ads()

        print("Đang quét tin xe...")

    except Exception as e:

        print("Lỗi:",e)

    time.sleep(30)

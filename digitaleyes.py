import  datetime
import requests
import threading
import time
import json

f = open('config.json',)
config = json.load(f)

OLD_NFTS = []
BASE_LINK = config['base_link']
webhooks = config['webhooks']
collections = config['collections']
avatar_url = config['avatar_url']
footer_name = config['footer_name']
footer_img_link = config['footer_image_url']

def getID(NFT):
    return NFT['metadata']['name']

def getPrice(NFT):
    return NFT['price'] / 1000000000

def getImg(NFT):
    return NFT['metadata']['image']

def getLink(NFT):
    return "https://digitaleyes.market/item/" + NFT['mint']

def getDate():
    return datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")

def getCollectionUrl(collection):
    return "https://digitaleyes.market/collections/" + collection.replace(" ", "%20")


def delete_nft(NFT, name):
    global OLD_NFTS
    print("Deleting : " + name + " in 5 minutes")
    time.sleep(300)
    OLD_NFTS.remove(NFT)

def sendCode(name, price, img, nft_url, webhook_name, webhook_url, collection):
    data = {
        "embeds": [
            {
                "title": name,
                "description": "Price : " + price + " sol",
                "url": nft_url,
                "fields": [
                    {
                      "name": "Collection",
                      "value": "[" + collection + "]" + "(" + getCollectionUrl(collection) + ")"
                    }
                ],
                "thumbnail": {
                "url": img
                },
                "footer": {
                    "text": footer_name + " | " + getDate(),
                    "icon_url": footer_img_link
                },
            }
        ],
        "username": "DigitalEyes",
        "avatar_url": avatar_url
    }
    result = requests.post(webhook_url, json=data)
    try:
        result.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(err)
    else:
        print("Webhook sent to : " + webhook_name)

def listNFTS(LINK, COLLECTION, PRICE_LIMIT, BASE_LINK):
    try:
        response = requests.get(LINK)
        cursor = response.json()['next_cursor']
        NFTS = response.json()['offers']
        for NFT in NFTS:
            if getPrice(NFT) <= PRICE_LIMIT:
                if NFT not in OLD_NFTS:
                    for webhook in webhooks:
                                sendCode(getID(NFT), str(getPrice(NFT)), getImg(NFT), getLink(NFT),webhook['name'], webhook['url'], COLLECTION)
                    OLD_NFTS.append(NFT)
                    delete_nft_thread = threading.Thread(target=delete_nft, args=(NFT,getID(NFT),))
                    delete_nft_thread.start()
            else:
                cursor = None
                break
        if cursor is not None:
            listNFTS(BASE_LINK + COLLECTION + "&cursor=" + cursor, COLLECTION, PRICE_LIMIT, BASE_LINK)
    except:
        print("Error detected !")

def monitor(collection, price):
    while True:
        listNFTS(BASE_LINK + collection, collection, price, BASE_LINK)
        
def main():
    for collection in collections:
        print("Monitoring : " + collection['collection'] + " <= " + str(collection['price']) + " sol")
        monitor_thread = threading.Thread(target=monitor, args=(collection['collection'],collection['price'],))
        monitor_thread.start()

main()
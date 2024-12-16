from fastapi import FastAPI, Request, Response
import uvicorn


import os
import logging
from pymessenger import Bot
from dotenv import load_dotenv


load_dotenv()


logger = logging.getLogger(__name__)

app = FastAPI()

VERIFICATION_TOKEN = os.environ.get("VERIFICATION_TOKEN")


@app.get("/")
def verify(request: Request):

    if request.query_params.get("hub.mode") == "subscribe" and request.query_params.get(
        "hub.challenge"
    ):
        if not request.query_params.get("hub.verify_token") == VERIFICATION_TOKEN:
            return Response(status_code=403, content="Verification token mismatch")

        return request.query_params.get("hub.challenge")

    return {"message": "Hello World"}


FB_ACCESS_TOKEN = os.environ.get("FB_ACCESS_TOKEN") or False
logger.info(f"FB_ACCESS_TOKEN: {FB_ACCESS_TOKEN}")

if not FB_ACCESS_TOKEN:
    raise BaseException("Invalid access token")

bot = Bot(FB_ACCESS_TOKEN)


@app.post("/")
async def webhook(request: Request):
    data = await request.json()
    logger.info(f"data: {data}")
    if data['object'] == "page":
        for entry in data['entry']:
            for messaging_event in entry['messaging']:
                sender_id = messaging_event['sender']['id']

                # Handle "Get Started" payload
                if messaging_event.get('postback'):
                    payload = messaging_event['postback']['payload']
                    
                    if payload == "GET_STARTED_PAYLOAD":
                        welcome_message = "Welcome to I Tanong mo kay kuya KC chatbot! I'm here to help you. You can:\n- Type 'Show Brands' to see available brands.\n- Ask me questions about our products."
                        bot.send_text_message(sender_id, welcome_message)

                    if payload == "BRAND_APPLE":
                        bot.send_text_message(sender_id, "Here are products for Apple:")
                        bot.send_image_url(sender_id, "https://example.com/images/apple_iphone.jpg")
                        bot.send_text_message(sender_id, "- iPhone 14")
                        bot.send_image_url(sender_id, "https://example.com/images/apple_macbook.jpg")
                        bot.send_text_message(sender_id, "- MacBook Air")
                        bot.send_image_url(sender_id, "https://example.com/images/apple_watch.jpg")
                        bot.send_text_message(sender_id, "- Apple Watch")

                    if payload == "BRAND_SAMSUNG":
                        bot.send_text_message(sender_id, "Here are products for Samsung:")
                        bot.send_image_url(sender_id, "https://example.com/images/samsung_galaxy.jpg")
                        bot.send_text_message(sender_id, "- Galaxy S23")
                        bot.send_image_url(sender_id, "https://example.com/images/samsung_tab.jpg")
                        bot.send_text_message(sender_id, "- Galaxy Tab S8")
                        bot.send_image_url(sender_id, "https://example.com/images/samsung_watch.jpg")
                        bot.send_text_message(sender_id, "- Galaxy Watch 5")

                    if payload == "BRAND_SONY":
                        bot.send_text_message(sender_id, "Here are products for Sony:")
                        bot.send_image_url(sender_id, "https://example.com/images/sony_bravia.jpg")
                        bot.send_text_message(sender_id, "- Sony Bravia TV")
                        bot.send_image_url(sender_id, "https://example.com/images/sony_headphones.jpg")
                        bot.send_text_message(sender_id, "- Sony WH-1000XM5")
                        bot.send_image_url(sender_id, "https://www.bing.com/images/search?view=detailV2&ccid=OcJRg5pD&id=03E263847F47455DCD15538F5CB0CAE8B0C6394A&thid=OIP.OcJRg5pD-4fDETVqIsOpeQHaE7&mediaurl=https%3A%2F%2Fwww.journaldugeek.com%2Fcontent%2Fuploads%2F2022%2F10%2Fps5-sony.jpg&exph=932&expw=1400&q=sony+playstation+5&simid=608053566294472077&FORM=IRPRST&ck=F1D7BB4508F1F571641D0956636613DA&selectedIndex=6&itb=0&cw=1375&ch=751&ajaxhist=0&ajaxserp=0")
                        bot.send_text_message(sender_id, "- Sony PlayStation 5")

                # Handle normal text messages
                if messaging_event.get('message'):
                    if messaging_event['message'].get('text'):
                        query = messaging_event['message']['text'].lower()

                        if query == "show brands":
                            buttons = [
                                {
                                    "type": "postback", 
                                    "title": "Apple", 
                                    "payload": "BRAND_APPLE"
                                },
                                {
                                    "type": "postback", 
                                    "title": "Samsung", 
                                    "payload": "BRAND_SAMSUNG"
                                },
                                {
                                    "type": "postback", 
                                    "title": "Sony", 
                                    "payload": "BRAND_SONY"
                                }
                            ]
                            bot.send_button_message(sender_id, "Select a brand to see products:", buttons)
                        else:
                            bot.send_text_message(sender_id, "Send 'Show Brands' to see available brands.")

    return "ok", 200


    # return {"received": data}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)

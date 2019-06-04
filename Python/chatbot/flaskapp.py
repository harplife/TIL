from flask import Flask, render_template, request
from telegram import say_hello, repeat, conversion, naver, bitcoin, dusty
import pprint
from decouple import config


token = config('TOKEN')
app = Flask(__name__)


@app.route(f"/{token}", methods=["POST"])
def incoming():
    # pprint prints dictionary properly formatted for viewing
    # pprint.pprint(request.get_json())

    message = request.get_json().get('message')
    if message is not None:
        sender_id = message.get('from').get('id')
        sender_name = message.get('from').get('first_name') + " " + \
            message.get('from').get('last_name')
        sender_msg = message.get('text')
        print(sender_id, sender_name, sender_msg)

        # MESSAGE REPLY METHODS HERE
        if sender_msg == 'hello':
            say_hello(sender_id, sender_name)
        elif sender_msg == '환율':
            conversion(sender_id)
        elif sender_msg == '네이버':
            naver(sender_id)
        elif sender_msg == 'bitcoin':
            bitcoin(sender_id)
        elif sender_msg == '미세먼지':
            dusty(sender_id)
        else:
            repeat(sender_id, sender_msg)

    return '', 200


if __name__ == '__main__':
    app.run(debug=True)

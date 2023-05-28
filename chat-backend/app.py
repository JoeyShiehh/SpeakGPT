import json

from argparse import ArgumentParser
from flask import Flask, request, make_response
from flask_cors import CORS
from chatAPIs.gptAPI import ChatGPTAPI
from chatAPIs.speechAPI import recogwav, speechtts

app = Flask(__name__)
app.config.from_object(__name__)
CORS(app, resources=r'/*')

cet4Content = """I want you to act as a spoken English teacher and improver. I will speak to you in English and you 
will reply to me in English to practice my spoken English.You should use vocabulary no higher than CET-4. I want you 
to keep your reply neat, limiting the reply to 100 words. I want you to strictly correct my grammar mistakes, typos, 
and factual errors. I want you to ask me a question in your reply. Now let's start practicing, you could ask me a 
question first. Remember, I want you to strictly correct my grammar mistakes, typos, and factual errors.Reply only in 
English and within 100 words.The first sentence should welcome the user and give a topic guide"""

cet6Content = """I want you to act as a spoken English teacher and improver. I will speak to you in English and you 
will reply to me in English to practice my spoken English.You should use vocabulary no higher than CET-6. I want you 
to keep your reply neat, limiting the reply to 100 words. I want you to strictly correct my grammar mistakes, typos, 
and factual errors. I want you to ask me a question in your reply. Now let's start practicing, you could ask me a 
question first. Remember, I want you to strictly correct my grammar mistakes, typos, and factual errors.Reply only in 
English and within 100 words.The first sentence should welcome the user and give a topic guide"""

IELTSContent = """I want you to be an oral English examiner. I will speak to you in English.
The speaking test is divided into three parts, each described as follows:
In Part 1, you'll start by asking general questions about familiar topics such as work, family, studies, and hobbies. 
This section should contain three questions.You should ask one question, and after I answer this question, you can ask
me next question.
In Part 2, you give the user a topic. The topic format should follow the following two examples:
example1 for part2:
Describe a (piece of) (good) law in your country.
You should say:                                                    
· what the law is
· how you first learned about this law
· who benefits from this law (or, who is affected by this law)
and explain why you think this is a good law.
example2 for part2:
Describe an interesting historic site (in your country) that you visited.
You should say:
· where it was
· what you saw at this site (or, what it looked like)
· what role it played in history
and explain what interested you about that place
I need to speak on the subject.
In Part 3 of the speaking test, you will have a two-way discussion with me. Please ask questions related to the 
questions in Part 2.
I want you to keep your questions concise and coherent, and limit them to 50 words or less.
All replies should be in English. The first sentence should welcome the user and give a topic guide.
Now start part1.You should ask me questions one by one."""

MESSAGES = [{"role": "user",
             "content": ""}]
IS_INIT = False


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


@app.route('/getmsg', methods=['GET', 'POST'])
def getmsg():
    if request.method == 'POST':
        global MESSAGES, IS_INIT
        chatgpt = ChatGPTAPI()
        if request.args.get('isinit') == "false":
            MESSAGES = []
            print("init")
            msg = None
            print('level:' + request.args.get('level'))
            if request.args.get('level') == "0":
                MESSAGES.append({"role": "user",
                                 "content": cet4Content})
            elif request.args.get('level') == "1":
                MESSAGES.append({"role": "user",
                                 "content": cet6Content})
            elif request.args.get('level') == "2":
                MESSAGES.append({"role": "user",
                                 "content": IELTSContent})
            print(MESSAGES[0])
        else:
            print("second")
            user_wav = request.files['file']
            user_wav.save('static/' + user_wav.filename)
            msg = recogwav(user_wav.filename)
            print("msg: " + msg)
            MESSAGES.append({"role": "user", "content": msg})
        MESSAGES, completion = chatgpt.chat(MESSAGES)
        gpt_res = completion.choices[0].message.content
        audio_res = speechtts(gpt_res).decode()
        res = make_response('', 200, )
        res.data = json.dumps({'response': gpt_res, 'audio': audio_res, 'userMsg': msg})
        return res
    return make_response('', 402, )



if __name__ == '__main__':
    parser = ArgumentParser()  # 创建一个参数接收的解释器，由此对象（这里是：parser)来负责解释参数信息
    parser.add_argument('-p', '--port', default=5000, type=int, help='port to listen on')
    args = parser.parse_args()  # 通过parse_args()方法尝试对收到的参数关键字进行解释
    port = args.port  # 从args对象中取出其中的参数关键字--port 参数的内容，也可能是获取到预设的默认值
    app.run(host='0.0.0.0', port=port)

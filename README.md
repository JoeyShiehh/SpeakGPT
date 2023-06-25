# SpeakGPT
一款支持语音输入、语音转换、语音评分的英语口语对话助手。

支持CET4、CET6词汇等级的对话。

可以进行IELTS口语仿真考试

![](https://s3.bmp.ovh/imgs/2023/05/30/5b99fa6b11d6dc3e.png)

# Frames
开发框架基于
- Flask
- Vue3
- Tailwind CSS

产品赋能基于
- ChatGPT
- 百度TTS
- 讯飞语音评判

# Usage
## 环境（仅供参考）
- Nodejs 14.17.1
- Python 3.10
## API key配置
需要在```/back-end```文件夹下新建```.env```文件，文件内需要包含以下信息：
```
OPENAI_API_KEY = 'sk-xxx' # 你的OPENAI Key
FLASK_KEY = 'xxx'
XF_APP_ID = 'xxx' # 讯飞云控制台获取
XF_API_SECRET = 'xxx' # 讯飞云控制台获取
XF_API_KEY = 'xxx' # 讯飞云控制台获取
API_KEY = "xxx" # 百度云控制台获取
SECRET_KEY = "xxx" # 百度云控制台获取
```
## 后端启动
入口文件```/back-end/app.py```

**请确保包含所有需要的依赖库**

## Vue启动
在```/chatfriend```文件夹下执行以下命令
```
npm install
npm run serve
```

# Collaborator
[@1vyyyyyy](https://github.com/1vyyyyyy)

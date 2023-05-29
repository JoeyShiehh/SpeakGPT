<template>
  <div class="flex h-screen">
    <aside class="default-sidebar bg-gray-50 dark:bg-gray-800">
      <div class="sidebar-header">
        <p class="m-10 text-4xl font-extrabold text-gray-900 dark:text-white">Chat Friend</p>
      </div>
      <div class="px-3 py-4 overflow-y-auto">
        <ul class="sidebar-menu">
          <li
            class="flex items-center p-2 text-gray-900 rounded-lg dark:text-white hover:bg-gray-100 dark:hover:bg-gray-700"
            v-for="(item, index) in sidebarItems" :key="index" :class="{ active: activeIndex === index }"
            @click="selectItem(index)">
            <span class="text-blue-900">{{ item }}</span>
          </li>
        </ul>
      </div>
      <div class="text-sm text-gray-500 text-center">
        Powered by <a class="underline" href="https://openai.com/blog/chatgpt"> ChatGPT</a>
      </div>
    </aside>
    <div class="h-screen flex flex-col">
      <!-- 语言等级General\Advanced等 -->
      <div class="m-5 mb-0">
        <p class="text-2xl font-bold text-blue-900 dark:text-white">当前等级：{{ sidebarItems[activeIndex] }}</p>
      </div>
      <!-- 消息盒子 -->
      <div class="flex-1 mx-2 mt-2 mb-2 overflow-y-auto">
        <div class="message bot-message">
          <div class="message-content">{{ hello }}</div>
        </div>
        <audio id="wav" ref="audioPlayer" autoplay="autoplay" visibility: hidden controls></audio>
        <div v-for="(message, index) in messages" :key="index"
          class="group flex mb-1 flex-col px-4 py-3 hover:bg-slate-100 rounded-lg"
          :class="{ 'user-message': message.isUserMessage, 'bot-message': !message.isUserMessage }">
          <svg v-if="message.isUserMessage" width="24" height="24" viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M4 30C4 36.6274 9.37258 42 16 42C22.6274 42 26 38 27 35L28.5385 30L35 9L44 42" stroke="#333" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/><path d="M40.7274 30H28.5386" stroke="#333" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/><path d="M22 15C22 11.6863 19.3137 9 16 9C12.6863 9 10 11.6863 10 15V30C10 33.3137 12.6863 36 16 36C19.3137 36 22 33.3137 22 30V15Z" fill="none" stroke="#333" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/></svg>
          <svg v-if="!message.isUserMessage" width="24" height="24" viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg"><rect x="9" y="18" width="30" height="24" rx="2" fill="none" stroke="#333" stroke-width="4"/><circle cx="17" cy="26" r="2" fill="#333"/><circle cx="31" cy="26" r="2" fill="#333"/><path d="M20 32C18.8954 32 18 32.8954 18 34C18 35.1046 18.8954 36 20 36V32ZM28 36C29.1046 36 30 35.1046 30 34C30 32.8954 29.1046 32 28 32V36ZM20 36H28V32H20V36Z" fill="#333"/><path d="M24 10V18" stroke="#333" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/><path d="M4 26V34" stroke="#333" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/><path d="M44 26V34" stroke="#333" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/><circle cx="24" cy="8" r="2" stroke="#333" stroke-width="4"/></svg>
          <div class="message-content">{{ message.content }}</div>
          <div class="flex flex-row" v-if="message.isUserMessage">
            <div v-for="(value,key) in message.score" :key="key|index" >
              {{ key }}
              <a :style="'color:'+(value > 3?'green':'red')+';'">
                {{ value }}
              </a>
              {{ '|\xa0' }}
            </div>
          </div>
          <div class="message-time">{{ message.time }}</div>
          <!-- <div v-if="!message.isUserMessage" class="message-time font-bold">{{ sidebarItems[activeIndex] }}</div> -->
        </div>
      </div>
      <!-- 底部按钮 -->
      <div class="sticky bottom-0 w-full p-2 pb-2 bg-gray-100">
        <p class="font-bold mb-1" v-if="isLoading">加载中...</p>
        <!-- 开始录音按钮 -->
        <button
          class="bg-green-300 hover:bg-green-500 text-gray-800 font-bold py-2 px-4 rounded inline-flex items-cente w-full"
          v-if="!isRecording" @click="onSpeak">
          <svg width="24" height="20" viewBox="8 -8 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
            <rect x="17" y="4" width="14" height="27" rx="7" fill="none" stroke="#333" stroke-width="4"
              stroke-linejoin="round" />
            <path d="M9 23C9 31.2843 15.7157 38 24 38C32.2843 38 39 31.2843 39 23" stroke="#333" stroke-width="4"
              stroke-linecap="round" stroke-linejoin="round" />
            <path d="M24 38V44" stroke="#333" stroke-width="4" stroke-linecap="round" stroke-linejoin="round" />
          </svg>
          <span class="text-center">点击录音</span>
        </button>
        <!-- 结束录音按钮 -->
        <button
          class="bg-red-300 hover:bg-red-400 text-gray-800 font-bold py-2 px-4 rounded inline-flex items-cente w-full"
          v-if="isRecording" @click="sendSpeak">
          <svg width="24" height="20" viewBox="8 -8 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
            <rect x="17" y="4" width="14" height="27" rx="7" fill="none" stroke="#333" stroke-width="4"
              stroke-linejoin="round" />
            <path d="M9 23C9 31.2843 15.7157 38 24 38C32.2843 38 39 31.2843 39 23" stroke="#333" stroke-width="4"
              stroke-linecap="round" stroke-linejoin="round" />
            <path d="M24 38V44" stroke="#333" stroke-width="4" stroke-linecap="round" stroke-linejoin="round" />
          </svg>
           <span>录音中... | 点击停止</span>
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import baseApiUrl from '../../config.default'
import Recorder from 'js-audio-recorder'

export default {
  name: 'HomePage',
  data () {
    return {
      isRecording: false,
      isLoading: false,
      sidebarItems: ['CET-4水平', 'CET-6水平', 'IELTS仿真测试'],
      activeIndex: 0,
      messages: [],
      prompts: '现在你将作为一个英语口语陪练助手，请给予用户以话题引导和纠错评分，并尽可能简洁地回答',
      hello: `你好，我是您的英语口语陪练助手，我可以提供一些常用服务和信息，例如：

1. 话题引导：我可以给你提供各种话题，帮助你展开对话或练习特定主题的表达。告诉我你感兴趣的话题或让我为你选择一个话题吧！

2. 咨询服务：如果你有任何问题需要咨询，例如健康、法律、投资等方面，我可以尽可能为你提供帮助。

3. 纠错评分：我会帮你检查口语表达中的错误，并给予适当的纠正和评分。请告诉我你需要我关注哪些方面，比如语法、发音、词汇或流利度。

4. 闲聊：如果你感到寂寞或无聊，我们可以聊一些有趣的话题，以减轻你的压力。

请告诉我你需要哪方面的帮助，我会根据你的需求给你提供相应的信息和建议。`,
      isInit: false
    }
  },
  mounted () {
    this.initRecorder()
    this.sendMessage(1)
  },
  methods: {
    initRecorder () {
      // 服务器需要https协议或者设置一下浏览器
      if (typeof (navigator.mediaDevices.getUserMedia) === 'undefined') {
        this.$message.error('当前没有语音权限！')
        return
      }
      if (navigator.mediaDevices.getUserMedia) {
        const constraints = { audio: true }
        navigator.mediaDevices.getUserMedia(constraints).then(() => {
          console.log('授权成功！')
        }, () => {
          console.error('授权失败！')
        })
      } else {
        console.error('浏览器不支持 getUserMedia')
      }
      this.recorder = new Recorder({
        sampleBits: 16, // 采样位数
        sampleRate: 16000, // 采样率，支持 11025、16000、22050、24000、44100、48000，根据浏览器默认值，我的chrome是48000
        numChannels: 1 // 声道，支持 1 或 2， 默认是1
      })
    },
    onSpeak () {
      this.isRecording = !this.isRecording
      this.recorder.start().then(function () {
        this.$message('speaking...')
      })
    },
    sendSpeak () {
      this.isRecording = !this.isRecording
      this.isLoading = true
      this.recorder.stop()
      // this.recorder.play()
      const blob = this.recorder.getWAVBlob()
      // this.blobToBase64(blob).then(stream => {
      //   console.log('语音打印', stream)
      //   this.sendMessage(stream)
      // })
      this.sendMessage(blob)
    },
    blobToBase64 (blob) {
      return new Promise((resolve, reject) => {
        const fileReader = new FileReader()
        fileReader.onload = (e) => {
          resolve(e.target.result)
        }
        fileReader.readAsDataURL(blob)
        fileReader.onerror = () => {
          reject(new Error('blobToBase64 error'))
        }
      })
    },
    selectItem (index) {
      this.activeIndex = index
      this.isInit = false
      this.sendMessage(1)
    },
    sendMessage (blobdata) {
      const url = `${baseApiUrl}/getmsg?isinit=` + this.isInit + '&level=' + this.activeIndex
      this.isInit = true
      const blob = new Blob([blobdata], { type: 'application/octet-stream' })
      const formData = new FormData()
      formData.append('file', blob, 'user.wav')
      // 在这里发送消息给后端并接收回复
      axios.post(url, formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      }).then(response => {
        // console.log('登录信息:', response.data.token)
        if (response.status === 200) {
          console.log(response.data.response)
          const res = {
            content: response.data.response,
            time: new Date().toLocaleTimeString(),
            isUserMessage: false,
            audio: response.data.audio
          }
          if (isNaN(response.data.userMsg)) {
            const usrRes = {
              content: response.data.userMsg,
              time: new Date().toLocaleTimeString(),
              isUserMessage: true,
              score:
              {
                '词汇精确度:': parseFloat(response.data.score.accuracy_score),
                '语言流畅度:': parseFloat(response.data.score.fluency_score),
                '语句完整度:': parseFloat(response.data.score.integrity_score),
                '发音标准度:': parseFloat(response.data.score.standard_score),
                '综合评分:': parseFloat(response.data.score.total_score)
              }
            }
            this.messages.push(usrRes)
          }
          this.messages.push(res)
          const audioBlob = this.base64ToBlob(res.audio)
          const wav = document.getElementById('wav')
          wav.src = window.URL.createObjectURL(audioBlob)
          this.isLoading = false
        } else if (response.status === 402) {
          this.$message.error('请输入您的问题')
        }
      }).catch(() => {
        this.$message.error('请输入您的问题')
      })
      this.inputMessage = ''
    },
    base64ToBlob (base64) {
      const typeHeader = 'data:application/wav' + ';base64,' // 定义base64 头部文件类型
      const audioSrc = typeHeader + base64 // 拼接最终的base64
      const arr = audioSrc.split(',')
      const array = arr[0].match(/:(.*?);/)
      const mime = (array && array.length > 1 ? array[1] : 'wav') || 'wav'
      // 去掉url的头，并转化为byte
      const bytes = window.atob(arr[1])
      // 处理异常,将ascii码小于0的转换为大于0
      const ab = new ArrayBuffer(bytes.length)
      // 生成视图（直接针对内存）：8位无符号整数，长度1个字节
      const ia = new Uint8Array(ab)
      for (let i = 0; i < bytes.length; i++) {
        ia[i] = bytes.charCodeAt(i)
      }
      const bb = new Blob([ab], { type: mime })
      return bb
    }
  }
}
</script>

<style>
.chat-container {
  display: flex;
}

.sidebar {
  width: 200px;
  background-color: #f1f1f1;
  padding: 20px;
  box-sizing: border-box;
}

.sidebar-header {
  text-align: center;
  margin-bottom: 20px;
}

.sidebar-menu {
  list-style: none;
  padding: 0;
  margin: 0;
}

.sidebar-menu li {
  cursor: pointer;
  padding: 10px;
  margin-bottom: 10px;
  background-color: #fff;
}

.sidebar-menu li.active {
  background-color: #ccc;
}

.chat-content {
  flex: 1;
  padding: 20px;
  box-sizing: border-box;
}

.chat-header {
  margin-bottom: 0px;
}

.chat-messages {
  overflow-y: scroll;
}

.message {
  margin-bottom: 10px;
  padding: 10px;
  border-radius: 5px;
}

.user-message {
  background-color: #e0dfdf;
  text-align: text;
  margin-left: 30%;
}

.bot-message {
  margin-right: 30%;
  background-color: #c6eec1;
}

.message-time {
  font-size: 12px;
  color: #888;
}

.chat-input {
  display: flex;
  margin-top: 20px;
}

.chat-input input {
  flex: 1;
  padding: 5px;
  margin-right: 5px;
}

.chat-input button {
  padding: 5px 10px;
}</style>

#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2024/8/23 17:35
@Author  : fengli
@File    : simhash_self
@Function:
"""

import hashlib
import jieba


class SimHash:
    def __init__(self, hash_size=64):
        self.hash_size = hash_size
        self.weight_dict = self.init_weight()
        self.tokenizer = jieba.cut
        self.stopwords = []

    def init_weight(self):
        res = {}
        with open('C://Users//Donson//Desktop//projects//self//work_lr//sim_hash_self//data//dict.txt', 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                line = line.split()

                res[line[0]] = res.get(line[0], int(line[1]))
        return res

    def segment(self, text: str) -> list:
        if not text or len(text.strip()) == 0:
            return []
        tokens = self.tokenizer(text)
        return [word for word in tokens if word not in self.stopwords and len(word.strip()) != 0]

    @staticmethod
    def han_hash(text: str, hash_size: int):
        if text == "":
            return 0
        else:
            x = ord(text[0]) << 7
            m = 1000003
            mask = 2 ** hash_size - 1
            for c in text:
                x = ((x * m) ^ ord(c)) & mask
            x ^= len(text)
            if x == -1:
                x = -2
            return bin(x)[2:].zfill(hash_size)[-hash_size:]

    @staticmethod
    def hamming(x: int, y: int, bit: int) -> int:
        x = (x ^ y) & ((1 << bit) - 1)
        y = 0
        while x != 0:
            x = x & x - 1
            y += 1
        return y

    @staticmethod
    def hash_weight(hash_code, weight):
        res = []
        for code in hash_code:
            if code == '1':
                res.append(weight)
            else:
                res.append(-weight)
        return res

    def encode(self, text: str) -> str:
        words = self.segment(text)  # step1: 分词
        code = [0] * self.hash_size
        for word in words:
            hash_code = self.han_hash(word, self.hash_size)  # step 2: Hash
            word_weight = self.weight_dict.get(word, 1)
            weights = self.hash_weight(hash_code, word_weight)  # step 3: 加权
            for i, w in enumerate(weights):
                code[i] += w  # step 4: 合并
        for i, c in enumerate(code):  # step 5: 降维
            if c > 0:
                code[i] = 1
            else:
                code[i] = 0
        return ''.join([str(x) for x in code])

    def similar(self, t1: str, t2: str, n: int = 3) -> bool:
        t1 = self.encode(t1)
        t2 = self.encode(t2)
        t1 = self.covert_str_to_int(t1)
        t2 = self.covert_str_to_int(t2)
        distance = self.hamming(t1, t2, self.hash_size)
        return True if distance <= n else False

    @staticmethod
    def covert_str_to_int(s: str) -> int:
        return int(s.encode(), 2)


if __name__ == "__main__":
    text1 = """今天我在中环的City Walk拍摄 阳光洒在繁忙的街道上 行人穿梭如织 这个地方总是充满活力 不管是独特的建筑还是丰富的美食 都让我停下脚步 无论是绚丽的街头艺术 还是街角的小店 都是值得牢记的瞬间 让我们一起捕捉这些瞬间，留下属于我们的回忆！ - 设备 富士相机 FUJIFILM·X-T30II + 18-55镜头 CCD N100 拍立得 iPhone14Pro Max iPhone8PM （即将换iPhone16） - 香港陪拍女生｜香港约拍｜富士相机｜陪拍 香港 ｜香港旅行 ｜香港拍照 ｜香港打卡 ｜中环 ｜香港旅游 ｜周末去哪儿 ｜香港旅游攻略 ｜香港约拍 ｜香港街拍 ｜城市活动超好玩 ｜城市摄影 ｜人像摄影 ｜人像约拍 ｜胶片摄影 ｜每秒都值得记录 ｜我的随手拍 ｜复古 ｜复古港风 ｜富士 ｜富士相机 ｜香港摄影师 ｜香港天气 ｜香港机位 ｜富士滤镜 nc滤镜｜胶片模拟｜坚尼地城｜尖沙咀｜旺角｜油麻地｜佐敦｜ #香港陪拍[话题]# #约拍[话题]# #香港拍照[话题]# #香港打卡[话题]# #香港拍照[话题]# #香港机位[话题]# #香港旅遊[话题]# #香港必吃[话题]# #香港必打卡[话题]# #网红打卡[话题]#"""
    text2 = """听听风的来意，和温柔城市的脾气☁️☁️ 昆明的温度确实舒适，好适合City walk，小街巷里边一不小心就遇到有调调的咖啡店之类的 因为带着娃，行程🔛0.6倍速😂 从对月楼到东方书店到黄公东街，然后游了个船就大半天过去了，有点遗憾没去成陆军讲武堂和文林街文化巷。 ✨对月楼两边都能拍，时间段不同光线不同，建议上午早一点人会少很多！ ✨东方书店确实很有味道，喜欢里面的设计～ ✨黄公东街是好拍，虽然简简单单，但黄墙绿窗确实容易出片，记得穿纯色！白色、红色都好看！ 🌟建议700米以上的路程可以扫个路边的小电驴，风吹着可舒服了，女儿很喜欢🥰 🌟非正常咖啡小踩雷，店很小，就门口一个打卡的地方也旧旧的，专门跑过去有点失望 btw：第一次用我的新卡片机📷！十分方便咱就说哈哈，扫街神器名不虚传，就是定焦吧宏观的是无能为力了 #扫街[话题]# #旅行日记 #昆明[话题]##citywalk[话题]# #对月楼[话题]# #东方书店[话题]# #黄公东街[话题]# #云南[话题]# #带娃旅行[话题]##理光gr3x[话题]# #理光直出[话题]##扫街#昆明#citywalk#对月楼#东方书店#黄公东街#云南#带娃旅行#理光gr3x#理光直出"""
    # text2 = """今天我在中环的City Walk拍摄 阳光洒在繁忙的街道上 行人穿梭如织 这个地方总是充满活力 不管是独特的建筑还是丰富的美食 都让我停下脚步 无论是绚丽的街头艺术 还是街角的小店 都是值得牢记的瞬间 让我们一起捕捉这些瞬间，留下属于我们的回忆！ - 设备 富士相机 FUJIFILM·X-T30II + 18-55镜头 CCD N100 拍立得 iPhone14Pro Max iPhone8PM （即将换iPhone16） - 香港陪拍女生｜香港约拍｜富士相机｜陪拍 香港 ｜香港旅行 ｜香港拍照 ｜香港打卡 ｜中环 ｜香港旅游 ｜周末去哪儿 ｜香港旅游攻略 ｜香港约拍 ｜香港街拍 ｜城市活动超好玩 ｜城市摄影 ｜人像摄影 ｜人像约拍 ｜胶片摄影 ｜每秒都值得记录 ｜我的随手拍 ｜复古 ｜复古港风 ｜富士 ｜富士相机 ｜香港摄影师 ｜香港天气 ｜香港机位 ｜富士滤镜 nc滤镜｜胶片模拟｜坚尼地城｜尖沙咀｜旺角｜油麻地｜佐敦｜ #香港陪拍[话题]# #约拍[话题]# #香港拍照[话题]# #香港打卡[话题]# #香港拍照[话题]# #香港机位[话题]# #香港旅遊[话题]# #香港必吃[话题]# #香港必打卡[话题]# #网红打卡[话题]#：官翻机 Ｎ：官换机 3A：展示机 第3️⃣步：检查一些常用功能是否正常 🟢录一段音频听一下扬声器🔉无杂音和自己的声音是否一致 🟢打开备忘录白色页面观察有无黑点斑块再用涂鸦笔涂满屏幕检查有无断触 🟢打开相机录一段长视频中间不能出现卡顿重启现象 🟢检查显示与亮度能否正常调节、有无原彩显示，没有就证明不是原装屏幕 🟢打开设置-隐私与安全-分析与改进-分析数据查看有无pan开头的如果有就表示主板有过重启现象不能要❗️ 第4️⃣步：设置-通用—还原-抹掉所有内容和设置 避免出现有隐藏ID🔒 💭以上就是我的整个验机流程，可能还不够全面但是也足够了 ✅再提醒大家🛎一定要边录视频边开箱这很重要‼️希望可以帮到姐妹们，还有什么疑问可以问我 #二手平板#二手ipad#ipadair5#分享真实感受#数码好物分享#苹果平板#苹果ipad#ipad#数码#后续#避雷"""
    sh = SimHash()
    encoded1 = sh.encode(text1)  # 进行SimHash编码
    encoded2 = sh.encode(text2)  # 进行SimHash编码
    similar = sh.similar(text1, text2, 6)  # 相似度计算，n=3
    print(encoded1)
    print(encoded2)
    print(similar)

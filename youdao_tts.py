import time
import math
import random
import sys
import hashlib
import requests
from pygame import mixer
from mutagen.mp3 import MP3


def encrypt(signStr:str):
    hash_a = hashlib.md5()
    hash_a.update(signStr.encode("utf8"))
    return hash_a.hexdigest()


def play(mp3_file:str):
    audio = MP3(mp3_file)
    mixer.init()
    mixer.music.load(mp3_file)
    mixer.music.play()
    time.sleep(math.ceil(audio.info.length))
    mixer.music.stop()


r = math.floor(time.time() * 1000)
i = r + int(random.random() * 10)
bv = encrypt(
    "5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36"
)
lang_dict = {
    0: "zh-CHS",
    1: "en",
    2: "ja",
    3: "ko",
    4: "fr",
    5: "de",
    6: "ru",
    7: "es",
    8: "pt",
    9: "it",
    10: "vi",
    11: "id",
    12: "ar",
    13: "nl",
    14: "th",
}
print(
    """----Code of languages----
 0:Chinese    1:English       2:Japanese
 3:Korean     4:French        5:German
 6:Russian    7:Spanish       8:Portuguese
 9:Italian   10:Vietnamese   11:Indonesian
12:Arabic    13:Dutch        14:Thai
"""
)
choice = input(
    "Enter the code of source and target language, separated by blank space:"
).split()
source_lang = lang_dict.get(int(choice[0]))
target_lang = lang_dict.get(int(choice[1]))
src_text = input("Enter the source text：")
sign = encrypt("fanyideskweb" + src_text + str(i) + "Y2FYu%TNSbMCxc3t2u^XT")
data = {
    "i": src_text,
    "from": source_lang,
    "to": target_lang,
    "smartresult": "dict",
    "client": "fanyideskweb",
    "salt": i,
    "sign": sign,
    "lts": r,
    "bv": bv,
    "doctype": "json",
    "version": "2.1",
    "keyfrom": "fanyi.web",
    "action": "FY_BY_CLICKBUTTION",
}
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36",
    "Referer": "https://fanyi.youdao.com/",
    "Cookie": '_ntes_nnid=01bafcc053a1b8c487f5320da1d35665,1611241914563; OUTFOX_SEARCH_USER_ID_NCOO=105258957.07438663; OUTFOX_SEARCH_USER_ID="667168764@10.169.0.83"; _ga=GA1.2.1849880949.1630482256; STUDY_SESS="1jDqkaa/hD6ysUHULpsW5fH296KN7EWTeD1Opea5EyVvIcjHARlolyGmyCUm5PgLbkZUGNYe4XlxGYWOWJurySbDEEAQqVbpNUGzCM+A79Yb2SbsB0oU44YFesEU6TZGC3Z1WEWIO+U9FPSuquxxAucE093QWB6rCXJp824v+53KYP+x96gU5YBIdRj+bud8"; STUDY_INFO="a18601631378@163.com|-1|1034127291|1632574565632"; JSESSIONID=aaaB0tiVlSXQc6t-mODWx; DICT_FORCE=true; NTES_SESS=HZ1RhLo9ztuIxsS8M1wb.x1Yl5ahHGuZgASUF6nuL8LyTPr9Tw.qDBZFDLXonhd53.FCsebQfBKhdl4nokWFHV.KZB5uM0jt__Xb_Age4l4kurNfPQh_ONQuIPmuhSOIwp4WufJYlh5H6qqs38GUubHTmTxoC3f_gGiikvJ.dOOVbxDVUSxTmwGHYzWCDxEvjNjfS6nbXXJyQQSGYdzGgT6udnRQeobYk; S_INFO=1632584722|0|3&80##|a18601631378; P_INFO=a18601631378@163.com|1632584722|0|youdao_fanyi|00&99|shh&1632574464&mail163#shh&null#10#0#0|186378&1|mail163&mailmaster_ios&newsclient|a18601631378@163.com; DICT_SESS=v2|9e1sWtDC70TSh4gLRHpuRJBPMJBOMQuRPZ0LzMPLe40p4nMUl0HPu0Yl0HpLnfJB0wuP4lG6LgLRTyk4OlOMgB0JFnMTBhHgZ0; DICT_PERS=v2|urscookie||DICT||web||604800000||1632584723068||114.85.106.16||a18601631378@163.com||kWOLTK6LkWRzlhfpShLpu0eynMgLhMUG0YE64JFnHqZ0eK6LwFRfq40z5k4TShfqu0OWk4YfhMkY0YEh4kYhHe4R; DICT_LOGIN=3||1632584723072; ___rl__test__cookies=1632588251252',
}
url = "https://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule"

html = requests.post(url=url, data=data, headers=headers)
result = html.json()
dict1 = result["translateResult"][0][0]
print(result["type"])
print(dict1["tgt"])
if target_lang in ["en", "ja", "ko", "fr"]:
    target = {"en": "eng", "ja": "jap", "ko": "ko", "fr": "fr"}.get(target_lang)
    url2 = f"https://tts.youdao.com/fanyivoice?word={dict1['tgt']}&le={target}&keyfrom=speaker-target"
    mp3 = requests.post(url=url2, data=data, headers=headers)
    file = dict1["tgt"].strip('\/:*?"<>|').split(",")[0]
    with open(f"{file}.mp3", "ab+") as f:
        f.write(mp3.content)
    play(f"{file}.mp3")
if input("Press q for quit:").lower() == "q":
    sys.exit()

# -*- coding: utf-8 -*-
import requests, json, textwrap, time, os, glob, random, hashlib
from random import randint
from PIL import Image, ImageDraw, ImageFont, ImageStat, ImageFilter, ImageEnhance
import nltk
from resizeimage import resizeimage
from tinydb import TinyDB, Query
import autoit
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains

def brightness(im):
   #im = Image.open(im_file).convert('L')
   stat = ImageStat.Stat(im)
   return stat.mean[0]

db = TinyDB('./db.json')
with open('myauth.json') as json_file:
    data = json.load(json_file)
    firebase = data['firebase']
    username = data['username']
    password = data['password']
    unsplashApiKey = data['unsplash']['apiKey']
    firebaseEmail = data['firebase-email']
    firebasePassword = data['firebase-password']
    ritekitClientId = data['ritekitClientId']
    ritekitClientSecret = data['ritekitClientSecret']

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
image_size_x = 1080
image_size_y = 1350
blur = 0
color = 'rgb(0, 0, 0)'

done = 0
while done >= 0 and done < 9:
    try:
        URL = "https://api.forismatic.com/api/1.0/?method=getQuote&lang=en&format=jsonp&jsonp=?"
        r = requests.get(url = URL)
        while not r:
            r = requests.get(url = URL)
        data = r.content
        data = data[2:]
        data = data[:-1]
        data = json.loads(data)
        text = data['quoteText']
        author = data['quoteAuthor']
        print(text)
        print(author)
        # get text hash
        md5hash = hashlib.md5(text)
        print(md5hash.hexdigest())

        while db.search(Query().textMd5 == md5hash.hexdigest()):
            r = requests.get(url = URL)
            while not r:
                r = requests.get(url = URL)
            data = r.content
            data = data[2:]
            data = data[:-1]
            data = json.loads(data)
            text = data['quoteText']
            author = data['quoteAuthor']
            print(text)
            print(author)
            # get text hash
            md5hash = hashlib.md5(text)

        db.insert({'textMd5': md5hash.hexdigest()})
        done = 10
    except:
        done += 1
        pass
#image = requests.get("https://picsum.photos/" + str(image_size_x) + "/" + str(image_size_y) + "/?blur=" + str(blur)).content-----
is_noun = lambda pos: pos[:2] == 'NN'
tokenized = nltk.word_tokenize(text)
nouns = [word for (word, pos) in nltk.pos_tag(tokenized) if is_noun(pos)] 
if len(nouns) != 0:
    for noun in nouns:
        URL = "https://source.unsplash.com/1080x1350/?" + noun
        r = requests.get(url = URL)
        if r.status_code == 200:
            break

if len(nouns) == 0 or r.status_code != 200:
    print ("< Using Default >")
    URL = "https://source.unsplash.com/random/1080x1350"
image = requests.get(URL).content
with open('latest.png', 'wb') as handler:
    handler.write(image)
with open('latest.png', 'r+b') as f:
    with Image.open(f) as image:
        cover = resizeimage.resize_cover(image, [1080, 1350])
        cover.save('latest.png', "PNG")

# get image hash
md5hash = hashlib.md5(Image.open('latest.png').tobytes())
print(md5hash.hexdigest())
while db.search(Query().imageMd5 == md5hash.hexdigest()):
    image = requests.get(URL).content
    with open('latest.png', 'wb') as handler:
        handler.write(image)
    with open('latest.png', 'r+b') as f:
        with Image.open(f) as image:
            cover = resizeimage.resize_cover(image, [1080, 1350])
            cover.save('latest.png', "PNG")
    md5hash = hashlib.md5(Image.open('latest.png').tobytes())

db.insert({'imageMd5': md5hash.hexdigest()})

background = cover
background = ImageEnhance.Contrast(background).enhance(random.uniform(0.7, 1.0))
background = background.filter(ImageFilter.GaussianBlur(radius = randint(0, 5)))

crop_rectangle = (200, 200, image_size_x - 200, image_size_y - 400)
cropped_im = background.crop(crop_rectangle)
template = "template_black.png"
if int(brightness(cropped_im)) < 120:
    color = 'rgb(255, 255, 255)'
    background = background.point(lambda  p: p * 0.9)   #darken
    template = "template_white.png"

foreground = Image.open(template)

background.paste(foreground, (0, 0), foreground)
img = background
draw = ImageDraw.Draw(img)
font_name = random.choice(glob.glob("./fonts/*.ttf"))
print ("font: " + font_name)
font = ImageFont.truetype(font_name, size=65)

para = textwrap.wrap(text, width=25)
current_h, pad = 250, 10
for line in para:
    w, h = draw.textsize(line, font=font)
    draw.text(((image_size_x - w) / 2, current_h), line, font=font, fill=color)
    current_h += h + pad
if author:
    font = ImageFont.truetype(font_name, size=75)
    current_h += h + pad
    para = textwrap.wrap(author, width=15)
    for line in para:
        w, h = draw.textsize(line, font=font)
        draw.text(((image_size_x - w) / 2, current_h), line + ".", font=font, fill=color)
        current_h += h + pad

img.save("ready.png", "PNG")
if os.path.exists("latest.png"):
    os.remove("latest.png")
img.show()

photo_path = "ready.png"
numberOfHashtags = 5
URL = "https://api.ritekit.com/v1/stats/auto-hashtag?post="
for word in text.split():
    URL += word
    URL += "%20"
URL += "&maxHashtags=" + str(numberOfHashtags) + "&hashtagPosition=auto&client_id=" + ritekitClientId
r = requests.get(url = URL)
while not r:
     r = requests.get(url = URL)
data = r.content
data = json.loads(data)
caption = data['post']
print (caption)
image_path = os.path.dirname(os.path.abspath(__file__)) + "\\ready.png"

mobile_emulation = { "deviceName": "Pixel 2" }
opts = webdriver.ChromeOptions()
opts.add_experimental_option("mobileEmulation", mobile_emulation)
#opts.add_argument("--headless")

driver = webdriver.Chrome(executable_path=r"./chromedriver",options=opts)

main_url = "https://www.instagram.com"
driver.get(main_url)

sleep(4)

def login():
    login_button = driver.find_element_by_xpath("//button[contains(text(),'Log In')]")
    login_button.click()
    sleep(randint(3,4))
    username_input = driver.find_element_by_xpath("//input[@name='username']")
    username_input.send_keys(username)
    password_input = driver.find_element_by_xpath("//input[@name='password']")
    password_input.send_keys(password)
    password_input.submit()

login()

sleep(randint(3,4))

def close_reactivated():
    try:
        sleep(randint(2,3))
        not_now_btn = driver.find_element_by_xpath("//a[contains(text(),'Not Now')]")
        not_now_btn.click()
    except:
        pass

close_reactivated()

def close_notification():
    try: 
        sleep(randint(2,3))
        close_noti_btn = driver.find_element_by_xpath("//button[contains(text(),'Not Now')]")
        close_noti_btn.click()
        sleep(randint(2,3))
    except:
        pass

close_notification()

def close_add_to_home():
    sleep(randint(3,4)) 
    close_addHome_btn = driver.find_element_by_xpath("//button[contains(text(),'Cancel')]")
    close_addHome_btn.click()
    sleep(randint(1,2))

close_add_to_home()
sleep(randint(3,4))
close_notification()
new_post_btn = driver.find_element_by_xpath("//div[@role='menuitem']").click()
sleep(randint(3,4))
autoit.win_active("Open") 
sleep(randint(3,4))
autoit.control_send("Open","Edit1",image_path) 
sleep(randint(3,4))
autoit.control_send("Open","Edit1","{ENTER}")
sleep(randint(3,4))
driver.find_element_by_xpath("//button[@class='pHnkA']").click()
sleep(randint(3,4))
next_btn = driver.find_element_by_xpath("//button[contains(text(),'Next')]").click()
sleep(randint(3,4))
caption_field = driver.find_element_by_xpath("//textarea[@aria-label='Write a caption…']")
caption_field.send_keys(caption)
share_btn = driver.find_element_by_xpath("//button[contains(text(),'Share')]").click()
sleep(randint(3,4))
driver.close()
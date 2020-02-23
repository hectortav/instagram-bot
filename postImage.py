# -*- coding: utf-8 -*-
import requests, json, textwrap, time, os
from PIL import Image, ImageDraw, ImageFont, ImageStat, ImageFilter, ImageEnhance
import nltk
from resizeimage import resizeimage

def brightness(im):
   #im = Image.open(im_file).convert('L')
   stat = ImageStat.Stat(im)
   return stat.mean[0]

with open('myauth.json') as json_file:
    data = json.load(json_file)
    firebase = data['firebase']
    username = data['username']
    password = data['password']
    unsplashApiKey = data['unsplash']['apiKey']
    firebaseEmail = data['firebase-email']
    firebasePassword = data['firebase-password']

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
image_size_x = 1080
image_size_y = 1350
blur = 0
color = 'rgb(0, 0, 0)'

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

#image = requests.get("https://picsum.photos/" + str(image_size_x) + "/" + str(image_size_y) + "/?blur=" + str(blur)).content
is_noun = lambda pos: pos[:2] == 'NN'
tokenized = nltk.word_tokenize(text)
nouns = [word for (word, pos) in nltk.pos_tag(tokenized) if is_noun(pos)] 
if len(nouns) != 0:
    for noun in nouns:
        URL = "https://source.unsplash.com/1080x1350/?" + noun
        r = requests.get(url = URL)
        if r.status_code == 200:
            break

if len(nouns) != 0 and r.status_code == 200:
    image = requests.get(URL).content
    with open('latest.png', 'wb') as handler:
        handler.write(image)

    with open('latest.png', 'r+b') as f:
        with Image.open(f) as image:
            cover = resizeimage.resize_cover(image, [1080, 1350])
            cover.save('latest.png', "PNG")
else:
    print ("< Using Default >")
    image = requests.get("https://picsum.photos/" + str(image_size_x) + "/" + str(image_size_y) + "/?blur=" + str(blur)).content
    with open('latest.png', 'wb') as handler:
        handler.write(image)


background = Image.open("latest.png")
background = ImageEnhance.Contrast(background).enhance(0.6)
background = background.filter(ImageFilter.GaussianBlur(radius = 5))
background.save("latest.png", "PNG")

crop_rectangle = (200, 200, image_size_x - 200, image_size_y - 400)
cropped_im = background.crop(crop_rectangle)
template = "template_black.png"
if int(brightness(cropped_im)) < 120:
    color = 'rgb(255, 255, 255)'
    background = background.point(lambda  p: p * 0.9)   #darken
    template = "template_white.png"

foreground = Image.open(template)

background.paste(foreground, (0, 0), foreground)
background.save("combine.png", "PNG")
exit(0)
img = Image.open("combine.png")
draw = ImageDraw.Draw(img)
font = ImageFont.truetype('./fonts/Great-Wishes.ttf', size=45)
#random.choice(fontList)
para = textwrap.wrap(text, width=35)
current_h, pad = 200, 10
for line in para:
    w, h = draw.textsize(line, font=font)
    draw.text(((image_size_x - w) / 2, current_h), line, font=font, fill=color)
    current_h += h + pad
if author:
    current_h += h + pad
    para = textwrap.wrap(author, width=25)
    current_h, pad = 200, 10
    for line in para:
        w, h = draw.textsize(line, font=font)
        draw.text(((image_size_x - w) / 2, current_h), line + ".", font=font, fill=color)
        current_h += h + pad

img.save("ready.png", "PNG")
img.show()

photo_path = "ready.png"
caption = "#inspiration #inspirationalquotes #inspirational #inspirationalquote #inspirations #inspirationoftheday \
    #inspirationalwords #love #instagood #me #cute #tbt #photooftheday #instamood #iphonesia #tweegram #picoftheday \
    #igers #girl #beautiful #instadaily #summer #instagramhub #follow #igdaily #bestoftheday #happy #picstitch #tagblender \
    #jj #sky #nofilter #fashion #followme #fun #su"

username = "__inspiredtoday__"
with open('.password.txt', 'r') as file:
    password = file.read().replace('\n', '')
image_path = os.path.dirname(os.path.abspath(__file__)) + "\\ready.png"

exit(0)

import autoit
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains

mobile_emulation = { "deviceName": "Pixel 2" }
opts = webdriver.ChromeOptions()
opts.add_experimental_option("mobileEmulation", mobile_emulation)

driver = webdriver.Chrome(executable_path=r"./chromedriver",options=opts)

main_url = "https://www.instagram.com"
driver.get(main_url)

sleep(4)

def login():
    login_button = driver.find_element_by_xpath("//button[contains(text(),'Log In')]")
    login_button.click()
    sleep(3)
    username_input = driver.find_element_by_xpath("//input[@name='username']")
    username_input.send_keys(username)
    password_input = driver.find_element_by_xpath("//input[@name='password']")
    password_input.send_keys(password)
    password_input.submit()

login()

sleep(4)

def close_reactivated():
    try:
        sleep(2)
        not_now_btn = driver.find_element_by_xpath("//a[contains(text(),'Not Now')]")
        not_now_btn.click()
    except:
        pass

close_reactivated()

def close_notification():
    try: 
        sleep(2)
        close_noti_btn = driver.find_element_by_xpath("//button[contains(text(),'Not Now')]")
        close_noti_btn.click()
        sleep(2)
    except:
        pass

close_notification()

def close_add_to_home():
    sleep(3) 
    close_addHome_btn = driver.find_element_by_xpath("//button[contains(text(),'Cancel')]")
    close_addHome_btn.click()
    sleep(1)

close_add_to_home()
sleep(3)
close_notification()
new_post_btn = driver.find_element_by_xpath("//div[@role='menuitem']").click()
sleep(1.5)
autoit.win_active("Open") 
sleep(2)
autoit.control_send("Open","Edit1",image_path) 
sleep(1.5)
autoit.control_send("Open","Edit1","{ENTER}")
sleep(2)
next_btn = driver.find_element_by_xpath("//button[contains(text(),'Next')]").click()
sleep(1.5)
caption_field = driver.find_element_by_xpath("//textarea[@aria-label='Write a caption…']")
caption_field.send_keys(caption)
share_btn = driver.find_element_by_xpath("//button[contains(text(),'Share')]").click()
sleep(1)
driver.close()
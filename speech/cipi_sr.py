import re
import datetime
import aiml
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import snowboydecoder
import sys
import signal

# Demo code for listening two hotwords at the same time

interrupted = False
yesno_state = False
listen_state = False
talk_state = False
cmd = ""

if cmd == "time":
    a = datetime.datetime.now()
    hour = a.time().hour
    minute = a.time().minute
    resp = "Sekarang jam " + str(hour)+ " lewat " + str(minute)


def cek_talking():
    try:
        m = browser.find_element_by_class_name("goog-toolbar-button-checked")
        talk_state = True
        return True
    except:
        talk_state = False
        return False

def get_speech():
    if talk_state == True: time.sleep(2)
    listen_state = True
    record = speech_rec.find_element_by_xpath('//*[@id="gt-speech"]/span')
    record.click()
    time.sleep(4)
    #record
    record.click()
    source = speech_rec.find_element_by_xpath('//*[@id="source"]')
    a = source.get_attribute("value")
    print a
    listen_state = False
    return a

def talk(speech):
    if listen_state == True: time.sleep(4)
    talk_state = True
    tts = browser.find_element_by_xpath('//*[@id="source"]')
    tts.clear()
    tts.send_keys(str(speech))
    time.sleep(2)
    talk = browser.find_element_by_xpath('//*[@id="gt-src-listen"]/span')
    talk.click()
    talk_state = False

def find_cmd(response):
    m = re.search(r'CMD:(\S+)\sPRM:(\S+)]',response)
    if m: 
        print m.groups()
        response = response[0:response.find("[")]+response[response.find("]")+1:]
    return response

def signal_handler(signal, frame):
    global interrupted
    interrupted = True

def interrupt_callback():
    global interrupted
    return interrupted

def play_ding():
    if not cek_talking():
        print "Play ding"
        snowboydecoder.play_audio_file(snowboydecoder.DETECT_DING)
        respn = get_speech()
        spik = find_cmd(a.respond(respn))
        talk(spik)

def yes_resp():
    print "He said: YES"
    if yesno_state: snowboydecoder.play_audio_file(snowboydecoder.DETECT_DONG)

def no_resp():
    print "He said: NO"
    if yesno_state: snowboydecoder.play_audio_file(snowboydecoder.DETECT_DONG)

'''if len(sys.argv) != 4:
    print("Error: need to specify 2 model names")
    print("Usage: python demo.py 1st.model 2nd.model")
    sys.exit(-1)'''

models = ['cipi.pmdl','ya.pmdl','enggak.pmdl']


# capture SIGINT signal, e.g., Ctrl+C
signal.signal(signal.SIGINT, signal_handler)

sensitivity = [0.5]*len(models)
detector = snowboydecoder.HotwordDetector(models, sensitivity=sensitivity)
callbacks = [lambda: play_ding(),
             lambda: yes_resp(),
             lambda: no_resp()]
print('Listening... Press Ctrl+C to exit')


browser = webdriver.Chrome()
browser.get('https://translate.google.com/?#id/en/apa%20kabar')
assert "Google Translate" in browser.title

chrome_options = Options()
chrome_options.add_argument("--use-fake-ui-for-media-stream")

speech_rec = webdriver.Chrome(chrome_options=chrome_options)
speech_rec.get('https://translate.google.com/?#id/en')
assert "Google Translate" in speech_rec.title


a = aiml.Kernel()
a.learn('/home/irq/intellegenciat/pyaiml/std-startup.xml')
a.respond('LOAD AIML IRZA')


# main loop
# make sure you have the same numbers of callbacks and models
detector.start(detected_callback=callbacks,
               interrupt_check=interrupt_callback,
               sleep_time=0.03)

detector.terminate()

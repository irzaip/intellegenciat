import re
import datetime
import aiml
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import snowboydecoder
import sys
import signal
from pyvirtualdisplay import Display

# Demo code for listening two hotwords at the same time

interrupted = False
yesno_state = False
listen_state = False
talk_state = False
sleep_state = False
cmd = ""
prm = ""

def command(cmd,prm):
    global talk_state, listen_state, sleep_state ,yesno_state
    if cmd == "JAM":
        a = datetime.datetime.now()
        hour = a.time().hour
        if hour > 12:
            hour = hour - 12
        minute = a.time().minute
        resp = "Sekarang jam %s lewat %s" % (hour, minute)
        return resp
    if cmd == "TIDUR":
        sleep_state = True
        yesno_state = True
        return "Sekarang bobo"
    if cmd == "LAMPOFF":
        resp = "oke, telah dimatikan"
        return resp

def cek_talking():
    global talk_state, listen_state, sleep_state ,yesno_state
    try:
        m = browser.find_element_by_class_name("goog-toolbar-button-checked")
        talk_state = True
        return True
    except:
        talk_state = False
        return False

def get_speech():
    global talk_state, listen_state, sleep_state ,yesno_state
    if not talk_state:
        if not sleep_state:
            listen_state = True
            source = browser.find_element_by_xpath('//*[@id="source"]')
            source.clear()
            record = browser.find_element_by_xpath('//*[@id="gt-speech"]/span')
            record.click()
            time.sleep(5)
            #record
            record.click()
            a = source.get_attribute("value")
            print a
            listen_state = False
            source.clear()
            return a

def talk(speech):
    global talk_state, listen_state, sleep_state ,yesno_state, cmd, prm
    if not talk_state:
        if not sleep_state:
            try:
                talk_state = True
                tts = browser.find_element_by_xpath('//*[@id="source"]')
                tts.clear()
                tts.send_keys(str(speech))
                time.sleep(1)
                talk = browser.find_element_by_xpath('//*[@id="gt-src-listen"]/span')
                talk.click()
                time.sleep(2)
                talk_state = False
            except:
                pass

def find_cmd(response):
    global talk_state, listen_state, sleep_state ,yesno_state, cmd, prm
    m = re.search(r'CMD:(\S+)\sPRM:(\S+)]',response)
    if m: 
        cmd = m.groups(1)[0]
        prm = m.groups(1)[1]
        print "CMD: %s , PRM: %s" % (cmd,prm)
        #
        #response = response[0:response.find("[")]+response[response.find("]")+1:]
        #response = response + " " + str(command(cmd,prm))
        response = command(cmd,prm)
    else:
        response = response
    return response

def signal_handler(signal, frame):
    global interrupted
    interrupted = True

def interrupt_callback():
    global interrupted
    return interrupted

def play_ding():
    global sleep_state, yesno_state
    if not yesno_state:
        if not sleep_state: 
            if not cek_talking():
                print "Play ding"
                snowboydecoder.play_audio_file(snowboydecoder.DETECT_DING)
                respn = get_speech()
                print "respn:",respn
                spik = find_cmd(a.respond(respn))
                print "spik:",spik
                talk(spik)

def yes_resp():
    print "He said: YES"
    if yesno_state: snowboydecoder.play_audio_file(snowboydecoder.DETECT_DONG)

def no_resp():
    global talk_state, listen_state, sleep_state ,yesno_state
    print "He said: NO"
    if yesno_state: snowboydecoder.play_audio_file(snowboydecoder.DETECT_DONG)


models = ['cipi.pmdl','ya.pmdl','enggak.pmdl']


# capture SIGINT signal, e.g., Ctrl+C
signal.signal(signal.SIGINT, signal_handler)

sensitivity = [0.5]*len(models)
detector = snowboydecoder.HotwordDetector(models, sensitivity=sensitivity)
callbacks = [lambda: play_ding(),
             lambda: yes_resp(),
             lambda: no_resp()]
print('Listening... Press Ctrl+C to exit')

display = Display(visible=0, size=(800, 600))
display.start()

chrome_options = Options()
chrome_options.add_argument("--use-fake-ui-for-media-stream")

browser = webdriver.Chrome(chrome_options=chrome_options)
browser.get('https://translate.google.com/?#id/en/apa%20kabar')
assert "Google Translate" in browser.title
talk("Halo, cipi siap menunggu perintah")

#speech_rec = webdriver.Chrome(chrome_options=chrome_options)
#speech_rec.get('https://translate.google.com/?#id/en')
#assert "Google Translate" in speech_rec.title


a = aiml.Kernel()
a.learn('/home/irq/intellegenciat/pyaiml/std-startup.xml')
a.respond('LOAD AIML IRZA')


# main loop
# make sure you have the same numbers of callbacks and models
detector.start(detected_callback=callbacks,
               interrupt_check=interrupt_callback,
               sleep_time=0.03)

detector.terminate()

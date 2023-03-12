from playwright.sync_api import Playwright, sync_playwright, expect
import curses, sys, os, time, datetime, random
from playsound import playsound
from gtts import gTTS
def name_generator():
    ran = random.randint(1,5000)
    ran = str(ran)
    return ran


def TTSTalk(case_ans):
    tts = gTTS(case_ans)
    new_name = name_generator()
    new_name= new_name+".mp3"
    tts.save(new_name)

    playsound(new_name)
    
    try:
        os.remove(new_name) 
    except:
        print("i cant do it")
        

def run(stdscr):
    if len(sys.argv) > 1:
        chara_id = sys.argv[1]
    else:
        chara_id = "hoCEWE0diTiUrLiup9Gn_OsgFKnhYTDgFid1yGE3YLA"
    browser = playwright.firefox.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()
    page.goto('https://beta.character.ai/chat?char='+chara_id)
    page.get_by_role("button", name="Accept").click()
    
    while True:
        stdscr.refresh()
        stdscr.addstr("> ")
        stdscr.refresh()
        curses.echo()
        
        
        now = datetime.datetime.now()
        time_str = "[{:%H:%M}]".format(now)
        message = stdscr.getstr().decode()
        page.get_by_placeholder("Type a message").fill(message)
        page.get_by_placeholder("Type a message").press("Enter")
        chara = page.query_selector('div.chattitle.p-0.pe-1.m-0')
        chara_name = chara.inner_text()
        page.wait_for_selector('.swiper-button-next').is_visible()
        div = page.query_selector('div.msg.char-msg')
        output_text = div.inner_text()
        stdscr.addstr(time_str+ chara_name + ' ✉\n' + output_text + '\n \n')
        
        TTSTalk(output_text);
        
        stdscr.refresh()
        if stdscr.getch() == 27:
            break

    context.close()
    browser.close()

if __name__ == '__main__':
    with sync_playwright() as playwright:
        curses.wrapper(run)

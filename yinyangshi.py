
import pyautogui
import random
import time
import cv2
# 鼠标移动策略


def mouse_method():
    m = [pyautogui.easeInOutElastic, pyautogui.easeInBack, pyautogui.easeInBounce,
         pyautogui.easeInCirc, pyautogui.easeInOutBack, pyautogui.easeInOutCirc]
    mouse_t = random.uniform(0.8, 1)
    mouse_m = random.randint(0, 5)
    return mouse_t, m[mouse_m]

#利用opencv寻找按键位置
def button(img_address,con:float=0.8,fre:float=0.5):
    while (True):
        button_pos = pyautogui.locateCenterOnScreen(
            img_address, confidence=con)
        if button_pos != None:
            return button_pos
        time.sleep(fre)
        
#可能出现的图片位置
def button_choice(img_address1,img_address2,con:float=0.8,fre:float=0.5):
    while (True):
        button_pos1 = pyautogui.locateCenterOnScreen(img_address1, confidence=con)
        button_pos2 = pyautogui.locateCenterOnScreen(img_address2,confidence=con)
        if button_pos1 is not None:
            return button_pos1
        elif button_pos2 is not None:
            return button_pos2
        time.sleep(fre)
        
# 魂11策略
def yuhun11(pos_x, pos_y):

    print('输入要循环的次数')
    N = int(input())
    print('输入你当前副本一次所需时间（整数，单位为s）：')
    yanchi = int(input())
    time.sleep(3)
    for i in range(1, N+1):
        # 取随机范围，防止点击同一个位置被检测
        num = random.randint(-40, 40)

        # 鼠标移动到挑战位置处
        pyautogui.moveTo(pos_x+num, pos_y+num, 1, pyautogui.easeInOutQuad)
        time.sleep(1.5)
        pyautogui.click()
        time.sleep(0.2)
        pyautogui.click()

        num2 = random.randint(-100, 100)
        pyautogui.moveTo(400+num2*2, 500+num2*1.5, 1, pyautogui.easeInOutQuad)
        time.sleep(yanchi+5)

    # 结束副本移到任意位置结算
        pyautogui.click()

        pyautogui.doubleClick()

        pyautogui.moveTo(900+num, 720+num, 1, pyautogui.easeInOutQuad)
        time.sleep(2)

        pyautogui.click()
        pyautogui.tripleClick()
        time.sleep((2))

        if i % 10 == 0:
            print('已经挂机{}次'.format(i))

        if i == N:
            print('挂机结束')

# 御灵策略


def yuling():
    print('输入要循环的次数')
    N = int(input())
    print('输入你当前副本一次所需时间（整数，单位为s）：')
    yanchi = int(input())
    time.sleep(3)
    for i in range(1, N+1):
        # 取随机范围，防止点击同一个位置被检测
        num = random.randint(-40, 40)
        mouse=mouse_method()
        p_tz=button('tz.png')
        # 鼠标移动到挑战位置处
        pyautogui.moveTo(p_tz[0]+num, p_tz[1]+num, mouse[0],mouse[1])
        
        pyautogui.click()

        # 选择大舅妈
        pyautogui.moveTo(1335+num/2, 677+num/2, 1, pyautogui.easeInOutQuad)
        time.sleep(3)
        pyautogui.click()

        #刷御灵时间，额外给2s富裕
        time.sleep(yanchi+2)
        
        #结算按钮
        p_js=button('jiesuan.png')
        pyautogui.moveTo(p_js[0]+num*5, p_js[1]+num, mouse[0],mouse[1])
        pyautogui.click()

        if i % 10 == 0:
            print('已经挂机{}次'.format(i))

        if i == N:
            print('挂机结束')

# 组队御魂策略


def zudui(pos_x, pos_y, pos_x1, pos_y1):
    print('输入要循环的次数')
    N = int(input())
    print('输入你当前副本一次所需时间（整数，单位为s）：')
    yanchi = int(input())
    time.sleep(3)
    for i in range(1, N+1):
        # 取随机范围，防止点击同一个位置被检测
        num = random.randint(-40, 40)

        # 鼠标移动到挑战位置处
        mouse = mouse_method()

        #pyautogui.moveTo(pos_x1+num, pos_y1+num, mouse[0], mouse[1])
        # time.sleep(1.5)
        # pyautogui.click()
        # time.sleep(0.2)
        # pyautogui.click()
        p_tz=button('hun11tz.png')
        mouse=mouse_method()
        pyautogui.moveTo(p_tz[0]+random.randint(-30,30),p_tz[1]+random.randint(-30,30),mouse[0],mouse[1])
        pyautogui.click()
    
        time.sleep(yanchi+5)

        num2 = random.randint(-50, 50)
        # 小号点击第一次结算御魂奖励
        mouse = mouse_method()
        time.sleep(0.5)
        pyautogui.moveTo(1200+num2, 880+num2*1.5, mouse[0], mouse[1])
        pyautogui.click()
        
        pyautogui.tripleClick()
        time.sleep(1)
        # 大号点击第一次结算御魂奖励
        mouse = mouse_method()
        pyautogui.moveTo(400+num2*2, 500+num2*1.5,  mouse[0], mouse[1])
        pyautogui.click()
        pyautogui.tripleClick()
        time.sleep(1)

        # 小号点击第二次退出结算界面
        mouse = mouse_method()
        pyautogui.moveTo(1700+num, 1100, mouse[0], mouse[1])
        pyautogui.click()
        pyautogui.tripleClick()
        time.sleep(1)

        # 大号点击第二次退出结算界面
        mouse = mouse_method()
        pyautogui.moveTo(600+num, 800, mouse[0], mouse[1])
        pyautogui.click()
        pyautogui.tripleClick()
        time.sleep(1)

        if i % 10 == 0:
            print('已经挂机{}次'.format(i))

        if i == N:
            print('挂机结束')

#困难28策略
def kun28():
    print('输入要循环的次数')
    N = int(input())
    for i in range(1,N+1):
        time.sleep(1)
        p_new=pyautogui.locateCenterOnScreen('kun28.png',confidence=0.8)
        p_start=pyautogui.locateCenterOnScreen('tansuokaishi.png',confidence=0.7)
        if p_start is None and p_new is not None:
            pyautogui.click(p_new[0]+random.randint(-20,20),p_new[1]+random.randint(0,15))
        p_start=button('tansuokaishi.png')
        #time.sleep(3)
        #p_start=pyautogui.locateCenterOnScreen('tansuokaishi.png',confidence=0.8)
        pyautogui.click(p_start[0]+random.randint(-20,20),p_start[1]+random.randint(0,10))
        time.sleep(1)
        p_end=pyautogui.locateCenterOnScreen('tansuojieshu.png',confidence=0.7)
        while p_end is None:
            p_ts=pyautogui.locateCenterOnScreen('tansuo.png',confidence=0.8)
            if p_ts is not None:
                pyautogui.click(p_ts)
                p_victory=button('victory.png')
                pyautogui.moveTo(p_victory[0],p_victory[1],0.5)
                pyautogui.click()
                p_js=button('jiesuan.png')
                pyautogui.moveTo(p_js[0],p_js[1],0.5)
                pyautogui.click()
                time.sleep(1.5)
                p_end=pyautogui.locateCenterOnScreen('tansuojieshu.png',confidence=0.8)
                
            else:
                time.sleep(1)
                p_end=pyautogui.locateCenterOnScreen('tansuojieshu.png',confidence=0.8)
                if p_end is None:
                    pyautogui.moveTo(1400+random.randint(-50,50),260+random.randint(-20,20))
                    pyautogui.dragRel(-800,0,random.uniform(0.8,1.5))
                
            
        pyautogui.click(p_end)
        p_victory=button('victory.png')
        mouse=mouse_method()
        pyautogui.moveTo(p_victory[0],p_victory[1],mouse[0],mouse[1])
        pyautogui.click(p_victory)
        p_js=button('jiesuan.png')
        mouse=mouse_method()
        pyautogui.moveTo(p_js[0],p_js[1],mouse[0],mouse[1])
        pyautogui.click()
        time.sleep(5)
        p_zhanlipin=pyautogui.locateCenterOnScreen('zhanlipin.png',confidence=0.8)
        #print(p_zhanlipin)
        while p_zhanlipin is not None:
            pyautogui.moveTo(p_zhanlipin[0],p_zhanlipin[1],0.3)
            pyautogui.click()
            time.sleep(0.5)
            pyautogui.click(810+random.randint(-80,80),770+random.randint(-5,30))
            time.sleep(1)
            p_zhanlipin=pyautogui.locateCenterOnScreen('zhanlipin.png',confidence=0.8)
        
        if i % 10 == 0:
            print('已经挂机{}次'.format(i))

        if i == N:
            print('挂机结束')

#结界突破策略
def jiejietupo():
        #结界突破
    print('输入要循环的次数')
    N = int(input())
    for i in range(1,N+1):
        pj_start=button('tupo1.png')
        pyautogui.click(pj_start[0]-20,pj_start[1])
        pj_attack=button('jingongjiejie.png')
        pyautogui.click(pj_attack)
        time.sleep(2)
        pyautogui.moveTo(1065,620,0.5)
        time.sleep(3)
        pyautogui.click()
        
        time.sleep(5)
        
        p_vic=button_choice('jiesuan.png','failure.png')
        #print(p_vic)
        
        """ if p_vic is None:
            p_fail=button('failure.png')
            pyautogui.click(p_fail)
            pyautogui.click()
        else: """
        # pyautogui.click(p_vic)
        # time.sleep(0.5)
        # pyautogui.moveTo(1351,300,0.5)
        # time.sleep(1)
        # pyautogui.click()
        pyautogui.moveTo(p_vic[0]+random.randint(-50,50),p_vic[1]+random.randint(-50,50),random.uniform(0.5,0.8))
        time.sleep(0.5)
        pyautogui.click()
        
        time.sleep(2)
        p_another=pyautogui.locateCenterOnScreen('jiesuan.png',confidence=0.7)
        if p_another is not None:
            pyautogui.moveTo(p_another[0],p_another[1],0.5)
            pyautogui.click()
        
        print(f'第{i}次结界突破完成')    

def zudui11():
    print('输入要循环的次数')
    N = int(input())
    print('输入你当前副本一次所需时间（整数，单位为s）：')
    yanchi = int(input())
    time.sleep(3)
    for i in range(1, N+1):
        p_tz=button('hun11tz.png')
        mouse=mouse_method()
        pyautogui.moveTo(p_tz[0]+random.randint(-30,30),p_tz[1]+random.randint(-30,30),mouse[0],mouse[1])
        pyautogui.click()
        time.sleep(yanchi)
        p_victory1=button('victory.png')
        pyautogui.moveTo(p_victory1[0]+random.randint(-30,30),p_victory1[1]+random.randint(-30,30),mouse[0],mouse[1])
        pyautogui.click()
        time.sleep(1.5)
        pyautogui.moveTo(2000+random.randint(-100,100),380+random.randint(-10,10,0.5))
        p_vic2=button('victory.png')
        pyautogui.moveTo(p_vic2[0]+random.randint(-30,30),p_vic2[1]+random.randint(-30,30),mouse[0],mouse[1])
        pyautogui.click()
        
        p_js1=button('jiesuan.png')
        pyautogui.moveTo(p_js1[0]+random.randint(-30,30),p_js1[1]+random.randint(-30,30),mouse[0],mouse[1])
        pyautogui.click()
        
        p_js2=button('jiesuan.png')
        pyautogui.moveTo(p_js2[0]+random.randint(-30,30),p_js2[1]+random.randint(-30,30),mouse[0],mouse[1])
        pyautogui.click()
        
        
def yeyuanhuo():
    print('输入要循环的次数')
    N = int(input())
    print('输入你当前副本一次所需时间（整数，单位为s）：')
    yanchi = int(input())
    time.sleep(2)
    for i in range(1, N+1):
        p_tz=button('tz.png')
        mouse=mouse_method()
        pyautogui.moveTo(p_tz[0]+random.randint(-30,30),p_tz[1]+random.randint(-30,30),mouse[0],mouse[1])    
        pyautogui.click()
        
        time.sleep(yanchi+3)
        p_vic=button('victory.png',0.6)
        pyautogui.moveTo(p_vic[0]+random.randint(-30,30),p_vic[1]+random.randint(-10,10),mouse[0],mouse[1])   
        pyautogui.click()
        p_js=button('jiesuan.png')
        pyautogui.moveTo(p_js[0]+random.randint(-30,30),p_js[1]+random.randint(-30,30),mouse[0],mouse[1])
        pyautogui.click()
        
        if i % 10 == 0:
            print('已经挂机{}次'.format(i))

        if i == N:
            print('挂机结束')
            
def daixinghuodong():
    print('输入要循环的次数')
    N = int(input())
    print('输入你当前副本一次所需时间（整数，单位为s）：')
    yanchi = int(input())
    time.sleep(3)
    for i in range(1, N+1):
        p_tz=button('huodong.png')
        mouse=mouse_method()
        pyautogui.moveTo(p_tz[0]+random.randint(-30,30),p_tz[1]+random.randint(-30,30),mouse[0],mouse[1])
        pyautogui.click()
        time.sleep(yanchi)
        p_victory1=button('finalscore.png')
        pyautogui.moveTo(p_victory1[0]+random.randint(-100,100),p_victory1[1]+random.randint(-200,-100),mouse[0],mouse[1])
        pyautogui.click()
        time.sleep(1.5)
        
        p_vic2=button('victory.png')
        pyautogui.moveTo(p_vic2[0]+random.randint(-300,-100),p_vic2[1]+random.randint(50,300),mouse[0],mouse[1])
        pyautogui.click()
# 主函数

if __name__ == '__main__':
    pos_x = 1540
    pos_y = 900
    pos_x1 = 2467
    pos_y1 = 1262
    print('''选择要刷的副本：
          a: 单人魂11
          b: 御灵
          c:组队魂11
          d:困难28
          e:结界突破
          f:业原火
          g:活动''')
    choice = input()
    if choice == 'a':
        yuhun11(pos_x, pos_y)
    elif choice == 'b':
        yuling()
    elif choice == 'c':
        zudui(pos_x, pos_y, pos_x1, pos_y1)
        #zudui11()
    elif choice=='d':
        kun28()
    elif choice=='e':
        jiejietupo()
    elif choice=='f':
        yeyuanhuo()
    elif choice=='g':
        daixinghuodong()

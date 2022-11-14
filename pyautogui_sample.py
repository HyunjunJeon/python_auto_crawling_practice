import pyautogui
import subprocess

'''
OpenCV 까지 적용했을 때 mac 에서도 동작함
- pip install opencv-python
- pip install image
- Retina Display 보정을 위한 x,y 좌표 => x/2, y/2
'''

print(pyautogui.position())
# pyautogui.screenshot('8.png', region=(2202, 693, 120, 120))
num_8 = pyautogui.locateCenterOnScreen('8.png', confidence=0.99, grayscale=True)
pyautogui.moveTo(num_8.x/2, num_8.y/2)
pyautogui.click()


def click_image(png_name):
    button = pyautogui.locateCenterOnScreen(png_name)
    x = button[0] / 2
    y = button[2] / 2
    pyautogui.moveTo(x, y)
    pyautogui.click()
    pyautogui.click()
    return "Clicked {0}".format(png_name)


def click_image_check_display(png_name):
    button = pyautogui.locateCenterOnScreen(png_name)
    x = button[0]
    y = button[1]
    if subprocess.call("system_profiler SPDisplaysDataType | grep 'retina'", shell=True) == 0:
        x = x / 2
        y = y / 2
    pyautogui.moveTo(x, y)
    pyautogui.click()
    pyautogui.click()
    return "Clicked {0}".format(png_name)


# click_image('8.png')
import os
from time import sleep
from random import choice
from selenium import webdriver

USERNAME   = os.environ['ID']
PASSWORD   = os.environ['PASSWORD']

reasons = ['就餐', '出游', '探亲访友']

print('初始化浏览器...')
driver = None
ua = 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_0_1 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) Mobile/14A403 MicroMessenger/6.3.27 NetType/WIFI Language/zh_CN'
option = webdriver.ChromeOptions()
option.headless = True
option.add_argument('user-agent='+ua)
option.add_experimental_option('w3c', False)
driver = webdriver.Chrome(executable_path='/usr/bin/chromedriver', options=option)

print('正在申请出校...')
# 统一认证登录
driver.get('https://ids.hit.edu.cn/authserver/')
driver.find_element_by_id('mobileUsername').send_keys(USERNAME)
driver.find_element_by_id('mobilePassword').send_keys(PASSWORD)
driver.find_element_by_id('load').click()
sleep(1)

# 进入申请出校页面
## method1: 直接输网址, 进不去
# driver.get('https://xg.hit.edu.cn/zhxy-xgzs/xg_mobile/xs/yqxx')
# driver.get('https://xg.hit.edu.cn/zhxy-xgzs/xg_mobile/xsCxsq')
## method2: 从学工主页点击进入
driver.get('https://xg.hit.edu.cn/zhxy-xgzs/xg_mobile/xsHome')    
driver.execute_script('wjdc()')
# print(driver.page_source)
# 点击“新建”
driver.find_element_by_class_name('right_btn').click()
sleep(1)
# 新建页面
# 出校类型 点击“临时出校”
driver.find_element_by_xpath("//label[@for='cxlx01']").click()
# 出校日期选择
driver.find_element_by_id('rqlscx').click()
sleep(1)

#%% =============
def pick_date():
    pickers = driver.find_elements_by_class_name('weui-picker__group')
    y_picker = pickers[0]
    m_picker = pickers[1]
    d_picker = pickers[2]
    d_picker_items = d_picker.find_elements_by_class_name('weui-picker__item')
    for item in d_picker_items:
        print(item.location)

    item_offset = abs(d_picker_items[0].location['y'] - d_picker_items[1].location['y'])

    # 1. 尝试使用ActionChains，失败，因为不能调整鼠标移动速度，而这个日期选择是有拖拽加速度检测的
    # action = webdriver.ActionChains(driver)
    # action.click_and_hold(d_picker_items[1])
    # # action.move_to_element(d_picker_items[0]).perform()
    # action.move_by_offset(0, -item_offset * .8).perform()
    # sleep(.3)
    # action.release().perform()

    # 2. 使用TouchActions - flick_element()
    touch_action = webdriver.TouchActions(driver)
    d_picker_indicator = d_picker.find_element_by_class_name('weui-picker__indicator')
    touch_action.flick_element(d_picker_indicator, xoffset=0, yoffset=-item_offset, speed=2*item_offset)
    touch_action.perform()

    # 3. 使用TouchAction - scroll_from_element
    # touch_action = webdriver.TouchActions(driver)
    # d_picker_indicator = d_picker.find_element_by_class_name('weui-picker__indicator')
    # touch_action.scroll_from_element(d_picker_indicator, 0, -item_offset).perform()

    # 注： 2、3需要在前面添加 option.add_experimental_option('w3c', False)， 1不用
# ==============

pick_date() # 滑动选择第二天，注释掉则选择当天
#%% 点击确定
sleep(.5)
driver.find_element_by_id('weui-picker-confirm').click()
# print current date
cur_date = driver.find_element_by_id('rqlscx').text
print('current date picked: ', cur_date)


# 填写出校理由
driver.find_element_by_id('cxly').send_keys(choice(reasons))
# 勾选一堆
# driver.find_element_by_id('cxlxdiv1').find_elements_by_xpath()
# checkboxes = driver.find_elements_by_xpath("//*[@id='cxlxdiv1']//input")
checkboxes = driver.find_elements_by_xpath("//*[@id='cxlxdiv1']/div[not(contains(@id, 'xslbxsyc'))]/label")  # 注：这里去掉了实际看不到的“已经与导师联系，导师知情同意”
for checkbox in checkboxes:
    checkbox.click()
# 提交
driver.execute_script('save()')
sleep(.5)
# 点击对话框的确认
# 1.
driver.execute_script('document.getElementsByClassName("weui-dialog__btn primary")[0].click()')
# 2.
# driver.find_element_by_class_name('weui-dialog__btn primary').click()

driver.quit()

print('申请临时出校完成')

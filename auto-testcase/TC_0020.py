# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC 
from datetime import datetime, timedelta
import unittest, time, re
import os
import inspect
import login_info as li
import project_info as pi

tc_file = inspect.getfile(inspect.currentframe())
tc_num = os.path.splitext(tc_file)[0]
tc_content = u"사용자가 PM이거나 ADIMN 권한일 경우, 프로젝트 설정 버튼이 있어야 하고, 일반 사용자일 경우 프로젝트 설정 버튼이 없어야한다."

class UntitledTestCase(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome('./chromedriver')
        self.driver.implicitly_wait(30)
        self.base_url = "https://www.google.com/"
        self.verificationErrors = []
        self.accept_next_alert = True
    
    def test_untitled_test_case(self):
        global test_details
        test_details = ''
        
        driver = self.driver
        
        project_name = "TC_0020"
        
        # ADMIN(X) / PM(O) :: PM 인 경우
        pm_user_id = "tc20pm"
        pm_user_pw = "1q2w3e!!"
        
        # ADMIN(X) / PM(X) :: 일반 사용자인 경우
        general_user_id = "tc20general"
        general_user_pw = "1q2w3e!!"
        
        # ADMIN(O) / PM(X) :: ADMIN 인 경우
        admin_user_id = "admin"
        admin_user_pw = "suresoft"
        
        # ROLE_NORMAL 사용자 2명 만들기
        print("STEP 0 -- 테스트용 일반 사용자 생성")
        test_details += li.join(self, pm_user_id, "김영희", "test1@naver.com", pm_user_pw, pm_user_pw)
        test_details += li.join(self, general_user_id, "김철수", "test2@naver.com", general_user_pw, general_user_pw)
        
        # 프로젝트 추가 사용자 이름
        user_list = []
        user_list.append(general_user_id)
        user_list.append(admin_user_id)
        
        print("STEP 1 -- PM 사용자 로그인 및 프로젝트 등록")
        li.login(self, pm_user_id, pm_user_pw)
        
        test_details += pi.project_essential_info(self, "GIT", "http://vpes@192.168.0.136:7990/scm/sprin/vpes.git", "vpes", "suresoft", project_name, "V-SPICE_CAR")
        test_details += pi.project_user_info(self, user_list)
        test_details += pi.create_project(self)
        
        print("STEP 2 -- 사용자가 PM 인 경우")
        print("STEP 2-1 -- 프로젝트 검색 및 클릭")
        #프로젝트 이름 검색구현
        driver.find_element_by_xpath("//div[@id='mainDashBoard-ProjectList_filter']/label/input").click()
        driver.find_element_by_xpath("//div[@id='mainDashBoard-ProjectList_filter']/label/input").clear()
        time.sleep(2)
        driver.find_element_by_xpath("//div[@id='mainDashBoard-ProjectList_filter']/label/input").send_keys(project_name)
        driver.find_element_by_xpath("//div[@id='mainDashBoard-ProjectList_filter']/label/input").send_keys(Keys.ENTER)
        time.sleep(2)
        
        #해당 프로젝트 클릭
        driver.find_element_by_xpath("//table[@id='mainDashBoard-ProjectList']/tbody/tr/td[2]").click()
        time.sleep(2)
        
        print("STEP 2-2 -- 프로젝트 설정 버튼 확인")
        # 프로젝트 배너 - 프로젝트 설정 버튼 확인
        wait = WebDriverWait(driver,10)
        try:
            wait.until(EC.visibility_of_element_located((By.XPATH, "//*[@id='setting-tab']")))
            print("STEP 2-2 -- SUCCESS")
        except Exception as e:
            print("STEP 2-2 -- FAILED")
            test_details+=u"사용자가 PM이지만, 프로젝트 배너의 설정 버튼이 뜨지 않음\n"
        time.sleep(3)
        
        print("STEP 2-3 -- PM 사용자 로그아웃")
        li.logout(self)
        
        print("STEP 3 -- 일반 사용자인 경우")
        li.login(self, general_user_id, general_user_pw)
        print("STEP 3-1 -- 프로젝트 검색 및 클릭")
        #프로젝트 이름 검색
        driver.find_element_by_xpath("//div[@id='mainDashBoard-ProjectList_filter']/label/input").click()
        driver.find_element_by_xpath("//div[@id='mainDashBoard-ProjectList_filter']/label/input").clear()
        time.sleep(2)
        driver.find_element_by_xpath("//div[@id='mainDashBoard-ProjectList_filter']/label/input").send_keys(project_name)
        driver.find_element_by_xpath("//div[@id='mainDashBoard-ProjectList_filter']/label/input").send_keys(Keys.ENTER)
        time.sleep(2)
        
        #해당 프로젝트 클릭
        driver.find_element_by_xpath("//table[@id='mainDashBoard-ProjectList']/tbody/tr/td[2]").click()
        time.sleep(2)
        
        print("STEP 3-2 -- 프로젝트 설정 버튼 확인")
        # 프로젝트 배너 - 프로젝트 설정 버튼 확인
        wait = WebDriverWait(driver,10)
        try:
            wait.until(EC.visibility_of_element_located((By.XPATH, "//*[@id='setting-tab']")))
            print("STEP 3-2 -- FAILED")
            test_details+=u"일반 사용자이지만, 프로젝트 배너의 설정 버튼이 뜸\n"
        except Exception as e:
            print("STEP 3-2 -- SUCCESS")
        time.sleep(3)
        li.logout(self)
        
        
        print("STEP 4 -- 사용자가 ADMIN 인 경우")
        li.login(self, admin_user_id, admin_user_pw)
        print("STEP 4-1 -- 프로젝트 검색 및 클릭")
        #프로젝트 이름 검색
        driver.find_element_by_xpath("//div[@id='mainDashBoard-ProjectList_filter']/label/input").click()
        driver.find_element_by_xpath("//div[@id='mainDashBoard-ProjectList_filter']/label/input").clear()
        time.sleep(2)
        driver.find_element_by_xpath("//div[@id='mainDashBoard-ProjectList_filter']/label/input").send_keys(project_name)
        driver.find_element_by_xpath("//div[@id='mainDashBoard-ProjectList_filter']/label/input").send_keys(Keys.ENTER)
        time.sleep(2)
        
        #해당 프로젝트 클릭
        driver.find_element_by_xpath("//table[@id='mainDashBoard-ProjectList']/tbody/tr/td[2]").click()
        time.sleep(2)
        
        print("STEP 4-2 -- 프로젝트 설정 버튼 확인")
        # 프로젝트 배너 - 프로젝트 설정 버튼 확인
        wait = WebDriverWait(driver,10)
        try:
            wait.until(EC.visibility_of_element_located((By.XPATH, "//*[@id='setting-tab']")))
            print("STEP 4-2 -- SUCCESS")
        except Exception as e:
            print("STEP 4-2 -- FAILED")
            test_details+=u"사용자가 ADMIN이지만, 프로젝트 배너의 설정 버튼이 뜨지 않음\n"
        time.sleep(3)
        
        if (test_details != ''):
            assert False
        
    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException as e: return False
        return True
    
    def is_alert_present(self):
        try: self.driver.switch_to_alert()
        except NoAlertPresentException as e: return False
        return True
    
    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally: self.accept_next_alert = True
    
    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

    def tearDown(self):
        if hasattr(self, '_outcome'):  # Python 3.4+
            result = self.defaultTestResult()  # these 2 methods have no side effects
            self._feedErrorsToResult(result, self._outcome.errors)
        else:  # Python 3.2 - 3.3 or 3.0 - 3.1 and 2.7
            result = getattr(self, '_outcomeForDoCleanups', self._resultForDoCleanups)
        error = self.list2reason(result.errors)
        failure = self.list2reason(result.failures)
        ok = not error and not failure
        
        # 테스트용 프로젝트 삭제 
        pi.delete_project(self, "TC_0020")
        
        # 테스트용 사용자 삭제
        li.login(self, "admin", "suresoft")
        li.delete_user(self, "tc20pm")
        li.delete_user(self, "tc20general")
        
        if ok:
            test_result = 'SUCCESS'
        else:
            test_result = 'FAILURE'
            typ, text = ('ERROR', error) if error else ('FAIL', failure)
            text = text.replace('\"', '\'')

		
        data = '"' + tc_num + '"' + ',' + '"' + tc_content + '"' + ',' + '"' + test_result + '"' + ',' + '"' + test_details + '"'
        command = 'echo ' + data + ' >> vspice_test_result.csv'
        '''print(command)'''
        #os.system(command.encode(str('cp949')))
        os.system(command)
    
    def list2reason(self, exc_list):
        if exc_list and exc_list[-1][0] is self:
            return exc_list[-1][1]
    
if __name__ == "__main__":
    unittest.main()

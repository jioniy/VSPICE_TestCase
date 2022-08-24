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
from selenium.webdriver.common.action_chains import ActionChains
from datetime import datetime, timedelta
import unittest, time, re
import os
import inspect
import login_info as li
import project_info as pi

tc_file = inspect.getfile(inspect.currentframe())
tc_num = os.path.splitext(tc_file)[0]
tc_content = u"작업 산출물 등록 시 전체 프로세스의 SUP8 카드에 마우스 오버 시 등록한 작업 산출물이 활성화되어야한다. "

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
        
        project_name = "TC_0098"
        
        user_id = "admin"
        user_pw = "suresoft"
        
        file_name_1 = u"SUP8_08-04_형상 관리 계획서.docx"
        file_name_2 = u"SUP8_08-14_복구 계획서.docx"
        file_path = os.path.dirname(os.path.realpath(__file__)) + u"\\wp_template\\SUP\\"
        
        print("STEP 1 -- 프로젝트 세팅")
        print("STEP 1-1 -- 사용자 로그인 및 프로젝트 등록")
        li.login(self, user_id, user_pw)
        
        # 프로젝트 생성
        test_details += pi.project_essential_info(self, "GIT", "http://vpes@192.168.0.136:7990/scm/sprin/vpes.git", "vpes", "suresoft", project_name, "V-SPICE_CAR")
        test_details += pi.create_project(self)
        
        time.sleep(2)
        
        print("STEP 1-2 -- 프로젝트 접속")
        pi.search_project(self, project_name)
        
        print("STEP 2 -- SUP8 작업 산출물 등록 확인")
        driver.find_element_by_id("processes-tab").click()
        driver.find_element_by_id("sup").click()
        time.sleep(3)
        driver.find_element_by_link_text("SUP.8 0/7").click()
        time.sleep(2)
        driver.execute_script("window.scrollTo(document.body.scrollWidth, 0);") 
        time.sleep(1)
        
        print("STEP 2-1 -- SUP8 형상 관리 계획서 / 복구 계획서 등록")
        driver.find_element_by_xpath("//div[@id='processDetail-ReportVue']/div[2]/ul/li[2]/div[5]/div/div").click()
        driver.find_element_by_xpath("//div[@id='processDetail-ReportVue']/div[2]/ul/li[2]/div[5]/div/div[2]/div/div[2]").click()
        
        file_input = driver.find_element_by_id("file-input")
        driver.execute_script("arguments[0].style.display = 'block';",file_input)
        file_input.clear()
        file_input.send_keys( file_path + file_name_1 )
        time.sleep(2)
        
        driver.find_element_by_xpath("//div[@id='uploadWorkProduct']/div/div/div[3]/button[2]").click()
        
        wait = WebDriverWait(driver, 15)
        element_text=""
        try:
            wait.until(EC.visibility_of_element_located((By.ID, 'alertModal')))
            element_text = driver.find_element_by_id("modal-content").text
        except Exception as e:
            print(e)
        time.sleep(3)
        if element_text != u"등록되었습니다.":
            print("STEP 2-1 -- SUP8 형상 관리 계획서 등록 FAILED")
            test_details += u"SUP8 형상 관리 계획서를 등록했으나, 모달창이 뜨지 않음.\n"
        else:
            print("STEP 2-1 -- SUP8 형상 관리 계획서 등록 SUCCESS")
        time.sleep(3)
        
        
        driver.find_element_by_xpath("//div[@id='processDetail-ReportVue']/div[2]/ul/li[3]/div[5]/div/div").click()
        driver.find_element_by_xpath("//div[@id='processDetail-ReportVue']/div[2]/ul/li[3]/div[5]/div/div[2]/div/div[2]").click()
        
        file_input = driver.find_element_by_id("file-input")
        driver.execute_script("arguments[0].style.display = 'block';",file_input)
        file_input.clear()
        file_input.send_keys( file_path + file_name_2 )
        time.sleep(2)
        
        driver.find_element_by_xpath("//div[@id='uploadWorkProduct']/div/div/div[3]/button[2]").click()
        
        wait = WebDriverWait(driver, 15)
        element_text=""
        try:
            wait.until(EC.visibility_of_element_located((By.ID, 'alertModal')))
            element_text = driver.find_element_by_id("modal-content").text
        except Exception as e:
            print(e)
        time.sleep(3)
        if element_text != u"등록되었습니다.":
            print("STEP 2-1 -- SUP8 복구 계획서 등록 FAILED")
            test_details += u"SUP8 복구 계획서를 등록했으나, 모달창이 뜨지 않음.\n"
        else:
            print("STEP 2-1 -- SUP8 복구 계획서 등록 SUCCESS")
        time.sleep(3)
        
        print("STEP 2-2 -- 전체 프로세스 페이지 SUP8 팝업창 확인")
        driver.find_element_by_id("processGroup").click()
        time.sleep(3)

        element_hover = driver.find_element_by_xpath("//*[@id='supProcessGroupArea']/div/div[3]/div[1]/div[2]")
        actions = ActionChains(driver)
        actions.move_to_element(element_hover)
        actions.perform()
        
        if driver.find_element_by_xpath("//*[@id='supProcessGroupArea']/div/div[3]/div[1]/div[1]").get_attribute("class").find("process-popup-hover_ko") != -1:
            print("STEP 2-2 -- SUCCESS")
            time.sleep(2)
        else:
            print("STEP 2-2 -- FAILED")
            test_details += u"전체 프로세스 페이지에서 SUP8의 작업 산출물 팝업창이 뜨지 않음.\n"
        print()
        
        print("STEP 2-3 -- 전체 프로세스 페이지 SUP8 작업 산출물 체크 아이콘 확인")
        for i in range(7):
            if i == 1 or i == 2 :
                if driver.find_element_by_xpath("//*[@id='supProcessGroupArea']/div/div[3]/div[1]/div[1]/div["+str(i+1)+"]/div[1]").get_attribute("class").find("process-doc-uploaded-svg") != -1: # 체크 상태
                    print("STEP 2-3 -- "+str(i+1)+"번째 항목 체크 SUCCESS")
                else:
                    print("STEP 2-3 -- "+str(i+1)+"번째 항목 체크 FAILED")
                    test_details += u"전체 프로세스 페이지에서 SUP8의 작업 산출물이 등록되고 오류가 있으나 오류 아이콘 뜨지 않음.\n"
            else:
                if driver.find_element_by_xpath("//*[@id='supProcessGroupArea']/div/div[3]/div[1]/div[1]/div["+str(i+1)+"]/div[1]").get_attribute("class").find("process-doc-not-upload-svg") != -1: # 미체크 상태
                    print("STEP 2-3 -- "+str(i+1)+"번째 항목 미체크 SUCCESS")
                else:
                    print("STEP 2-3 -- "+str(i+1)+"번째 항목 미체크 FAILED")
                    test_details += u"전체 프로세스 페이지에서 SUP8의 작업 산출물이 미등록되었으나 체크 아이콘 뜸.\n"
        print()
        
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
            
        pi.delete_project(self, "TC_0098")
        
        error = self.list2reason(result.errors)
        failure = self.list2reason(result.failures)
        ok = not error and not failure

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

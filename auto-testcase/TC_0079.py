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
from login import login
from datetime import datetime, timedelta
import unittest, time, re
import os
import inspect
import project_info as pi

tc_file = inspect.getfile(inspect.currentframe())
tc_num = os.path.splitext(tc_file)[0]
tc_content = u"SUP1 프로세스 작업 산출물을 등록할 경우, 프로세스 상세 화면과 전체 프로세스 화면의 프로세스 갯수에 반영되어야 한다."

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
        
        project_name = "TC_0079"
        
        user_id = "admin"
        user_pw = "suresoft"
        
        file_name_1 = "SUP1_08-13_품질 계획서.docx"
        file_name_2 = "SUP1_13-07_문제 기록.xlsx"
        file_path = u"D:\\auto-testcase\\wp_template\\SUP\\"
        
        print("STEP 1 -- 프로젝트 세팅")
        
        print("STEP 1-1 -- 사용자 로그인 및 프로젝트 등록")
        login(self, user_id, user_pw)
        
        # 프로젝트 생성
        test_details += pi.project_essential_info(self, "GIT", "http://vpes@192.168.0.136:7990/scm/sprin/vpes.git", "vpes", "suresoft", project_name, "VPES_CAR")
        test_details += pi.create_project(self)
        
        time.sleep(2)
        
        print("STEP 1-2 -- 프로젝트 접속")
        pi.search_project(self, project_name)
        
        print("STEP 2 -- SUP1 작업 산출물 등록")
        # SUP1 프로세스 접속
        driver.find_element_by_id("processes-tab").click()
        driver.find_element_by_id("sup").click()
        time.sleep(3)
        driver.find_element_by_link_text("SUP.1 0/7").click()
        time.sleep(2)
        
       # 작업 산출물 등록 - 품질 계획서
        print("STEP 2-1 -- SUP1 품질 계획서 등록")
        driver.find_element_by_xpath("//div[@id='processDetail-ReportVue']/div[2]/ul/li[1]/div[5]/div/div").click()
        driver.find_element_by_xpath("//div[@id='processDetail-ReportVue']/div[2]/ul/li[1]/div[5]/div/div[2]/div/div[2]").click()
        
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
            print("STEP 2-1 -- FAILED")
            test_details += u"SUP1 품질 계획서를 등록했으나, 모달창이 뜨지 않음.\n"
        else:
            print("STEP 2-1 -- SUCCESS")
        time.sleep(3)
        
        # 작업 산출물 등록 - 문제 기록
        print("STEP 2-2 -- SUP1 문제 기록 등록")
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
            print("STEP 2-2 -- FAILED")
            test_details += u"SUP1 문제 기록을 등록했으나, 모달창이 뜨지 않음.\n"
        else:
            print("STEP 2-2 -- SUCCESS")
        time.sleep(3)
        
        
        # 전체 프로세스 - 카드 갯수 확인 
        print("STEP 3 -- SUP1 작업 산출물 갯수 확인")
        
        print("STEP 3-1 -- SUP1 작업 산출물 체크 갯수 count")
        check_cnt = 0 
        for i in range(7): 
            if driver.find_element_by_xpath("//div[@id='processDetail-ReportVue']/div[2]/ul/li["+str(i+1)+"]/div").get_attribute("class").find("process-detail-check-icon") != -1 : # 문자열이 없을 경우 -1을 반환 / 있을 때는 해당 문자열의 시작 인덱스를 반환
                check_cnt += 1
        print("STEP 3-1 -- SUP1 작업 산출물 체크 갯수 : " + str(check_cnt))
        
        
        print("STEP 3-2 -- SUP1 작업 산출물 갯수 비교")
        driver.find_element_by_id("processGroup").click()
        time.sleep(3)
        
        if driver.find_element_by_xpath("//div[@id='supProcessGroupArea']/div/div[2]/div/div[2]/div/div[2]/font[1]").text==str(check_cnt): 
            print("STEP 3-2 -- SUCCESS")
        else:
            print("STEP 3-2 -- FAILED")
            test_details += u"사용자가 SUP1 프로세스에 등록한 작업 산출물 갯수와 표시되는 갯수가 일치하지 않음.\n"
        
        
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
            
        pi.delete_project(self, "TC_0079")
        
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
        command = 'echo ' + data + ' >> vpes_test_result.csv'
        '''print(command)'''
        #os.system(command.encode(str('cp949')))
        os.system(command)
    
    def list2reason(self, exc_list):
        if exc_list and exc_list[-1][0] is self:
            return exc_list[-1][1]
    
if __name__ == "__main__":
    unittest.main()

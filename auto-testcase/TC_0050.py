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
tc_content = u"SUP 그룹의 SUP9 템플릿을 다운로드 받을 경우, 각 작업 산출물에 해당하는 템플릿 파일이 다운로드 되어야 한다. "

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
        
        project_name = "TC_0050"
        
        user_id = "admin"
        user_pw = "suresoft"
        
        dir_path = u'C:\\Users\\대전회의실2\\Downloads\\' # 템플릿 파일 다운로드 경로
        
        print("STEP 1 -- 프로젝트 세팅")
        
        print("STEP 1-1 -- 사용자 로그인 및 프로젝트 등록")
        login(self, user_id, user_pw)
        
        # 프로젝트 생성
        test_details += pi.project_essential_info(self, "GIT", "http://vpes@192.168.0.136:7990/scm/sprin/vpes.git", "vpes", "suresoft", project_name, "VPES_CAR")
        test_details += pi.create_project(self)
        
        time.sleep(2)
        
        print("STEP 1-2 -- 프로젝트 접속")
        pi.search_project(self, project_name)
        
        print("STEP 2 -- SUP9 작업 산출물 템플릿 다운로드 확인")
        driver.find_element_by_id("processes-tab").click()
        driver.find_element_by_id("sup").click()
        time.sleep(3)
        driver.find_element_by_xpath("//div[@id='processDetail-HeaderVue']/div/ul/li[3]/a/span").click()
        time.sleep(3)
        
        # 문제 관리 계획서
        print("STEP 2-1 -- 문제 관리 계획서")
        driver.find_element_by_xpath("//div[@type='button']").click()
        driver.find_element_by_xpath("//div[@id='processDetail-ReportVue']/div[2]/ul/li/div[5]/div/div[2]/div[5]/div[2]").click()
        time.sleep(10)
        
        file_path = max([dir_path + f for f in os.listdir(dir_path)], key=os.path.getctime) # 파일 경로 +  이름 (파일 생성 날짜가 제일 최근인 파일을 찾아서 반환)
        file_name = file_path.strip(dir_path) # 파일 이름
        
        if file_name == "SUP9_08-27_문제 관리 계획서.docx":
            print("STEP 2-1 -- SUCCESS")
        else: 
            print("STEP 2-1 -- FAILED")
            test_details + u"SUP9 문제 관리 계획서 템플릿 다운로드 실패\n"
        time.sleep(2)
        
        if os.path.exists(file_path): # 파일 삭제
            print("STEP 2-1 -- 다운로드 파일(템플릿) 삭제")
            os.remove(file_path)
            print("STEP 2-1 -- SUCCESS")
        time.sleep(3)
        
        # 문제 기록
        print("STEP 2-2 -- 문제 기록")
        driver.find_element_by_xpath("//div[@id='processDetail-ReportVue']/div[2]/ul/li[2]/div[5]/div/div").click()
        driver.find_element_by_xpath("//div[@id='processDetail-ReportVue']/div[2]/ul/li[2]/div[5]/div/div[2]/div[5]/div[2]").click()
        time.sleep(10)
        
        file_path = max([dir_path + f for f in os.listdir(dir_path)], key=os.path.getctime) # 파일 경로 +  이름 (파일 생성 날짜가 제일 최근인 파일을 찾아서 반환)
        file_name = file_path.strip(dir_path) # 파일 이름
        
        if file_name == "SUP9_13-07_문제 기록.xlsx":
            print("STEP 2-2 -- SUCCESS")
        else: 
            print("STEP 2-2 -- FAILED")
            test_details + u"SUP9 문제 기록 템플릿 다운로드 실패\n"
        time.sleep(2)
        
        if os.path.exists(file_path): # 파일 삭제
            print("STEP 2-2 -- 다운로드 파일(템플릿) 삭제")
            os.remove(file_path)
            print("STEP 2-2 -- SUCCESS")
            
        # 분석 보고서
        print("STEP 2-3 -- 분석 보고서")
        driver.find_element_by_xpath("//div[@id='processDetail-ReportVue']/div[2]/ul/li[3]/div[5]/div/div").click()
        driver.find_element_by_xpath("//div[@id='processDetail-ReportVue']/div[2]/ul/li[3]/div[5]/div/div[2]/div[5]").click()
        time.sleep(10)
        
        file_path = max([dir_path + f for f in os.listdir(dir_path)], key=os.path.getctime) # 파일 경로 +  이름 (파일 생성 날짜가 제일 최근인 파일을 찾아서 반환)
        file_name = file_path.strip(dir_path) # 파일 이름
        
        if file_name == "SUP9_15-01_분석 보고서.xlsx":
            print("STEP 2-3 -- SUCCESS")
        else: 
            print("STEP 2-3 -- FAILED")
            test_details + u"SUP9 분석 보고서 템플릿 다운로드 실패\n"
        time.sleep(2)
        
        if os.path.exists(file_path): # 파일 삭제
            print("STEP 2-3 -- 다운로드 파일(템플릿) 삭제")
            os.remove(file_path)
            print("STEP 2-3 -- SUCCESS")
            
            
        # 평가 보고서
        print("STEP 2-4 -- 평가 보고서")
        driver.find_element_by_xpath("//div[@id='processDetail-ReportVue']/div[2]/ul/li[4]/div[5]/div/div").click()
        driver.find_element_by_xpath("//div[@id='processDetail-ReportVue']/div[2]/ul/li[4]/div[5]/div/div[2]/div[5]/div[2]").click()
        time.sleep(10)
        
        file_path = max([dir_path + f for f in os.listdir(dir_path)], key=os.path.getctime) # 파일 경로 +  이름 (파일 생성 날짜가 제일 최근인 파일을 찾아서 반환)
        file_name = file_path.strip(dir_path) # 파일 이름
        
        if file_name == "SUP9_15-05_평가 보고서.xlsx":
            print("STEP 2-4 -- SUCCESS")
        else: 
            print("STEP 2-4 -- FAILED")
            test_details + u"SUP9 평가 보고서 템플릿 다운로드 실패\n"
        time.sleep(2)
        
        if os.path.exists(file_path): # 파일 삭제
            print("STEP 2-4 -- 다운로드 파일(템플릿) 삭제")
            os.remove(file_path)
            print("STEP 2-4 -- SUCCESS")
        
        # 문제 상태 보고서
        print("STEP 2-5 -- 문제 상태 보고서")
        driver.find_element_by_xpath("//div[@id='processDetail-ReportVue']/div[2]/ul/li[5]/div[5]/div/div").click()
        driver.find_element_by_xpath("//div[@id='processDetail-ReportVue']/div[2]/ul/li[5]/div[5]/div/div[2]/div[5]/div[2]").click()
        time.sleep(10)
        
        file_path = max([dir_path + f for f in os.listdir(dir_path)], key=os.path.getctime) # 파일 경로 +  이름 (파일 생성 날짜가 제일 최근인 파일을 찾아서 반환)
        file_name = file_path.strip(dir_path) # 파일 이름
        
        if file_name == "SUP9_15-12_문제 상태 보고서.xlsx":
            print("STEP 2-5 -- SUCCESS")
        else: 
            print("STEP 2-5 -- FAILED")
            test_details + u"SUP9 문제 상태 보고서 템플릿 다운로드 실패\n"
        time.sleep(2)
        
        if os.path.exists(file_path): # 파일 삭제
            print("STEP 2-5 -- 다운로드 파일(템플릿) 삭제")
            os.remove(file_path)
            print("STEP 2-5 -- SUCCESS")
            
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
            
        pi.delete_project(self, "TC_0050")
        
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

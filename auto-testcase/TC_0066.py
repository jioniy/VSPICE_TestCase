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
tc_content = u"SWE 그룹 SWE6의 시험 계획서 작업 산출물을 업로드할 경우, 업로드한 파일의 이름이 해당 산출물 Row에 출력되어야하고 Hover 시 파일 수정 시간이 툴팁으로 출력되어야 한다."

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
        
        project_name = "TC_0066"
        
        user_id = "admin"
        user_pw = "suresoft"
        
        file_name = "SWE6_08-52_시험 계획서.docx"
        file_path = u"D:\\auto-testcase\\wp_template\\SWE\\"+file_name
        
        print("STEP 1 -- 프로젝트 세팅")
        
        print("STEP 1-1 -- 사용자 로그인 및 프로젝트 등록")
        login(self, user_id, user_pw)
        
        # 프로젝트 생성
        test_details += pi.project_essential_info(self, "GIT", "http://vpes@192.168.0.136:7990/scm/sprin/vpes.git", "vpes", "suresoft", project_name, "VPES_CAR")
        test_details += pi.create_project(self)
        
        time.sleep(2)
        
        print("STEP 1-2 -- 프로젝트 접속")
        pi.search_project(self, project_name)
        
        print("STEP 2 -- SWE6 시험 계획서 업로드 확인")
        driver.find_element_by_id("processes-tab").click()
        driver.find_element_by_id("swe").click()
        driver.find_element_by_link_text("SWE.6 0/7").click()
        time.sleep(3)
        
        print("STEP 2-1 -- SWE6 시험 계획서파일 업로드 (등록 창 확인)")
        # 등록 클릭
        driver.find_element_by_xpath("//div[@id='processDetail-ReportVue']/div[2]/ul/li[2]/div[5]/div/div").click()
        driver.find_element_by_xpath("//div[@id='processDetail-ReportVue']/div[2]/ul/li[2]/div[5]/div/div[2]/div/div[2]").click()
        time.sleep(2)
        
        # 등록 유형 선택 (템플릿) 
        driver.find_element_by_xpath("//div[@id='uploadWorkProduct']/div/div/div[2]/div/div[2]/div/div/div").click()
        time.sleep(1)
        driver.find_element_by_xpath("//div[@id='uploadWorkProduct']/div/div/div[2]/div/div[2]/div/div/div[3]/ul/li/span").click()
        time.sleep(2)
        
        # 파일 업로드
        file_input = driver.find_element_by_id("file-input")
        driver.execute_script("arguments[0].style.display = 'block';",file_input)
        file_input.send_keys(file_path)
        time.sleep(2)
        
        # 파일 업로드 이름 / 시간 확인
        if driver.find_element_by_xpath("//form[@id='uploadFile']/div[2]/div/span").text!= file_name : # 파일 이름
            print("STEP 2-1 -- 산출물 등록 페이지 파일 이름 정상 등록 FAILED")
            test_details += "파일 업로드 시 파일 이름 정상 등록되지 않음.\n"
        else:
            print("STEP 2-1 -- 산출물 등록 페이지 파일 이름 정상 등록")
        time.sleep(2)
        
        file_time = str(datetime.fromtimestamp(os.path.getmtime(file_path))).split('.')[0]
        if driver.find_element_by_xpath("//form[@id='uploadFile']/div[2]/div/span[2]").text != file_time: # 파일 등록 시간
            print("STEP 2-1 -- 산출물 등록 페이지 파일 시간 정상 등록 FAILED")
            test_details += "파일 업로드 시 파일 시간 정상 등록되지 않음.\n"
        else:
            print("STEP 2-1 -- 산출물 등록 페이지 파일 시간 정상 등록")
        time.sleep(2)
        
        # 설명 추가
        modify_explain = u"서버 내 자료로 대체함"
        driver.find_element_by_xpath("//div[@id='uploadWorkProduct']/div/div/div[2]/div[4]/div[2]/textarea").click()
        driver.find_element_by_xpath("//div[@id='uploadWorkProduct']/div/div/div[2]/div[4]/div[2]/textarea").clear()
        driver.find_element_by_xpath("//div[@id='uploadWorkProduct']/div/div/div[2]/div[4]/div[2]/textarea").send_keys(modify_explain)
        time.sleep(2)
        
        # 등록 버튼 클릭
        driver.find_element_by_xpath("//div[@id='uploadWorkProduct']/div/div/div[3]/button[2]/span").click()
        
        # 모달 확인
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
            test_details += u"SWE6의 시험 계획서를 등록했으나, 모달창이 뜨지 않음.\n"
        else:
            print("STEP 2-1 -- SUCCESS")
        time.sleep(3)
        
        print("STEP 2-2 -- SWE6 시험 계획서파일 업로드 (row 확인)")
        # 파일 이름 확인 
        
        if driver.find_element_by_xpath("//div[@id='processDetail-ReportVue']/div[2]/ul/li[2]/div[4]/div/div").text == file_name :
            print("STEP 2-2 -- 파일 이름 확인 SUCCESS")
        else:
            print("STEP 2-2 -- 파일 이름 확인 FAILED")
            test_details += u"SWE6의 시험 계획서를 등록했으나, 파일이름이 일치하지 않음.\n"
        time.sleep(2)
        
        # 파일 수정 시간 확인
        driver.find_element_by_xpath("//div[@id='processDetail-ReportVue']/div[2]/ul/li[2]/div[4]/div/div").click()
        tooltip_text = "파일 수정 시간 : " + file_time + "<br>설명:" + modify_explain
        if driver.find_element_by_xpath("//div[@id='processDetail-ReportVue']/div[2]/ul/li[2]/div[4]/div/div[1]").get_attribute("data-original-title") == tooltip_text:
            print("STEP 2-2 -- 파일 수정 시간 확인 SUCCESS")
        else:
            print("STEP 2-2 -- 파일 수정 시간 확인 FAILED")
            test_details += u"SWE6의 시험 계획서를 등록했으나, 수정시간이 일치하지 않음.\n"
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
            
        pi.delete_project(self, "TC_0066")
        
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

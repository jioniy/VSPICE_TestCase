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
tc_content = u"SWE3 프로세스에 리뷰 작성 시 검토 기록 항목이 활성화되어야 한다. "

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
        
        project_name = "TC_0109"
        
        user_id = "admin"
        user_pw = "suresoft"

        
        print("STEP 1 -- 프로젝트 세팅")
        print("STEP 1-1 -- 사용자 로그인 및 프로젝트 등록")
        li.login(self, user_id, user_pw)
        
        # 프로젝트 생성
        test_details += pi.project_essential_info(self, "GIT", "http://vpes@192.168.0.136:7990/scm/sprin/vpes.git", "vpes", "suresoft", project_name, "V-SPICE_CAR")
        test_details += pi.create_project(self)
        
        time.sleep(2)
        
        print("STEP 1-2 -- 프로젝트 접속")
        pi.search_project(self, project_name)
        
        
        print("STEP 2 -- SWE3 리뷰 작성")
        driver.find_element_by_id("processes-tab").click()
        driver.find_element_by_id("swe").click()
        time.sleep(3)
        driver.find_element_by_link_text("SWE.3 0/5").click()
        time.sleep(2)
        
        driver.find_element_by_xpath("//div[@id='processDetail-HeaderVue']/div[2]/button/div/div[2]").click()
        time.sleep(2)
        driver.find_element_by_id("reviewTitle").click()
        driver.find_element_by_id("reviewTitle").clear()
        driver.find_element_by_id("reviewTitle").send_keys(u"SWE3 리뷰")
        time.sleep(2)
        driver.find_element_by_id("writer").click()
        driver.find_element_by_id("writer").clear()
        driver.find_element_by_id("writer").send_keys(u"홍길동")
        time.sleep(2)
        driver.find_element_by_id("sourceVersion").click()
        driver.find_element_by_id("sourceVersion").clear()
        driver.find_element_by_id("sourceVersion").send_keys("0.5")
        time.sleep(2)
        driver.find_element_by_id("reviewDate").click()
        driver.find_element_by_id("reviewDate").clear()
        driver.find_element_by_id("reviewDate").send_keys(datetime.now().strftime('%Y-%m-%d'))
        time.sleep(2)
        driver.find_element_by_xpath("//table[@id='activitiesStandardTable']/tbody/tr[2]/td[5]/div/div[2]/span").click()
        driver.find_element_by_xpath("//table[@id='activitiesStandardTable']/tbody/tr[2]/td[5]/div/div[2]/span").click()
        time.sleep(2)
        driver.find_element_by_xpath("//div[@id='ProjectReviewWriteModal']/div/div/div[2]/div[4]/div[2]/div[2]/span").click()
        driver.find_element_by_xpath("//div[@id='ProjectReviewWriteModal']/div/div/div[2]/div[4]/div[2]/div[3]/ul/li[2]/span").click()
        time.sleep(2)
        driver.find_element_by_id("contents").click()
        driver.find_element_by_id("contents").clear()
        driver.find_element_by_id("contents").send_keys(u"활동 내용 작성")
        time.sleep(2)
        driver.execute_script("window.scrollTo(document.body.scrollWidth, 0);") 
        time.sleep(2)
        driver.find_element_by_xpath("//div[@id='ProjectReviewWriteModal']/div/div/div[3]/button[2]").click()
        
        wait = WebDriverWait(driver, 15)
        element_text=""
        try:
            wait.until(EC.visibility_of_element_located((By.ID, 'alertModal')))
            element_text = driver.find_element_by_id("modal-content").text
        except Exception as e:
            print(e)
        time.sleep(3)
        if element_text != u"저장 성공":
            print("STEP 2 -- FAILED")
            test_details += u"SWE3 리뷰를 작성했으나, 모달창이 뜨지 않음.\n"
        else:
            print("STEP 2 -- SUCCESS")
        time.sleep(3)
        
        print("STEP 3 -- SWE3 검토기록 체크 아이콘 확인")
        if driver.find_element_by_xpath("//div[@id='processDetail-ReportVue']/div[2]/ul/li[4]/div").get_attribute("class").find("process-detail-check-icon") != -1 :
            print("STEP 3 -- SUCCESS")
        else:
            print("STEP 3 -- FAILED")
            test_details += u"SWE3 리뷰를 작성했으나, 검토 기록의 체크 아이콘이 활성화되지 않음.\n"
        
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
            
        pi.delete_project(self, "TC_0109")
        
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

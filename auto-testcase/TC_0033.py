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
import default_url

tc_file = inspect.getfile(inspect.currentframe())
tc_num = os.path.splitext(tc_file)[0]
tc_content = u"각 프로세스 그룹의 프로세스 탭에는 프로젝트 등록 시 설정한 프로세스 항목만 존재해야한다. "

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
        
        li.login(self, "admin","suresoft")
        print("STEP 1-1 -- 프로젝트 생성")
        project_name = "TC_0033"
        base_url_process = default_url.VSPICE_URL + "ProcessDetail/"+project_name
        
        test_details += pi.project_essential_info(self, "GIT", "http://vpes@192.168.0.136:7990/scm/sprin/vpes.git", "vpes", "suresoft", project_name, "V-SPICE_CAR")
        test_details += pi.project_process_info(self, True, True, True, True, True, True, False, True)# SUP9 제외
        test_details += pi.create_project(self)
        
        print("STEP 1-2 -- 프로젝트 접속")
        pi.search_project(self, project_name)
        print()
        
        print("STEP 2 -- 프로세스 목록 확인")
        print()
        driver.find_element_by_id("processes-tab").click()
        time.sleep(1)
        
        print("STEP 2-1 -- ACQ4 프로세스 확인")
        driver.find_element_by_id("acq").click()
        time.sleep(3)
        if driver.find_element_by_xpath("//div[@id='processDetail-HeaderVue']/div/ul/li/a/span").text == "ACQ.4":
            print("STEP 2-1 -- SUCCESS")
        else:
            print("STEP 2-1 -- FAILED")
            test_details += u"ACQ4 프로세스탭 존재하지 않음\n"
        print()
        time.sleep(2)
        
        print("STEP 2-2 -- MAN3 프로세스 목록 확인")
        driver.find_element_by_id("man").click()
        time.sleep(3)
        if driver.find_element_by_xpath("//div[@id='processDetail-HeaderVue']/div/ul/li/a/span").text == "MAN.3":
            print("STEP 2-2 -- SUCCESS")
        else:
            print("STEP 2-2 -- FAILED")
            test_details += u"MAN3 프로세스탭 존재하지 않음\n"
        print()
        time.sleep(2)
        
        
        driver.find_element_by_id("sys").click()
        time.sleep(3)
        for i in range(2,6):# SYS 2~5 , STEP 2-3~6
            print("STEP 2-"+str(i+1)+" -- SYS"+str(i)+" 프로세스 목록 확인")
            if driver.find_element_by_xpath("//div[@id='processDetail-HeaderVue']/div/ul/li["+str(i-1)+"]/a/span").text == "SYS."+str(i):
                print("STEP 2-"+str(i+1)+" -- SUCCESS")
            else:
                print("STEP 2-"+str(i+1)+" -- FAILED")
                test_details += u"SYS"+str(i)+u" 프로세스탭 존재하지 않음\n"
            time.sleep(2)
        print()
        
        driver.find_element_by_id("swe").click()
        time.sleep(3)
        for i in range(1,7):# SWE 1~6, STEP 2-7~12
            print("STEP 2-"+str(i+6)+" -- SWE"+str(i)+" 프로세스 목록 확인")
            if driver.find_element_by_xpath("//div[@id='processDetail-HeaderVue']/div/ul/li["+str(i)+"]/a/span").text == "SWE."+str(i):
                print("STEP 2-"+str(i+6)+" -- SUCCESS")
            else:
                print("STEP 2-"+str(i+6)+" -- FAILED")
                test_details += u"SWE"+str(i)+u" 프로세스탭 존재하지 않음\n"
            time.sleep(2)
        print()
        
        
        driver.find_element_by_id("sup").click()
        time.sleep(3)
        
        print("STEP 2-13 -- SUP1 프로세스 목록 확인")
        if driver.find_element_by_xpath("//div[@id='processDetail-HeaderVue']/div/ul/li/a/span").text == "SUP.1":
            print("STEP 2-13 -- SUCCESS")
        else:
            print("STEP 2-13 -- FAILED")
            test_details += u"SUP1 프로세스탭 존재하지 않음\n"
        time.sleep(2)
        
        print("STEP 2-14 -- SUP8 프로세스 목록 확인")
        if driver.find_element_by_xpath("//div[@id='processDetail-HeaderVue']/div/ul/li[2]/a/span").text == "SUP.8":
            print("STEP 2-14 -- SUCCESS")
        else:
            print("STEP 2-14 -- FAILED")
            test_details += u"SUP8 프로세스탭 존재하지 않음\n"
        time.sleep(2)
        
        print("STEP 2-15 -- SUP10 프로세스 목록 확인")
        if driver.find_element_by_xpath("//div[@id='processDetail-HeaderVue']/div/ul/li[3]/a/span").text == "SUP.10":
            print("STEP 2-15 -- SUCCESS")
        else:
            print("STEP 2-15 -- FAILED")
            test_details += u"SUP10 프로세스탭 존재하지 않음\n"
        time.sleep(2)
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
            
        pi.delete_project(self, "TC_0033")
        
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

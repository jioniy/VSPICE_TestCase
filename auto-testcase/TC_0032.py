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
import project_info as pi
import login_info as li
import default_url

tc_file = inspect.getfile(inspect.currentframe())
tc_num = os.path.splitext(tc_file)[0]
tc_content = u"전체 프로세스 페이지에서는 프로젝트 등록 시 설정한 프로세스 항목만 활성화되어야 하고, 카드 클릭 시 각 페이지로 전환되어야 한다."

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
        print("STEP 1 -- 프로젝트 생성")
        project_name = "TC_0032"
        base_url_process = default_url.VSPICE_URL + "ProcessDetail/"+project_name
        
        test_details += pi.project_essential_info(self, "GIT", "http://vpes@192.168.0.136:7990/scm/sprin/vpes.git", "vpes", "suresoft", project_name, "VSPICE_CAR")
        test_details += pi.project_process_info(self, True, False, True, True, True, False, True, True)# MAN, SUP8 제외
        test_details += pi.create_project(self)
        
        print("STEP 1-2 -- 프로젝트 접속")
        pi.search_project(self, project_name)
        
        # 전체 프로세스 창 선택
        driver.find_element_by_xpath("//a[@id='processes-tab']/font").click()
        driver.find_element_by_id("processGroup").click()
        
        print("STEP 2 -- ACQ4 카드 활성화 / 페이지 전환 확인 ")
        time.sleep(1)
        print("STEP 2-1 -- ACQ4 카드 활성화 확인")
        if driver.find_element_by_xpath("//*[@id='acqProcessGroupArea']/div/div[3]/div[2]").get_attribute("class").find("process-card-enable")!= -1: # 존재하지 않으면 -1을 리턴
            print("STEP 2-1 -- SUCCESS")
        else:
            print("STEP 2-1 -- FAILED")
            test_details += u"ACQ4가 활성화되었지만, 전체 프로세스에서 해당 카드가 활성화되지 않음.\n"
        
        print("STEP 2-2 -- ACQ4 페이지 전환 확인")
        driver.find_element_by_xpath("//div[@id='acqProcessGroupArea']/div/div[3]/div[2]/div/div[2]").click()
        time.sleep(3)
        
        expected_url = base_url_process+"/ACQ/ACQ_4"
        if driver.current_url == expected_url : 
            print("STEP 2-2 -- SUCCESS")
        else:
            print("STEP 2-2 -- FAILED")
            test_details += u"ACQ4 카드를 클릭하였으나, 해당 페이지로 넘어가지 않음.\n"
        print()
        driver.back()
        time.sleep(3)
        
        
        print("STEP 3 -- MAN3 카드 비활성화 확인 ")
        time.sleep(1)
        if driver.find_element_by_xpath("//*[@id='manProcessGroupArea']/div/div[2]/div[2]").get_attribute("class").find("process-card-enable")== -1: # 존재하지 않으면 -1을 리턴
            print("STEP 3 -- SUCCESS")
        else:
            print("STEP 3 -- FAILED")
            test_details += u"MAN3가 비활성화되었지만, 전체 프로세스에서 해당 카드가 활성화됨.\n"
        print()
        time.sleep(3)
        
        print("STEP 4 -- SYS2 카드 활성화 / 페이지 전환 확인 ")
        time.sleep(1)
        print("STEP 4-1 -- SYS2 카드 활성화 확인")
        if driver.find_element_by_xpath("//*[@id='sysProcessGroupArea']/div/div[3]/div[1]/div[2]").get_attribute("class").find("process-card-enable")!= -1: # 존재하지 않으면 -1을 리턴
            print("STEP 4-1 -- SUCCESS")
        else:
            print("STEP 4-1 -- FAILED")
            test_details += u"SYS2가 활성화되었지만, 전체 프로세스에서 해당 카드가 활성화되지 않음.\n"
        
        print("STEP 4-2 -- SYS2 페이지 전환 확인")
        driver.find_element_by_xpath("//div[@id='sysProcessGroupArea']/div/div[3]/div/div[2]/div/div/div").click()
        time.sleep(3)
        
        expected_url = base_url_process+"/SYS/SYS_2"
        if driver.current_url == expected_url : 
            print("STEP 4-2 -- SUCCESS")
        else:
            print("STEP 4-2 -- FAILED")
            test_details += u"SYS2 카드를 클릭하였으나, 해당 페이지로 넘어가지 않음.\n"
        print()
        driver.back()
        time.sleep(3)
        
        print("STEP 5 -- SYS3 카드 활성화 / 페이지 전환 확인 ")
        time.sleep(1)
        print("STEP 5-1 -- SYS3 카드 활성화 확인")
        if driver.find_element_by_xpath("//*[@id='sysProcessGroupArea']/div/div[4]/div[1]/div[2]").get_attribute("class").find("process-card-enable")!= -1: # 존재하지 않으면 -1을 리턴
            print("STEP 5-1 -- SUCCESS")
        else:
            print("STEP 5-1 -- FAILED")
            test_details += u"SYS3가 활성화되었지만, 전체 프로세스에서 해당 카드가 활성화되지 않음.\n"
        
        print("STEP 5-2 -- SYS3 페이지 전환 확인")
        driver.find_element_by_xpath("//div[@id='sysProcessGroupArea']/div/div[4]/div/div[2]/div[2]/div").click()
        time.sleep(3)
        
        expected_url = base_url_process+"/SYS/SYS_3"
        if driver.current_url == expected_url : 
            print("STEP 5-2 -- SUCCESS")
        else:
            print("STEP 5-2 -- FAILED")
            test_details += u"SYS3 카드를 클릭하였으나, 해당 페이지로 넘어가지 않음.\n"
        print()
        driver.back()
        time.sleep(3)
        
        print("STEP 6 -- SYS4 카드 활성화 / 페이지 전환 확인 ")
        time.sleep(1)
        print("STEP 6-1 -- SYS4 카드 활성화 확인")
        if driver.find_element_by_xpath("//*[@id='sysProcessGroupArea']/div/div[4]/div[2]/div[2]").get_attribute("class").find("process-card-enable")!= -1: # 존재하지 않으면 -1을 리턴
            print("STEP 6-1 -- SUCCESS")
        else:
            print("STEP 6-1 -- FAILED")
            test_details += u"SYS4가 활성화되었지만, 전체 프로세스에서 해당 카드가 활성화되지 않음.\n"
        
        print("STEP 6-2 -- SYS4 페이지 전환 확인") 
        driver.find_element_by_xpath("//div[@id='sysProcessGroupArea']/div/div[4]/div[2]/div[2]/div/div[2]").click()
        time.sleep(3)
        
        expected_url = base_url_process+"/SYS/SYS_4"
        if driver.current_url == expected_url : 
            print("STEP 6-2 -- SUCCESS")
        else:
            print("STEP 6-2 -- FAILED")
            test_details += u"SYS4 카드를 클릭하였으나, 해당 페이지로 넘어가지 않음.\n"
        print()
        driver.back()
        time.sleep(3)
        
        print("STEP 7 -- SYS5 카드 활성화 / 페이지 전환 확인 ")
        time.sleep(1)
        print("STEP 7-1 -- SYS5 카드 활성화 확인")
        if driver.find_element_by_xpath("//*[@id='sysProcessGroupArea']/div/div[3]/div[2]/div[2]").get_attribute("class").find("process-card-enable")!= -1: # 존재하지 않으면 -1을 리턴
            print("STEP 7-1 -- SUCCESS")
        else:
            print("STEP 7-1 -- FAILED")
            test_details += u"SYS5가 활성화되었지만, 전체 프로세스에서 해당 카드가 활성화되지 않음.\n"
        
        print("STEP 7-2 -- SYS5 페이지 전환 확인") 
        driver.find_element_by_xpath("//div[@id='sysProcessGroupArea']/div/div[3]/div[2]/div[2]/div[2]/div").click()
        time.sleep(3)
        
        expected_url = base_url_process+"/SYS/SYS_5"
        if driver.current_url == expected_url : 
            print("STEP 7-2 -- SUCCESS")
        else:
            print("STEP 7-2 -- FAILED")
            test_details += u"SYS5 카드를 클릭하였으나, 해당 페이지로 넘어가지 않음.\n"
        print()
        driver.back()
        time.sleep(3)
        
        
        print("STEP 8 -- SWE1 카드 활성화 / 페이지 전환 확인 ")
        time.sleep(1)
        print("STEP 8-1 -- SWE1 카드 활성화 확인")
        if driver.find_element_by_xpath("//*[@id='sweProcessGroupArea']/div/div[2]/div[1]/div[2]").get_attribute("class").find("process-card-enable")!= -1: # 존재하지 않으면 -1을 리턴
            print("STEP 8-1 -- SUCCESS")
        else:
            print("STEP 8-1 -- FAILED")
            test_details += u"SWE1가 활성화되었지만, 전체 프로세스에서 해당 카드가 활성화되지 않음.\n"
        
        print("STEP 8-2 -- SWE1 페이지 전환 확인") 
        driver.find_element_by_xpath("//div[@id='sweProcessGroupArea']/div/div[2]/div/div[2]/div/div[2]").click()
        time.sleep(3)
        
        expected_url = base_url_process+"/SWE/SWE_1"
        if driver.current_url == expected_url : 
            print("STEP 8-2 -- SUCCESS")
        else:
            print("STEP 8-2 -- FAILED")
            test_details += u"SWE1 카드를 클릭하였으나, 해당 페이지로 넘어가지 않음.\n"
        print()
        driver.back()
        time.sleep(3)
        
        print("STEP 9 -- SWE2 카드 활성화 / 페이지 전환 확인 ")
        time.sleep(1)
        print("STEP 9-1 -- SWE2 카드 활성화 확인")
        if driver.find_element_by_xpath("//*[@id='sweProcessGroupArea']/div/div[3]/div[1]/div[2]").get_attribute("class").find("process-card-enable")!= -1: # 존재하지 않으면 -1을 리턴
            print("STEP 9-1 -- SUCCESS")
        else:
            print("STEP 9-1 -- FAILED")
            test_details += u"SWE2가 활성화되었지만, 전체 프로세스에서 해당 카드가 활성화되지 않음.\n"
        
        print("STEP 9-2 -- SWE2 페이지 전환 확인") 
        driver.find_element_by_xpath("//div[@id='sweProcessGroupArea']/div/div[3]/div/div[2]/div/div[2]").click()
        time.sleep(3)
        
        expected_url = base_url_process+"/SWE/SWE_2"
        if driver.current_url == expected_url : 
            print("STEP 9-2 -- SUCCESS")
        else:
            print("STEP 9-2 -- FAILED")
            test_details += u"SWE2 카드를 클릭하였으나, 해당 페이지로 넘어가지 않음.\n"
        print()
        driver.back()
        time.sleep(3)
        
        print("STEP 10 -- SWE3 카드 활성화 / 페이지 전환 확인 ")
        time.sleep(1)
        print("STEP 10-1 -- SWE3 카드 활성화 확인")
        if driver.find_element_by_xpath("//*[@id='sweProcessGroupArea']/div/div[4]/div[1]/div[2]").get_attribute("class").find("process-card-enable")!= -1: # 존재하지 않으면 -1을 리턴
            print("STEP 10-1 -- SUCCESS")
        else:
            print("STEP 10-1 -- FAILED")
            test_details += u"SWE3가 활성화되었지만, 전체 프로세스에서 해당 카드가 활성화되지 않음.\n"
        
        print("STEP 10-2 -- SWE3 페이지 전환 확인") 
        driver.find_element_by_xpath("//div[@id='sweProcessGroupArea']/div/div[4]/div/div[2]/div/div[2]").click()
        time.sleep(3)
        
        expected_url = base_url_process+"/SWE/SWE_3"
        if driver.current_url == expected_url : 
            print("STEP 10-2 -- SUCCESS")
        else:
            print("STEP 10-2 -- FAILED")
            test_details += u"SWE3 카드를 클릭하였으나, 해당 페이지로 넘어가지 않음.\n"
        print()
        driver.back()
        time.sleep(3)
        
        print("STEP 11 -- SWE4 카드 활성화 / 페이지 전환 확인 ")
        time.sleep(1)
        print("STEP 11-1 -- SWE4 카드 활성화 확인")
        if driver.find_element_by_xpath("//*[@id='sweProcessGroupArea']/div/div[4]/div[2]/div[2]").get_attribute("class").find("process-card-enable")!= -1: # 존재하지 않으면 -1을 리턴
            print("STEP 11-1 -- SUCCESS")
        else:
            print("STEP 11-1 -- FAILED")
            test_details += u"SWE4가 활성화되었지만, 전체 프로세스에서 해당 카드가 활성화되지 않음.\n"
        
        print("STEP 11-2 -- SWE4 페이지 전환 확인") 
        driver.find_element_by_xpath("//div[@id='sweProcessGroupArea']/div/div[4]/div[2]/div[2]").click()
        time.sleep(3)
        
        expected_url = base_url_process+"/SWE/SWE_4"
        if driver.current_url == expected_url : 
            print("STEP 11-2 -- SUCCESS")
        else:
            print("STEP 11-2 -- FAILED")
            test_details += u"SWE4 카드를 클릭하였으나, 해당 페이지로 넘어가지 않음.\n"
        print()
        driver.back()
        time.sleep(3)
        
        print("STEP 12 -- SWE5 카드 활성화 / 페이지 전환 확인 ")
        time.sleep(1)
        print("STEP 12-1 -- SWE5 카드 활성화 확인")
        if driver.find_element_by_xpath("//*[@id='sweProcessGroupArea']/div/div[3]/div[2]/div[2]").get_attribute("class").find("process-card-enable")!= -1: # 존재하지 않으면 -1을 리턴
            print("STEP 12-1 -- SUCCESS")
        else:
            print("STEP 12-1 -- FAILED")
            test_details += u"SWE5가 활성화되었지만, 전체 프로세스에서 해당 카드가 활성화되지 않음.\n"
        
        print("STEP 12-2 -- SWE5 페이지 전환 확인") 
        driver.find_element_by_xpath("//div[@id='sweProcessGroupArea']/div/div[3]/div[2]/div[2]/div/div[2]").click()
        time.sleep(3)
        
        expected_url = base_url_process+"/SWE/SWE_5"
        if driver.current_url == expected_url : 
            print("STEP 12-2 -- SUCCESS")
        else:
            print("STEP 12-2 -- FAILED")
            test_details += u"SWE5 카드를 클릭하였으나, 해당 페이지로 넘어가지 않음.\n"
        print()
        driver.back()
        time.sleep(3)
        
        print("STEP 13 -- SWE6 카드 활성화 / 페이지 전환 확인 ")
        time.sleep(1)
        print("STEP 13-1 -- SWE6 카드 활성화 확인")
        if driver.find_element_by_xpath("//*[@id='sweProcessGroupArea']/div/div[2]/div[2]/div[2]").get_attribute("class").find("process-card-enable")!= -1: # 존재하지 않으면 -1을 리턴
            print("STEP 13-1 -- SUCCESS")
        else:
            print("STEP 13-1 -- FAILED")
            test_details += u"SWE6가 활성화되었지만, 전체 프로세스에서 해당 카드가 활성화되지 않음.\n"
        
        print("STEP 13-2 -- SWE6 페이지 전환 확인") 
        driver.find_element_by_xpath("//div[@id='sweProcessGroupArea']/div/div[2]/div[2]/div[2]/div/div[2]").click()
        time.sleep(3)
        
        expected_url = base_url_process+"/SWE/SWE_6"
        if driver.current_url == expected_url : 
            print("STEP 13-2 -- SUCCESS")
        else:
            print("STEP 13-2 -- FAILED")
            test_details += u"SWE6 카드를 클릭하였으나, 해당 페이지로 넘어가지 않음.\n"
        print()
        driver.back()
        time.sleep(3)
        
        print("STEP 14 -- SUP1 카드 활성화 / 페이지 전환 확인 ")
        time.sleep(1)
        print("STEP 14-1 -- SUP1 카드 활성화 확인")
        if driver.find_element_by_xpath("//*[@id='supProcessGroupArea']/div/div[2]/div[1]/div[2]").get_attribute("class").find("process-card-enable")!= -1: # 존재하지 않으면 -1을 리턴
            print("STEP 14-1 -- SUCCESS")
        else:
            print("STEP 14-1 -- FAILED")
            test_details += u"SUP1가 활성화되었지만, 전체 프로세스에서 해당 카드가 활성화되지 않음.\n"
        
        print("STEP 14-2 -- SUP1 페이지 전환 확인") 
        driver.find_element_by_xpath("//div[@id='supProcessGroupArea']/div/div[2]/div/div[2]/div[2]/div").click()
        time.sleep(3)
        
        expected_url = base_url_process+"/SUP/SUP_1"
        if driver.current_url == expected_url : 
            print("STEP 14-2 -- SUCCESS")
        else:
            print("STEP 14-2 -- FAILED")
            test_details += u"SUP1 카드를 클릭하였으나, 해당 페이지로 넘어가지 않음.\n"
        print()
        driver.back()
        time.sleep(3)
        
        print("STEP 15 -- SUP8 카드 비활성화 확인 ")
        time.sleep(1)
        if driver.find_element_by_xpath("//*[@id='supProcessGroupArea']/div/div[3]/div[1]/div[2]").get_attribute("class").find("process-card-enable")== -1: # 존재하지 않으면 -1을 리턴
            print("STEP 15 -- SUCCESS")
        else:
            print("STEP 15 -- FAILED")
            test_details += u"SUP8가 비활성화되었지만, 전체 프로세스에서 해당 카드가 활성화됨.\n"
        print()
        time.sleep(3)
        
        print("STEP 16 -- SUP9 카드 활성화 / 페이지 전환 확인 ")
        time.sleep(1)
        print("STEP 16-1 -- SUP9 카드 활성화 확인")
        if driver.find_element_by_xpath("//*[@id='supProcessGroupArea']/div/div[3]/div[2]/div[2]").get_attribute("class").find("process-card-enable")!= -1: # 존재하지 않으면 -1을 리턴
            print("STEP 16-1 -- SUCCESS")
        else:
            print("STEP 16-1 -- FAILED")
            test_details += u"SUP9가 활성화되었지만, 전체 프로세스에서 해당 카드가 활성화되지 않음.\n"
        
        print("STEP 16-2 -- SUP9 페이지 전환 확인") 
        driver.find_element_by_xpath("//div[@id='supProcessGroupArea']/div/div[3]/div[2]/div[2]").click()
        time.sleep(3)
        
        expected_url = base_url_process+"/SUP/SUP_9"
        if driver.current_url == expected_url : 
            print("STEP 16-2 -- SUCCESS")
        else:
            print("STEP 16-2 -- FAILED")
            test_details += u"SUP9 카드를 클릭하였으나, 해당 페이지로 넘어가지 않음.\n"
        print()
        driver.back()
        time.sleep(3)
        
        print("STEP 17 -- SUP10 카드 활성화 / 페이지 전환 확인 ")
        time.sleep(1)
        print("STEP 17-1 -- SUP10 카드 활성화 확인")
        if driver.find_element_by_xpath("//*[@id='supProcessGroupArea']/div/div[3]/div[3]/div[2]").get_attribute("class").find("process-card-enable")!= -1: # 존재하지 않으면 -1을 리턴
            print("STEP 17-1 -- SUCCESS")
        else:
            print("STEP 17-1 -- FAILED")
            test_details += u"SUP10가 활성화되었지만, 전체 프로세스에서 해당 카드가 활성화되지 않음.\n"
        
        print("STEP 17-2 -- SUP10 페이지 전환 확인") 
        driver.find_element_by_xpath("//div[@id='supProcessGroupArea']/div/div[3]/div[3]/div[2]/div/div[2]").click()
        time.sleep(3)
        
        expected_url = base_url_process+"/SUP/SUP_10"
        if driver.current_url == expected_url : 
            print("STEP 17-2 -- SUCCESS")
        else:
            print("STEP 17-2 -- FAILED")
            test_details += u"SUP10 카드를 클릭하였으나, 해당 페이지로 넘어가지 않음.\n"
        print()
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
            
        pi.delete_project(self, "TC_0032")
        
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

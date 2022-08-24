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
tc_content = u"SYS와 SWE 그룹의 작업 산출물을 파일 수정 시간에 따라 추가할 경우, 전체 프로세스 화면의 해당 프로세스 카드에 오류 아이콘이 떠야 한다. "

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
        
        project_name = "TC_0084"
        
        user_id = "admin"
        user_pw = "suresoft"
        
        sys2_file_name = u"SYS2_17-12_시스템 요구사항 명세서.xlsx"
        sys3_file_name = u"SYS3_04-06_시스템 아키텍처 설계서.xlsx"
        sys4_file_name_list = [u"SYS4_08-50_시험 명세서.xlsx", u"SYS4_08-52_시험 계획서.docx"]
        sys5_file_name_list = [u"SYS5_08-50_시험 명세서.xlsx", u"SYS5_08-52_시험 계획서.docx"]
        
        swe1_file_name = u"SWE1_17-11_소프트웨어 요구사항 명세서.xlsx"
        swe2_file_name = u"SWE2_04-04_소프트웨어 아키텍처 설계서.xlsx"
        swe3_file_name = u"SWE3_04-05_소프트웨어 상세 설계서.xlsx"
        swe4_file_name_list = [u"SWE4_08-50_시험 명세서.xlsx",u"SWE4_08-52_시험 계획서.docx"]
        swe5_file_name_list = [u"SWE5_08-50_시험 명세서.xlsx",u"SWE5_08-52_시험 계획서.docx"]
        swe6_file_name_list = [u"SWE6_08-50_시험 명세서.xlsx",u"SWE6_08-52_시험 계획서.docx"]
        
        sys_file_path = os.path.dirname(os.path.realpath(__file__)) + u"\\wp_template\\SYS\\disorder\\"
        swe_file_path = os.path.dirname(os.path.realpath(__file__)) + u"\\wp_template\\SWE\\disorder\\"
        process_list = ["SYS2", "SYS3", "SWE1", "SWE2", "SWE3", "SWE4", "SWE5", "SWE6", "SYS4", "SYS5"] 
        process_card_icon_xpath_list = ["//*[@id='sysProcessGroupArea']/div/div[3]/div[1]/div[2]/div[1]/div[2]",# SYS2
                                        "//*[@id='sysProcessGroupArea']/div/div[4]/div[1]/div[2]/div[1]/div[2]",# SYS3
                                        "//*[@id='sweProcessGroupArea']/div/div[2]/div[1]/div[2]/div[1]/div[2]",# SWE1
                                        "//*[@id='sweProcessGroupArea']/div/div[3]/div[1]/div[2]/div[1]/div[2]",# SWE2
                                        "//*[@id='sweProcessGroupArea']/div/div[4]/div[1]/div[2]/div[1]/div[2]",# SWE3
                                        "//*[@id='sweProcessGroupArea']/div/div[4]/div[2]/div[2]/div[1]/div[2]",# SWE4
                                        "//*[@id='sweProcessGroupArea']/div/div[3]/div[2]/div[2]/div[1]/div[2]",# SWE5
                                        "//*[@id='sweProcessGroupArea']/div/div[2]/div[2]/div[2]/div[1]/div[2]",# SWE6
                                        "//*[@id='sysProcessGroupArea']/div/div[4]/div[2]/div[2]/div[1]/div[2]",# SYS4
                                        "//*[@id='sysProcessGroupArea']/div/div[3]/div[2]/div[2]/div[1]/div[2]" # SYS5
                                        ]
        
        print("STEP 1 -- 프로젝트 세팅")
        print("STEP 1-1 -- 사용자 로그인 및 프로젝트 등록")
        li.login(self, user_id, user_pw)
        
        # 프로젝트 생성
        test_details += pi.project_essential_info(self, "GIT", "http://vpes@192.168.0.136:7990/scm/sprin/vpes.git", "vpes", "suresoft", project_name, "V-SPICE_CAR")
        test_details += pi.create_project(self)
        
        time.sleep(2)
        
        print("STEP 1-2 -- 프로젝트 접속")
        pi.search_project(self, project_name)
        
        print("STEP 2 -- 추적, 필수 작업 산출물 등록")
        driver.find_element_by_id("processes-tab").click()
        driver.find_element_by_id("sys").click()# SYS 프로세스 그룹 접속
        time.sleep(3)
        
        print("STEP 2-1 -- SYS2 시스템 요구사항 명세서 등록")
        driver.find_element_by_link_text("SYS.2 0/8").click()
        time.sleep(2)
        driver.execute_script("window.scrollTo(document.body.scrollWidth, 0);") 
        time.sleep(1)
        if self.upload_work_file_in_process(7, sys_file_path + sys2_file_name) == True:
            print("STEP 2-1 -- SUCCESS")
        else:
            print("STEP 2-1 -- FAILED")
            test_details += u"SYS2 시스템 요구사항 명세서를 등록했으나, 파일 정상 업로드 되지 않음.\n"
        time.sleep(2)
        
        print("STEP 2-2 -- SYS3 시스템 아키텍쳐 설계서 등록")
        driver.find_element_by_link_text("SYS.3 0/5").click()
        time.sleep(2)
        driver.execute_script("window.scrollTo(document.body.scrollWidth, 0);") 
        time.sleep(1)
        if self.upload_work_file_in_process(1, sys_file_path + sys3_file_name) == True:
            print("STEP 2-2 -- SUCCESS")
        else:
            print("STEP 2-2 -- FAILED")
            test_details += u"SYS3 시스템 아키텍쳐 설계서를 등록했으나, 파일 정상 업로드 되지 않음.\n"
        time.sleep(2)
        
        print("STEP 2-3 -- SWE1 소프트웨어 요구사항 명세서 등록")
        driver.find_element_by_id("swe").click()# SWE 프로세스 그룹 접속
        time.sleep(3)
        driver.find_element_by_link_text("SWE.1 0/8").click()
        time.sleep(2)
        driver.execute_script("window.scrollTo(document.body.scrollWidth, 0);") 
        time.sleep(1)
        if self.upload_work_file_in_process(7, swe_file_path + swe1_file_name) == True:
            print("STEP 2-3 -- SUCCESS")
        else:
            print("STEP 2-3 -- FAILED")
            test_details += u"SWE1 소프트웨어 요구사항 명세서를 등록했으나, 파일 정상 업로드 되지 않음.\n"
        time.sleep(2)
        
        
        print("STEP 2-4 -- SWE2 소프트웨어 아키텍쳐 설계서 등록")
        driver.find_element_by_link_text("SWE.2 0/5").click()
        time.sleep(2)
        driver.execute_script("window.scrollTo(document.body.scrollWidth, 0);") 
        time.sleep(1)
        if self.upload_work_file_in_process(1, swe_file_path + swe2_file_name) == True:
            print("STEP 2-4 -- SUCCESS")
        else:
            print("STEP 2-4 -- FAILED")
            test_details += u"SWE2 소프트웨어 아키텍쳐 설계서를 등록했으나, 파일 정상 업로드 되지 않음.\n"
        time.sleep(2)
        
        
        print("STEP 2-5 -- SWE3 소프트웨어 상세 설계서 등록")
        driver.find_element_by_link_text("SWE.3 0/5").click()
        time.sleep(2)
        driver.execute_script("window.scrollTo(document.body.scrollWidth, 0);") 
        time.sleep(1)
        if self.upload_work_file_in_process(1, swe_file_path + swe3_file_name) == True:
            print("STEP 2-5 -- SUCCESS")
        else:
            print("STEP 2-5 -- FAILED")
            test_details += u"SWE3 소프트웨어 상세 설계서를 등록했으나, 파일 정상 업로드 되지 않음.\n"
        time.sleep(2)
        
        
        print("STEP 2-6 -- SWE4 시험 명세서 / 시험 계획서 등록")
        driver.find_element_by_link_text("SWE.4 0/8").click()
        time.sleep(2)
        driver.execute_script("window.scrollTo(document.body.scrollWidth, 0);") 
        time.sleep(1)
        if self.upload_work_file_in_process(1, swe_file_path + swe4_file_name_list[0]) == True:
            print("STEP 2-6 -- 시험 명세서 SUCCESS")
        else:
            print("STEP 2-6 -- 시험 명세서 FAILED")
            test_details += u"SWE4 시험 명세서를 등록했으나, 파일 정상 업로드 되지 않음.\n"
        time.sleep(2)
        if self.upload_work_file_in_process(2, swe_file_path + swe4_file_name_list[1]) == True:
            print("STEP 2-6 -- 시험 계획서 SUCCESS")
        else:
            print("STEP 2-6 -- 시험 계획서 FAILED")
            test_details += u"SWE4 시험 계획서를 등록했으나, 파일 정상 업로드 되지 않음.\n"
        time.sleep(2)   
        
        
        print("STEP 2-7 -- SWE5 시험 명세서 / 시험 계획서 등록")
        driver.find_element_by_link_text("SWE.5 0/9").click()
        time.sleep(2)
        driver.execute_script("window.scrollTo(document.body.scrollWidth, 0);") 
        time.sleep(1)
        if self.upload_work_file_in_process(3, swe_file_path + swe5_file_name_list[0]) == True:
            print("STEP 2-7 -- 시험 명세서 SUCCESS")
        else:
            print("STEP 2-7 -- 시험 명세서 FAILED")
            test_details += u"SWE5 시험 명세서를 등록했으나, 파일 정상 업로드 되지 않음.\n"
        time.sleep(2)
        if self.upload_work_file_in_process(4, swe_file_path + swe5_file_name_list[1]) == True:
            print("STEP 2-7 -- 시험 계획서 SUCCESS")
        else:
            print("STEP 2-7 -- 시험 계획서 FAILED")
            test_details += u"SWE5 시험 계획서를 등록했으나, 파일 정상 업로드 되지 않음.\n"
        time.sleep(2)   
        
        
        print("STEP 2-8 -- SWE6 시험 명세서 / 시험 계획서 등록")
        driver.find_element_by_link_text("SWE.6 0/7").click()
        time.sleep(2)
        driver.execute_script("window.scrollTo(document.body.scrollWidth, 0);") 
        time.sleep(1)
        if self.upload_work_file_in_process(1, swe_file_path + swe6_file_name_list[0]) == True:
            print("STEP 2-8 -- 시험 명세서 SUCCESS")
        else:
            print("STEP 2-8 -- 시험 명세서 FAILED")
            test_details += u"SWE6 시험 명세서를 등록했으나, 파일 정상 업로드 되지 않음.\n"
        time.sleep(2)
        if self.upload_work_file_in_process(2, swe_file_path + swe6_file_name_list[1]) == True:
            print("STEP 2-8 -- 시험 계획서 SUCCESS")
        else:
            print("STEP 2-8 -- 시험 계획서 FAILED")
            test_details += u"SWE6 시험 계획서를 등록했으나, 파일 정상 업로드 되지 않음.\n"
        time.sleep(2)   
        
        
        print("STEP 2-9 -- SYS4 시험 명세서 / 시험 계획서 등록")
        driver.find_element_by_id("sys").click()# SYS 프로세스 그룹 접속
        time.sleep(3)
        driver.find_element_by_link_text("SYS.4 0/7").click()
        time.sleep(2)
        driver.execute_script("window.scrollTo(document.body.scrollWidth, 0);") 
        time.sleep(1)
        if self.upload_work_file_in_process(1, sys_file_path + sys4_file_name_list[0]) == True:
            print("STEP 2-9 -- 시험 명세서 SUCCESS")
        else:
            print("STEP 2-9 -- 시험 명세서 FAILED")
            test_details += u"SYS4 시험 명세서를 등록했으나, 파일 정상 업로드 되지 않음.\n"
        time.sleep(2)
        if self.upload_work_file_in_process(2, sys_file_path + sys4_file_name_list[1]) == True:
            print("STEP 2-9 -- 시험 계획서 SUCCESS")
        else:
            print("STEP 2-9 -- 시험 계획서 FAILED")
            test_details += u"SYS4 시험 계획서를 등록했으나, 파일 정상 업로드 되지 않음.\n"
        time.sleep(2) 
        
        
        print("STEP 2-10 -- SYS5 작업 산출물 등록")
        driver.find_element_by_link_text("SYS.5 0/6").click()
        time.sleep(2)
        driver.execute_script("window.scrollTo(document.body.scrollWidth, 0);") 
        time.sleep(1)
        if self.upload_work_file_in_process(1, sys_file_path + sys5_file_name_list[0]) == True:
            print("STEP 2-10 -- 시험 명세서 SUCCESS")
        else:
            print("STEP 2-10 -- 시험 명세서 FAILED")
            test_details += u"SYS5 시험 명세서를 등록했으나, 파일 정상 업로드 되지 않음.\n"
        time.sleep(2)
        if self.upload_work_file_in_process(2, sys_file_path + sys5_file_name_list[1]) == True:
            print("STEP 2-10 -- 시험 계획서 SUCCESS")
        else:
            print("STEP 2-10 -- 시험 계획서 FAILED")
            test_details += u"SYS5 시험 계획서를 등록했으나, 파일 정상 업로드 되지 않음.\n"
        time.sleep(2) 
        
        print("STEP 3 -- 전체 프로세스 카드별 에러 아이콘 확인")
        driver.find_element_by_id("processGroup").click()
        time.sleep(3)
        
        for i in range(1,len(process_list)):
            if driver.find_element_by_xpath(process_card_icon_xpath_list[i]).get_attribute("class") != "process-doc-reconfirm-uploaded-svg process-doc-reconfirm-icon":
                print("STEP 3 -- "+process_list[i]+" FAILED")
                test_details += u"파일 수정 일자 순에 맞지 않게 작업 산출물을 등록하였으나, 전체 프로세스의 "+process_list[i]+"카드에서 에러 아이콘이 출력되지 않음.\n"
            else:
                print("STEP 3 -- "+process_list[i]+" SUCCESS")
        if (test_details != ''):
            assert False
    # 프로세스 상세 페이지에서 작업 산출물 업로드 
    def upload_work_file_in_process(self, row_num, file_full_path):
        driver = self.driver
        driver.find_element_by_xpath("//div[@id='processDetail-ReportVue']/div[2]/ul/li[" + str(row_num) + "]/div[5]/div/div").click()
        driver.find_element_by_xpath("//div[@id='processDetail-ReportVue']/div[2]/ul/li[" + str(row_num) + "]/div[5]/div/div[2]/div/div[2]").click()
        
        file_input = driver.find_element_by_id("file-input")
        driver.execute_script("arguments[0].style.display = 'block';",file_input)
        file_input.clear()
        file_input.send_keys( file_full_path )
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
            return False
        else:
            return True

        
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
            
        pi.delete_project(self, "TC_0084")
        
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

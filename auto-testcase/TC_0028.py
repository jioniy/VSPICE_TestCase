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


tc_file = inspect.getfile(inspect.currentframe())
tc_num = os.path.splitext(tc_file)[0]
tc_content = u"작업 추가한 일정이 오늘 일자 이전일 경우 '완료', 오늘 일자가 포함될 경우 '진행 중', 오늘 일자 이후일 경우 '예정'이라는 문구가 출력되어야 한다."

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
        
        project_name = "TC_0028"
        
        user_id = "admin"
        user_pw = "suresoft"
        
        print("STEP 1 -- 프로젝트 세팅")
        print("STEP 1-1 -- 사용자 로그인 및 프로젝트 등록")
        li.login(self, user_id, user_pw)
        
        # 프로젝트 생성
        test_details += pi.project_essential_info(self, "GIT", "http://vpes@192.168.0.136:7990/scm/sprin/vpes.git", "vpes", "suresoft", project_name, "V-SPICE_CAR")
        test_details += pi.create_project(self)
        
        time.sleep(2)
        
        print("STEP 1-2 -- 프로젝트 접속 후 WBS 페이지로 이동")
        pi.search_project(self, project_name)
        driver.find_element_by_xpath("//a[@id='wbs-tab']/font").click() # WBS 페이지로 이동
        time.sleep(3)
        
        print("STEP 2 -- '완료' 상태 작업 추가")
        print("STEP 2-1 -- 작업 필수 항목 작성 후 저장")
        # 완료 상태 작업 추가
        driver.find_element_by_xpath("//div[@id='ChartVue']/div/div[2]/button/div/div[2]").click()
        time.sleep(2)
        # 작업 명 등록
        driver.find_element_by_xpath("//input[@type='text']").click()
        driver.find_element_by_xpath("//input[@type='text']").clear()
        driver.find_element_by_xpath("//input[@type='text']").send_keys("ACQ_WORK")
        time.sleep(1)
        # 프로세스 그룹 설정
        driver.find_element_by_xpath("//div[@id='wbsRegisterModal']/div/div/div[2]/div/div[2]/div[2]/div/div[2]/span").click()
        driver.find_element_by_xpath("//div[@id='wbsRegisterModal']/div/div/div[2]/div/div[2]/div[2]/div/div[3]/ul/li/span").click()
        time.sleep(1)
        # 담당자 설정
        driver.find_element_by_xpath("//div[@id='wbsRegisterModal']/div/div/div[2]/div/div[4]/div[2]/div/div[2]").click()
        driver.find_element_by_xpath("//div[@id='wbsRegisterModal']/div/div/div[2]/div/div[4]/div[2]/div/div[3]/ul/li/span/div").click()
        time.sleep(1)
        # 일정 시작일 입력(오늘 일자의 이전으로 일정 등록)
        work_start_date_res = datetime.now()+timedelta(days=-20)
        work_start_date = work_start_date_res.strftime('%Y-%m-%d')
        driver.find_element_by_id("wbs-startDate").click()
        driver.find_element_by_id("wbs-startDate").clear()
        time.sleep(1)
        driver.find_element_by_id("wbs-startDate").send_keys(work_start_date)
        time.sleep(2)
        # 일정 종료일 입력
        work_end_date_res = datetime.now()+timedelta(days=-10)
        work_end_date = work_end_date_res.strftime('%Y-%m-%d')
        driver.find_element_by_id("wbs-endDate").send_keys(work_end_date)
        driver.find_element_by_id("wbs-endDate").send_keys(Keys.ENTER)
        time.sleep(2)
        # 공수 입력
        driver.find_element_by_xpath("//input[@type='number']").click()
        driver.find_element_by_xpath("//input[@type='number']").clear()
        driver.find_element_by_xpath("//input[@type='number']").send_keys("2")
        time.sleep(2)
        # 작업 생성
        wait = WebDriverWait(driver, 10)
        driver.find_element_by_xpath("//div[@id='wbsRegisterModal']/div/div/div[3]/div/div/button[2]").click()
        element_text=""
        try:
            wait.until(EC.visibility_of_element_located((By.ID, 'alertModal')))
            element_text = driver.find_element_by_id("modal-content").text
        except Exception as e:
            print(e)
        time.sleep(2)
        
        if element_text != u"저장에 성공했습니다.":
            test_details += u"변경 저장 실패\n"
            print("STEP 2-1 -- FAILED")
        else:
            print("STEP 2-1 -- SUCCESS")
        time.sleep(2)
        
        print("STEP 2-2 -- 작업 상태 확인")
        # 작업 상태 (완료)
        element_text1 = driver.find_element_by_xpath("//div[@id='ChartVue']/div[2]/div/div/div/div/div/div/div/div/div[2]/div[3]/div[3]/div/div/div").text
        # 상위 프로세스 작업 상태 (완료) 
        element_process_text1 = driver.find_element_by_xpath("//div[@id='ChartVue']/div[2]/div/div/div/div/div/div/div/div/div[2]/div/div[3]/div/div/div").text
        
        if element_text1 == u"완료":
            if element_process_text1 == u"완료":
                print("STEP 2-2 -- SUCCESS")
            else: 
                print("STEP 2-2 -- FAILED")
                test_details += u"완료된 작업의 진행 상태가 '완료'로 표시되지 않음.\n"
        else:
            print("STEP 2-2 -- FAILED")
            test_details += u"완료된 상위 작업의 진행 상태가 '완료'로 표시되지 않음.\n"
        time.sleep(2)
        
        print("STEP 3 -- '진행 중' 상태 작업 추가")
        print("STEP 3-1 -- 작업 필수 항목 작성 후 저장")
        # '진행 중' 상태 작업 등록
        driver.find_element_by_xpath("//div[@id='ChartVue']/div/div[2]/button/div/div[2]").click()
        time.sleep(2)
        # 작업 명 등록
        driver.find_element_by_xpath("//input[@type='text']").click()
        driver.find_element_by_xpath("//input[@type='text']").clear()
        driver.find_element_by_xpath("//input[@type='text']").send_keys("MAN_WORK")
        time.sleep(1)
        # 프로세스 그룹 설정
        driver.find_element_by_xpath("//div[@id='wbsRegisterModal']/div/div/div[2]/div/div[2]/div[2]/div/div[2]/span").click()
        driver.find_element_by_xpath("//div[@id='wbsRegisterModal']/div/div/div[2]/div/div[2]/div[2]/div/div[3]/ul/li[2]/span").click()
        time.sleep(1)
        # 담당자 설정
        driver.find_element_by_xpath("//div[@id='wbsRegisterModal']/div/div/div[2]/div/div[4]/div[2]/div/div[2]").click()
        driver.find_element_by_xpath("//div[@id='wbsRegisterModal']/div/div/div[2]/div/div[4]/div[2]/div/div[3]/ul/li/span/div/span").click()
        time.sleep(1)
        # 일정 시작일 입력
        work_start_date_res = datetime.now()+timedelta(days=-10)
        work_start_date = work_start_date_res.strftime('%Y-%m-%d')
        driver.find_element_by_id("wbs-startDate").click()
        driver.find_element_by_id("wbs-startDate").clear()
        time.sleep(1)
        driver.find_element_by_id("wbs-startDate").send_keys(work_start_date)
        time.sleep(2)
        # 일정 종료일 입력
        work_end_date_res = datetime.now()+timedelta(days=10)
        work_end_date = work_end_date_res.strftime('%Y-%m-%d')
        driver.find_element_by_id("wbs-endDate").send_keys(work_end_date)
        driver.find_element_by_id("wbs-endDate").send_keys(Keys.ENTER)
        time.sleep(2)
        # 공수 입력
        driver.find_element_by_xpath("//input[@type='number']").click()
        driver.find_element_by_xpath("//input[@type='number']").clear()
        driver.find_element_by_xpath("//input[@type='number']").send_keys("2")
        time.sleep(2)
        # 작업 생성
        wait = WebDriverWait(driver, 10)
        driver.find_element_by_xpath("//div[@id='wbsRegisterModal']/div/div/div[3]/div/div/button[2]").click()
        element_text=""
        try:
            wait.until(EC.visibility_of_element_located((By.ID, 'alertModal')))
            element_text = driver.find_element_by_id("modal-content").text
        except Exception as e:
            print(e)
        time.sleep(2)
        
        if element_text != u"저장에 성공했습니다.":
            test_details += u"변경 저장 실패\n"
            print("STEP 3-1 -- FAILED")
        else:
            print("STEP 3-1 -- SUCCESS")
        time.sleep(2)

        print("STEP 3-2 -- 작업 상태 확인")
        # 작업 상태 확인
        element_text2 = driver.find_element_by_xpath("//div[@id='ChartVue']/div[2]/div/div/div/div/div/div/div/div/div[2]/div[6]/div[3]/div/div/div").text
        # 상위 프로세스 작업 상태 확인 
        element_process_text2 = driver.find_element_by_xpath("//div[@id='ChartVue']/div[2]/div/div/div/div/div/div/div/div/div[2]/div[4]/div[3]/div/div/div").text
        
        if element_text1 == u"완료":
            if element_process_text1 == u"완료":
                print("STEP 3-2 -- SUCCESS")
            else: 
                print("STEP 3-2 -- FAILED")
                test_details += u"진행 중인 작업의 진행 상태가 '진행 중'으로 표시되지 않음.\n"
        else:
            print("STEP 3-2 -- FAILED")
            test_details += u"진행 중인 상위 작업의 진행 상태가 '진행 중'으로 표시되지 않음.\n"
        time.sleep(2)
        
        print("STEP 4 -- '예정' 상태 작업 추가")
        print("STEP 4-1 -- 작업 필수 항목 작성 후 저장")
        # 예정 상태 작업 등록
        driver.find_element_by_xpath("//div[@id='ChartVue']/div/div[2]/button/div/div[2]").click()
        time.sleep(2)
        # 작업 명 등록
        driver.find_element_by_xpath("//input[@type='text']").click()
        driver.find_element_by_xpath("//input[@type='text']").clear()
        driver.find_element_by_xpath("//input[@type='text']").send_keys("SYS_WORK")
        time.sleep(1)
        # 프로세스 그룹 설정
        driver.find_element_by_xpath("//div[@id='wbsRegisterModal']/div/div/div[2]/div/div[2]/div[2]/div/div[2]/span").click()
        driver.find_element_by_xpath("//div[@id='wbsRegisterModal']/div/div/div[2]/div/div[2]/div[2]/div/div[3]/ul/li[3]/span").click()
        time.sleep(1)
        # 담당자 설정
        driver.find_element_by_xpath("//div[@id='wbsRegisterModal']/div/div/div[2]/div/div[4]/div[2]/div/div[2]").click()
        driver.find_element_by_xpath("//div[@id='wbsRegisterModal']/div/div/div[2]/div/div[4]/div[2]/div/div[3]/ul/li/span/div/span").click()
        time.sleep(1)
       # 일정 시작일 입력
        work_start_date_res = datetime.now()+timedelta(days=10)
        work_start_date = work_start_date_res.strftime('%Y-%m-%d')
        driver.find_element_by_id("wbs-startDate").click()
        driver.find_element_by_id("wbs-startDate").clear()
        time.sleep(1)
        driver.find_element_by_id("wbs-startDate").send_keys(work_start_date)
        time.sleep(2)
        # 일정 종료일 입력
        work_end_date_res = datetime.now()+timedelta(days=20)
        work_end_date = work_end_date_res.strftime('%Y-%m-%d')
        driver.find_element_by_id("wbs-endDate").send_keys(work_end_date)
        driver.find_element_by_id("wbs-endDate").send_keys(Keys.ENTER)
        time.sleep(2)
        # 공수 입력
        driver.find_element_by_xpath("//input[@type='number']").click()
        # 작업 생성
        wait = WebDriverWait(driver, 10)
        driver.find_element_by_xpath("//div[@id='wbsRegisterModal']/div/div/div[3]/div/div/button[2]").click()
        element_text=""
        try:
            wait.until(EC.visibility_of_element_located((By.ID, 'alertModal')))
            element_text = driver.find_element_by_id("modal-content").text
        except Exception as e:
            print(e)
        time.sleep(2)
        
        if element_text != u"저장에 성공했습니다.":
            test_details += u"변경 저장 실패\n"
            print("STEP 4-1 -- FAILED")
        else:
            print("STEP 4-1 -- SUCCESS")
        time.sleep(2)

        print("STEP 4-2 -- 작업 상태 확인")
        # 작업 상태 확인
        element_text3 = driver.find_element_by_xpath("//div[@id='ChartVue']/div[2]/div/div/div/div/div/div/div/div/div[2]/div[12]/div[3]/div/div/div").text
        # 상위 프로세스 작업 상태 확인 
        element_process_text3 = driver.find_element_by_xpath("//div[@id='ChartVue']/div[2]/div/div/div/div/div/div/div/div/div[2]/div[7]/div[3]/div/div/div").text
        
        if element_text3 == u"예정":
            if element_process_text3 == u"예정":
                print("STEP 4-2 -- SUCCESS")
            else: 
                print("STEP 4-2 -- FAILED")
                test_details += u"예정인 작업의 진행 상태가 '예정'으로 표시되지 않음.\n"
        else:
            print("STEP 4-2 -- FAILED")
            test_details += u"예정인 상위 작업의 진행 상태가 '예정'으로 표시되지 않음.\n"
        time.sleep(2)
        
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

    def tearDown(self): # 프로그램 종료 전 호출
        if hasattr(self, '_outcome'):  # Python 3.4+
            result = self.defaultTestResult()  # these 2 methods have no side effects
            self._feedErrorsToResult(result, self._outcome.errors)
        else:  # Python 3.2 - 3.3 or 3.0 - 3.1 and 2.7
            result = getattr(self, '_outcomeForDoCleanups', self._resultForDoCleanups)
        
        # 테스트용 프로젝트 삭제 
        pi.delete_project(self, "TC_0028")
        
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

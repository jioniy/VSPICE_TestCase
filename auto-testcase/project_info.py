from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC 
from selenium.common.exceptions import NoSuchElementException
import time 
from datetime import datetime, timedelta
import default_url

'''
project_info.py :: 프로젝트 생성 / 삭제 모듈
    - project_essential_info() :: 기본 정보 등록
    - project_process_info() :: 프로세스 정보, 승인요청 등록
    - project_extra_info() :: 기타 정보 등록
    - project_user_info() :: 사용자 등록
    - create_project() :: 프로젝트 생성
    - delete_project() :: 프로젝트 삭제
    - search_project() ::프로젝트 검색 및 클릭
return FAILED Message
'''

def project_essential_info(self, scm_type, scm_url, scm_id, scm_pw, project_key, project_car, start_date = "", end_date = ""):
    # return failed_messages(test_details) 
    failed_messages = ""
    
    driver = self.driver
    print(":: PROJECT_ESSENTIAL_INFO :: 프로젝트 기본 정보 등록")
    
    #메인 페이지 접속
    driver.get(default_url.VSPICE_URL)
    time.sleep(3)
    
    #프로젝트 등록 버튼
    driver.find_element_by_xpath("//div[@id='mainDashBoard-ProjectList_wrapper']/div/button/span").click()
    time.sleep(3)
    
    print(":: PROJECT_ESSENTIAL_INFO - SCM 인증 :: ")
    if scm_type=="GIT" or scm_type=="SVN":
        if scm_type=="SVN":
            driver.find_element_by_xpath("//div[@id='projectCreate-basicOpt']/div/div/div[2]/div/div/div[2]").click()
            driver.find_element_by_xpath("//div[@id='projectCreate-basicOpt']/div/div/div[2]/div/div/div[3]/ul/li[2]/span").click()
        #scm url 등록
        driver.find_element_by_id("projectCreate-scmUrl").click()
        driver.find_element_by_id("projectCreate-scmUrl").clear()
        driver.find_element_by_id("projectCreate-scmUrl").send_keys(scm_url)
        time.sleep(3)
        #scm id 등록
        driver.find_element_by_id("projectCreate-scmID").click()
        driver.find_element_by_id("projectCreate-scmID").clear()
        driver.find_element_by_id("projectCreate-scmID").send_keys(scm_id)
        time.sleep(3)
        #scm pw 등록
        driver.find_element_by_id("projectCreate-scmPW").click()
        driver.find_element_by_id("projectCreate-scmPW").clear()
        driver.find_element_by_id("projectCreate-scmPW").send_keys(scm_pw)
        time.sleep(3)
    elif scm_type=="DIRECTORY":
        driver.find_element_by_xpath("//div[@id='projectCreate-basicOpt']/div/div/div[2]/div/div/div[2]").click()
        driver.find_element_by_xpath("//div[@id='projectCreate-basicOpt']/div/div/div[2]/div/div/div[3]/ul/li[3]/span").click()
        time.sleep(3)
        #scm url 등록
        driver.find_element_by_id("projectCreate-scmUrl").click()
        driver.find_element_by_id("projectCreate-scmUrl").clear()
        driver.find_element_by_id("projectCreate-scmUrl").send_keys(scm_url)
    #scm 인증
    driver.find_element_by_id("projectCreate-scmAuthBtn").click()
    #ajax return 값 대기 
    wait = WebDriverWait(driver, 15)
    element_text=""
    try:
        wait.until(EC.visibility_of_element_located((By.ID, 'alertModal')))
        element_text = driver.find_element_by_id("modal-content").text
    except Exception as e:
        print(e)
    time.sleep(2)
    if element_text != u"SCM 인증 성공":
        print(":: PROJECT_ESSENTIAL_INFO - SCM 인증 :: FAILED")
        failed_messages += u"프로젝트 생성 시, SCM 인증 오류\n"
    else:
        print(":: PROJECT_ESSENTIAL_INFO - SCM 인증 :: SUCCESS")
    
    time.sleep(3)
    
    print(":: PROJECT_ESSENTIAL_INFO - 프로젝트 키 중복 ::")
    #프로젝트 키 입력
    driver.find_element_by_id("projectCreate-projectKey").click()
    driver.find_element_by_id("projectCreate-projectKey").clear()
    driver.find_element_by_id("projectCreate-projectKey").send_keys(project_key)
    time.sleep(1)
    driver.find_element_by_id("projectCreate-duplicationBtn").click()
    try:
        wait.until(EC.visibility_of_element_located((By.ID, 'alertModal')))
        element_text = driver.find_element_by_id("modal-content").text
    except Exception as e:
        print(e)
    time.sleep(3)
    if element_text != u"사용가능한 프로젝트 키 입니다.":
        print(":: PROJECT_ESSENTIAL_INFO - 프로젝트 키 중복 :: FAILED")
        failed_messages += u"프로젝트 생성 시, 프로젝트 키 중복 오류\n"
    else:
        print(":: PROJECT_ESSENTIAL_INFO - 프로젝트 키 중복 :: SUCCESS")
    time.sleep(3)

    print(":: PROJECT_ESSENTIAL_INFO - 프로젝트 차량/목표/기간 기타 필수 정보 입력 ::")
    #프로젝트 차량명 입력
    driver.find_element_by_id("projectCreate-name").click()
    driver.find_element_by_id("projectCreate-name").clear()
    driver.find_element_by_id("projectCreate-name").send_keys(project_car)
    time.sleep(1)
    
    #프로젝트 목표 입력
    driver.find_element_by_xpath("//div[@id='projectCreate-basicOpt']/div[3]/div[3]/div/div/div/div[2]/span").click()
    driver.find_element_by_xpath("//div[@id='projectCreate-basicOpt']/div[3]/div[3]/div/div/div/div[3]/ul/li/span").click()
    time.sleep(1)

    #프로젝트 기간 입력
    if start_date == "" : 
        start_date_res = datetime.now()+timedelta(days=-30)
        start_date = start_date_res.strftime('%Y-%m-%d')
    if end_date == "":
        end_date_res = datetime.now()+timedelta(days=30)
        end_date = end_date_res.strftime('%Y-%m-%d')
        
    driver.find_element_by_id("projectCreate-startDate").click()
    driver.find_element_by_id("projectCreate-startDate").click()
    driver.find_element_by_id("projectCreate-startDate").clear()
    time.sleep(1)
    driver.find_element_by_id("projectCreate-startDate").send_keys(start_date)
    time.sleep(1)
    driver.find_element_by_id("projectCreate-endDate").click()
    driver.find_element_by_id("projectCreate-endDate").click()
    driver.find_element_by_id("projectCreate-endDate").clear()
    time.sleep(1)
    driver.find_element_by_id("projectCreate-endDate").send_keys(end_date)
    time.sleep(3)
    
    driver.implicitly_wait(3) # xpath로 존재하지 않는 element를 찾는 소요 시간이 길어서 초기 세팅 값 변경
                              # 프로젝트 기간 에러 메세지는 바로 반응이 되므로 element를 오래 찾을 이유가 없음 
    try: 
        driver.find_element(By.XPATH, "//div[@id='projectCreate-basicOpt']/div[4]/div[2]/div[4]/span")
        print(":: PROJECT_ESSENTIAL_INFO - 프로젝트 차량/목표/기간 기타 필수 정보 입력 :: FAILED")
        failed_messages+=u"프로젝트 생성 시, 프로젝트 기간 입력 오류\n"
    except NoSuchElementException as e:
        print(":: PROJECT_ESSENTIAL_INFO - 프로젝트 차량/목표/기간 기타 필수 정보 입력 :: SUCCESS")    
    driver.implicitly_wait(30) # 초기 세팅 값으로 변경
    return failed_messages
    
def project_extra_info(self, item, chipset, toolchain):
    failed_messages = ""
    print(":: PROJECT_EXTRA_INFO -  기타 정보 입력 ::")
    driver = self.driver
    
    driver.find_element_by_id("projectCreate-subName").click()
    driver.find_element_by_id("projectCreate-subName").clear()
    driver.find_element_by_id("projectCreate-subName").send_keys(item)
    time.sleep(2)
    driver.find_element_by_id("projectCreate-chipset").click()
    driver.find_element_by_id("projectCreate-chipset").clear()
    driver.find_element_by_id("projectCreate-chipset").send_keys(chipset)
    time.sleep(2)
    driver.find_element_by_id("projectCreate-toolchain").click()
    driver.find_element_by_id("projectCreate-toolchain").clear()
    driver.find_element_by_id("projectCreate-toolchain").send_keys(toolchain)
    time.sleep(1)
    
    return failed_messages
    
    

def project_process_info(self, ACQ4=True, MAN3=True, SYS=True, SWE=True, SUP1=True, SUP8=True, SUP9=True, SUP10=True, ACQ_Approval=False, MAN_Approval=False, SYS_Approval=False, SWE_Approval=False, SUP_Approval=False): # 프로세스 정보 선택
    
    failed_messages = ""
    print(":: PROJECT_PROCESS_INFO :: 프로세스 정보 선택")
    driver = self.driver
    
    #프로세스 정보 탭 클릭
    driver.find_element_by_id("projectCreate-processOpt-tab").click()
    #프로세스 제외 선택
    if ACQ4==False:
        driver.find_element_by_xpath("//div[@id='projectCreate-processOpt']/div/div/div[2]/div/input").click()
        time.sleep(1)
    if MAN3==False:
        driver.find_element_by_xpath("//div[@id='projectCreate-processOpt']/div[2]/div/div[2]/div/input").click()
        time.sleep(1)
    if SYS==False:
        driver.find_element_by_xpath("//div[@id='projectCreate-processOpt']/div[3]/div/div[2]/div/input").click()
        time.sleep(1)
    if SWE==False:
        driver.find_element_by_xpath("//div[@id='projectCreate-processOpt']/div[4]/div/div[2]/div/input").click()
        time.sleep(1)
    if SUP1==False:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);") # 끝까지 스크롤 다운
        driver.find_element_by_xpath("//div[@id='projectCreate-processOpt']/div[5]/div/div[2]/div/input").click()
        time.sleep(1)
    if SUP8==False:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);") # 끝까지 스크롤 다운
        driver.find_element_by_xpath("//div[@id='projectCreate-processOpt']/div[5]/div/div[2]/div[2]/input").click()
        time.sleep(1)
    if SUP9==False:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);") # 끝까지 스크롤 다운
        driver.find_element_by_xpath("//div[@id='projectCreate-processOpt']/div[5]/div/div[2]/div[3]/input").click()
        time.sleep(1)
    if SUP10==False:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);") # 끝까지 스크롤 다운
        driver.find_element_by_xpath("//div[@id='projectCreate-processOpt']/div[5]/div/div[2]/div[4]/input").click()
        time.sleep(1)
    time.sleep(1)
    
    # 승인 요청
    if ACQ_Approval == True:
        driver.find_element_by_xpath("//input[@type='checkbox']").click()
        time.sleep(1)
    if MAN_Approval == True:
        driver.find_element_by_xpath("//div[@id='projectCreate-processOpt']/div[2]/div/div/div[2]/input").click()
        time.sleep(1)
    if SYS_Approval == True:
        driver.find_element_by_xpath("//div[@id='projectCreate-processOpt']/div[3]/div/div/div[2]/input").click()
        time.sleep(1)
    if SWE_Approval == True:
        driver.find_element_by_xpath("//div[@id='projectCreate-processOpt']/div[4]/div/div/div[2]/input").click()
        time.sleep(1)
    if SUP_Approval == True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);") # 끝까지 스크롤 다운
        driver.find_element_by_xpath("//div[@id='projectCreate-processOpt']/div[5]/div/div/div[2]/input").click()
        time.sleep(1)        
    time.sleep(1)
    
    print(":: PROJECT_PROCESS_INFO :: SUCCESS")
    
    return failed_messages

def project_user_info(self, user_list): # 사용자 등록
    failed_messages = ""
    driver=self.driver
    print(":: PROJECT_USER_INFO :: 사용자 등록")    
    
    # user_list 이름순 정렬 
    user_list.sort()
    
    # 사용자 추가 란 클릭
    driver.find_element_by_id("projectCreate-memberRegistration-tab").click()
    time.sleep(2)
    print(user_list)
    
    
    # 사용자 추가
    for user_id in user_list:
        driver.find_element_by_xpath("//div[@id='projectCreate-memberRegistration']/div/div/div/div").click()
        time.sleep(2)
        driver.find_element_by_id("projectCreate-memberBox").clear()
        driver.find_element_by_id("projectCreate-memberBox").send_keys(user_id)
        time.sleep(2)
        driver.find_element_by_xpath("//div[@id='projectCreate-memberRegistration']/div/div/div/div/div[3]/ul/li/span").click()
        time.sleep(2)
        driver.find_element_by_xpath("//div[@id='projectCreate-memberRegistration']/div/div/div/div").click()
        time.sleep(1)
        driver.find_element_by_id("projectCreate-memberBox").send_keys(Keys.CONTROL + "a")
        time.sleep(1)
        driver.find_element_by_id("projectCreate-memberBox").send_keys(Keys.DELETE)
        time.sleep(1)
        driver.find_element_by_id("projectCreate-projectMng").click()
        time.sleep(2)
    time.sleep(1)

    element_text=""
    try: 
        for i in range(len(user_list)):
            element_text = driver.find_element(By.XPATH, "//*[@id='projectCreate-memberList']/tbody/tr["+str(i+1)+"]/td[1]").text
            if element_text == user_list[i]:
                print(":: PROJECT_USER_INFO ["+user_list[i]+"] :: SUCCESS")   
            else:
                print(":: PROJECT_USER_INFO ["+user_list[i]+"] :: FAILED")  
                failed_messages += user_list[i] + u"사용자 등록 오류\n";
    except NoSuchElementException as e:
        print(":: PROJECT_USER_INFO :: FAILED")   
        failed_messages+=u"프로젝트 생성 시, 사용자 등록 오류\n"
    
    return failed_messages

def create_project(self): # 프로젝트 생성
    failed_messages = ""
    driver = self.driver
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);") # 끝까지 스크롤 다운
    time.sleep(3)
    print(":: CREATE_PROJECT :: 프로젝트 생성 버튼 클릭")
    element_text=""
    driver.find_element_by_id("projectCreate-createProjectBtn").click()
    wait = WebDriverWait(driver,15)
    try:
        wait.until(EC.visibility_of_element_located((By.ID, 'alertModal')))
        element_text = driver.find_element_by_id("modal-content").text
    except Exception as e:
        print(e)
    time.sleep(2)
    if element_text != u"프로젝트 생성":
        print(":: CREATE_PROJECT :: FAILED")
        failed_messages+=u"프로젝트를 생성하였으나, 모달창 뜨지 않음\n"
    else:
        print(":: CREATE_PROJECT :: SUCCESS")
    time.sleep(3)
    
    return failed_messages

def delete_project(self, project_name):
    failed_messages = ""
    driver=self.driver
    print(":: DELETE_PROJECT :: 프로젝트 삭제")
    
    #메인 페이지 접속
    driver.get(default_url.VSPICE_URL)
    time.sleep(3)
    
    #프로젝트 이름 검색 & 해당 프로젝트 클릭
    search_project(self, project_name)
    
    #환경 설정 배너 클릭
    driver.find_element_by_xpath("//a[@id='setting-tab']/font").click()
    time.sleep(2)
    
    driver.execute_script("window.scrollTo(document.body.scrollWidth, 0);") 
    #메뉴 드롭다운 -> 프로젝트 삭제 클릭
    driver.find_element_by_xpath("//*[@id='dropdownMenuButton']").click()
    driver.find_element_by_xpath("//*[@id='projectModify-HeaderVue']/div[2]/div/div/a[3]").click()
    time.sleep(2)
    
    wait = WebDriverWait(driver, 15)
    element_modal = ""
    try:
        wait.until(EC.visibility_of_element_located((By.ID, 'projectDeleteModal')))
        element_modal = driver.find_element_by_id("modal-content")
        #프로젝트 이름 입력
        driver.find_element_by_id("projectKeyForDelete").send_keys(project_name)
        #버튼 활성화 및 클릭 시 프로젝트 삭제
        element_btn = driver.find_element_by_xpath("//div[@id='projectDeleteModal']/div/div/div[3]/button[2]")
        if element_btn.get_attribute("disabled") == None:
            print(":: DELETE_PROJECT :: SUCCESS")
            element_btn.click()
            time.sleep(2)
        elif element_btn.get_attribute("disabled") == true:
            print(":: DELETE_PROJECT :: FAILED")
            failed_messages += u"프로젝트 이름을 입력해도 버튼이 활성화되지 않음\n"
    except Exception as e:
        print(":: DELETE_PROJECT :: FAILED")
        failed_messages += "프로젝트 삭제 모달창이 뜨지 않음.\n"
    time.sleep(2)
    return failed_messages
    

# 프로젝트 검색
def search_project(self, project_name):
    driver=self.driver
    
    #메인 페이지 접속
    driver.get(default_url.VSPICE_URL)
    time.sleep(3)
    
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
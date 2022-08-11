
var deselectPM;

/*
 * 
 * 프로젝트 키 - $('#TopNavBarRtmsCommonDataReqProjectId').val();
리비전 넘버 - $('#TopNavBarRtmsCommonDataReqRevisionNum').val();
UI 동작 버전 - $('#TopNavBarRtmsCommonDataReqUiModeKey').val();
 * 
 * 
 * 
 * */
//create globally
Vue.component('multiselect', VueMultiselect.Multiselect);
/* SCM 계정 검사 중인지 확인하는 함수 */
var isScmAccountRunCheck = null;
var projectMngTabVue = new Vue({
	el : '#projectCreate-projectMngTab',
	data : {
		currentTab : 'basicOpt',
		color : {
			active : "#007fea",
			inactive : "#767676"
		}
	},
	watch : {
		currentTab : function(newVal, oldVal) {
			var basicOptIcon = document.getElementById('projectCreate-basicOptIcon').contentDocument;
			var processOptIcon = document.getElementById('projectCreate-processOptIcon').contentDocument;
			var memberRegistrationIcon = document.getElementById('projectCreate-memberRegistrationIcon').contentDocument;
			
			if(newVal === 'memberRegistration') {
				memberRegistrationIcon.getElementsByTagName('path')[0].setAttribute("fill", this.color.active);
				//projectMngVue.getMemberRegistration();
			} else if(newVal === 'processOpt') {
				processOptIcon.getElementsByTagName('path')[0].setAttribute("fill", this.color.active);
			} else {
				basicOptIcon.getElementsByTagName('path')[0].setAttribute("fill", this.color.active);
			}
			
			if(oldVal === 'memberRegistration') {
				memberRegistrationIcon.getElementsByTagName('path')[0].setAttribute("fill", this.color.inactive);
			} else if(oldVal === 'processOpt') {
				processOptIcon.getElementsByTagName('path')[0].setAttribute("fill", this.color.inactive);
			} else {
				basicOptIcon.getElementsByTagName('path')[0].setAttribute("fill", this.color.inactive);
			}
		}
	},
	methods : {
		clickTab : function(tab) {
			this.currentTab = tab;
		}
	}
});


var projectMngVue = new Vue({
	el : '#projectCreate-projectMng',
	data : {
		type : "",
		isModified : {
			value : false, //프로젝트 설정인지 등록인지 체크
			projectInfo : null,
			checkScmInfo_First : false //프로젝트 설정일 경우 최초 scm 정보를 띄우기 위해 watch에서 조작되지 않도록 하기 위한 변수, 			
		},		
		isCreated : false,  //등록 또는 저장 가능한지 체크
		isCreatedMsg : "",	//등록 또는 저장 안될 경우 메시지
		isProjectUILock: false,		
		scmList : ['GIT','SVN','DIRECTORY'],
		staticToolSetting : {
			list : [ {value: "CI", text :'Code Inspector'},
              {value: "STATIC", text :'STATIC'}],
            value : {value: "CI", text :'Code Inspector'}
		},
		reliabilityToolSetting : {
			list : [ {value: "SN", text :'SNIPER'},
              {value: "STATIC", text :'STATIC'}],
            value : {value: "SN", text :'SNIPER'}
		},
		objectiveSetting : ["CL0", "CL1", "CL2", "CL3", "CL4", "CL5"],
		scmInfo : {
			selectedType : "GIT",
			id : "",
			password : "",
			url : "",
			valid : false,
			checking : false //인증 확인 중인지 아닌지 상태체크 변수
		},
		scmInfoClass : {
			id : "",
			password : "",
			url : ""
		},
		prjInfoClass : {
			projectKey : {
				class : "",
				enableCheckingButton : false, // 프로젝트 생성 버튼 클릭시 중복확인 활성 / 비활성 체크 변수
				msg : ""
			},
			name : {
				class : "",
				msg : ""
			},
			objective: {
				class : "",
				msg : ""
			},
			date : {
				class : "",
				msg : ""
			},
			process : {
				class : "",
				msg : ""
			}
		},
		prjInfo : {
			certifying : {	//인증 여부
				projectKey : false,
				name : false,
				date : false,
				process : true
			},
			basic : {	//필수 정보
				projectId : "",
				projectKey : "", 						//프로젝트 키
				name : "",								//차량명
				objective : "CL0", 					//목표 CL
				startDate : "",							//전체 일정 시작일
				endDate : "",							//전체 일정 종료일
				subName : "",							//아이템
				chipset : "",
				toolchain : ""				
			},
			processInfoList : {
			},
			state : 0,
		},
		memberListDT : null,
		member : {
			selected : new Array,
			selectList : new Array,
			pm : null,
			oldpm : null
		},
		waitMemberListDT : null,
		waitMember : {
			approvalList : new Array,
			list : new Array,
			cancelList : new Array
		},
		isAdmin: topNavBarGlobalSettingVue.isAccessUserAuthAdmin,
		addNewMember : new Array,
		originMember : new Array,
		reqUiModeKey : "korea",
		approval : {
			ACQ : false,
			MAN : false,
			SYS : false,
			SWE : false,
			SUP : false
		}
	},
	watch : {
		'scmInfo.selectedType' : function(newVal, oldVal) {
			if(newVal != oldVal && !this.isModified.checkScmInfo_First){
				this.scmInfo = {
						selectedType : newVal,
						id : '',
						password : '',
						url : '',
						valid : false,
						checking : false
				};
				
				this.scmInfoClass = {
						id : "",
						password : "",
						url : ""
				};
			}
			this.isModified.checkScmInfo_First = false;
		},
		'scmInfo.id' : function(newVal, oldVal) {
			this.scmInfo.valid = false;
			this.scmInfoClass.id = "";
			if (newVal == '') {
				this.scmInfoClass.id = 'is-invalid';
			} else {
				
			}
		},
		'scmInfo.password' : function(newVal, oldVal) {
			this.scmInfo.valid = false;
			this.scmInfoClass.password = "";
			if (newVal == '') {
				this.scmInfoClass.password = 'is-invalid';
			} else {
				
			}
		},
		'scmInfo.url' : function(newVal, oldVal) {
			this.scmInfo.valid = false;
			this.scmInfoClass.url = "";
			if (newVal == '') {
				this.scmInfoClass.url = 'is-invalid';
			} else {
				
			}
		},
		'prjInfo.basic.name' : function(newVal, oldVal) {
			this.prjInfo.certifying.name = this.checkTextMsg(newVal, this.prjInfoClass.name, 40);
		},
		'prjInfo.basic.startDate' : function(newVal, oldVal) {
			this.prjInfo.certifying.date = this.checkDate(newVal, this.prjInfo.basic.endDate);
		},
		'prjInfo.basic.endDate' : function(newVal, oldVal) {
			this.prjInfo.certifying.date = this.checkDate(this.prjInfo.basic.startDate, newVal)
		},
		'prjInfo.processInfoList' : {
			deep : true,
			handler : function(newVal, oldVal) {
				this.checkProcess();
			}
		},
		'member.selected' : function(newVal, oldVal) {
			$('#projectCreate-memberList').DataTable().clear().draw();
			for(var i=0; i<newVal.length; i++) {
				var row = $('#projectCreate-memberList').DataTable().row.add( {
	                "id": newVal[i].userId,
	                "name":   newVal[i].name,
	                "position":   newVal[i].position,
	                "delete": ""
	            } ).draw();
			}
			
			this.addNewMember = [];
			for(var i=0; i < this.member.selected.length; i++) {
				var exist = false;
				for(var j=0; j < this.originMember.length; j++) {
					if(this.originMember[j].userId == this.member.selected[i].userId) {
						exist = true;
					}
				}
				
				if(!exist) {
					this.addNewMember.push(this.member.selected[i]);
				}
			}
		},
		'waitMember.list' : function(newVal, oldVal) {
			$('#projectCreate-waitMemberList').DataTable().clear().draw();
			for(var i=0; i<newVal.length; i++) {
				$('#projectCreate-waitMemberList').DataTable().row.add( {
	                "id": newVal[i].userId,
	                "name":   newVal[i].name,
	                "position":   newVal[i].position,
	                "approve" : "",
	                "delete": ""
	            } ).draw();
			}
		},
		'prjInfo.processInfoList.ACQ.approval' : function(newVal, oldVal) {
			this.setApproval('ACQ', newVal);
		},
		'prjInfo.processInfoList.MAN.approval' : function(newVal, oldVal) {
			this.setApproval('MAN', newVal);
		},
		'prjInfo.processInfoList.SYS.approval' : function(newVal, oldVal) {
			this.setApproval('SYS', newVal);
		},
		'prjInfo.processInfoList.SWE.approval' : function(newVal, oldVal) {
			this.setApproval('SWE', newVal);
		},
		'prjInfo.processInfoList.SUP.approval' : function(newVal, oldVal) {
			this.setApproval('SUP', newVal);
		}
	},
	beforeMount : function() {
		this.getProcessList();		
	},
	mounted : function() {
		if((typeof projectSideBar !== 'undefined') && projectSideBar.projectInfo != undefined && (projectSideBar.projectInfo.id !=null && projectSideBar.projectInfo.id != '') ) {
			this.isModified.value = true;
			this.isModified.checkScmInfo_First = true; //설정일 경우에는 true로변환하여 최초 scmInfo 체크를 watch에서 변경되지 않도록 함
			this.getProjectInfo();
			this.checkScm('byReload');
			this.getProcessListUsed();
		}else if(typeof projectSideBar !== 'undefined' && projectSideBar.projectInfo == undefined) {
			alertModalVue.selectAlert("warning", getMessage("acst.message.ui.project.manage.alert.project.unable.project.information"));
		} else {
			this.getProcessListInit();
		}
		this.getMemberRegistration();
		this.reqUiModeKey = $("#TopNavBarAcstCommonDataReqUiModeKey").val();
		this.isProjectUILock = typeof projectSideBar !== 'undefined' ? projectSideBar.setProjectHeaderByBaselineProject() : false;
	},
	methods : {
		//프로세스 전체 리스트 가져오기
		getProcessList : function() {			
			var self = this;			
			var encodedUrl = encodeURI($('#TopNavBarAcstCommonDataContextRoot').val() + "/ProjectControll/getProcessListToUse");			
			
			$.ajax({
	            type : "POST",
	            url : encodedUrl,
	            async : false,
	            success : function(data){
	            	if(data.result) {
	            		var groupList = {};
	            		for(var i =0; i < data.resultData.length; i++){
	            			var group = data.resultData[i].substring(0, 3);
	            			if(groupList[group] == undefined || groupList[group] == null){
	            				groupList[group] = {
	            					processList : [],
	            					approval : false,
	            					disabled : true
	            				};
	            			}
	            			var obj = {
	            					process : data.resultData[i],
	            					active : false,
	            					approval : false
	            			}
	            			groupList[group].processList.push(obj);
	            		}
	            		self.prjInfo.processInfoList = groupList; 
	            	}
	            	
	            }
			});
		},
		//가져온 프로세스 리스트 생성의 경우 디폴트를 true로 변경하기
		getProcessListInit : function() {
			var keys = Object.keys(this.prjInfo.processInfoList);
			for(var i=0; i < keys.length; i++) {
				for(var j=0; j < this.prjInfo.processInfoList[keys[i]].processList.length; j++) {//전체 프로세스
					this.prjInfo.processInfoList[keys[i]].processList[j].active = true;
				}
			}
		},		
		//사용하고 있는 프로세스 리스트 가져오기
		getProcessListUsed : function() {			
			var self = this;			
			var encodedUrl = encodeURI($('#TopNavBarAcstCommonDataContextRoot').val() + "/ProjectDetail/getActiveProcessInfoList");			
			
			$.ajax({
	            type : "POST",
	            url : encodedUrl,
	            data : {
	            	"projectId" : this.prjInfo.basic.projectId
	            },
	            async : false,
	            success : function(data){
	            	if(data.result) {
	            		for(var i=0; i < data.resultData.length; i++) {
	            			var group = self.prjInfo.processInfoList[data.resultData[i].processGroup];
	            			for(var j =0; j < group.processList.length; j++) {
	            				if(group.processList[j].process == data.resultData[i].process) {
	            					group.processList[j].active = data.resultData[i].active;
	            					group.processList[j].approval = data.resultData[i].approval;
	            					group.disabled = false;
	            					break;
	            				}
	            			}
	            			if(data.resultData[i].approval) { //작업 산출물 등록 요청 기능 활성화
	            				self.prjInfo.processInfoList[data.resultData[i].processGroup].approval = true;
	            			}
	            		}
	            	}
	            	
	            }
			});
		},
		idWithName : function (member) {
		      return member.name +" ( " + member.userId + " )"
		},
		//필수 정보 초기화 함수
		getBasicOpt : function() {
		},
		//추가 정보 초기화 함수
		getProcessOpt : function() {
			
		},
		//사용자 등록 초기화 함수
		getMemberRegistration : function() {
			var self = this;
			
			//대기 테이블 생성
			this.waitMemberListDT = $('#projectCreate-waitMemberList').DataTable({
				dom: "lftpr",
				"initComplete": function () { 
					var api = this.api();
					$('#projectCreate-waitMemberList_filter input').off('.DT').on('keyup.DT', function(e) {
						if(e.keyCode == 13) {
							api.search(this.value).draw();
			            } 
			        });
				},
				"search": { 
				    "smart": false
				},				
				"deferRender": true,
				destroy: true,
				pageLength : 5,
				bPaginate : true,
				"pagingType": "simple_numbers",
				bLengthChange : true,
				lengthMenu : [ [ 5, 10, 30, 50, 100 ],
				             [ 5, 10, 30, 50, 100 ] ],
				processing : true,
				ordering : true,
				searching : true,
				serverSide: false,
				select : false,
				"language" : dataTable_language,
                columns : [
                    {data: "id"},
                    {data: "name"},
                    {data: "position"},
                    {data: "approve"},
                    {data: "delete"}
                ],
                columnDefs : [ {
    				targets : [ 3 ],
    				orderable: false,
    				createdCell : function(td, cellData, rowData, row, col) {
    					$(td).css("text-align", "center");
    				},
    				render : function(data, type, row) {
    					
    					var text = "<input type='checkbox' name='" + row.id +"_approval' onClick='projectMngVue.checkIfApproval(this)' id='" + row.id + "'/>";
    					
    					if(self.isProjectUILock) {
    						text = "<input type='checkbox' name='" + row.id +"_approval' id='" + row.id + "' disabled />";
    					}
    					
    					return text;
    				}

    			}, {
    				targets : [ 4 ],
    				orderable: false,
    				createdCell : function(td, cellData, rowData, row, col) {
    					$(td).css("text-align", "center");
    				},
    				render : function(data, type, row) {
    					
    					var text = "<input type='checkbox' name='" + row.id +"_cancel' onClick='projectMngVue.checkIfCancel(this)' id='" + row.id + "'/>";
    					
    					if(self.isProjectUILock) {
    						text = "<input type='checkbox' name='" + row.id +"_cancel' id='" + row.id + "' disabled/>";
    					}
    					
    					return text;
    				}

    			}]
			});
			
			// DataTable - HEADER ORDER CLICK EVENT
			$('#projectCreate-waitMemberList').on('order.dt', function() {
				var order = $('#projectCreate-waitMemberList').DataTable().order();

				var colCount = $('#projectCreate-waitMemberList').DataTable().columns().header().length;
				var headerColumnIdx = order[0][0];
				var orderDirection = order[0][1];
				
				for (var i = 0; i < colCount; i++) {
					$($($('#projectCreate-waitMemberList').DataTable().columns(i).header()).children()).removeClass('sort-arrow-asc');
					$($($('#projectCreate-waitMemberList').DataTable().columns(i).header()).children()).removeClass('sort-arrow-desc');
				}
				$($($('#projectCreate-waitMemberList').DataTable().columns(headerColumnIdx).header()).children()).addClass('sort-arrow-' + orderDirection);
			});
			
			//멤버 테이블 생성
			this.memberListDT = $('#projectCreate-memberList').DataTable({
				dom: "lftpr",
				"initComplete": function () { 
					var api = this.api();
					$('#projectCreate-memberList_filter input').off('.DT').on('keyup.DT', function(e) {
						if(e.keyCode == 13) {
							api.search(this.value).draw();
			            } 
			        });
				},
				"search": { 
				    "smart": false
				},				
				"deferRender": true,
				destroy: true,
				pageLength : 5,
				bPaginate : true,
				"pagingType": "simple_numbers",
				bLengthChange : true,
				lengthMenu : [ [ 5, 10, 30, 50, 100 ],
				             [ 5, 10, 30, 50, 100 ] ],
				processing : true,
				ordering : true,
				order: [[ 1, 'asc' ]],
				searching : true,
				serverSide: false,
				select: this.isProjectUILock ? false : { style: 'single', selector: 'td:first-child'},
				"language" : dataTable_language,
                columns : [
                    {data: "pm" , "visible": this.isModified.value},
                    {data: "id"},
                    {data: "name"},
                    {data: "position"},
                    {data: "delete"}
                ],
                columnDefs : [ {
                    orderable: false,
                    className: 'select-checkbox',
                    defaultContent: '',
                    targets:   [0]
                } ,{
    				targets : [ 4 ],
    				orderable: false,
    				createdCell : function(td, cellData, rowData, row, col) {
    					if(self.isProjectUILock) {
    						$(td).css("cursor", "not-allowed");
    					} else {
    						$(td).attr("onclick", "projectMngVue.removeMember(projectMngVue.findMemberById('"+ rowData.id +"')," + row +")");
    						$(td).css("cursor", "pointer");
    					}
    					$(td).css("text-align", "center");
    				},
    				render : function(data, type, row) {
    					return '<img src="' + $('#TopNavBarAcstCommonDataContextRoot').val() + '/image/svg/remove.svg" alt="제거"/>';
    				}

    			}]
			}).on( 'deselect', function ( e, dt, type, indexes ) { //PM변경 해제
	        	self.changePM(null, null);
	        } ).on( 'select', function ( e, dt, type, indexes ) {//PM변경
	        	var rowData = dt.rows( indexes ).data().toArray();
	            self.changePM(rowData[0].id, rowData[0].name);
	        });
			
			// DataTable - HEADER ORDER CLICK EVENT
			$('#projectCreate-memberList').on('order.dt', function() {
				var order = $('#projectCreate-memberList').DataTable().order();

				var colCount = $('#projectCreate-memberList').DataTable().columns().header().length;
				var headerColumnIdx = order[0][0];
				var orderDirection = order[0][1];
				
				for (var i = 0; i < colCount; i++) {
					$($($('#projectCreate-memberList').DataTable().columns(i).header()).children()).removeClass('sort-arrow-asc');
					$($($('#projectCreate-memberList').DataTable().columns(i).header()).children()).removeClass('sort-arrow-desc');
				}
				$($($('#projectCreate-memberList').DataTable().columns(headerColumnIdx).header()).children()).addClass('sort-arrow-' + orderDirection);
			});
			
			this.getUserList(); //전체 사용자 리스트 가져오기 , 생성일 때는 pm 정보도 추출
			if(this.isModified.value){
				this.getPM(); //현재 프로젝트의 PM정보 가져오기
				this.getMemberList(); //현재 프로젝트의 구성원 리스트 가져오기
				this.getWaitMemberList(); // 현재 프로젝트의 대기중 사용자 리스트 가져오기		
			}			
		},
		//구성원 테이블에서 현재 구성원의 member 객체 가져오기
		findMemberById : function(userId) {
			var fm = null;
			for(var i=0; i < this.member.selected.length; i++) {
				if(this.member.selected[i].userId === userId) {
					fm = this.member.selected[i];
					break;
				}
			}
			return fm;
		},
		// 구성원 테이블에서 member 객체 제외하는 함수
		removeMember : function(deselected, rowIdx) {
			if(deselected.userId == this.member.pm.userId) {
				this.member.pm = this.member.oldpm;
				this.member.pm.change = false;
			}
			if(this.member.selected.indexOf(deselected) > -1){
				this.member.selected.splice(this.member.selected.indexOf(deselected), 1);
			}
			
		},
		/* 전체 사용자 데이터 로드하는 함수 */ 
		getUserList : function() {
			var self = this;			
			var encodedUrl = encodeURI($('#TopNavBarAcstCommonDataContextRoot').val() + "/LoginControll/showAllUser");			
			var accessUserId = $('#TopNavBarAcstCommonDataReqAccessUserId').val();
			$.ajax({
	            type : "POST",
	            url : encodedUrl,
	            dataType : "json",
	            async : false,
	            success : function(data){
	            	if(data.data.length > 0 || data != null) {
	            		if(!self.isModified.value) {
	            			for(var i =0; i < data.data.length; i++){
	            				if(accessUserId === data.data[i].userId) {
	            					self.member.pm = data.data[i];
	            					data.data.splice(i, 1);
	            					break;
	            				}
	            			}	
	            		}
						self.member.selectList = data.data;  
	            	}
	            }
			});
		},
		//대기중인 사용자들을 승인할지 결정하는 함수
		checkIfApproval : function(check) {
			
			if(check.checked){ // 추가할 경우
				var exist = false;
				for(var j in this.waitMember.approvalList){
					if(check.id == this.waitMember.approvalList[j].userId) { //기존 추가되어져 있다면 추가 안함
						exist = true;
						break;
					}
				}
				
				if(!exist){// 추가한다면 대기중 사용자 리스트에서 찾아서 추가
					for(var i in this.waitMember.list){
						if(check.id == this.waitMember.list[i].userId) {
							this.waitMember.approvalList.push(this.waitMember.list[i]);									
						}
					}
				}
				
				for(var j in this.waitMember.cancelList){//추가가 되면 취소 리스트에서는 삭제 및 체크 해제
					if(check.id == this.waitMember.cancelList[j].userId) {
						this.waitMember.cancelList.splice(j,1);
						$("input[name='"+check.id+"_cancel']").click();
					}
				}
			} else { //추가 안할 경우
				for(var j in this.waitMember.approvalList){
					if(check.id == this.waitMember.approvalList[j].userId) {
						this.waitMember.approvalList.splice(j,1);
					}
				}
			}
		},
		//대기중인 사용자들을 승인취소할지 결정하는 함수
		checkIfCancel : function(check) {
			
			if(check.checked){ // 추가할 경우
				var exist = false;
				for(var j in this.waitMember.cancelList){
					if(check.id == this.waitMember.cancelList[j].userId) { //기존 추가되어져 있다면 추가 안함
						exist = true;
						break;
					}
				}
				
				if(!exist){// 추가한다면 대기중 사용자 리스트에서 찾아서 추가
					for(var i in this.waitMember.list){
						if(check.id == this.waitMember.list[i].userId) {
							this.waitMember.cancelList.push(this.waitMember.list[i]);									
						}
					}
				}
				
				for(var j in this.waitMember.approvalList){//추가가 되면 승인 리스트에서는 삭제 및 체크 해제
					if(check.id == this.waitMember.approvalList[j].userId) {
						this.waitMember.approvalList.splice(j,1);
						$("input[name='"+check.id+"_approval']").click();
					}
				}
			} else { //추가 안할 경우
				for(var j in this.waitMember.cancelList){
					if(check.id == this.waitMember.cancelList[j].userId) {
						this.waitMember.cancelList.splice(j,1);
					}
				}
			}
		},
		//변경할 PM 저장하기 - PM 객체에 변수 저장만함
		changePM : function(userId, userName) {
			if(userId == null || userName == null) {
				this.getPM();
			} else {
				this.member.pm = {
						userId : userId,
						name : userName,
						change : true
				}
			}
		},		
		//현재 프로젝트의 PM 가져오기
		getPM : function() {
			var self = this;
			var encodedUrl = encodeURI($('#TopNavBarAcstCommonDataContextRoot').val() + "/ProjectControll/getMemberByprojectId");			
			
			$.ajax({
	            type : "POST",
	            url : encodedUrl,
	            data : {
	            	"projectId" : this.prjInfo.basic.projectId,
	            	"role" : "PROJECT_PM"
	            },
	            dataType : "json",
	            success : function(data){
	            	if(data.length > 0 || data != null) {
	            		self.member.pm = data[0]; 
	            		self.member.oldpm = data[0];
	            		
	            		for(var i =0; i < self.member.selectList.length; i++){
            				if(self.member.selectList[i].userId === self.member.pm.userId) {
            					self.member.selectList.splice(i, 1);
            					break;
            				}
            			}	
	            	}
	            }
			});
		},
		//현재 프로젝트의 멤버 등록 대기중인 사용자 데이터 가져오는 함수
		getWaitMemberList : function() {
			var self = this;
			var encodedUrl = encodeURI($('#TopNavBarAcstCommonDataContextRoot').val() + "/ProjectControll/getMemberByprojectId");			
			
			$.ajax({
	            type : "POST",
	            url : encodedUrl,
	            data : {
	            	"projectId" : this.prjInfo.basic.projectId,
	            	"role" : "PROJECT_UNAPPROVED"
	            },
	            dataType : "json",
	            success : function(data){
	            	if(data.length > 0 || data != null) {						
						//대기 명단에 추가
						self.waitMember.list = data;
						for(var i in self.waitMember.list) {
							for(var j in self.member.selectList){
								if(self.member.selectList[j].userId == self.waitMember.list[i].userId) {
									self.member.selectList[j].$isDisabled = true;
								}
							}
						}
	            	}
	            }
			});
		},
		//현재 프로젝트의 구성원 데이터 가져오는 함수
		getMemberList : function() {
			var self = this;
			var encodedUrl = encodeURI($('#TopNavBarAcstCommonDataContextRoot').val() + "/ProjectControll/getMemberByprojectId");			
			
			$.ajax({
	            type : "POST",
	            url : encodedUrl,
	            data : {
	            	"projectId" : this.prjInfo.basic.projectId,
	            	"role" : "PROJECT_NORMAL"
	            },
	            dataType : "json",
	            success : function(data){
	            	if(data.length > 0 || data != null) {
						//기존 구성원에 추가하기
						self.member.selected = data;
						self.originMember = data;
	            	}
	            }
			});
		},		
		/* 프로젝트 생성하는 함수 */
		createProject : function() {
			this.checkRequired();
			if(!this.isCreated) {
				alertModalVue.selectAlert("warning", this.isCreatedMsg);
				this.isCreatedMsg = "";
				return;
			}
			var encodedUrl = encodeURI($('#TopNavBarAcstCommonDataContextRoot').val() + "/ProjectControll/createProject");
			
			var memberList = new Array;
			for(var i=0; i<this.member.selected.length; i++){
				memberList.push("PROJECT_NORMAL:" + this.member.selected[i].userId + ";" + this.member.selected[i].name);
			}
			
			/*memberList.push("PROJECT_PM:" + this.member.pm.userId + ";" + this.member.pm.name);*/
			$.ajax({

				type : "POST",
				url : encodedUrl,
				data :{
					basicData :  JSON.stringify(this.prjInfo.basic),
					processData :  JSON.stringify(this.prjInfo.processInfoList),
					scmData :  JSON.stringify(this.scmInfo),
					memberList : memberList					
				},
				success : function(data) {
					if(data.result) {
						//registeredModalVue.showModal = true;
						alertModalVue.selectAlert("success", getMessage('acst.message.ui.project.manage.alert.project.create'));
						alertModalVue.$watch('showModal', function(newVal, oldVal){
							if(!newVal) movePage("");
						});
					} else {
						alertModalVue.selectAlert("fail", getMessage('acst.message.ui.project.manage.alert.project.create.fail'));
					}
				}
			});
			
		},
		/* 프로젝트 설정하는 함수 */
		modifyProject : function() {
			var self = this;
			
			if(self.isProjectUILock) {
				return alertModalVue.selectAlert("warning", getMessage("acst.message.ui.notification.not.available.for.baselineproject"));
			} else if(projectSideBar.alertMessageByProjectStatus() != 'none'){
				return alertModalVue.selectAlert("warning", projectSideBar.alertMessageByProjectStatus());
			}			
			
			self.checkRequired();
			if(!self.isCreated) {
				alertModalVue.selectAlert("warning", this.isCreatedMsg);
				self.isCreatedMsg = "";
				return;
			}
			var encodedUrl = encodeURI($('#TopNavBarAcstCommonDataContextRoot').val() + "/ProjectControll/modifyProject");
			
			var memberList = new Array;
			var approvalList = new Array;
			var cancelList = new Array;
			for(var i=0; i<self.member.selected.length; i++){
				if(!(self.member.selected[i].userId == self.member.pm.userId)) {
					memberList.push("PROJECT_NORMAL:" + self.member.selected[i].userId + ";" + self.member.selected[i].name);					
				} 
			}
			if(this.member.pm.change ) {
				memberList.push("PROJECT_NORMAL:" + self.member.oldpm.userId + ";" + self.member.oldpm.name);
			} 
			memberList.push("PROJECT_PM:" + self.member.pm.userId + ";" + self.member.pm.name);
			
			for(var i=0; i<self.waitMember.approvalList.length; i++){
				approvalList.push("PROJECT_NORMAL:" + self.waitMember.approvalList[i].userId + ";" + self.waitMember.approvalList[i].name);
			}
			
			for(var i=0; i<self.waitMember.cancelList.length; i++){
				cancelList.push("PROJECT_UNAPPROVED:" + self.waitMember.cancelList[i].userId + ";" + self.waitMember.cancelList[i].name);
			}
			
			$.ajax({

				type : "POST",
				url : encodedUrl,
				data :{
					basicData :  JSON.stringify(this.prjInfo.basic),
					processData :  JSON.stringify(this.prjInfo.processInfoList),
					scmData :  JSON.stringify(this.scmInfo),
					memberList : memberList,
					approvalList : approvalList,
					cancelList : cancelList
				},
				success : function(data) {
					if(data.result) {
						if((self.member.pm.userId != data.resultData.userId) && (self.isAdmin == false)) {
							alertModalVue.returnPage("success" , getMessage("acst.message.ui.project.manage.alert.project.modify.success"), "ProjectOverView", self.prjInfo.basic.projectId, 0);
						} else {
							alertModalVue.selectAlert("success" , getMessage("acst.message.ui.project.manage.alert.project.modify.success"));
							alertModalVue.$watch('showModal', function(newVal, oldVal){
								if(!newVal) location.reload();
							});
						}
					} else {
						alertModalVue.selectAlert("fail" , getMessage("acst.message.ui.project.manage.alert.project.modify.fail"));
					}
					
				}
			});
			
		},		
		// SCM URL 경로 확인하는 함수
		checkScm : function(entryFlag) {
			/*if(this.prjInfo.state > 1 ) {				
				return;
			}*/
			this.scmInfo.valid = false;			
			this.scmInfo.checking = true;	
			
			var scmType = this.scmInfo.selectedType;
			var scmID = this.scmInfo.id.trim();
			var scmPW = this.scmInfo.password;
			var url = this.findAndReplace(this.scmInfo.url.trim(),"\\","/");
			
			var isNull = false;
		
			if(scmType != "DIRECTORY") {
				if(this.isScmNullCheck()) {
					alertModalVue.selectAlert("warning",  getMessage('acst.message.ui.project.manage.alert.input.scm.information'));
					this.scmInfo.checking = false;
					return;
				}
			}
			
			var encodedUrl = encodeURI($('#TopNavBarAcstCommonDataContextRoot').val() + "/ProjectControll/checkPath");
			
			var data = {
					type : scmType,
					url : url,
					scmID : scmID,
					scmPW : scmPW
			};
			var self = this;
			isScmAccountRunCheck = $.ajax({
				type : "POST",
				url : encodedUrl,
				data : data,
				dataType : "json",
				success : function(data) {
					self.getReturnValueOfScm(data.resultCode, data.checkType, entryFlag);
					self.scmInfo.checking = false;
				}
			});
			/*self.getReturnValueOfScm("OK", "DIRECTORY"); //임시 2021.08.30 - SCM 관련 로직 구현되어있지 않음
			self.scmInfo.checking = false;*/
				
		
		},
		// 치환 하는 함수
		findAndReplace : function(string, target, replacement) {

			for (var i = 0; i < string.length; i++) {
				string = string.replace(target, replacement);
			}
			return string;
		},
		/* SCM 정보 입력 했는지 체크하는 함수 (ID, PW, URL) */
		isScmNullCheck : function() {
			var scmID = this.scmInfo.id.trim();
			var scmPW = this.scmInfo.password;
			var url = this.findAndReplace(this.scmInfo.url.trim(),"\\","/");
			var isNull = false;
			if(scmID === null || scmID.length === 0) {
				isNull = true;
			}			
			if(scmPW === null || scmPW.length === 0) {
				isNull = true;
			}
			if(url === null || url.length === 0) {
				isNull = true;
			}			
			return isNull;
			
		},
		/* 인증 버튼 클릭 후 SCM 유효성 검사 중 Project 모달 창 닫으면 Ajax 끊어주는 함수 */
		IsScmAccountRunCheck_Abort : function() {
			if(isScmAccountRunCheck != null) {
				isScmAccountRunCheck.abort();
				this.scmInfo.valid = false;
				this.scmInfo.checking = false;
				isScmAccountRunCheck = null;
			}
			
		},
		// scm url 리턴 결과에 대한 메시지 반환	
		getReturnValueOfScm : function(resultCode, checkType, entryFlag) {
			if (resultCode == "OK") {
				this.scmInfo.valid=true;
				// 버튼 클릭으로 인증 요청시에만 성공 팝업 띄움
				if(entryFlag == 'byButton') {
					alertModalVue.selectAlert("success", getMessage('acst.message.ui.project.manage.alert.scm.certification.success'));
				}
				
				this.scmInfoClass = {
						id : "is-valid",
						password : "is-valid",
						url : "is-valid"
				};
			} else {
				this.scmInfo.valid=false;
				if(resultCode == "FAIL") {
					if(checkType == "DIRECTORY") {
						alertModalVue.selectAlert("warning", getMessage('acst.message.ui.project.manage.alert.invalid.path'));
					} else {
						alertModalVue.selectAlert("warning", getMessage('acst.message.ui.project.manage.alert.wrong.user.or.invalid.path'));
					}
				} else {
					var msgCode = "";
					pathFlag = false;
					if (resultCode == "URLNULL") {
						// 존재하지 않은 경로입니다.
						msgCode = 'acst.message.ui.project.manage.alert.no.existent.path';
					} else if (resultCode == "WRONGROOTPATH") {
						// 유효하지 않은 ROOT PATH 입니다.
						msgCode = 'acst.message.ui.project.manage.alert.invalid.rootpath';
					} else if ((resultCode == "NONROOTPATH") || (resultCode == "NONDATE" && checkType == "DIRECTORY")) {
						// ROOT PATH를 설정해 주세요.
						msgCode = 'acst.message.ui.project.manage.alert.set.rootpath';
					} else if (resultCode == "PATHINSTALLED") {
						// 설치경로를 참조 합니다.
						msgCode = 'acst.message.ui.project.manage.alert.installed.path';
					} else if (resultCode == "PATHERROR") {
						// 유효하지 않은 경로 입니다.
						msgCode = 'acst.message.ui.project.manage.alert.invalid.path';
					} else if (resultCode == "SvnURLFAIL" || resultCode == "GitUrlPortRange") {
						// 경로가 존재하지 않거나 접근 권한이 없습니다.
						msgCode = 'acst.message.ui.project.manage.alert.no.existent.path.or.dont.access';
					} else if (resultCode == "ERROR") {
						// DIRECTORY 경로 설정 중 문제가 발생했습니다.
						msgCode = 'acst.message.ui.project.manage.alert.set.directory.problem';
					} else if (resultCode == "NONDATE") {
						// SCM 계정정보를 설정해주세요.
						msgCode = 'acst.message.ui.project.manage.alert.set.scm.account.problem';
					} else if (resultCode == "SvnAccountFAIL" || resultCode == "GitAuthorizedFAIL") {
						// SCM 계정 정보를 확인해주세요.
						msgCode = 'acst.message.ui.project.manage.alert.set.scm.account.problem';
					} else if(resultCode == "SvnForbiddenFAIL") {
						// 접근 권한이 없습니다.
						/* msgCode = "<spring:message code='rtms.message.ui.project.Problem.SvnForbiddenFAIL' />"; */
						// 경로가 존재하지 않거나 접근 권한이 없습니다.
						msgCode = 'acst.message.ui.project.manage.alert.no.existent.path.or.dont.access'; 
					} else if(resultCode == "GitUrlFAIL") {
						// 경로가 존재하지 않거나 접근 권한이 없습니다.
						msgCode = 'acst.message.ui.project.manage.alert.no.existent.path.or.dont.access'; 
					} else if(resultCode == "GitAccountLocked") {
						// 계정이 잠겨있습니다.
						msgCode = 'acst.message.ui.project.manage.alert.git.account.locked';
					} else if(resultCode == "SvnConnectionFAIL") {
						msgCode = 'acst.message.ui.project.manage.alert.svn.connection.fail';
					}					
					alertModalVue.selectAlert("warning", getMessage(msgCode));
				}
				this.scmInfoClass = {
						id : "is-invalid",
						password : "is-invalid",
						url : "is-invalid"
				};
			}
		},
		//프로젝트 생성 가능성 확인
		checkRequired : function() {
			
			this.isCreatedMsg = "";
			
			//var type = $('#scmType option:selected').val();
			var type = this.scmInfo.selectedType;
			if(!this.scmInfo.valid && this.scmInfo.selectedType != "DIRECTORY") {
				this.scmInfoClass.id = 'is-invalid';
				this.scmInfoClass.password = 'is-invalid';
				this.scmInfoClass.url = 'is-invalid';
				this.isCreatedMsg = getMessage('acst.message.ui.project.manage.warning.certify.scm.information');
			} 
			
			if(!this.scmInfo.valid && this.scmInfo.selectedType === "DIRECTORY") {
				this.scmInfoClass.url = 'is-invalid';
				
				if(this.isCreatedMsg == "") {
					this.isCreatedMsg = getMessage('acst.message.ui.project.manage.warning.input.path');
				}
			} 
			
			if(!this.prjInfo.certifying.projectKey) {
				this.prjInfoClass.projectKey.class = "is-invalid";
				this.prjInfoClass.projectKey.enableCheckingButton = true;
				
				if(this.isCreatedMsg == "") {
					this.isCreatedMsg = getMessage('acst.message.ui.project.manage.warning.no.projectkey.duplication.checking');
				}
			} 
			
			if(!this.prjInfo.certifying.name) {
				this.prjInfoClass.name.class = "is-invalid";

				if(this.isCreatedMsg == "") {
					this.isCreatedMsg = getMessage('acst.message.ui.project.manage.warning.input.vehicle.name');
				}
			}
			
			if(!this.prjInfo.certifying.date) {
				this.prjInfoClass.date.class = "is-invalid";
				
				if(this.isCreatedMsg == "") {
					this.isCreatedMsg = getMessage('acst.message.ui.project.manage.warning.set.incorrect.time');
				}
			}
			
			if(!this.prjInfo.certifying.process) {
				if(this.isCreatedMsg == "") {
					this.isCreatedMsg = getMessage('acst.message.ui.project.manage.warning.selected.atleast.one.process');
				}
			}
			
			if(this.isCreatedMsg == "") {
				this.isCreated = true;
			} else {
				this.isCreated = false;
			}
		},
		//프로젝트명 중복 확인
		checkProject : function() {
			this.prjInfo.certifying.projectKey = false;
			
			var projectKey = "";
			projectKey = this.prjInfo.basic.projectKey;

			if (projectKey === null || typeof projectKey == 'undefined' || projectKey == "") {
				alertModalVue.selectAlert("warning", getMessage('acst.message.ui.project.manage.alert.input.projectkey'));
				return;				
			} else if(!this.checkProjectKey(projectKey)) {
				alertModalVue.selectAlert("fail", getMessage('acst.message.ui.project.manage.alert.invalid.projectkey', 40, "(-), (_)"));
				return;
			} else {
				var encodedUrl = encodeURI($('#TopNavBarAcstCommonDataContextRoot').val() + "/ProjectControll/checkProjectKey");

				var data = {
					projectKey : projectKey,
					"${_csrf.parameterName}" : "${_csrf.token}"
				}

				var self = this;
				$.ajax({
					type : "POST",
					url : encodedUrl,
					data : data,
					success : function(data) {
						if (data.result) {
							self.prjInfo.certifying.projectKey = false;
							self.prjInfoClass.projectKey.class = "is-invalid";
							self.prjInfoClass.projectKey.msg = "";
							alertModalVue.selectAlert("warning", getMessage('acst.message.ui.project.manage.alert.duplication.projectkey'));
						} else {
							self.prjInfo.certifying.projectKey = true;
							alertModalVue.selectAlert("success", getMessage('acst.message.ui.project.manage.alert.duplication.checking.success'));
							self.prjInfoClass.projectKey.class = "";
							self.prjInfoClass.projectKey.msg = "";
						}
					}
				});
			}
		},
		inputProjectKeyText : function(event) {
			this.prjInfoClass.projectKey.enableCheckingButton = false;
			if(!this.isModified.value) {//생성일 때만하고, 설정일 때는 아예 변경이 불가능하기때문에 필요없음
				this.prjInfo.certifying.projectKey = false; //프로젝트 키는 변경되면 무조건 재인증하여야 하며, 중복확인 버튼을 통해서만 인증할수 있다.		
			}			
			this.checkProjectKey(event.target.value);			
			this.prjInfo.basic.projectKey=event.target.value;
			/*var reg = /[ㄱ-ㅎ|ㅏ-ㅣ|가-힣]/g;
			if(reg.test(e.target.value)) {
				this.prjInfoClass.projectKey.enableCheckingButton = false;
				this.prjInfoClass.projectKey.class="is-invalid";
				this.prjInfoClass.projectKey.msg = "한글은 입력할 수 없습니다.";
			}
			this.prjInfo.basic.projectKey=e.target.value.replace(/[ㄱ-ㅎ|ㅏ-ㅣ|가-힣]/g, '' )*/
		},
		checkProjectKey : function(value) {
			var text = '^[a-zA-Z0-9\_\-]{0,40}$';
			var regex = new RegExp(text);
			var result = false;
			if(!regex.test(value)) {
				this.prjInfoClass.projectKey.class = "is-invalid";
				this.prjInfoClass.projectKey.msg = getMessage('acst.message.ui.project.manage.alert.invalid.projectkey', 40, "(-), (_)");
			} else {
				if(value.charAt(value.length-1) === "_" || value.charAt(value.length-1) === "-") {
					this.prjInfoClass.projectKey.class = "is-invalid";
					this.prjInfoClass.projectKey.msg = getMessage('acst.message.ui.project.manage.alert.invalid.projectkey', 40, "(-), (_)");
				} else if(value.charAt(0) === "_" || value.charAt(0) === "-") {
					this.prjInfoClass.projectKey.class = "is-invalid";
					this.prjInfoClass.projectKey.msg = getMessage('acst.message.ui.project.manage.alert.invalid.projectkey', 40, "(-), (_)");
				} else {
					this.prjInfoClass.projectKey.class = "";
					this.prjInfoClass.projectKey.msg = "";
					this.prjInfoClass.projectKey.enableCheckingButton = true;
					result=true;
				}
			}	
			return result;
		},
		//필수입력값 텍스트 값 확인
		checkTextMsg : function(value, classVal, length) {
			var result = true;		
			value = value.trim();
			if(value.length > length) {
				classVal.class = "is-invalid";
				classVal.msg = getMessage('acst.message.ui.project.manage.alert.invalid.msg', length);
				result = false;
			} else if (value.length > 0 ) {
				/*if (value.indexOf("\"") != -1
						|| value.indexOf("'") != -1
						|| value.indexOf("/") != -1
						|| value.indexOf("?") != -1
						|| value.indexOf("*") != -1
						|| value.indexOf("|") != -1
						|| value.indexOf("<") != -1
						|| value.indexOf(">") != -1
						|| value.indexOf(":") != -1
						|| value.indexOf("\\") != -1) {
					classVal.class = "is-invalid";
					classVal.msg = getMessage('acst.message.ui.project.manage.warning.cant.used.special.characters', "( \", ', /, ?, *, |, <, >, :, \\ )");
					result = false;
				} else if(value.charAt(value.length-1) === "_" || value.charAt(value.length-1) === "-") {
					classVal.class = "is-invalid";
					classVal.msg = getMessage('acst.message.ui.project.manage.warning.cant.used.ending.characters', "( \'-\', \'_\' )");
					result = false;
				} else if(value.charAt(0) === "_" || value.charAt(0) === "-") {
					classVal.class = "is-invalid";
					classVal.msg = getMessage('acst.message.ui.project.manage.warning.cant.used.starting.characters', "( \'-\', \'_\' )");
					result = false;
				} else {
					classVal.class = "";
					classVal.msg = "";
					result = true;
					if(checkProjecjKey) {
						var regex = /^[a-zA-Z0-9\_\-]{0,255}$/g
						if(!regex.test(value)) {
							classVal.class = "is-invalid";
							classVal.enableCheckingButton = true;
							classVal.msg = getMessage('acst.message.ui.project.manage.alert.invalid.projectkey');
							result = false;
						}
					}
				}*/
				classVal.class = "";
				classVal.msg = "";
				result = true;
			} else {
				classVal.class = "is-invalid";
				classVal.msg = "";
				result = false;
			}
			
			
			return result;
		},
		setProcessSysAndSweAllSelect : function(processGroup, checked) {
			var self = this;
			var process = self.prjInfo.processInfoList[processGroup];
			var isProcessCheck = (processGroup === "SYS" || processGroup === "SWE") ? true : false;
			// CheckBox 영역이 SYS, SWE 영역일 경우에만 모든 CheckBox 클릭 시 모두 True
			if(isProcessCheck) {
				for(var i=0; i<process.processList.length; i++) {
					process.processList[i].active = checked;
				}	
			}
		},
		preventCheckbox : function() {
			alertModalVue.selectAlert("warning", getMessage('acst.message.ui.project.manage.alert.selected.atleast.one.test.target'));
		},
		checkDate : function ( startDate, endDate ) {
			var self = this;
			var result = false;
			if(startDate != undefined && startDate != null && endDate != undefined && endDate != null) {
				
				var afterDate = self.getDate(new Date(startDate).getTime(), 4);
								
				if(new Date(startDate) > new Date(endDate)) {
					result = false;
				} else {
					if((new Date(endDate).getTime() - new Date(startDate).getTime()) < (new Date(afterDate).getTime() - new Date(startDate).getTime())) {
						result = true;
					} else {
						result = false;
					}					
				}
			} else {
				result = false;
			}
			
			if(result) {
				this.prjInfoClass.date.class = "";
				this.prjInfoClass.date.msg = "";
			} else {
				this.prjInfoClass.date.class = "is-invalid";
				this.prjInfoClass.date.msg = getMessage('acst.message.ui.project.manage.warning.set.incorrect.time');					
			}
			return result;
		},
		checkProcess : function() {
			var moreThanOne = false ;
			for (var key in this.prjInfo.processInfoList) {
				var selectProcess = false;
				for ( var i=0 ; i < this.prjInfo.processInfoList[key].processList.length; i++ ) {
					if(this.prjInfo.processInfoList[key].processList[i].active) {
						moreThanOne = true;
						selectProcess = true;
						break;
					}
				}
				
				//그룹 중에 한개 이상의 프로세스가 active 상태이면 버튼 활성화 아니면 버튼 비활성화 및 승인 기능 false
				if(!selectProcess) {
					this.prjInfo.processInfoList[key].approval = false;
					this.prjInfo.processInfoList[key].disabled = true;
				}else {
					this.prjInfo.processInfoList[key].disabled = false;
				}
			}		
			if(moreThanOne) {
				this.prjInfo.certifying.process = true; 
				this.prjInfoClass.process.msg = "";
			} else {
				this.prjInfo.certifying.process = false; 
				this.prjInfoClass.process.msg = getMessage('acst.message.ui.project.manage.warning.selected.atleast.one.process');
				alertModalVue.selectAlert("warning", this.prjInfoClass.process.msg);
			}
			
		},
		getTitle : function(group, process) {
			var ret = '';
			if(process == null || process ==""){
				ret = getDocumentMessage("acst.message.ui.processgroup." + group.toLowerCase() + ".title");
			} else {
				ret = getDocumentMessage("acst.message.ui.processgroup." + group.toLowerCase() + "." + process.replace("_", "").toLowerCase()+ ".title"); 
			}
			return ret;
		},
		//수정과 관련된 함수		
		getProjectInfo : function() {
			
			this.prjInfo = {
				certifying : {	//인증 여부
					projectKey : true,
					name : true,
					date : true,
					process : true
				},
				basic : {	//필수 정보
					projectId : projectSideBar.projectInfo.id,
					projectKey : projectSideBar.projectInfo.projectKey, 						//프로젝트 키, progress 계산에서 제외
					name : projectSideBar.projectInfo.name,								//차량명
					objective : projectSideBar.projectInfo.objective, 					//목표 CL
					startDate : this.getDate(projectSideBar.projectInfo.startDate),						//전체 일정 시작일
					endDate : this.getDate(projectSideBar.projectInfo.endDate),						//전체 일정 종료일
					subName : projectSideBar.projectInfo.subName,						//아이템
					chipset : projectSideBar.projectInfo.chipset,
					toolchain : projectSideBar.projectInfo.toolchain						
				},
				processInfoList : this.prjInfo.processInfoList,			
				state : projectSideBar.projectInfo.projectState,
			}
			this.scmInfo = {
					selectedType : projectSideBar.projectInfo.scmType,
					id : projectSideBar.projectInfo.scmID,
					password : projectSideBar.projectInfo.scmPW,
					url : projectSideBar.projectInfo.scmUrl,
					valid : false,
					checking : false
			}
		},
		getDate : function(times, laterTime) {
			
			var currentDate = new Date();
			
			if(times != undefined && times != null && !isNaN(times)) {
				currentDate = new Date(times)
			}

			var currentYear = currentDate.getFullYear();
			
			if(laterTime != undefined && laterTime != null && !isNaN(laterTime)) {
				currentYear += laterTime;
			}
			
			var currentMonth = currentDate.getMonth() + 1;
			var currentDay = currentDate.getDate();
			
		    if(currentMonth < 10){
		    	currentMonth = "0"+ currentMonth;
		    }
		    
		    if(currentDay < 10){
		    	currentDay = "0"+ currentDay;
		    }
			
			const defaultToday = currentYear + "-" + currentMonth + "-" + currentDay;	
			
			return defaultToday;
		},
		setApproval : function(group, value) { //작업 산출물 등록 요청 기능 활성화 로직
			/*var value = event.target.checked;*/
			for(var i=0;  i < this.prjInfo.processInfoList[group].processList.length; i++) {
				this.prjInfo.processInfoList[group].processList[i].approval = value;
			}
		},
		/*getDisabledApproval : function(group) {//작업 산출물 등록 요청 기능 disabled 할지 안할지 정함 - 프로세스가 하나도 사용중이지 않을 경우에는 작업 산출물 등록 요청 기능을 설정할 수 없음
			var disabled = true;
			for(var i=0;  i < this.prjInfo.processInfoList[group].length; i++) {
				if(this.prjInfo.processInfoList[group][i].active) { //하나라도 활성화 되어있다면 작업 산출물 등록 요청 기능 활성화 버튼 사용 가능
					disabled = false;
					break;
				}
			}
			return disabled;
		}*/
	}
});
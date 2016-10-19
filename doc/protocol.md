## 前后端函数协议

<font size = 5>

<table>
	<tr>
		<td>函数名</td>
		<td>功能描述</td>
		<td>函数所在文件</td>
		<td>参数列表</td>
		<td>返回值和类型</td>
		<td>GET / POST</td>
		<td>填写人</td>
		<td>完成反馈(后端填写)</td>
	</tr>
	 <td>search_student_by_name</td>
	 <td>根据姓名查找学生，返回部分信息</td>
	 <td>database/views.py</td>
	 <td>request(.POST['name']: 姓名)</td>
	 <td>类型：JsonResponse 包含匹配的学生的姓名(name)、性别(gender)、生源地(source)、学校(school)、身份证号(id_card) 注意key必须和括号内的内容相同</td>
	 <td>POST</td>       
	 <td>段清楠</td>        
	 <td>侯禺凡完成</td>
	 </tr>

	 <tr>
	 <td>remove_student_by_id</td>
	 <td>根据ID删除学生</td>
	 <td>database/views.py</td>
	 <td>request(.POST['id']: ID)</td>
	 <td>类型：JsonResponse （空字典）</td>
	 <td>POST</td>
	 <td>段清楠</td>
	 <td>侯禺凡完成</td>
	 </tr>

    <tr>
 		<td>student_list_all</td>
 		<td>返回所有学生的部分信息</td>
 		<td>database/views.py</td>
 		<td>request</td>
 		<td>类型：JsonResponse([{},{},{},...]) 包含所有学生的姓名(name)、性别(gender)、生源地(source)、学校(school)、身份证号(id_card) 注意key必须和括号内的内容相同</td>
 		<td>POST</td>
 		<td>段清楠</td>
 		<td>侯禺凡完成</td>
 	</tr>

	<tr>
		<td>profile</td>
		<td>查看、修改教师的信息</td>
		<td>teacher/views.py</td>
		<td>request</td>
		<td>类型：JsonResponse(dict)  dict = {'teacher_name': '', 'email': '', 'work_address': '', 'home_address': '', 'postcode': '',
                'homephone': '', 'phone': '', 'qqn': '', 'weichat': '', 'describe': '', }
                GET直接返回字典 POST返回JSON</td>
		<td>GET/POST</td>
		<td>白云仁</td>
		<td>李昊阳完成，目前有些信息比如邮编等尚未加入数据库，故暂时不能get和set，是否保留此字段后续讨论</td>
	</tr>
	
	<tr>
		<td>student_info_show</td>
		<td>通过传递student参数将学生信息显示在student_info.html中</td>
		<td>teacher/views.py</td>
		<td>request</td>
		<td>HttpResponese</td>
		<td>GET</td>
		<td>邵韵秋</td>
		<td>完成</td>
	</tr>
	
	<tr>
		<td>student_info_save</td>
		<td>保存表单中修改的学生信息并返回显示在student_info.html中</td>
		<td>teacher/views.py</td>
		<td>request</td>
		<td>HttpResponese</td>
		<td>post</td>
		<td>邵韵秋</td>
		<td> __尚未完成，无法获取account和id__ </td>
	</tr>
	
	<tr>
		<td>student_info_edit</td>
		<td>在student_info_edit.html中显示学生的信息，基本与student_info_show相同，但是增加了两个变量</td>
		<td>teacher/views.py</td>
		<td>request</td>
		<td>HttpResponse(需要映射student, province(中国所有省份）,nation(中国所有民族）,major(清华所有专业，以及一项“无”))</td>
		<td>post</td>
		<td>邵韵秋</td>
		<td>完成</td>
	</tr>

	<tr>
		<td>student_list_all</td>
		<td>显示志愿者可以看到的学生的信息</td>
		<td>volunteer/views.py</td>
		<td>request(.POST['id']: <volunteer_ID>)</td>
		<td>JsonResponse</td>
		<td>POST</td>
		<td>侯禺凡</td>
		<td>完成，某些字段如qq号，最后可能会删掉，所以未显示，其他信息可以显示</td>
	</tr>

	<tr>
		<td>profile</td>
		<td>显示、修改志愿者的个人信息（保存失败建议返回失败的字段）</td>
		<td>volunteer/views.py</td>
		<td>request</td>
		<td>JsonResponse</td>
		<td>POST和GET</td>
		<td>侯禺凡</td>
		<td>完成，可以显示。已经可以返回修改志愿者的失败字段，待前端显示字段定下来后即可加上去</td>
	</tr>

	<tr>
		<td>logincheck</td>
		<td>志愿者登录，需要向前端给出志愿者的ID</td>
		<td>login/views.py</td>
		<td>request</td>
		<td>HttpResponse和redirect('/volunteer')（已写好）</td>
		<td>POST</td>
		<td>侯禺凡</td>
		<td>完成并且已经和显示志愿者信息调通</td>
	</tr>
	
	</tr>
	 <td>search_volunteer_by_name</td>
	 <td>根据姓名查找志愿者，返回部分信息</td>
	 <td>database/views.py</td>
	 <td>request(.POST['name']: 姓名)</td>
	 <td>类型：JsonResponse 包含匹配的志愿者的姓名(name)、院系(department)、班级(class)、学号(student_id) 注意key必须和括号内的内容相同</td>
	 <td>POST</td>       
	 <td>段清楠</td>        
	 <td> 完成 </td>
	 </tr>

	 <tr>
	 <td>remove_volunteer_by_id</td>
	 <td>根据ID删除志愿者</td>
	 <td>database/views.py</td>
	 <td>request(.POST['id']: ID)</td>
	 <td>类型：JsonResponse （空字典）</td>
	 <td>POST</td>
	 <td>段清楠</td>
	 <td> 完成 </td>
	 </tr>

    <tr>
 		<td>volunteer_list_all</td>
 		<td>返回所有志愿者的部分信息</td>
 		<td>database/views.py</td>
 		<td>request</td>
 		<td>类型：JsonResponse([{},{},{},...]) 包含所有学生的姓名(name)、院系(department)、班级(class)、学号(student_id) 注意key必须和括号内的内容相同</td>
 		<td>POST</td>
 		<td>段清楠</td>
 		<td> 完成 </td>
 	</tr>
	
	<tr>
	 <td>add_student</td>
	 <td>自动生成学生注册码</td>
	 <td>database/views.py</td>
	 <td>request(.POST['num']: 添加的学生账户数量)</td>
	 <td>类型：JsonResponse ([{},{},{},...]) 包含新账号的注册码(code) 注意：后端请同时将注册码添加到数据库！</td>
	 <td>POST</td>
	 <td>段清楠</td>
	 <td>后端已经实现，但是前端页面暂时未完成所以没有测试正确性</td>
	 </tr>

	<tr>
	 <td>volunteer_search_student_by_name</td>
	 <td>根据姓名查找志愿者可见的学生</td>
	 <td>volunteer/views.py</td>
	 <td>request(POST['name']: 学生姓名)，志愿者id通过session获取</td>
	 <td>类型：JsonResponse</td>
	 <td>POST</td>
	 <td>侯禺凡</td>
	 <td> 完成 </td>
	 </tr>
	 
	 <tr>
	 <td>volunteer_info_edit</td>
	 <td>修改志愿者的信息</td>
		<td>teacher/views.py</td>
		<td>request</td>
		<td>类型：JsonResponse(dict)  dict = {
		'user_name' : '',
		'realName' : '',
		'idNumber' : '',
		'sex' : '',
		'nation' : '',
		'birth_year' : '',
		'birth_month' : '',
		'birth_date' : '',
		'department' : '',
		'class' : '',
		'phone' : '',
		'email' : '',
		'province' : '',
		'distribute' : '',
		'qqn' : '',
		'weichat' : '',
		'teacher' : '',
		'comment' : '',
	}
                GET直接返回字典 POST返回JSON</td>
		<td>GET/POST</td>
		<td>白云仁</td>
	 <td>   尚未完成 前端传过来的信息不全   </td>
	 </tr>
	<tr>
	<td>volunteer_info</td>
	 <td>查看志愿者的信息</td>
		<td>teacher/views.py</td>
		<td>request</td>
		<td>类型：JsonResponse(dict)  dict = {
		'user_name' : '',
		'realName' : '',
		'idNumber' : '',
		'sex' : '',
		'nation' : '',
		'birth_year' : '',
		'birth_month' : '',
		'birth_date' : '',
		'department' : '',
		'class' : '',
		'phone' : '',
		'email' : '',
		'province' : '',
		'distribute' : '',
		'qqn' : '',
		'weichat' : '',
		'teacher' : '',
		'comment' : '',
	}
                GET直接返回字典</td>
		<td>GET</td>
		<td>白云仁</td>
	 <td>  完成 </td>
	 </tr>
	 <tr>
	 <td>add_volunteer</td>
	 <td>添加志愿者账号</td>
	 <td>database/views.py</td>
	 <td>request(.POST['username']: 用户名  .POST['password']: 用户名)</td>
	 <td>类型：JsonResponse（用户名已存在则添加失败） 见样例 注意：后端请同时将账号添加到数据库！</td>
	 <td>POST</td>
	 <td>段清楠</td>
	 <td> 完成 </td>

	</tr>
		<tr>
		<td>student_info_show</td>
		<td>显示志愿者可见的学生详细信息（说明：已将老师端同样部分的代码移植过来，后端决定是否需要做修改；另外，后端还需要根据学生id和志愿者id判断这个GET请求是否有权限，没有权限则返回到上一页面）</td>
		<td>volunteer/views.py</td>
		<td>request(GET['stu_id'])</td>
		<td>HttpResponse</td>
		<td>GET</td>
		<td>侯禺凡</td>
		<td>h</td>
	</tr>

	 </tr>
		<tr>
		<td>a</td>
		<td>b</td>
		<td>c</td>
		<td>d</td>
		<td>e</td>
		<td>f</td>
		<td>g</td>
		<td>h</td>
	</tr>
</table>

### 备注：前七列由前端填写，目的是给后端提出需求，在后端实现功能前，前段应该搭好框架。后端实现后，会在表格最后一列给予反馈。

</font>
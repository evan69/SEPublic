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
	<tr>
		<td>search_student_by_name</td>
		<td>根据姓名查找学生，返回部分信息</td>
		<td>database/views.py</td>
		<td>request(.POST['name']: 姓名)</td>
		<td>类型：JsonResponse([{},{},{},...]) 包含匹配的学生的姓名(name)、性别(gender)、生源地(source)、学校(school)、身份证号(school) 注意key必须和括号内的内容相同</td>
		<td>POST</td>
		<td>段清楠</td>
		<td>8</td>
	</tr>
	<tr>
		<td>remove_student_by_id</td>
		<td>根据ID删除学生</td>
		<td>database/views.py</td>
		<td>request(.POST['id']: ID)</td>
		<td>类型：JsonResponse({}) （空字典）</td>
		<td>POST</td>
		<td>段清楠</td>
		<td>8</td>
	</tr>
	<tr>
		<td>student_list_all</td>
		<td>返回所有学生的部分信息</td>
		<td>database/views.py</td>
		<td>request</td>
		<td>类型：JsonResponse([{},{},{},...]) 包含所有学生的姓名(name)、性别(gender)、生源地(source)、学校(school)、身份证号(school) 注意key必须和括号内的内容相同</td>
		<td>POST</td>
		<td>段清楠</td>
		<td>8</td>
	</tr>
	<tr>
		<td>get_teacher_name_by_id</td>
		<td>返回指定ID对应的教师姓名</td>
		<td>database/views.py</td>
		<td>request(.POST['id']: ID)</td>
		<td>类型：JsonResponse({'name':姓名})</td>
		<td>POST</td>
		<td>段清楠</td>
		<td>8</td>
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
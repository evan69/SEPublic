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
		<td>1</td>
		<td>2</td>
		<td>3</td>
		<td>4</td>
		<td>5</td>
		<td>6</td>
		<td>7</td>
		<td>8</td>
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
		<td>h</td>
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
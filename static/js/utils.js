/**
javascript提交表单

	obj 		表单父容器
	action 		表单处理URL
	callback	处理完成回调

EXAMPLE:

	(1) 单一表单
	<form id="login-form">
		<input type="text" name="username" />
		<input type="password" name="password" />
		<input type="button" value="Submit" onclick="$submit('#login-form', '/login', mycallback)" />
	</form>
	<script>
		function mycallback(data,status){
			if(status=="success"){ alert("成功"); }
			else{ alert("失败"); }
		}
	</script>

	(2) 项目编辑表单
	<ul>
		<li id="category_1">
			<input type="text" name="title" />
			<input type="button" value="Submit" onclick="$submit(['category',1], '/edit', mycallback)" />
		</li>
		<!-- ... -->
	</ul>
	<script>
		function mycallback(pk,data,status){
			if(status=="success"){ alert("编辑成功 id:"+pk); }
			else{ alert("失败"); }
		}
	</script>
*/
function $submit (obj, action, callback) {
	$.post(action,$fetch(obj),function(data,status) {
		if((typeof obj)=="object"&&obj.hasOwnProperty("length")){ callback(obj[1], data, status); }
		else{ callback(data, status); }
	});
}

/**
提取表单数据

	obj 		表单父容器
	返回值		含有表单数据的js对象
*/
function $fetch (obj) {
	var form = null;
	switch(typeof obj){
		case "object": form = obj.hasOwnProperty("length") ? $($id(obj[0], obj[1])) : obj; break;
		case "string": form = $(obj); break;
	}
	var r={};
	$(form).find("input[name],textarea[name],select[name]").each(function(){ r[$(this).attr("name")]=$(this).val(); });
	return r;
}

/**
产生id选择器

	prefix 		前缀
	pk 			项目主码
	返回值		id选择器
*/
function $id (prefix, pk) {
	return "#"+prefix+"_"+pk;
}



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
		if(callback==undefined) return;
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
	r["jssubmittedmark"]="$submit 2014";
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


/**
get param in url

	name 		查询串的名字
*/
function getUrlParam(name) {
            var reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)");
            var r = window.location.search.substr(1).match(reg);  //匹配目标参数
            if (r != null) return unescape(r[2]); return null;
        }



/**
init customed modal.
usage: use this function in document ready function to create modals with id,then call $(modal_id).modal('show') in button action

	modal_id	to figure out the modal
	title 		info title
	content 	other information
	btn_one 	bottom left button text
	btn_another	bottom right button text
	fun_one 	function wehen click btn_one
	fun_another	function when click btn_another
*/
function createModal(modal_id,title,content,btn_one,btn_another,fun_one,fun_another){
	mod=$('#md_template').clone();
	mod.attr('id',modal_id);
	mod.find('#md_title').texttitle;
	mod.find('#md_content').text(content);
	mod.find('#btn_one').text(button_one);
	mod.find('#btn_another').text(button_another);
	mod.find('#btn_one').click(fun_one);
	mod.find('#btn_another').click(fun_another);
	mod.find('#md_main').modal('show');
	$('#md_template').after(mod);
}
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
		case "object": form = obj.hasOwnProperty("length") ? (obj.length>1?$($id(obj[0], obj[1])):obj[0]) : obj; break;
		case "string": form = $(obj); break;
	}
	var r={};
	$(form).find("input[name],textarea[name],select[name]").each(function(){ r[$(this).attr("name")]=$(this).val(); });
	r["jssubmittedmark"]="$submit 2014";
	return r;
}

/**
为django渲染的表单补充样式

	obj 		表单父容器
*/
function $djform (obj) {
	$(obj).find(".form-group label").addClass("col-sm-1 control-label");
	$(obj).find(".form-group input,textarea,select").addClass("form-control");
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
在浏览器控制台输出调试信息

	o 			任意对象
*/
function $dbg (o) {
	try{console.debug(o);}
	catch(e){}
}

/**
UI模块URL缓冲
*/
var mods={};

/**
加载UI模块

	id 			容器id
	url 		UI模块URL，重新加载时可以省略
*/
function $load (id, url) {
	if(url==undefined) url=mods[id];
	$.get(url, function (data,status) {
		if(status=="success"){ $("#"+id).html(data); }
	});
	mods[id]=url;
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
创建一个描述按钮的对象

	buttons 	描述按钮的字符串，例如"button"
				默认按钮前标记"*"，例如"*OK"
				提交表单按钮前标记"$"，例如"$Submit"
				危险操作标记"!"，例如"!Delete"
				需要其他样式标记"![0-9]"，感叹号后一位数字为样式下标，例如"!7Activate"
				标记不能混合使用
*/
function mk_button (button) {
	var style=0, s=false;
	if(button.match(/^!\d/)){ style=button[1]; button=button.slice(2); }
	else if(button.match(/^[*$!]/)){
		switch(button[0]){
			case "$": s=true;
			case "*": style=1; break;
			case "!": style=2; break;
		}
		button=button.slice(1);
	}
	return {
		text: button,
		style: [ // disclose available classes
			"btn-default", "btn-primary", "btn-danger",
			"btn-info", "btn-reverse", "btn-royal",
			"btn-social", "btn-success", "btn-transparent",
			"btn-warning"
		][style],
		submit: s
	};
}

/**
模态对话框，UI模板在 templates/mod/modal_dialogue.html

	title 		标题
	content 	内容(HTML)
	buttons 	按钮数组，例如["*Yes","No"]，默认按钮前标记"*"（参考），次序与渲染结果一致
	callback 	回调函数，例如function(r){}，形参r代表用户点击的按钮（所显示的文字）或表单内容
*/
function showModal (title, content, buttons, callback) {
	$.get("/mod/modal_dialogue", function (template, status) {
		if(status!="success"){ $dbg(template); $dbg(status); return; }
		var mod=$(template);
		$(mod).find('.modal-title').text(title);
		$(mod).find('.modal-body').html(content);
		eval($(mod).find('script').text()); // import append_button
		for(var i=0;i<buttons.length;i++) append_button(mk_button(buttons[i]));
		$(mod).modal('show');
		$("body").attr("style","");
	});
}

/**
常用对话框
*/
var Dialogue={
	alert: function(msg, title){
		if(title==undefined)title=msg;
		showModal(msg, msg, ["*确定"], function(r){});
	},
	confirm: function(msg, title, callback){
		showModal(title, msg, ["取消","*确定"], callback);
	},
	confirm_danger: function(msg, title, callback){
		showModal(title, msg, ["取消","!确定"], callback);
	},
	prompt: function(msg, title, callback) {
		showModal(title, 
		'<div>'+msg+'</div><div><input name="user_input"/></div>', 
		["取消","$确定"],
		function (r) { if(typeof r=="object")callback(r.user_input); });
	}
}

function test_showModal () {
	showModal("Alarm clock", "Get up!", ["Feeling lazy","*Dismiss"], $dbg);
}

function test_alert () {
	Dialogue.alert("Success");
}

function test_confirm () {
	Dialogue.confirm("Leaving so soon?","Quit",$dbg);
}

function test_prompt () {
	Dialogue.prompt("Time zone","Install Ubuntu",$dbg);
}

/**
高亮导航栏 li

	suffix 		id后缀

	li元素id命名规则 "#nav_li_"+suffix
*/
function select_nav (suffix) {
	$("#nav_li_"+suffix).addClass("active");
}

function get_public_key () {
	var z = "";
	$.ajax({ url: "/lpub.hex", async: false, success: function (r){ z=r; } });
	return z;
}

function encrypt(m){
	setMaxDigits(80);
	var key = new RSAKeyPair("10001", "", get_public_key());
	return encryptedString(key, m, RSAAPP.PKCS1Padding);
}

function ras_encryption(string){
	setMaxDigits(19);
	key = new RSAKeyPair(
 		"16d1507964604313b5121c52c1051115",  //e
 		"",  
 		"70a6c76c3631387e7eaca739f7f5cbe7"   //n
	);
	return encryptedString(key,string);
}

function ras_decryption(en_string){          //测试时用的解密函数，之后可删
	setMaxDigits(19);
	key = new RSAKeyPair(
 		"16d1507964604313b5121c52c1051115",  //e
 		"55afdcf744d8f5fe0c655fee417b3765",  //d
 		"70a6c76c3631387e7eaca739f7f5cbe7"   //n
	);
	return decryptedString(key,en_string);
}
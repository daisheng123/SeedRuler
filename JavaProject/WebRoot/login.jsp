<%@ page language="java" import="java.util.*" pageEncoding="UTF-8"%>

<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>login in</title>
<meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">
<meta http-equiv="Access-Control-Allow-Origin" content="*">
<meta name="viewport"
	content="width=device-width, initial-scale=1, maximum-scale=1">
<meta name="apple-mobile-web-app-status-bar-style" content="black">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="format-detection" content="telephone=no">
<link rel="stylesheet" href="resource/lib/layui-v2.5.5/css/layui.css"
	media="all">
<!--[if lt IE 9]> <script src="https://cdn.staticfile.org/html5shiv/r29/html5.min.js"></script> <script src="https://cdn.staticfile.org/respond.js/1.4.2/respond.min.js"></script> <![endif]-->
<style>
body {
	background-image: url("resource/images/bg.jpg");
	height: 100%;
	width: 100%;
}

#container {
	height: 100%;
	width: 100%;
}

input:-webkit-autofill {
	-webkit-box-shadow: inset 0 0 0 1000px #fff;
	background-color: transparent;
}

.admin-login-background {
	width: 300px;
	height: 300px;
	position: absolute;
	left: 50%;
	top: 40%;
	margin-left: -150px;
	margin-top: -100px;
}

.admin-header {
	text-align: center;
	margin-bottom: 20px;
	color: #ffffff;
	font-weight: bold;
	font-size: 40px
}

.admin-input {
	border-top-style: none;
	border-right-style: solid;
	border-bottom-style: solid;
	border-left-style: solid;
	height: 50px;
	width: 300px;
	padding-bottom: 0px;
}

.admin-input::-webkit-input-placeholder {
	color: #a78369
}

.layui-icon-username {
	color: #a78369 !important;
}

.layui-icon-username:hover {
	color: #9dadce !important;
}

.layui-icon-password {
	color: #a78369 !important;
}

.layui-icon-password:hover {
	color: #9dadce !important;
}

.admin-input-username {
	border-top-style: solid;
	border-radius: 10px 10px 0 0;
}

.admin-input-verify {
	border-radius: 0 0 10px 10px;
}

.admin-button {
	margin-top: 20px;
	font-weight: bold;
	font-size: 18px;
	width: 300px;
	height: 50px;
	border-radius: 5px;
	background-color: #a78369;
	border: 1px solid #d8b29f
}

.admin-icon {
	margin-left: 260px;
	margin-top: 10px;
	font-size: 30px;
}

i {
	position: absolute;
}

.admin-captcha {
	position: absolute;
	margin-left: 205px;
	margin-top: -40px;
}
</style>

</head>
<body>
	<div id="container layui-anim layui-anim-upbit">
		<div></div>
		<div class="admin-login-background">
			<div class="admin-header">
				<span>Intelligent grain prediction</span>
			</div>
			<form class="layui-form" action="">
				<div>
					<i class="layui-icon layui-icon-username admin-icon"></i> <input
						type="text" id="userName" name="username" placeholder="Please enter username"
						autocomplete="off"
						class="layui-input admin-input admin-input-username" value="">
				</div>
				<div>
					<i class="layui-icon layui-icon-password admin-icon"></i> <input
						type="password" id="password" name="password" placeholder="Please enter password"
						autocomplete="off" class="layui-input admin-input" value="">
				</div>
				<div>
					<input type="text" name="captcha" placeholder="Please enter verification code"
						autocomplete="off"
						class="layui-input admin-input admin-input-verify" value="">
					<img class="admin-captcha" width="90" height="30"
						src="resource/images/captcha.jpg">
				</div>
				<button class="layui-btn admin-button" lay-submit=""
					lay-filter="login">login in</button>
			</form>
		</div>
	</div>
	<script src="resource/lib/layui-v2.5.5/layui.js" charset="utf-8"></script>
	<script src="https://code.jquery.com/jquery-3.6.0.min.js"
		charset="utf-8"></script>
	<script type="text/javascript">
	layui.use([ 'form' ], function() {
		var form = layui.form,
			layer = layui.layer;

		// 登录过期的时候，跳出ifram框架
		if (top.location != self.location)
			top.location = self.location;

		// 进行登录操作
		form.on('submit(login)', function(data) {
			data = data.field;
			if(data.username!=''&&data.password != ''&&data.captcha != ''){
			  
			   $.ajax({
			    url :'user/login',
				type : 'post',
				dataType:'text',
				data : {
					userName:data.username,
					password:data.password,
				},
				success:function (result){
				console.log(result);
				if(result=="登录成功")
				   {
				      layer.msg('Login Successfully',function(){
				      window.location = 'index.jsp';
				});
				   return false;
				}
				else
				    {
				       layer.msg('Login Failed',function(){window.location = 'login.jsp';});
				       return false;
				    }
				
				},
				error:function(){
				console.error('Data load failed');
				}
			});
			console.log(data);
			return false;
			}
			
			if (data.username == '') {
				layer.msg('The username cannot be empty');
				return false;
			}
			if (data.password == '') {
				layer.msg('The password cannot be empty');
				return false;
			}
			if (data.captcha == '') {
				layer.msg('The verification code cannot be empty');
				return false;
			}
			
			
		
	});
	});
	/*function login(){
	    $.ajax({
			    url :'/user/login',
				type : 'post',
				dataType : 'json',
				data : {
					userName:$("userName").attr("id"),
					password:$("password").attr("id"),
				},
				success:function (data){
				if(data=="登录成功")
				   {
				      console.log(data)
				      layer.msg('登录成功',function(){
				      window.location = 'index.jsp';
				});
				}
				else
				    {
				       layer.msg('登录失败',function(){window.location = 'login.jsp';});
				       return false;
				       }
				
				},
				error:function(data){
				console.error('数据加载失败');
				}
			});
	}	*/
				
	
</script>
</body>
</html>
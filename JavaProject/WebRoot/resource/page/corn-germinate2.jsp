<%@ page language="java" import="java.util.*" pageEncoding="UTF-8"%>

<%
	String path = request.getContextPath();
	String basePath = request.getScheme() + "://" + request.getServerName() + ":" + request.getServerPort()
			+ path + "/";
%>
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html>
<head>
<base href="<%=basePath%>">

<title>My JSP 'corn_phenotype.jsp' starting page</title>


<meta http-equiv="pragma" content="no-cache">
<meta http-equiv="cache-control" content="no-cache">
<meta http-equiv="expires" content="0">
<meta http-equiv="keywords" content="keyword1,keyword2,keyword3">
<meta http-equiv="description" content="This is my page">
<meta http-equiv="Content-Security-Policy" content="upgrade-insecure-requests">
<!--
	<link rel="stylesheet" type="text/css" href="styles.css">
	-->
<script>
	layui.use([ 'form' ], function() {
		var form = layui.form;
		form.render(); // 渲染表单组件
	});
</script>
<style>
.top-panel {
	border: 1px solid #eceff9;
	border-radius: 5px;
	text-align: center;
}

.top-panel>.layui-card-body {
	height: 60px;
}

.top-panel-number {
	line-height: 60px;
	font-size: 30px;
	border-right: 1px solid #eceff9;
}

.top-panel-tips {
	line-height: 30px;
	font-size: 12px
}

#camera-preview video {
	position: fixed;
	z-index: 9999;
	left: 50%;
	transform: translateX(-50%);
}

#loadedImage {
	width: 400px;
	height: 300px;
	display: none;
}
/*.layui-unselect{
 display:none;
}*/
.layuimini-main1 {
	margin: 10px 10px 10px 10px;
}
#echarts-records {
	position: relative;
	overflow: hidden;
}

#resultimage {
	width: 100%;
	height: auto;
	cursor: zoom-in; /* 设置光标样式为放大镜 */
	transition: transform 0.3s ease; /* 添加过渡效果 */
}

#echarts-records.zoomed {
	cursor: zoom-out; /* 设置光标样式为缩小镜 */
}
.animation {
  width: 100vw;
  height: 100vh;
  background: rgba(255, 255, 255);
  --amount: 20;
  display:none;
  z-index:100;
}
.animation.active {
  display: flex; /* 点击测量按钮后显示动画 */
}
.animation span {
  width: 8vmin;
  height: 8vmin;
  border-radius: 4vmin;
  backface-visibility: hidden;
  position: absolute;
  animation-name: move;
  animation-timing-function: cubic-bezier(0.4, 0, 1, 0.8);
  animation-iteration-count: infinite;
  animation-duration: 3s;
  top: calc(50% - 4vmin);
  left: 50%;
  transform-origin: -4vmin center;
  opacity: 0;
}

.animation span:nth-child(1) {
  background: #C5F0A4;
  animation-delay: -0s;
}

.animation span:nth-child(2) {
  background: #35B0AB;
  animation-delay: -0.5s;
}

.animation span:nth-child(3) {
  background: #226B80;
  animation-delay: -1s;
}

.animation span:nth-child(4) {
  background: #C5F0A4;
  animation-delay: -1.5s;
}

.animation span:nth-child(5) {
  background: #35B0AB;
  animation-delay: -2s;
}

.animation span:nth-child(6) {
  background: #226B80;
  animation-delay: -2.5s;
}

@keyframes move {
  0% {
    transform: scale(1) rotate(0deg) translate3d(0, 0, 1px);
  }
  30% {
    opacity: 1;
  }
  100% {
    z-index: 10;
    transform: scale(0) rotate(360deg) translate3d(0, 0, 1px);
  }
}
</style>
</head>

<body>
<div class="animation">
		<span></span> <span></span> <span></span> <span></span> <span></span>
		<span></span>
	</div>
	<div id="big">
<div style="display:none" id="measureSelect">IP</div>
	<div style=" display:flex;padding:10px">
	 <p  style="display:flex;padding-top: 10px;padding-left: 10px;padding-bottom: 10px;">Set germination threshold：</p><input id="range" type="range" min="0.1" max="0.9" value="0.4"step="0.1" oninput="change()" onchange="change()">
		<span id="value" style="padding:15px">0.4</span>
		<script type='text/javascript'>  
			function change() {
  				var value = document.getElementById('range').value ;
  				document.getElementById('value').innerHTML = value;
			}
		</script>
		<form class="layui-form" action="" method="post"
			enctype="multipart/form-data">
			<div class="layui-upload" style="display:flex;">
				<input type="file" name="files" id="batchInput" style="display:none"
					multiple>
				<button type="button" class="layui-btn layui-btn-normal" lay-submit
					lay-filter="upload" id="batch">Batch upload</button>
				<!--  <button type="button" class="layui-btn layui-btn-normal"
					id="uploadButton">Picture upload</button>-->
				<input type="file" name="file" id="fileInput" style="display:none">
				<!--  <button type="button" lay-submit lay-filter="submit"
					class=" layui-btn" id="measureButton">算法选择</button>-->
				<div style="margin:0 10px; display:flex;">
					<!--<select lay-filter="submit" id="measureSelect"
						style="width: 200px; outline: none; text-indent: 5px;background: #ffffff;">
						<option value="" class="layui-select-tips layui-this">select
							algorithm</option>
						<option value="machine learning">machine learning</option>
						<option value="deep learning">deep learning</option>
					</select> -->

					<button type="button" lay-submit lay-filter="submit"
						class=" layui-btn " id="measureButton">Run</button>
				</div>
		</form>
	</div>
	<div style="width:570px;margin-left:13%">
		<div class="layui-row">
			<div class="layui-col-md3">
				<div id="camera-preview"
					style="width: 100%; height: auto;margin-top:50px"></div>
			</div>
			<div class="layui-col-md">
				<!--  <button id="start-camera" class="layui-btn layui-btn-primary">Open
					camera</button>-->
				<button id="open-usb-camera" class="layui-btn layui-btn-normal">Open
					camera</button>
				<button id="stop-camera" class="layui-btn layui-btn-normal">Close
					camera</button>
				<button id="take-photo" class="layui-btn ">Photograph</button>
			</div>
		</div>
	</div>
</div>

	<div id="loadedImage">
		<img id="uploadedImage"
			style="width:100%;height:100%;margin-left: 500px;" src="">
	</div>
	<div class="layuimini-main1" style="margin-top:-15px">
		<div class="layui-row layui-col-space15">

			<div class="layui-col-xs12 layui-col-md12">
				<div class="layui-card top-panel">
					<div class="layui-card-header" style="font-size: 25px">Grain
						germination</div>
					<div class="layui-card-body">
						<div class="layui-row layui-col-space5">
							<div id="germinateCount"
								class="layui-col-xs3 layui-col-md3 top-panel-tips">
								Number of germinated grains <br> <a
									style="color: #1aa094;font-size: 20px">0</a>
							</div>
							<div id="nogerminateCount"
								class="layui-col-xs3 layui-col-md3 top-panel-tips">
								Number of ungerminated grains <br> <a
									style="color: #bd3004;font-size: 20px">0</a><br>
							</div>
							<div id="grainCount"
								class="layui-col-xs3 layui-col-md3 top-panel-tips">
								Total number of grains <br> <a
									style="color: #1aa094;font-size: 20px">0</a><br>
							</div>
							<div id="germinateRate"
								class="layui-col-xs3 layui-col-md3 top-panel-tips">
								Germinate rate <br> <a
									style="color: #1aa094;font-size: 20px">0.00</a><br>
							</div>
						</div>
					</div>
				</div>
			</div>

			<!--  <div class="layui-col-xs12 layui-col-md6">
				<div class="layui-card top-panel">
					<div class="layui-card-header">谷粒粒高</div>
					<div class="layui-card-body">
						<div class="layui-row layui-col-space5">
							<div id="max_value_height"
								class="layui-col-xs3 layui-col-md3 top-panel-tips">
								最大值 <br> <a style="color: #1aa094;font-size: 20px">0.00</a>
							</div>
							<div id="min_value_height"
								class="layui-col-xs3 layui-col-md3 top-panel-tips">
								最小值 <br> <a style="color: #bd3004;font-size: 20px">0.00</a><br>
							</div>
							<div id="average_value_height"
								class="layui-col-xs3 layui-col-md3 top-panel-tips">
								均值 <br> <a style="color: #1aa094;font-size: 20px">0.00</a><br>
							</div>
							<div id="SD_value_height"
								class="layui-col-xs3 layui-col-md3 top-panel-tips">
								标准差 <br> <a style="color: #1aa094;font-size: 20px">0.00</a><br>
							</div>
						</div>
					</div>
				</div>
			</div>
		</div>-->

			<div class="layui-row layui-col-space15">
				<div id="result" class="layui-col-xs12 layui-col-md4">
					<div id="echarts-records"
						style="background-color:#ffffff;min-height:400px;padding: 10px;height:400px"><img id="resultimage" style="max-width: 100%; max-height: 100%;"
						src="resource/images/1.jpg"></div>
				</div>
				<div id="echarts" class="layui-col-xs12 layui-col-md8">
					<div id="echarts-pies"
						style="background-color:#ffffff;height:400px;padding: 10px;"></div>
				</div>
			</div>
			<div class="layui-row layui-col-space15">
				<div class="layui-col-xs12 layui-col-md12">
			<div id="echarts-map"
				style="background-color:#ffffff;height:440px;padding: 10px;overflow-y: auto;display:none">
				<table id="data-table" class="layui-table" style="font-size: 18px">
					<colgroup>
						<col width="200">
						<col width="200">
						<col width="200">
						<col width="200">
						<col width="200">
					</colgroup>
					<thead>
						<tr>
							<th style="font-size: 18px">Image Name</th>
							<th style="font-size: 18px">Germinate Number</th>
							<th style="font-size: 18px">Nogerminate Number</th>
							<th style="font-size: 18px">Total Number</th>
							<th style="font-size: 18px">GerminateRate</th>
						</tr>
					</thead>
					<tbody></tbody>
				</table>
			</div>
		</div>
		</div>
		</div>
			<script type="text/javascript">
			function changeImage(change,length,imagePath) 
		{
           var image = document.getElementById("resultimage");
           image.src = imagePath[parseInt(change)%parseInt(length)];
         }
			
				/**
				 * 图片上传
				 */
				/*layui.use([ 'jquery', 'form' ], function() {
					var $ = layui.jquery;
					var form = layui.form;
				
					//监听表单提交  
					form.on('submit(uploadForm)', function(data) {
						//阻止表单跳转  
						data.preventDefault();
						console.log(1)
						//获取文件数据  
						var file = $('#uploadFile')[0].files[0];
				
						//创建FormData对象  
						var formData = new FormData();
						formData.append('image', file);
				
						//发送Ajax请求  
						$.ajax({
							url : 'image/upload', //替换为您的服务器URL  
							type : 'POST',
							data : formData,
							processData : false, //告诉jQuery不要去处理发送的数据  
							contentType : false, //告诉jQuery不要去设置Content-Type请求头  
							enctype : 'multipart/form-data',
							success : function(response) {
								//处理服务器响应  
								console.log(response);
							},
							error : function(xhr, status, error) {
								//处理请求错误  
								console.log(status, error);
							}
						});
					});
				});*/
				/** 拍照
				*/
				layui.use([ 'layer', 'jquery' ], function() {
					var layer = layui.layer;
					var $ = layui.jquery;
			
					var videoElement = document.createElement('video');
					videoElement.autoplay = true;
					//var startButton = document.getElementById('start-camera');
					var stopButton = document.getElementById('stop-camera');
					var takePhotoButton = document.getElementById('take-photo');
					var openUsbCameraButton = document.getElementById('open-usb-camera');
					var mediaStream;
			
					/*startButton.addEventListener('click', function() {
						navigator.mediaDevices.getUserMedia({
							video : true
						})
							.then(function(stream) {
								mediaStream = stream;
								videoElement.srcObject = stream;
								document.getElementById('camera-preview').appendChild(videoElement);
							})
							.catch(function(error) {
								console.log('The camera is not accessible：', error);
							});
					});*/
					openUsbCameraButton.addEventListener('click', function() {
						navigator.mediaDevices.enumerateDevices()
							.then(function(devices) {
								var deviceIds = [];
								devices.forEach(function(device) {
									if (device.kind === 'videoinput') {
										deviceIds.push(device.deviceId);
									}
								});
								if (deviceIds.length > 0) {
									var selectedDeviceId = deviceIds[0]; // 这里选择第一个设备
			
									var constraints = {
										video : {
											deviceId : {
												exact : selectedDeviceId
											}
										}
									};
									navigator.mediaDevices.getUserMedia(constraints)
										.then(function(stream) {
											mediaStream = stream;
											videoElement.srcObject = stream;
											document.getElementById('camera-preview').appendChild(videoElement);
										})
										.catch(function(error) {
											console.log('The camera is not accessible：', error);
										});
								} else {
									console.log('No available camera devices were found');
								}
							})
							.catch(function(error) {
								console.log('Unable to get the device list：', error);
							});
			
			
					});
			
					stopButton.addEventListener('click', function() {
						if (mediaStream) {
							mediaStream.getTracks().forEach(function(track) {
								track.stop();
							});
							videoElement.srcObject = null;
							document.getElementById('camera-preview').removeChild(videoElement);
						}
					});
			
					takePhotoButton.addEventListener('click', function() {
						if (mediaStream) {
							var canvasElement = document.createElement('canvas');
							canvasElement.width = videoElement.videoWidth;
							canvasElement.height = videoElement.videoHeight;
							var canvasContext = canvasElement.getContext('2d');
							canvasContext.drawImage(videoElement, 0, 0, canvasElement.width, canvasElement.height);
			
							var photoDataUrl = canvasElement.toDataURL('image/jpeg');
							layer.open({
								type : 1,
								title : 'Captured image',
								content : '<img src="' + photoDataUrl + '" style="max-width: 100%;"> <div style="text-align:right;"><button class="layui-btn" id="save" >Save</button></div>',
								area : [ '500px', '450px' ],
								success : function(layero, index) {
									var saveBtn = layero.find('#save');
									saveBtn.on('click', function() {
										if (mediaStream) {
											var canvasElement = document.createElement('canvas');
											canvasElement.width = videoElement.videoWidth;
											canvasElement.height = videoElement.videoHeight;
											var canvasContext = canvasElement.getContext('2d');
											canvasContext.drawImage(videoElement, 0, 0, canvasElement.width, canvasElement.height);
			
											var photoDataUrl = canvasElement.toDataURL('image/jpeg');
											//var photoBlob = dataURLtoBlob(photoDataUrl);
											var formData = new FormData();
											formData.append('dataUrl', photoDataUrl);
			
											$.ajax({
												url : 'image/save', // 后端接口地址
												type : 'POST',
												data : formData,
												processData : false,
												contentType : false,
												success : function(response) {
													layer.msg('The photo was saved successfully', {
														icon : 1
													});
												},
												error : function(error) {
													layer.msg('Photo saving failed', {
														icon : 2
													});
												}
											});
										}
										console.log('Clicked the Save button');
									});
								}
							});
						}
						console.log(photoDataUrl)
					});
					/*var saveButton = document.getElementById('save');
					saveButton.addEventListener('click', function() {
						if (mediaStream) {
							var canvasElement = document.createElement('canvas');
							canvasElement.width = videoElement.videoWidth;
							canvasElement.height = videoElement.videoHeight;
							var canvasContext = canvasElement.getContext('2d');
							canvasContext.drawImage(videoElement, 0, 0, canvasElement.width, canvasElement.height);
					
							var photoDataUrl = canvasElement.toDataURL('image/jpeg');
							var photoBlob = dataURLtoBlob(photoDataUrl);
							var formData = new FormData();
							formData.append('file', photoBlob);
					
							$.ajax({
								url : 'image/save', // 后端接口地址
								type : 'POST',
								data : formData,
								processData : false,
								contentType : false,
								success : function(response) {
									console.log('照片保存成功！');
								},
								error : function(error) {
									console.log('照片保存失败：', error);
								}
							});
						}
					  });*/
			
					function dataURLtoBlob(dataURL) {
						var byteString = atob(dataURL.split(',')[1]);
						var mimeString = dataURL.split(',')[0].split(':')[1].split(';')[0];
						var ab = new ArrayBuffer(byteString.length);
						var ia = new Uint8Array(ab);
						for (var i = 0; i < byteString.length; i++) {
							ia[i] = byteString.charCodeAt(i);
						}
						return new Blob([ ab ], {
							type : mimeString
						});
					}
				});
				layui.use([ 'form', 'upload', 'layer', 'echarts' ], function() {
					var form = layui.form;
					var upload = layui.upload;
					var layer = layui.layer;
					var echarts = layui.echarts;
			
					// 文件上传按钮的点击事件
					/*document.getElementById("uploadButton").onclick = function() {
						document.getElementById("fileInput").click();
					};*/
					// 创建一个上传实例
					var uploadInst = upload.render({
						elem : '#fileInput', // 绑定文件上传的按钮
						url : 'image/upload', // 替换为您的服务器上传接口
						done : function(res) {
							// 上传完成的回调函数
							console.log(res.url);
							// 根据服务器返回的数据进行相应的处理
			
							document.getElementById("uploadedImage").src = res.url;
							if (document.getElementById("uploadedImage").src != "") {
								document.getElementById("loadedImage").style.display = "none";
							}
							layer.msg('The image has been uploaded successfully', {
								icon : 1
							});
						},
						error : function() {
							layer.msg('Image upload failed', {
								icon : 2
							});
						}
					});
					//参数测量
					// 监听参数测量按钮的点击事件
					document.getElementById("measureButton").onclick = function() {
					     document.getElementById("big").style.display = "none";
			             var animation = document.querySelector('.animation');
				         animation.classList.add('active');
						// 获取图片的src
						var imageSrc = document.getElementById("uploadedImage").src;
						var algorithm = document.getElementById("measureSelect").textContent;
						var threshold =document.getElementById('range').value;
						// 创建一个表单数据对象
						var formData = new FormData();
						formData.append("imageSrc", imageSrc);
						formData.append("algorithm", algorithm);
						formData.append("threshold", threshold);
						console.log(threshold)
						// 发送POST请求给控制器
						var xhr = new XMLHttpRequest();
						xhr.open("POST", "image/germinatemeasure_ImageProcess", true);
						xhr.onreadystatechange = function() {
							if (xhr.readyState === 4 && xhr.status === 200) {
								// 请求成功的处理逻辑
								var response = JSON.parse(xhr.responseText);
								console.log(response);
								if (response.status == "success") {
									var animationElement = document.querySelector('.animation');
                                    animationElement.classList.remove('active');
                                    document.getElementById("big").style.display = "block";
									document.getElementById("germinateCount").querySelector("a").innerText = response.germinateCount.toFixed(0);
									document.getElementById("nogerminateCount").querySelector("a").innerText = response.nogerminateCount.toFixed(0);
									document.getElementById("grainCount").querySelector("a").innerText = response.grainCount.toFixed(0);
									document.getElementById("germinateRate").querySelector("a").innerText = response.germinateRate.toFixed(3);
			
									//跟新结果图
									var change = 0;
									document.getElementById("resultimage").src = response.imagePath[change];
									document.getElementById("result").style.display = "block";
									document.getElementById("echarts").className = "layui-col-xs12 layui-col-md8";
									var echartsDataset = document.getElementById('echarts-records');
									
							var resultImage = document.getElementById('resultimage');
							var scaleFactor = 0.05; // 设置缩放因子
							var throttleTimeout = null; // 节流的超时标识
	
							function handleMouseWheel(event) {
								event.preventDefault(); // 阻止滚轮默认行为
	
								if (throttleTimeout) return; // 如果节流超时标识已存在，则说明事件已经在执行中
	
								var zoomDelta = event.deltaY * -scaleFactor;
								var scale = 1 + zoomDelta;
	
								var rect = resultImage.getBoundingClientRect();
								var mouseX = event.clientX - rect.left;
								var mouseY = event.clientY - rect.top;
	
								var transformOriginX = (mouseX / rect.width) * 100 + '%';
								var transformOriginY = (mouseY / rect.height) * 100 + '%';
	
								resultImage.style.transformOrigin = transformOriginX + ' ' + transformOriginY;
								resultImage.style.transform = 'scale(' + scale + ')';
	
								throttleTimeout = setTimeout(function() {
									throttleTimeout = null; // 清除节流的超时标识
								}, 100); // 设置节流的时间间隔（单位：毫秒）
							}
	
							echartsDataset.addEventListener('wheel', handleMouseWheel, {
								passive : false
							});
								
								
									
									//萌发率
									var echartsPies = echarts.init(document.getElementById('echarts-pies'), 'walden');
									optionPies.series[0].data[0].value=response.germinateRate.toFixed(3);
									
									echartsPies.setOption(optionPies);
			
			
									//点击切换图片
									var image = document.getElementById("resultimage");
									image.addEventListener("click", function() {
										change++;
										changeImage(change, response.imagePath.length, response.imagePath);
									});
			
			
									//跟新数据
									var tbody = document.querySelector("#data-table tbody");
									for (var i = 0; i < response.CornGerminateList.length; i++) {
										var row = document.createElement("tr");
										for (var j = 0; j < 5; j++) {
											var cell = document.createElement("td");
											if (j % 5 == 0) {
												cell.textContent = response.CornGerminateList[i].imageName;
											}
											if (j % 5 == 1) {
												cell.textContent = Number(response.CornGerminateList[i].germinationCount).toFixed(3);
											}
											if (j % 5 == 2) {
												cell.textContent = Number(response.CornGerminateList[i].nogerminationCount).toFixed(3);
											}
											if (j % 5 == 3) {
												cell.textContent = Number(response.CornGerminateList[i].sumCount).toFixed(3);
											}
											if (j % 5 == 4) {
												cell.textContent = Number(response.CornGerminateList[i].germinationRate).toFixed(3);
											}
											row.appendChild(cell);
										}
										tbody.appendChild(row);
									}
									document.getElementById("echarts-map").style.display = "block";
			
									}
							}
						};
						xhr.send(formData);
					}
					
				});
			
				layui.use([ 'form', 'upload', 'layer' ], function() {
					var form = layui.form;
					var upload = layui.upload;
					var layer = layui.layer;
					var $ = layui.jquery;
			
					// 批量上传按钮的点击事件
					document.getElementById("batch").onclick = function() {
						document.getElementById("batchInput").click();
					};
					// 绑定文件选择事件
					document.getElementById("batchInput").addEventListener("change", function(event) {
						// 获取选择的文件列表
						var files = event.target.files;
						// 创建一个 FormData 对象来存储文件数据
						var formData = new FormData();
						// 将选择的文件添加到 FormData 对象中
						for (var i = 0; i < files.length; i++) {
							formData.append('files', files[i]);
						}
						// 使用 AJAX 请求将文件数据传递给后端
						$.ajax({
							url : 'image/batchUpload', // 替换为您的后端接口地址
							type : 'POST',
							data : formData,
							processData : false,
							contentType : false,
							success : function(response) {
								// 处理上传成功后的逻辑
								console.log(response.imagePaths);
								var url;
								/*for (var i = 0; i < response.imagePaths.length; i++) {
									url = response.imagePaths[i]
								}*/
								document.getElementById("uploadedImage").src = response.imagePaths;
								if (document.getElementById("uploadedImage").src != "") {
									document.getElementById("loadedImage").style.display = "none";
								}
								layer.msg('Upload successfully', {
									icon : 1
								});
							},
							error : function() {
								// 处理上传失败后的逻辑
								layer.msg('Upload Failed', {
									icon : 2
								});
							}
						});
					});
				});
				layui.use([ 'layer', 'echarts' ], function() {
					var $ = layui.jquery,
						layer = layui.layer,
						echarts = layui.echarts;
			
					/**
					 * 报表功能
					 */
					/* echartsRecords = echarts.init(document.getElementById('echarts-records'), 'walden');
					 optionRecords = {
						title : {
							text : 'GerminateRate'
						},
						tooltip : {
							trigger : 'axis',
							axisPointer : {
								type : 'cross',
								label : {
									backgroundColor : '#6a7985'
								}
							}
						},
						legend : {
							data : [ 'GerminateRate' ]
						},
						toolbox : {
							feature : {
								saveAsImage : {}
							}
						},
						grid : {
							left : '3%',
							right : '4%',
							bottom : '3%',
							containLabel : true
						},
						xAxis : [
							{
								type : 'category',
								boundaryGap : false,
								data : [ '第一次', ' 第二次', '第三次', '第四次', '第五次', '第六次' ]
							}
						],
						yAxis : [
							{
								type : 'value'
							}
						],
						series : [
							{
								name : 'GerminateRate',
								type : 'line',
								stack : '总量',
								areaStyle : {},
								data : [ 120, 132, 101, 134, 90, 230, 210 ]
							},
							{
								name : '2',
								type : 'line',
								areaStyle : {},
								data : [ 220, 182, 191, 234, 290, 330, 310 ]
							},
							{
								name : '3',
								type : 'line',
								stack : '总量',
								areaStyle : {},
								data : [ 150, 232, 201, 154, 190, 330, 410 ]
							},
							{
								name : '4',
								type : 'line',
								stack : '总量',
								areaStyle : {},
								data : [ 320, 332, 301, 334, 390, 330, 320 ]
							},
							{
								name : '5',
								type : 'line',
								stack : '总量',
								label : {
									normal : {
										show : true,
										position : 'top'
									}
								},
								areaStyle : {},
								data : [ 820, 932, 901, 934, 1290, 1330, 1320 ]
							}
						]
					};
					echartsRecords.setOption(optionRecords);*/
			
			
					/**
					 * 玫瑰图表
					 */
					var echartsPies = echarts.init(document.getElementById('echarts-pies'), 'walden');
					 optionPies = {
					title : {
							text : 'Grain',
							left : 'center',
							
						},
						series : [
							{
								type : 'gauge',
								startAngle : 180,
								endAngle : 0,
								center : [ '50%', '75%' ],
								radius : '90%',
								min : 0,
								max : 1,
								splitNumber : 8,
								axisLine : {
									lineStyle : {
										width : 6,
										color : [
											[ 0.25, '#FF6E76' ],
											[ 0.5, '#FDDD60' ],
											[ 0.75, '#58D9F9' ],
											[ 1, '#7CFFB2' ]
										]
									}
								},
								pointer : {
									icon : 'path://M12.8,0.7l12,40.1H0.7L12.8,0.7z',
									length : '12%',
									width : 20,
									offsetCenter : [ '0', '-60%' ],
									itemStyle : {
										color : 'auto'
									}
								},
								axisTick : {
									length : 12,
									lineStyle : {
										color : 'auto',
										width : 2
									}
								},
								splitLine : {
									length : 20,
									lineStyle : {
										color : 'auto',
										width : 5
									}
								},
								axisLabel : {
									color : '#464646',
									fontSize : 20,
									distance : -60,
									rotate : 'tangential',
									formatter : function(value) {
										if (value === 1) {
											return '100%';
										} else if (value === 0.75) {
											return '75%';
										} else if (value === 0.5) {
											return '50%';
										} else if (value === 0.25) {
											return '25%';
										}
										else if(value==0){
										return '0%'
										}
										return '';
									}
								},
								title : {
									offsetCenter : [ 0, '-10%' ],
									fontSize : 20
								},
								detail : {
									fontSize : 30,
									offsetCenter : [ 0, '-35%' ],
									valueAnimation : true,
									formatter : function(value) {
										return Math.round(value * 100) + '';
									},
									color : 'inherit'
								},
								data : [
									{
										value : 0.7,
										name : 'Germinate Rate'
									}
								]
							}
						]
					};
					echartsPies.setOption(optionPies);
					/*var optionPies = {
						title : {
							text : 'proportion',
							left : 'center'
						},
						tooltip : {
							trigger : 'item',
							formatter : '{a} <br/>{b} : {c} ({d}%)'
						},
						legend : {
							orient : 'vertical',
							left : 'left',
							data : [ 'germinate', 'nogerminate' ]
						},
						series : [
							{
								name : 'Proportional distribution',
								type : 'pie',
								radius : '55%',
								center : [ '50%', '60%' ],
								roseType : 'radius',
								data : [
									{
										value : 36,
										name : 'germinate'
									},
									{
										value : 4,
										name : 'nogerminate'
									}
								],
								emphasis : {
									itemStyle : {
										shadowBlur : 10,
										shadowOffsetX : 0,
										shadowColor : 'rgba(0, 0, 0, 0.5)'
									}
								}
							}
						]
					};
						
					*/
			
			
					/**
					 * 柱状图
					 */
					var echartsDataset = echarts.init(document.getElementById('echarts-dataset'), 'walden');
			
					var optionDataset = {
						legend : {},
						tooltip : {},
						dataset : {
							dimensions : [ 'product', '2015', '2016', '2017' ],
							source : [
								{
									product : 'Matcha Latte',
									'2015' : 43.3,
									'2016' : 85.8,
									'2017' : 93.7
								},
								{
									product : 'Milk Tea',
									'2015' : 83.1,
									'2016' : 73.4,
									'2017' : 55.1
								},
								{
									product : 'Cheese Cocoa',
									'2015' : 86.4,
									'2016' : 65.2,
									'2017' : 82.5
								},
								{
									product : 'Walnut Brownie',
									'2015' : 72.4,
									'2016' : 53.9,
									'2017' : 39.1
								}
							]
						},
						xAxis : {
							type : 'category'
						},
						yAxis : {},
						// Declare several bar series, each will be mapped
						// to a column of dataset.source by default.
						series : [
							{
								type : 'bar'
							},
							{
								type : 'bar'
							},
							{
								type : 'bar'
							}
						]
					};
			
					echartsDataset.setOption(optionDataset);
			
			
					/**
					 * 中国地图
					 */
					//var echartsMap = echarts.init(document.getElementById('echarts-map'), 'walden');
			
					/**
							var optionMap = {
								legend : {},
								tooltip : {
									trigger : 'axis',
									showContent : false
								},
								dataset : {
									source : [
										[ 'product', '2012', '2013', '2014', '2015', '2016', '2017' ],
										[ 'Matcha Latte', 41.1, 30.4, 65.1, 53.3, 83.8, 98.7 ],
										[ 'Milk Tea', 86.5, 92.1, 85.7, 83.1, 73.4, 55.1 ],
										[ 'Cheese Cocoa', 24.1, 67.2, 79.5, 86.4, 65.2, 82.5 ],
										[ 'Walnut Brownie', 55.2, 67.1, 69.2, 72.4, 53.9, 39.1 ]
									]
								},
								xAxis : {
									type : 'category'
								},
								yAxis : {
									gridIndex : 0
								},
								grid : {
									top : '55%'
								},
								series : [
									{
										type : 'line',
										smooth : true,
										seriesLayoutBy : 'row'
									},
									{
										type : 'line',
										smooth : true,
										seriesLayoutBy : 'row'
									},
									{
										type : 'line',
										smooth : true,
										seriesLayoutBy : 'row'
									},
									{
										type : 'line',
										smooth : true,
										seriesLayoutBy : 'row'
									},
									{
										type : 'pie',
										id : 'pie',
										radius : '30%',
										center : [ '50%', '25%' ],
										label : {
											formatter : '{b}: {@2012} ({d}%)'
										},
										encode : {
											itemName : 'product',
											value : '2012',
											tooltip : '2012'
										}
									}
								]
							};
							echartsMap.setOption(optionMap);*/
					// echarts 窗口缩放自适应
					window.onresize = function() {
						echartsRecords.resize();
					}
			
				});
			</script>
</body>

</html>

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
<meta http-equiv="Content-Security-Policy"
	content="upgrade-insecure-requests">

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
#echarts-dataset {
	position: relative;
	overflow: hidden;
}
#resultimage {
	width: 100%;
	height: auto;
	cursor: zoom-in; /* 设置光标样式为放大镜 */
	transition: transform 0.3s ease; /* 添加过渡效果 */
}

#echarts-dataset.zoomed {
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
	<div style="display:none" id="measureSelect">YOLOrot2.0</div>
	<div style=" display:flex;justify-content: space-between;padding:10px">
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
					<!--  <select lay-filter="submit" id="measureSelect"
						style="width: 200px; outline: none; text-indent: 5px;background: #ffffff;">
						<option value="" class="layui-select-tips layui-this">select
							algorithm</option>
						<option value="machine learning">machine learning</option>
						<option value="deep learning">deep learning</option>
					</select>-->

					<button type="button" lay-submit lay-filter="submit"
						class=" layui-btn " id="measureButton">Run</button>
				</div>
		</form>
	</div>
	<div style="width:570px;">
		<div class="layui-row">
			<div class="layui-col-md3">
				<div id="camera-preview"
					style="width: 100%; height: auto;margin-top:50px"></div>
			</div>
			<div class="layui-col-md">
				<!-- <button id="start-camera" class="layui-btn layui-btn-primary">Open
					camera</button> -->
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

			<div class="layui-col-xs12 layui-col-md6">
				<div class="layui-card top-panel">
					<div class="layui-card-header">Grain length(mm)</div>
					<div class="layui-card-body">
						<div class="layui-row layui-col-space5">
							<div id="max_value_width"
								class="layui-col-xs3 layui-col-md3 top-panel-tips">
								Maximum <br> <a style="color: #1aa094;font-size: 20px">0.00</a>
							</div>
							<div id="min_value_width"
								class="layui-col-xs3 layui-col-md3 top-panel-tips">
								Minimum <br> <a style="color: #bd3004;font-size: 20px">0.00</a><br>
							</div>
							<div id="average_value_width"
								class="layui-col-xs3 layui-col-md3 top-panel-tips">
								Average <br> <a style="color: #1aa094;font-size: 20px">0.00</a><br>
							</div>
							<div id="SD_value_width"
								class="layui-col-xs3 layui-col-md3 top-panel-tips">
								Standard deviation <br> <a
									style="color: #1aa094;font-size: 20px">0.00</a><br>
							</div>
						</div>
					</div>
				</div>
			</div>

			<div class="layui-col-xs12 layui-col-md6">
				<div class="layui-card top-panel">
					<div class="layui-card-header">Grain width(mm)</div>
					<div class="layui-card-body">
						<div class="layui-row layui-col-space5">
							<div id="max_value_height"
								class="layui-col-xs3 layui-col-md3 top-panel-tips">
								Maximum <br> <a style="color: #1aa094;font-size: 20px">0.00</a>
							</div>
							<div id="min_value_height"
								class="layui-col-xs3 layui-col-md3 top-panel-tips">
								Minimum <br> <a style="color: #bd3004;font-size: 20px">0.00</a><br>
							</div>
							<div id="average_value_height"
								class="layui-col-xs3 layui-col-md3 top-panel-tips">
								Average <br> <a style="color: #1aa094;font-size: 20px">0.00</a><br>
							</div>
							<div id="SD_value_height"
								class="layui-col-xs3 layui-col-md3 top-panel-tips">
								Standard deviation <br> <a
									style="color: #1aa094;font-size: 20px">0.00</a><br>
							</div>
						</div>
					</div>
				</div>
			</div>
		</div>


		<div id="result" class="layui-row layui-col-space15">
			<div class="layui-col-xs12 layui-col-md4">
				<div id="echarts-dataset"
					style="background-color:#ffffff;min-height:300px;padding: 10px;height:380px;padding-top: 30px">
					<img id="resultimage" style="max-width: 100%; max-height: 100%;"
						src="resource/images/IMG_20211102_101228.jpg">
				</div>
			</div>
			<div class="layui-col-xs12 layui-col-md8">
				<div id="echarts-records"
					style="background-color:#ffffff;min-height:400px;padding: 10px"></div>
			</div>
		</div>
	</div>

	<div class="layui-row layui-col-space15">
		<div class="layui-col-xs12 layui-col-md4">
			<div id="echarts-map"
				style="background-color:#ffffff;height:440px;padding: 10px;overflow-y: auto;display:none">
				<table id="data-table" class="layui-table" style="font-size: 18px">
					<colgroup>
						<col width="100">
						<col width="100">
						<col width="100">
					</colgroup>
					<thead>
						<tr>
							<th style="font-size: 18px">No</th>
							<th style="font-size: 18px">Length(mm)</th>
							<th style="font-size: 18px">Width(mm)</th>
						</tr>
					</thead>
					<tbody></tbody>
				</table>
			</div>
		</div>
		<div class="layui-col-xs12 layui-col-md8">
			<div id="echarts-pies"
				style="background-color:#ffffff;min-height:440px;padding: 10px;display:none">
				<table id="data-table-total" class="layui-table"
					style="font-size: 16px">
					<colgroup>
						<col width="250">
						<col width="225">
						<col width="225">
						
					</colgroup>
					<thead>
						<tr>
							<th style="font-size: 18px">Name</th>
							<th style="font-size: 18px">Mean length(mm)</th>
							<th style="font-size: 18px">Mean width(mm)</th>
							
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
           console.log(change)
           console.log(length)
           console.log(imagePath)
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
		layui.use([ 'form', 'upload', 'layer' ], function() {
			var form = layui.form;
			var upload = layui.upload;
			var layer = layui.layer;
	
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
				// 创建一个表单数据对象
				var formData = new FormData();
				formData.append("imageSrc", imageSrc);
				formData.append("algorithm", algorithm);
				console.log(algorithm)
				// 发送POST请求给控制器
				var xhr = new XMLHttpRequest();
				xhr.open("POST", "hzy/phenotypemeasure", true);
				xhr.onreadystatechange = function() {
					if (xhr.readyState === 4 && xhr.status === 200) {
						// 请求成功的处理逻辑
						var response = JSON.parse(xhr.responseText);
						console.log(response);
						if (response.status == "success") {
							var animationElement = document.querySelector('.animation');
                            animationElement.classList.remove('active');
                             document.getElementById("big").style.display = "block";
							document.getElementById("max_value_width").querySelector("a").innerText = response.widthMax.toFixed(3);
							document.getElementById("min_value_width").querySelector("a").innerText = response.widthMin.toFixed(3);
							document.getElementById("average_value_width").querySelector("a").innerText = response.heightAvg.toFixed(3);
							document.getElementById("SD_value_width").querySelector("a").innerText = response.widthSD.toFixed(3);
							document.getElementById("max_value_height").querySelector("a").innerText = response.heightMax.toFixed(3);
							document.getElementById("min_value_height").querySelector("a").innerText = response.heightMin.toFixed(3);
							document.getElementById("average_value_height").querySelector("a").innerText = response.widthAvg.toFixed(3);
							document.getElementById("SD_value_height").querySelector("a").innerText = response.heightSD.toFixed(3);
							/**
							   * 散点图*/
							var echartsRecords = echarts.init(document.getElementById('echarts-records'), 'walden');
							var converteData = [];
							var data = [];
							var lengthMax = 0,
								lengthMin = 1000,
								indexMax,
								indexMin;
							for (var i = 0; i < response.returnCornList.length; i++) {
								var convertedItem = [ response.returnCornList[i].width, response.returnCornList[i].heigth ];
								converteData.push(convertedItem);
								if (response.returnCornList[i].width > lengthMax) {
									lengthMax = response.returnCornList[i].width;
									indexMax = i;
								}
								if (response.returnCornList[i].width < lengthMin) {
									lengthMin = response.returnCornList[i].width;
									indexMin = i;
								}
							}
							var convertedMax = [ response.returnCornList[indexMax].width, response.returnCornList[indexMax].heigth ];
							data.push(convertedMax);
							var convertedMin = [ response.returnCornList[indexMin].width, response.returnCornList[indexMin].heigth ];
							data.push(convertedMin);
	
							/*optionRecords.yAxis = {
								min : 0, // 设置最小刻度值
								max : 12 // 设置最大刻度值
							};
							optionRecords.xAxis = {
								min : 0, // 设置最小刻度值
								max : 12 // 设置最大刻度值
							};*/
							optionRecords.series[1].data = converteData;
							optionRecords.series[0].data = data;
							echartsRecords.setOption(optionRecords);
	
							//跟新图片
	
							var change=0;
								document.getElementById("resultimage").src = response.imagePath[change];
							var echartsDataset = document.getElementById('echarts-dataset');
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
	
	
							//跟新数据
							var tbody = document.querySelector("#data-table tbody");
							for (var i = 0; i < response.returnCornList.length; i++) {
								var row = document.createElement("tr");
								for (var j = 0; j < 3; j++) {
									var cell = document.createElement("td");
									if (j % 3 == 0) {
										cell.textContent = response.returnCornList[i].cornId;
									}
									if (j % 3 == 1) {
										cell.textContent = Number(response.returnCornList[i].width).toFixed(3);
									}
									if (j % 3 == 2) {
										cell.textContent = Number(response.returnCornList[i].heigth).toFixed(3);
									}
									row.appendChild(cell);
								}
								tbody.appendChild(row);
							}
							var tbodyT = document.querySelector("#data-table-total tbody");
							for (var i = 0; i < response.CornTotalList.length; i++) {
								var rowT = document.createElement("tr");
								for (var j = 0; j < 3; j++) {
									var cellT = document.createElement("td");
									if (j % 3 == 0) {
										cellT.textContent = response.CornTotalList[i].name;
									}
									if (j % 3 == 1) {
										cellT.textContent = Number(response.CornTotalList[i].lengthMeans).toFixed(3);
									}
									if (j % 3 == 2) {
										cellT.textContent = Number(response.CornTotalList[i].widthMeans).toFixed(3);
									}
									
									rowT.appendChild(cellT);
								}
								tbodyT.appendChild(rowT);
							}
							document.getElementById("echarts-map").style.display = "block"
							document.getElementById("echarts-pies").style.display = "block"
	
							//点击切换图片
							var image = document.getElementById("resultimage");
								image.addEventListener("click", function() {
									change++;
									changeImage(change, response.imagePath.length, response.imagePath);
								});
	
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
						layer.msg('Upload Successfully', {
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
			 * 散点图
			 */
			var echartsRecords = echarts.init(document.getElementById('echarts-records'), 'walden');
			optionRecords = {
				xAxis : {
					scale : true,
					type : 'value',
					name : 'Length',
					nameTextStyle : {
						color : 'black', // 设置 x 轴名称颜色为黑色
						fontSize : 18
					},
					axisLabel : {
						formatter : '{value} mm', // 添加单位，例如 cm
						color : 'black'
					}
				},
				yAxis : {
					type : 'value',
					name : 'Width',
					nameTextStyle : {
						color : 'black', // 设置 x 轴名称颜色为黑色
						fontSize : 18
					},
					scale : true,
					axisLabel : {
						formatter : '{value} mm', // 添加单位，例如 cm
						color : 'black'
					}
				},
				legend : {
					orient : 'vertical', // 图例的布局方向，可以设置为 'horizontal' 水平布局
					right : 10, // 图例距离右侧的距离
					top : 10, // 图例距离顶部的距离
					textStyle : {
						color : 'black' // 图例文本颜色为黑色
					}
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
				toolbox : {
					feature : {
						dataZoom : {
							yAxisIndex : 'none' // 只启用水平方向的缩放
						},
						restore : {} // 添加还原按钮
					}
				},
				series : [
					{
						type : 'effectScatter',
						symbolSize : 20,
						data : [
							[ 7.619, 2.329 ], [ 9.763, 1.953 ]
						]
					},
					{
						type : 'scatter',
						// prettier-ignore
						data : [ [ 8.938, 2.041 ], [ 8.895, 1.969 ], [ 8.359, 2.267 ], [ 9.388, 2.248 ], [ 8.054, 2.35 ], [ 8.718, 2.282 ], [ 8.559, 2.087 ], [ 8.701, 2.354 ], [ 9.486, 2.078 ], [ 7.619, 2.329 ], [ 9.615, 2.054 ], [ 8.911, 1.99 ], [ 8.885, 2.601 ], [ 8.895, 1.758 ], [ 9.685, 2.31 ], [ 8.772, 2.194 ], [ 8.595, 2.134 ], [ 9.734, 2.089 ], [ 9.53, 1.976 ], [ 9.203, 2.204 ], [ 8.064, 1.847 ], [ 8.624, 2.289 ], [ 8.571, 2.239 ], [ 9.451, 2.195 ], [ 8.827, 2.006 ], [ 8.928, 2.138 ], [ 8.929, 2.152 ], [ 8.747, 1.95 ], [ 8.976, 2.392 ], [ 8.024, 2.17 ], [ 9.1, 2.236 ], [ 9.384, 2.186 ], [ 8.811, 2.118 ], [ 8.406, 2.356 ], [ 9.065, 2.068 ], [ 8.302, 2.202 ], [ 9.489, 1.999 ], [ 8.509, 2.556 ], [ 8.572, 1.981 ], [ 9.551, 2.052 ], [ 8.614, 1.884 ], [ 9.265, 1.965 ], [ 9.459, 1.783 ], [ 9.763, 1.953 ], [ 8.535, 2.163 ], [ 8.979, 2.433 ], [ 8.571, 2.084 ], [ 8.592, 2.193 ], [ 8.282, 1.956 ], [ 9.718, 2.173 ], [ 8.883, 2.18 ], [ 8.935, 2.378 ], [ 8.676, 1.956 ], [ 8.966, 2.239 ], [ 9.024, 2.212 ], [ 9.019, 1.968 ], [ 8.565, 2.277 ], [ 9.198, 2.215 ], [ 9.266, 2.112 ], [ 9.233, 2.144 ], [ 9.416, 2.251 ], [ 9.129, 2.057 ], [ 8.804, 2.129 ], [ 8.897, 2.268 ], [ 8.928, 1.906 ], [ 9.374, 2.273 ], [ 8.621, 2.312 ], [ 8.771, 2.034 ], [ 9.743, 2.033 ], [ 8.165, 2.119 ], [ 9.206, 2.276 ], [ 8.865, 1.839 ], [ 9.571, 2.059 ], [ 8.758, 1.896 ], [ 8.719, 2.225 ], [ 9.27, 2.286 ], [ 8.814, 2.199 ], [ 8.883, 2.003 ], [ 9.018, 2.166 ], [ 9.751, 2.133 ], [ 8.978, 2.228 ], [ 9.623, 2.015 ], [ 8.97, 2.266 ], [ 9.247, 2.048 ], [ 8.118, 2.424 ], [ 8.744, 2.129 ], [ 8.84, 2.209 ], [ 8.863, 2.203 ], [ 8.636, 1.936 ], [ 8.774, 2.164 ], [ 8.772, 2.03 ], [ 9.254, 2.239 ], [ 8.894, 2.317 ], [ 8.963, 2.131 ], [ 8.92, 2.234 ], [ 9.545, 1.987 ], [ 9.105, 2.048 ], [ 9.039, 2.326 ], [ 9.243, 2.049 ], [ 8.059, 2.223 ], [ 9.051, 2.212 ], [ 8.211, 2.008 ], [ 9.029, 2.364 ], [ 8.785, 2.289 ], [ 8.831, 2.18 ], [ 8.813, 2.113 ], [ 9.201, 1.937 ], [ 8.444, 2.284 ], [ 8.808, 2.192 ], [ 8.953, 2.193 ], [ 9.275, 2.264 ], [ 8.095, 2.471 ], [ 9.247, 2.425 ], [ 9.083, 2.095 ], [ 8.544, 2.019 ], [ 8.103, 2.032 ], [ 8.801, 2.259 ], [ 8.747, 2.317 ], [ 8.852, 2.189 ], [ 8.429, 2.21 ], [ 9.174, 2.417 ], [ 8.895, 2.301 ], [ 8.333, 2.232 ], [ 8.74, 2.117 ], [ 8.744, 1.863 ], [ 8.835, 1.917 ], [ 7.981, 2.181 ], [ 9.294, 2.012 ], [ 8.215, 2.166 ], [ 8.931, 2.235 ], [ 9.078, 2.093 ], [ 9.008, 2.229 ], [ 8.964, 2.154 ], [ 8.479, 2.4 ], [ 8.605, 1.91 ], [ 9.093, 2.145 ], [ 9.024, 2.263 ], [ 8.964, 2.258 ], [ 8.97, 2.205 ], [ 9.034, 2.138 ], [ 8.539, 2.065 ], [ 8.34, 2.136 ], [ 8.804, 1.889 ], [ 8.481, 2.331 ], [ 8.512, 1.966 ], [ 8.426, 2.106 ], [ 8.783, 1.939 ], [ 8.181, 2.119 ], [ 7.833, 1.905 ], [ 8.734, 2.225 ], [ 8.561, 2.176 ], [ 9.491, 2.206 ], [ 8.356, 1.903 ], [ 8.683, 2.202 ], [ 8.269, 1.887 ], [ 8.765, 2.106 ], [ 7.924, 2.006 ], [ 8.692, 2.201 ], [ 8.959, 2.224 ], [ 7.697, 1.843 ], [ 8.741, 2.07 ], [ 9.105, 1.965 ], [ 8.481, 1.934 ], [ 8.395, 1.882 ], [ 9.086, 2.249 ], [ 8.836, 2.144 ], [ 8.821, 1.957 ], [ 8.708, 1.952 ], [ 8.876, 2.189 ], [ 8.449, 1.892 ], [ 8.614, 2.141 ], [ 8.572, 2.193 ], [ 8.388, 2.213 ], [ 8.419, 2.065 ], [ 8.634, 2.313 ], [ 8.718, 2.23 ], [ 8.309, 2.327 ], [ 8.75, 1.965 ], [ 8.391, 2.34 ], [ 8.639, 2.308 ], [ 8.126, 2.196 ], [ 8.817, 2.147 ], [ 8.928, 2.335 ], [ 9.022, 1.923 ], [ 8.453, 2.188 ], [ 7.965, 2.413 ], [ 8.5, 2.367 ], [ 8.771, 2.141 ], [ 8.86, 1.991 ], [ 8.828, 2.247 ], [ 8.693, 2.284 ], [ 8.431, 2.096 ], [ 8.828, 2.062 ], [ 8.399, 2.158 ], [ 8.453, 2.419 ], [ 8.176, 2.106 ], [ 8.904, 1.976 ], [ 8.653, 2.236 ], [ 7.897, 2.232 ], [ 8.779, 2.251 ], [ 9.161, 2.119 ], [ 8.624, 1.996 ], [ 9.136, 1.985 ], [ 8.879, 2.292 ], [ 8.495, 2.069 ], [ 9.045, 2.15 ], [ 8.989, 1.965 ], [ 8.481, 2.187 ], [ 8.031, 2.227 ], [ 8.163, 2.135 ], [ 8.103, 2.246 ], [ 8.748, 2.139 ], [ 8.542, 1.926 ], [ 8.538, 1.966 ], [ 8.452, 2.327 ], [ 8.26, 2.102 ], [ 8.736, 1.857 ], [ 8.915, 2.205 ], [ 8.505, 2.272 ], [ 8.556, 2.211 ], [ 8.539, 1.985 ], [ 8.627, 2.311 ], [ 8.305, 1.895 ], [ 8.523, 2.321 ], [ 8.955, 2.121 ], [ 8.399, 2.006 ], [ 8.285, 1.829 ], [ 7.968, 2.229 ], [ 9.123, 2.006 ], [ 7.842, 1.942 ], [ 8.891, 2.2 ], [ 7.67, 2.293 ], [ 8.422, 2.297 ], [ 8.243, 2.207 ], [ 8.294, 2.225 ], [ 8.27, 2.314 ], [ 8.806, 2.198 ], [ 8.079, 2.122 ], [ 9.357, 2.183 ], [ 8.131, 1.917 ], [ 8.851, 2.246 ], [ 8.114, 1.895 ], [ 7.823, 2.194 ], [ 8.614, 2.109 ], [ 8.454, 2.104 ], [ 8.18, 2.146 ], [ 8.554, 1.908 ], [ 8.325, 2.126 ], [ 8.343, 2.181 ], [ 8.711, 1.937 ], [ 8.474, 2.141 ], [ 8.201, 2.295 ]
	
						]
					}
				]
			};
			echartsRecords.setOption(optionRecords);
	
	
			/**
			 * 玫瑰图表
			 */
			/*var echartsPies = echarts.init(document.getElementById('echarts-pies'), 'walden');
			var optionPies = {
				title : {
					text : '类型-玫瑰图',
					left : 'center'
				},
				tooltip : {
					trigger : 'item',
					formatter : '{a} <br/>{b} : {c} ({d}%)'
				},
				legend : {
					orient : 'vertical',
					left : 'left',
					data : [ '1', '2', '3', '4', '5' ]
				},
				series : [
					{
						name : '1',
						type : 'pie',
						radius : '55%',
						center : [ '50%', '60%' ],
						roseType : 'radius',
						data : [
							{
								value : 335,
								name : '1'
							},
							{
								value : 310,
								name : '2'
							},
							{
								value : 234,
								name : '3'
							},
							{
								value : 135,
								name : '4'
							},
							{
								value : 368,
								name : '5'
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
			echartsPies.setOption(optionPies);*/
	
	
			/**
			 * 柱状图
			 */
			/**var echartsDataset = echarts.init(document.getElementById('echarts-dataset'), 'walden');
			
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
			
			echartsDataset.setOption(optionDataset);*/
	
	
			/**
			 * 中国地图
			 */
			/*var echartsMap = echarts.init(document.getElementById('echarts-map'), 'walden');
			
			
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

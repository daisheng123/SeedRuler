/*package com.it.ssm.controller;

import java.io.BufferedReader;
import java.io.File;
import java.io.IOException;
import java.io.InputStreamReader;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.nio.file.StandardCopyOption;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import com.jcraft.jsch.*;
import javax.servlet.http.HttpServletRequest;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.util.ResourceUtils;
import org.springframework.web.multipart.MultipartFile;
import org.springframework.web.multipart.MultipartHttpServletRequest;
import org.springframework.web.bind.annotation.*;

import com.google.gson.Gson;
import com.google.gson.reflect.TypeToken;
import com.it.ssm.entity.Corn;
import com.it.ssm.entity.CornGerminate;
import com.it.ssm.entity.CornTotal;
import com.it.ssm.entity.image;
import com.it.ssm.service.UploadService;

@Controller
@RequestMapping("image")
public class clientController {
	@Autowired
	private UploadService uploadService;

	@ResponseBody
	@RequestMapping(value = "upload", method = RequestMethod.POST, consumes = "multipart/form-data")
	public Map<String, String> uploadImage(HttpServletRequest request, @RequestParam("file") MultipartFile image)
			throws IOException {
		// 文件上传后的存储路径
		String uploadDir = request.getSession().getServletContext().getRealPath("/resource/images/original/");

		// 获取文件名
		String imageName = image.getOriginalFilename();

		// 创建目标文件路径
		Path imageUrl = Paths.get(uploadDir + imageName);

		// 保存文件到目标路径
		try {
			Files.copy(image.getInputStream(), imageUrl, StandardCopyOption.REPLACE_EXISTING);
		} catch (Exception e) {
			e.printStackTrace();
		}

		// 根据需要进行相应的处理，如将文件路径保存到数据库等
		String Url = imageUrl.toString();

		System.out.println(Url);

		// 封装返回的JSON对象
		Map<String, String> response = new HashMap<>();
		int index = Url.indexOf("resource");
		String lasturl = Url.substring(index);
		System.out.println(lasturl);
		response.put("url", lasturl);
		return response;
	}

	@RequestMapping(value = "batchUpload", method = RequestMethod.POST)
	@ResponseBody
	public Map<String, Object> batchUpload(HttpServletRequest request, @RequestParam("files") MultipartFile[] files) {
		Map<String, Object> response = new HashMap<>();
		List<String> imagePaths = new ArrayList<>();
		// 处理文件上传逻辑
		for (MultipartFile file : files) {
			if (!file.isEmpty()) {
				try {
					// 获取文件名
					String fileName = file.getOriginalFilename();
					// 文件上传后的存储路径
					String filePath = request.getSession().getServletContext().getRealPath("/resource/images/original/")
							+ fileName;
					// 创建文件对象
					File destFile = new File(filePath);
					// 保存文件
					File destFolder = destFile.getParentFile();
					if (!destFolder.exists()) {
						destFolder.mkdirs();
					}
					file.transferTo(destFile);
					imagePaths.add(filePath.substring(filePath.indexOf("resource")));
				} catch (IOException e) {
					e.printStackTrace();
					// 文件保存失败，进行相应的处理
				}
			}
		}
		response.put("imagePaths", imagePaths);
		response.put("status", "success");
		response.put("message", "上传成功");
		return response;

	}

	@RequestMapping(value = "phenotypemeasure", method = RequestMethod.POST)
	@ResponseBody
	public Map<String, Object> measureImage(HttpServletRequest request, @RequestParam("imageSrc") String imageSrc,
			@RequestParam("algorithm") String algorithm) {
		String uploadDir = request.getSession().getServletContext().getRealPath("");
		String lasturl = imageSrc.substring(imageSrc.indexOf("resource"));
		String url = "";
		String[] lasturlArray = lasturl.split(",");
		List<String> lasturlList = Arrays.asList(lasturlArray);
		List<image> imageList = new ArrayList<image>();
		for (int i = 0; i < lasturlList.size(); i++) {
			image Image = new image();
			Image.setImageName(lasturlList.get(i).substring(lasturlList.get(i).lastIndexOf("/") + 1));
			Image.setImageUrl((uploadDir + lasturlList.get(i)).replace("/", "\\"));
			//Image.setImageUrl((uploadDir + lasturlList.get(i)));
			Image.setAlgorithm(algorithm);
			imageList.add(Image);
			url += imageList.get(i).getImageUrl() + " ";
		}
		String[] urls = url.split(" ");
		uploadService.upload(imageList);
		// 创建本地ProcessBuilder对象

		String pythonInterpreter = "D:\\software\\anaconda3\\envs\\yolov5\\python";
		String pythonScript = "ro_yolo/zjf_detect_rotation_6.py";
		List<String> commandArgs = new ArrayList<>();
		commandArgs.add(pythonInterpreter);
		commandArgs.add(pythonScript);
		commandArgs.add("--img-size");
		commandArgs.add("640");
		commandArgs.add("--weights");
		if(algorithm=="DL measure") {
			commandArgs.add("ro_yolo/runs/train/exp7/weights/best.pt");
		}
		else if(algorithm=="Image process"){
			commandArgs.add("ro_yolo/runs/train/exp8/weights/best.pt");
		}
		commandArgs.add("--conf");
		commandArgs.add("0.9");
		commandArgs.add("--save-txt");
		commandArgs.add("--source");
		commandArgs.addAll(Arrays.asList(urls));
		ProcessBuilder pb = new ProcessBuilder(commandArgs);
		pb.directory(new File("E:\\yjs\\yjs\\research\\Demo\\yolov5-3.1"));

		// 创建服务器ProcessBuilder对象

		
		  
		String pythonInterpreter = "/root/miniconda3/bin/python3";
		String pythonScript = "./ro_yolo/zjf_detect_rotation_6.py";
		List<String> commandArgs = new ArrayList<>();
		commandArgs.add(pythonInterpreter);
		commandArgs.add(pythonScript);
		commandArgs.add("--device");
		commandArgs.add("0");
		commandArgs.add("--img-size");
		commandArgs.add("640");
		commandArgs.add("--weights");
		if (algorithm == "DL measure") {
			commandArgs.add("ro_yolo/runs/train/exp7/weights/best.pt");
		} else {
			commandArgs.add("ro_yolo/runs/train/exp8/weights/best.pt");
		}
		
		commandArgs.add("--conf");
		commandArgs.add("0.9");
		commandArgs.add("--save-txt");
		commandArgs.add("--source");
		commandArgs.addAll(Arrays.asList(urls));
		ProcessBuilder pb = new ProcessBuilder(commandArgs);
		pb.directory(new File("/root/autodl-tmp/pythonProject"));
		 
		 

		pb.redirectErrorStream(true);
		Process p = null;
		try {
			p = pb.start();
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		// 读取Python脚本的输出
		double heightSum = 0, widthSum = 0, heightMax = 0, widthMax = 0, heightMin = 100000, widthMin = 100000,
				heightSD = 0, widthSD = 0, heightAvg = 0, widthAvg = 0;
		BufferedReader in = new BufferedReader(new InputStreamReader(p.getInputStream()));
		String ret;
		int index;
		Gson gson = new Gson();
		Map<Integer, List<Object>> map = new HashMap<>();
		List<Corn> returnCornList = new ArrayList<Corn>();
		List<CornTotal> CornTotalList = new ArrayList<CornTotal>();
		try {
			int t = 0, x = 0;
			List<Corn> SDList = new ArrayList<Corn>();

			while ((ret = in.readLine()) != null) {
				index = ret.indexOf("{");
				if (index != -1) {
					if (x % 2 == 0) {
						List<Corn> CornList = new ArrayList<Corn>();
						ret = ret.substring(index);
						System.out.println(ret);
						map = gson.fromJson(ret, new TypeToken<Map<Integer, List<Object>>>() {
						}.getType());
						for (Integer key : map.keySet()) {
							Corn corn = new Corn();
							corn.setCornId(key);
							corn.setWidth(map.get(key).get(0));
							corn.setHeigth(map.get(key).get(1));
							CornList.add(corn);
							SDList.add(corn);
							returnCornList.add(corn);
							heightSum += (Double) map.get(key).get(0);
							widthSum += (Double) map.get(key).get(1);
							if (widthMax < (Double) map.get(key).get(0)) {
								widthMax = (Double) map.get(key).get(0);
							}
							if (heightMax < (Double) map.get(key).get(1)) {
								heightMax = (Double) map.get(key).get(1);
							}
							if (widthMin > (Double) map.get(key).get(0)) {
								widthMin = (Double) map.get(key).get(0);
							}
							if (heightMin > (Double) map.get(key).get(1)) {
								heightMin = (Double) map.get(key).get(1);
							}
						}
						int imageId = uploadService.getImageId(new File(urls[t]).getName().trim());
						uploadService.phenotypemeasure(imageId, CornList);
						x++;
					}
					if (x % 2 == 1) {
						ret = in.readLine();
						index = ret.indexOf("{");
						ret = ret.substring(index);
						System.out.println(ret);
						map = gson.fromJson(ret, new TypeToken<Map<Integer, List<Object>>>() {
						}.getType());
						for (Integer key : map.keySet()) {
							CornTotal cornTotal = new CornTotal();
							cornTotal.setLengthMeans(map.get(key).get(1));
							cornTotal.setName(map.get(key).get(0));
							cornTotal.setNumber(map.get(key).get(3));
							cornTotal.setWidthMeans(map.get(key).get(2));
							CornTotalList.add(cornTotal);
						}
						x++;
					}
					t++;
				}
				heightAvg = heightSum / SDList.size();
				widthAvg = widthSum / SDList.size();
				double widthSD1 = 0, heightSD1 = 0;
				for (int i = 0; i < SDList.size(); i++) {
					widthSD1 += Math.pow((Double) SDList.get(i).getWidth() - widthAvg, 2);
					heightSD1 += Math.pow((Double) SDList.get(i).getHeigth() - heightAvg, 2);
				}
				widthSD = Math.sqrt(widthSD1 / SDList.size());
				heightSD = Math.sqrt(heightSD1 / SDList.size());
			}
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		List<String> measureurlArray=new ArrayList<String> ();
		for(int x=0;x<lasturlArray.length;x++) {
			measureurlArray.add(lasturlArray[x].replace("original", "measure"));
		}
		// 封装返回的JSON对象
		Map<String, Object> response = new HashMap<>();
		response.put("heightMax", heightMax);
		response.put("widthMax", widthMax);
		response.put("heightMin", heightMin);
		response.put("widthMin", widthMin);
		response.put("widthSD", widthSD);
		response.put("heightSD", heightSD);
		response.put("heightAvg", heightAvg);
		response.put("widthAvg", widthAvg);
		response.put("returnCornList", returnCornList);
		response.put("CornTotalList", CornTotalList);
		response.put("imagePath", measureurlArray);
		response.put("status", "success");
		response.put("message", "参数测量成功");
		return response;
	}

	*//**
	 * 萌发率测量
	 * 
	 * @param request
	 * @param imageSrc
	 * @param algorithm
	 * @return
	 *//*
	@RequestMapping(value = "germinatemeasure", method = RequestMethod.POST)
	@ResponseBody
	public Map<String, Object> germinatemeasure(HttpServletRequest request, @RequestParam("imageSrc") String imageSrc,
			@RequestParam("algorithm") String algorithm,@RequestParam("model") String model) {
		String uploadDir = request.getSession().getServletContext().getRealPath("");
		String lasturl = imageSrc.substring(imageSrc.indexOf("resource"));
		String url = "";
		String[] lasturlArray = lasturl.split(",");
		List<String> lasturlList = Arrays.asList(lasturlArray);
		List<image> imageList = new ArrayList<image>();
		for (int i = 0; i < lasturlList.size(); i++) {
			image Image = new image();
			Image.setImageName(lasturlList.get(i).substring(lasturlList.get(i).lastIndexOf("/") + 1));
			Image.setImageUrl((uploadDir + lasturlList.get(i)).replace("/", "\\"));
			//Image.setImageUrl((uploadDir + lasturlList.get(i)));
			Image.setAlgorithm(algorithm);
			imageList.add(Image);
			url += imageList.get(i).getImageUrl() + " ";
		}
		String[] urls = url.split(" ");
		uploadService.upload(imageList);
		// 创建本地ProcessBuilder对象

		
		 String pythonInterpreter = "D:\\software\\anaconda3\\envs\\yolov5\\python";
		 String pythonScript = "detect.py"; List<String> commandArgs = new
		 ArrayList<>(); commandArgs.add(pythonInterpreter);
		 commandArgs.add(pythonScript); commandArgs.add("--agnostic-nms");
		 commandArgs.add("--weights"); 
		 if(model=="TG/UTG") {
			 commandArgs.add("runs/exp10/weights/best.pt");
		 }
		 else if(model=="OG/UOG") {
			 commandArgs.add("runs/exp0/weights/best.pt");
		 }
		 
		 commandArgs.add("--conf"); commandArgs.add(" 0.4");
		 commandArgs.add("--save-txt"); commandArgs.add("--source");
		 commandArgs.addAll(Arrays.asList(urls)); ProcessBuilder pb = new
		 ProcessBuilder(commandArgs); pb.directory(new
		 File("E:\\yjs\\yjs\\research\\Demo\\yolov5-3.1"));
		 

		// 创建服务器ProcessBuilder对象

		String pythonInterpreter = "/root/miniconda3/bin/python3";
		String pythonScript = "./detect.py";
		List<String> commandArgs = new ArrayList<>();
		commandArgs.add(pythonInterpreter);
		commandArgs.add(pythonScript);
		commandArgs.add("--device");
		commandArgs.add("0");
		commandArgs.add("--agnostic-nms");
		commandArgs.add("--weights");
		if(model=="TG/UTG") {
			 commandArgs.add("runs/exp10/weights/best.pt");
		 }
		 else{
			 commandArgs.add("runs/exp0/weights/best.pt");
		 }
		commandArgs.add("--conf");
		commandArgs.add(" 0.4");
		commandArgs.add("--save-txt");
		commandArgs.add("--source");
		commandArgs.addAll(Arrays.asList(urls));
		ProcessBuilder pb = new ProcessBuilder(commandArgs);
		pb.directory(new File("/root/autodl-tmp/pythonProject"));

		pb.redirectErrorStream(true);
		Process p = null;
		try {
			p = pb.start();
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		// 读取Python脚本的输出
		int germinateCount = 0, nogerminateCount = 0, graincount = 0;
		double germinateRate = 0;
		BufferedReader in = new BufferedReader(new InputStreamReader(p.getInputStream()));
		String ret;
		int index;
		Gson gson = new Gson();
		Map<Integer, List<Object>> map = new HashMap<>();
		try {
			int t = 0;
			while ((ret = in.readLine()) != null) {
				index = ret.indexOf("{");
				if (index != -1) {
					List<CornGerminate> CornGerminateList = new ArrayList<CornGerminate>();
					ret = ret.substring(index);
					System.out.println(ret);
					map = gson.fromJson(ret, new TypeToken<Map<Integer, List<Object>>>() {
					}.getType());
					for (Integer key : map.keySet()) {
						CornGerminate cornGerminate = new CornGerminate();
						cornGerminate.setSumCount(map.get(key).get(3));
						cornGerminate.setGerminationCount(map.get(key).get(1));
						cornGerminate.setNogerminationCount(map.get(key).get(2));
						cornGerminate.setGerminationRate(map.get(key).get(4));
						CornGerminateList.add(cornGerminate);
						int imageId = uploadService.getImageId(new File(urls[t]).getName().trim());
						uploadService.germinatemeasure(imageId, CornGerminateList);
						germinateCount += (Double) map.get(key).get(1);
						nogerminateCount += (Double) map.get(key).get(2);
						graincount += (Double) map.get(key).get(3);
						germinateRate += (Double) map.get(key).get(4);
					}
					t++;
				}
			}
			germinateRate = germinateRate / t;
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		List<String> measureurlArray=new ArrayList<String> ();
		for(int x=0;x<lasturlArray.length;x++) {
			measureurlArray.add(lasturlArray[x].replace("original", "measure"));
		}
		// 封装返回的JSON对象
		Map<String, Object> response = new HashMap<>();
		response.put("germinateCount", germinateCount);
		response.put("nogerminateCount", nogerminateCount);
		response.put("grainCount", graincount);
		response.put("germinateRate", germinateRate);
		response.put("imagePath", measureurlArray);
		response.put("status", "success");
		response.put("message", "参数测量成功");
		return response;
	}
	
	*//**
	 * 萌发率测量
	 * 
	 * @param request
	 * @param imageSrc
	 * @param algorithm
	 * @return
	 *//*
	@RequestMapping(value = "germinatemeasure_ImageProcess", method = RequestMethod.POST)
	@ResponseBody
	public Map<String, Object> germinatemeasure_ImageProcess(HttpServletRequest request, @RequestParam("imageSrc") String imageSrc,
			@RequestParam("algorithm") String algorithm,@RequestParam("threshold") String threshold) {
		String uploadDir = request.getSession().getServletContext().getRealPath("");
		String lasturl = imageSrc.substring(imageSrc.indexOf("resource"));
		String url = "";
		String[] lasturlArray = lasturl.split(",");
		List<String> lasturlList = Arrays.asList(lasturlArray);
		List<image> imageList = new ArrayList<image>();
		for (int i = 0; i < lasturlList.size(); i++) {
			image Image = new image();
			Image.setImageName(lasturlList.get(i).substring(lasturlList.get(i).lastIndexOf("/") + 1));
			Image.setImageUrl((uploadDir + lasturlList.get(i)).replace("/", "\\"));
			//Image.setImageUrl((uploadDir + lasturlList.get(i)));
			Image.setAlgorithm(algorithm);
			imageList.add(Image);
			url += imageList.get(i).getImageUrl() + " ";
		}
		String[] urls = url.split(" ");
		uploadService.upload(imageList);
		// 创建本地ProcessBuilder对象

		 String pythonInterpreter = "D:\\software\\anaconda3\\envs\\yjw\\python";
		 String pythonScript = "imageProcess.py"; 
		 List<String> commandArgs = new ArrayList<>(); 
		 commandArgs.add(pythonInterpreter);
		 commandArgs.add(pythonScript); 
		 commandArgs.add("--source");
		 commandArgs.addAll(Arrays.asList(urls)); 
		 commandArgs.add("--range");
		 commandArgs.add(threshold);
		 ProcessBuilder pb = new ProcessBuilder(commandArgs); pb.directory(new
		 File("E:\\yjs\\yjs\\research\\Demo\\test_2"));
		 

		// 创建服务器ProcessBuilder对象

		String pythonInterpreter = "/root/miniconda3/bin/python3";
		String pythonScript = "./imageProcess.py";
		List<String> commandArgs = new ArrayList<>();
		commandArgs.add(pythonInterpreter);
		commandArgs.add(pythonScript);
		commandArgs.add("--source");
		commandArgs.addAll(Arrays.asList(urls));
		commandArgs.add("--range");
		commandArgs.add(threshold);
		ProcessBuilder pb = new ProcessBuilder(commandArgs);
		pb.directory(new File("/root/autodl-tmp/pythonProject"));

		pb.redirectErrorStream(true);
		Process p = null;
		try {
			p = pb.start();
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		// 读取Python脚本的输出
		int germinateCount = 0, nogerminateCount = 0, graincount = 0;
		double germinateRate = 0;
		BufferedReader in = new BufferedReader(new InputStreamReader(p.getInputStream()));
		String ret;
		int index;
		Gson gson = new Gson();
		Map<Integer, List<Object>> map = new HashMap<>();
		List<CornGerminate> CornGerminateList = new ArrayList<CornGerminate>();
		try {
			int t = 0;
			while ((ret = in.readLine()) != null) {
				index = ret.indexOf("{");
				if (index != -1) {
					ret = ret.substring(index);
					System.out.println(ret);
					map = gson.fromJson(ret, new TypeToken<Map<Integer, List<Object>>>() {
					}.getType());
					for (Integer key : map.keySet()) {
						CornGerminate cornGerminate = new CornGerminate();
						cornGerminate.setSumCount(map.get(key).get(0));
						cornGerminate.setGerminationCount(map.get(key).get(1));
						cornGerminate.setNogerminationCount((double)map.get(key).get(0)-(double)map.get(key).get(1));
						cornGerminate.setGerminationRate(map.get(key).get(2));
						cornGerminate.setImageName((String)map.get(key).get(3));
						CornGerminateList.add(cornGerminate);
						int imageId = uploadService.getImageId(new File(urls[t]).getName().trim());
						uploadService.germinatemeasure(imageId, CornGerminateList);
						germinateCount += (Double) map.get(key).get(1);
						nogerminateCount += (double)map.get(key).get(0)-(double)map.get(key).get(1);
						graincount += (Double) map.get(key).get(0);
						germinateRate += (Double) map.get(key).get(2);
					}
					t++;
				}
			}
			germinateRate = germinateRate / t;
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		List<String> measureurlArray=new ArrayList<String> ();
		for(int x=0;x<lasturlArray.length;x++) {
			measureurlArray.add(lasturlArray[x].replace("original", "measure"));
		}
		// 封装返回的JSON对象
		Map<String, Object> response = new HashMap<>();
		response.put("germinateCount", germinateCount);
		response.put("nogerminateCount", nogerminateCount);
		response.put("grainCount", graincount);
		response.put("germinateRate", germinateRate);
		response.put("CornGerminateList", CornGerminateList);
		response.put("imagePath", measureurlArray);
		response.put("status", "success");
		response.put("message", "参数测量成功");
		return response;
	}

	*//**
	 * 拍照保存
	 * 
	 * @param request
	 * @param image
	 * @return
	 * @throws IOException
	 *//*
	@ResponseBody
	@RequestMapping(value = "save", method = RequestMethod.POST, consumes = "multipart/form-data")
	public String saveImage(HttpServletRequest request, @RequestParam("dataUrl") String dataUrl) throws IOException {
		// 图片保存后的存储路径

		
		 String folderPath = "C:/images/"; // 指定文件夹的路径 
		 File folder = new File(folderPath); 
		 if (!folder.exists()) { boolean created = folder.mkdirs();
		 } // 生成唯一的文件名 
		 String fileName = System.currentTimeMillis() + ".png"; //文件保存路径
		 String filePath = folderPath + fileName; // 截取dataURL中的Base64编码数据
		 String base64Data = dataUrl.substring(dataUrl.indexOf(",") + 1); try { 
         //将Base64编码数据转换为二进制数据 
		 byte[] binaryData =javax.xml.bind.DatatypeConverter.parseBase64Binary(base64Data); // 保存图片文件
		 org.apache.commons.io.FileUtils.writeByteArrayToFile(new File(filePath),
		 binaryData); return "保存图片成功"; } catch (IOException e) { e.printStackTrace();
		 return "保存图片失败"; }
		 

		// linux图片保存到本地

		String remoteFilePath = "/root/tomcat/apache-tomcat-8.5.96/webapps/IMSFGM/resource/images/temp/";
		String fileName = System.currentTimeMillis() + ".png";
		String remotefilePath = remoteFilePath + fileName;
		String base64Data = dataUrl.substring(dataUrl.indexOf(",") + 1);
		try { // 将Base64编码数据转换为二进制数据
			byte[] binaryData = javax.xml.bind.DatatypeConverter.parseBase64Binary(base64Data); // 保存图片文件
			org.apache.commons.io.FileUtils.writeByteArrayToFile(new File(remotefilePath), binaryData);
			return "图片保存成功！";
		} catch (IOException e) {
			e.printStackTrace();
			return "图片保存失败！";
		}

		
		 * String remoteHost = "connect.westc.gpuhub.com"; String username = "root";
		 * String password = "Xyaog82+++jg"; try { JSch jsch = new JSch(); Session
		 * session = jsch.getSession(username, remoteHost, 22);
		 * session.setPassword(password); session.setConfig("StrictHostKeyChecking",
		 * "no"); session.connect(); String localFilePath = "C:/saveImages"; File
		 * folder=new File(localFilePath); if (!folder.exists()) {boolean created =
		 * folder.mkdirs();}; // 获取远程文件名 String remotefileName =
		 * remoteFilePath.substring(remotefilePath.lastIndexOf("/") + 1); // 本地保存路径
		 * String localFile = localFilePath + File.separator + remotefileName;
		 * ChannelSftp channel = (ChannelSftp) session.openChannel("sftp");
		 * channel.connect(); channel.get(remotefilePath, localFile); // 从远程服务器下载文件到本地
		 * 
		 * channel.disconnect(); session.disconnect();
		 * 
		 * return "图片保存成功！"; } catch (JSchException | SftpException e) {
		 * e.printStackTrace(); return "图片保存失败！"; }
		 

	}
}
*/
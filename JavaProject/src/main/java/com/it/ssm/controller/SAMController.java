package com.it.ssm.controller;

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
import java.util.Random;

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
@RequestMapping("SAM")
public class SAMController {
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
	
	/**
	 * 萌发率测量
	 * 
	 * @param request
	 * @param imageSrc
	 * @param algorithm
	 * @return
	 */
	@RequestMapping(value = "germinatemeasure_SAM", method = RequestMethod.POST)
	@ResponseBody
	public Map<String, Object> germinatemeasure_SAM(HttpServletRequest request, @RequestParam("imageSrc") String imageSrc,
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
		 String pythonScript = "detect.py"; List<String> commandArgs = new
		 ArrayList<>(); commandArgs.add(pythonInterpreter);
		 commandArgs.add(pythonScript); commandArgs.add("--agnostic-nms");
		 commandArgs.add("--weights"); 
		 commandArgs.add("runs/exp10/weights/best.pt");
		 commandArgs.add("--conf"); commandArgs.add(" 0.4");
		 commandArgs.add("--save-txt"); commandArgs.add("--source");
		 commandArgs.addAll(Arrays.asList(urls)); ProcessBuilder pb = new
		 ProcessBuilder(commandArgs); pb.directory(new
		 File("E:\\yjs\\yjs\\research\\Demo\\yolov5-3.1"));
		 

		// 创建服务器ProcessBuilder对象

		/*String pythonInterpreter = "/root/miniconda3/bin/python3";
		String pythonScript = "./detect.py";
		List<String> commandArgs = new ArrayList<>();
		commandArgs.add(pythonInterpreter);
		commandArgs.add(pythonScript);
		commandArgs.add("--device");
		commandArgs.add("0");
		commandArgs.add("--agnostic-nms");
		commandArgs.add("--weights");
		commandArgs.add("runs/exp10/weights/best.pt");
		commandArgs.add("--conf");
		commandArgs.add(" 0.4");
		commandArgs.add("--save-txt");
		commandArgs.add("--source");
		commandArgs.addAll(Arrays.asList(urls));
		ProcessBuilder pb = new ProcessBuilder(commandArgs);
		pb.directory(new File("/root/autodl-tmp/pythonProject"));*/

		pb.redirectErrorStream(true);
		Process p = null;
		try {
			p = pb.start();
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		String ret1;
		int index1;
		BufferedReader in1 = new BufferedReader(new InputStreamReader(p.getInputStream()));
		try {
			while ((ret1 = in1.readLine()) != null) {
				index1 = ret1.indexOf("{");
				if (index1 != -1) {
					ret1 = ret1.substring(index1);
					System.out.println(ret1);}
			}
		} catch (IOException e1) {
			// TODO Auto-generated catch block
			e1.printStackTrace();
		}
		//SAM
		String[] xmlurl1 = new String[urls.length];
		String[] xmlurl2 = new String[urls.length];
		//String[] xmlNames = null;
		for(int i=0;i<urls.length;i++) {
			xmlurl1[i]=urls[i].replace("original", "xml");
			xmlurl2[i]=xmlurl1[i].replace("jpg", "xml");
			//xmlNames[i]=new File(xmlurls[i]).getName();
		}
		String[] image_xml=new String[urls.length*2];
		int x=0,y=0;
		for(int t=0;t<(urls.length)*2&&t<(xmlurl2.length)*2;t++) {
			if(t%2==0) {
				image_xml[t]=urls[x++];
			}
			if(t%2==1) {
				image_xml[t]=xmlurl2[y++];
			}
		}
		//服务器
		/*String pythonInterpreter_SAM = "/root/miniconda3/bin/python3";
		String pythonScript_SAM= "./SAM_RGB_XML.py";
		List<String> commandArgs_SAM = new ArrayList<>();
		commandArgs_SAM.add(pythonInterpreter_SAM);
		commandArgs_SAM.add(pythonScript_SAM);
		commandArgs_SAM.add("--source");
		commandArgs_SAM.addAll(Arrays.asList(image_xml));
		ProcessBuilder pb_SAM = new ProcessBuilder(commandArgs_SAM);
		pb_SAM.directory(new File("/root/autodl-tmp/pythonProject/interface"));*/
		
		//本地
		String pythonInterpreter_SAM = "D:\\software\\anaconda3\\envs\\yolov5\\python";
		String pythonScript_SAM= "./SAM_RGB_XML.py";
		List<String> commandArgs_SAM = new ArrayList<>();
		commandArgs_SAM.add(pythonInterpreter_SAM);
		commandArgs_SAM.add(pythonScript_SAM);
		commandArgs_SAM.add("--source");
		commandArgs_SAM.addAll(Arrays.asList(image_xml));
		ProcessBuilder pb_SAM = new ProcessBuilder(commandArgs_SAM);
		pb_SAM.directory(new File("E:\\yjs\\yjs\\research\\Demo\\yolov5-3.1\\interface"));
		
		
		pb_SAM.redirectErrorStream(true);
		Process p_SAM = null;
		try {
			p_SAM = pb_SAM.start();
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		String ret;
		int index;
		double width = 0,height = 0;
		Gson gson = new Gson();
		Map<Integer, List<Object>> map = new HashMap<>();
		BufferedReader in = new BufferedReader(new InputStreamReader(p_SAM.getInputStream()));
		try {
			while ((ret = in.readLine()) != null) {
				index = ret.indexOf("{");
				if (index != -1) {
					ret = ret.substring(index);
					System.out.println(ret);
					map = gson.fromJson(ret, new TypeToken<Map<Integer, List<Object>>>() {
					}.getType());
					for (Integer key : map.keySet()) {
						width=(double) map.get(key).get(0);
						height=(double) map.get(key).get(1);
					}
				}
			}
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		// 封装返回的JSON对象
		Map<String, Object> response = new HashMap<>();
		/*List<String> SAMurlArray=new ArrayList<String> ();
		for(int x1=0;x1<lasturlArray.length;x1++) {
			SAMurlArray.add(lasturlArray[x1].replace("original", "image_xml"));
		}*/
		List<String> measureurlArray=new ArrayList<String> ();
		for(int x1=0;x1<lasturlArray.length;x1++) {
			measureurlArray.add(lasturlArray[x1].replace("original", "measure"));
		}
		response.put("imagePath", measureurlArray);
		response.put("width", width);
		response.put("height", height);
		response.put("status", "success");
		response.put("message", "参数测量成功");
		return response;
	}
	
	@RequestMapping(value = "SAM", method = RequestMethod.POST)
	@ResponseBody
	public Map<String, Object> SAM(HttpServletRequest request, @RequestParam("imageSrc") String imageSrc,
			@RequestParam("algorithm") String algorithm,@RequestParam("filename")String filename,@RequestParam("pos_x")String pos_x,@RequestParam("pos_y") String pos_y) {
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
		
		String[] source=new String[3];
		
		source[0]=filename.substring(0,filename.lastIndexOf('.'));
		source[1]=pos_x;
		source[2]=pos_y;
		
		// 创建本地ProcessBuilder对象

		 String pythonInterpreter = "D:\\software\\anaconda3\\envs\\yolov5\\python";
		 String pythonScript = "SAM.py"; List<String> commandArgs = new
		 ArrayList<>(); commandArgs.add(pythonInterpreter);
		 commandArgs.add(pythonScript); 		 
		 commandArgs.add("--source");
		 commandArgs.addAll(Arrays.asList(source)); ProcessBuilder pb = new
		 ProcessBuilder(commandArgs); pb.directory(new
		 File("E:\\yjs\\yjs\\research\\Demo\\yolov5-3.1\\interface"));
		 

		// 创建服务器ProcessBuilder对象

		/*String pythonInterpreter = "/root/miniconda3/bin/python3";
		String pythonScript = "./SAM.py";
		List<String> commandArgs = new ArrayList<>();
		commandArgs.add(pythonInterpreter);
		commandArgs.add(pythonScript);
		commandArgs.add("--source");
		commandArgs.addAll(Arrays.asList(source));
		ProcessBuilder pb = new ProcessBuilder(commandArgs);
		pb.directory(new File("/root/autodl-tmp/pythonProject/interface"));*/

		pb.redirectErrorStream(true);
		Process p = null;
		try {
			p = pb.start();
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
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
		Map<String, Object> response = new HashMap<>();
		List<String> measureurlArray=new ArrayList<String> ();
		String[] murlArray=new String[lasturlArray.length];
		Random random = new Random();
		String a="";
		int n=-1,m=-1;
        int r = random.nextInt();
		for(int x1=0;x1<lasturlArray.length;x1++) {
			n=lasturlArray[x1].lastIndexOf('/');
			m=lasturlArray[x1].length();
			a=lasturlArray[x1].substring(n+1);
			if(lasturlArray[x1].substring(lasturlArray[x1].lastIndexOf('/')+1).equals(filename)) {
				murlArray[x1]=lasturlArray[x1].replace("original", "measure");
				measureurlArray.add(murlArray[x1].replace("jpg", "png")+"?t="+r);
			}
		}
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

		/*String remoteFilePath = "/root/tomcat/apache-tomcat-8.5.96/webapps/IMSFGM/resource/images/temp/";
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
		}*/

		/*
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
		 */

	}

}

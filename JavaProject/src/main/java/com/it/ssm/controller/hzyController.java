package com.it.ssm.controller;

import java.io.BufferedReader;
import java.io.File;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import javax.servlet.http.HttpServletRequest;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.*;

import com.google.gson.Gson;
import com.google.gson.reflect.TypeToken;
import com.it.ssm.entity.Corn;
import com.it.ssm.entity.CornTotal;
import com.it.ssm.entity.image;
import com.it.ssm.service.UploadService;

@Controller
@RequestMapping("hzy")
public class hzyController {
	@Autowired
	private UploadService uploadService;

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
			//Image.setImageUrl((uploadDir + lasturlList.get(i)).replace("/", "\\"));
			Image.setImageUrl((uploadDir + lasturlList.get(i)));
			Image.setAlgorithm(algorithm);
			imageList.add(Image);
			url += imageList.get(i).getImageUrl() + " ";
		}
		String[] urls = url.split(" ");
		uploadService.upload(imageList);
		// 创建本地ProcessBuilder对象

		/*String pythonInterpreter = "D:\\software\\anaconda3\\envs\\hzy\\python";
		String pythonScript = "output.py";
		List<String> commandArgs = new ArrayList<>();
		commandArgs.add(pythonInterpreter);
		commandArgs.add(pythonScript);
		commandArgs.add("--source");
		commandArgs.addAll(Arrays.asList(urls));
		ProcessBuilder pb = new ProcessBuilder(commandArgs);
		pb.directory(new File("E:\\yjs\\yjs\\research\\Demo\\hzy"));*/

		// 创建服务器ProcessBuilder对象

		
		  
		String pythonInterpreter = "/root/miniconda3/bin/python3";
		String pythonScript = "output.py";
		List<String> commandArgs = new ArrayList<>();
		commandArgs.add(pythonInterpreter);
		commandArgs.add(pythonScript);
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
				System.out.print(ret);
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
	
}

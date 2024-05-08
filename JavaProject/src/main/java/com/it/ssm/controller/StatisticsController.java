package com.it.ssm.controller;

import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.ResponseBody;

import com.google.gson.Gson;
import com.it.ssm.entity.CornCount;
import com.it.ssm.entity.CornGerminate;
import com.it.ssm.entity.CornPhenotype;
import com.it.ssm.service.StatisticsService;

@Controller
@RequestMapping("statistics")
public class StatisticsController {

	@Autowired
	private StatisticsService statisticsService;
	
	
	@RequestMapping(value = "findCornCountList")
	@ResponseBody 
	public void findCornCountList(String imageName, Integer page, Integer limit, HttpServletRequest request,
			HttpServletResponse response) throws IOException {
		List<CornCount> cornCount = new ArrayList<>();
		cornCount = statisticsService.findCornCountList(imageName, page, limit);
		int sumCount=0;
		for(int i=0;i<cornCount.size();i++) {
			sumCount+=cornCount.get(i).getCount();
		}
		for(int j=0;j<cornCount.size();j++) {
			cornCount.get(j).setSumCount(sumCount);
		}
		HashMap<String, Object> map = new HashMap<>();
		int count=statisticsService.findCornCount(imageName);
		map.put("code", 0);
		map.put("msg", "请求成功");
		map.put("count", count);
		map.put("data", cornCount);
		response.setContentType("text/html;charset=UTF-8");
		response.getWriter().write(new Gson().toJson(map));
	}
	
	
	@RequestMapping(value = "findCornPhenotypeList")
	@ResponseBody // 需要将返回的数据先转换成json格式
	public void findCornPhenotypeList(String imageName, Integer page, Integer limit, HttpServletRequest request,
			HttpServletResponse response) throws IOException {
		List<CornPhenotype> cornPhenotype = new ArrayList<>();
		int count ;
		cornPhenotype = statisticsService.findCornPhenotypeList(imageName, page, limit);
		count=statisticsService.findCornPhenotypeCount(imageName);
		HashMap<String, Object> map = new HashMap<>();
		map.put("code", 0);
		map.put("msg", "请求成功");
		map.put("count", count);
		map.put("data", cornPhenotype);
		response.setContentType("text/html;charset=UTF-8");
		response.getWriter().write(new Gson().toJson(map));
	}
	
	
	@RequestMapping(value = "findCornGerminateList")
	@ResponseBody 
	public void findCornGerminateList(String imageName, Integer page, Integer limit, HttpServletRequest request,
			HttpServletResponse response) throws IOException {
		List<CornGerminate> cornGerminate = new ArrayList<>();
		cornGerminate = statisticsService.findCornGerminateList(imageName, page, limit);
		HashMap<String, Object> map = new HashMap<>();
		int count=statisticsService.findCornGerminateCount(imageName);
		map.put("code", 0);
		map.put("msg", "请求成功");
		map.put("count", count);
		map.put("data", cornGerminate);
		response.setContentType("text/html;charset=UTF-8");
		response.getWriter().write(new Gson().toJson(map));
	}

}

package com.it.ssm.controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.ResponseBody;

import com.google.gson.Gson;
import com.it.ssm.entity.User;
import com.it.ssm.service.UserService;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import java.io.IOException;
import java.util.*;

@Controller
@RequestMapping("user")
public class UserController {

	@Autowired
	private UserService userService;

	@RequestMapping(value = "findProviderList")
	@ResponseBody // 需要将返回的数据先转换成json格式
	// 参数中 Integer page, Integer limit 是用来接收layui自带的分页中的参数（隐藏小彩蛋），这样就实现了自动翻页
	public void findUserList(String userName, Integer page, Integer limit, HttpServletRequest request,
			HttpServletResponse response) throws IOException {
		List<User> users = new ArrayList<>();
		// 就把这两个参数往方法里一传就行，妙啊
		users = userService.findUserList(userName, page, limit);
		HashMap<String, Object> map = new HashMap<>();
		map.put("code", 0);
		map.put("msg", "请求成功");
		map.put("count", users.size());
		map.put("data", users);
		response.setContentType("text/html;charset=UTF-8");
		response.getWriter().write(new Gson().toJson(map));
	}

	/*@RequestMapping(value = "addUserInfo")
	@ResponseBody // 前端接收json字符串，这个必须设置，否则两端数据对应不上ajax会默认解析成string类型变成路径（如果你配置了视图解析器还会自动加上，看起来很离谱的404错误路径）
	public JSONMassage addProviderInfo(User user) {
		int i = userService.addUserInfo(user);
		if (i > 0) {
			return new JSONMassage(0, "成功", null);
		} else {
			return new JSONMassage(1, "请求失败", null);
		}
	}*/
	@RequestMapping(value = "login",produces="text/html;charset=UTF-8")
	@ResponseBody 
	public String  login(HttpServletRequest request,HttpServletResponse response ) throws IOException{
		String userName=request.getParameter("userName");
		String password=request.getParameter("password");
		User user=userService.login(userName,password);
		String result;
		if(user!=null) {
			result="登录成功";
		}
		else result="登录失败";
		return result;
	}
}

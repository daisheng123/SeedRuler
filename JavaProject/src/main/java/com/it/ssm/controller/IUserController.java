package com.it.ssm.controller;
 
 
import javax.servlet.http.HttpServletRequest;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.ResponseBody;
import com.it.ssm.entity.User;
import com.it.ssm.service.IUserService;
 
@Controller
@RequestMapping("/user")
public class IUserController {
 
	@Autowired
	private IUserService userService;
	
	@RequestMapping("/login.do")
	@ResponseBody
	public String login(HttpServletRequest request){
		String username = request.getParameter("username");
		String pwd = request.getParameter("pwd");
		String msg = null;
		User user = userService.login(username);
		if (user.getPassword().equals(pwd)) {
			msg = "login successfully!";
		}else {
			msg = "please check your username and password!";
		}
		return msg;
	}
}
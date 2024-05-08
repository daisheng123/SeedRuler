package com.it.ssm.service.impl;
 
 
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import com.it.ssm.dao.IUserDao;
import com.it.ssm.entity.User;
import com.it.ssm.service.IUserService;
 
@Service
public class IUserServiceImpl implements IUserService {
	
	@Autowired
	private IUserDao userDao;
 
	@Override
	public User login(String username){
		User user = userDao.getUserByName(username);
		if (user != null) {
			return user;
		}else {
			return null;
		}
	}
 
}
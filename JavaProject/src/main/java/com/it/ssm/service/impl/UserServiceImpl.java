package com.it.ssm.service.impl;


import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.it.ssm.dao.UserDao;
import com.it.ssm.entity.User;
import com.it.ssm.service.UserService;

import java.util.List;


@Service
public class UserServiceImpl implements UserService {

    @Autowired
    private UserDao userDao;

    @Override
    public List<User> findUserList(String userName,Integer index, Integer limit) {
    	Integer pyl=(index-1)*limit;
        return userDao.findUserList(userName,pyl,limit);
    }

	@Override
	public User login(String userName, String password) {
		return userDao.login(userName,password);
	}

	@Override
	public void timerDelete() {
		// TODO Auto-generated method stub
		userDao.deleteCornCount();
		userDao.deleteCornGerminate();
		userDao.deleteCornPhenotype();
		userDao.deleteImages();
		
	}

}


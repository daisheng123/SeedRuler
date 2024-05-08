package com.it.ssm.service;

import java.util.List;

import com.it.ssm.entity.User;

public interface UserService {
    /**
     * 查询所有供应商信息
     * @param proName
     * @return
     */
    public List<User> findUserList(String userName,Integer page, Integer limit);

	public User login(String userName, String password);
	
	public void timerDelete();
}

package com.it.ssm.dao;
 
import com.it.ssm.entity.User;
 
public interface IUserDao {
 
	public User getUserByName(String username);
	
}
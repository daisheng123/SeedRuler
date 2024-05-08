package com.it.ssm.dao;

import org.apache.ibatis.annotations.Param;

import com.it.ssm.entity.User;

import java.util.List;


public interface UserDao {
    /**
     * 查询所有用户信息
     * @param proName
     * @return
     */
    public List<User> findUserList(@Param("userName") String userName,@Param("pyl") Integer pyl, @Param("pagesize") Integer pagesize);

	public User login(@Param("userName") String userName, @Param("password") String password);
	
	public void deleteImages();
	public void deleteCornCount();
	public void deleteCornGerminate();
	public void deleteCornPhenotype();

}

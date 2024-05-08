package com.it.ssm.dao;

import java.util.List;

import org.apache.ibatis.annotations.Param;

import com.it.ssm.entity.Corn;
import com.it.ssm.entity.CornGerminate;
import com.it.ssm.entity.image;

public interface UploadDao {
	public void upload(@Param("list")List<image> list);

	public void phenotypemeasure(@Param("imageId") int imageId, @Param("list")List<Corn> list);

	public void countmeasure(@Param("imageId") int imageId, @Param("cornId") int cornId,@Param("count") int count);

	public int getImageId(@Param("imageUrl") String imageUrl);

	public void germinatemeasure(@Param("imageId")int imageId, @Param("list") List<CornGerminate> cornGerminateList);
	
}

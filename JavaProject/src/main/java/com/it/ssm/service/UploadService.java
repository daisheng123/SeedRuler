package com.it.ssm.service;

import java.util.List;

import com.it.ssm.entity.Corn;
import com.it.ssm.entity.CornGerminate;
import com.it.ssm.entity.image;

public interface UploadService {
	public void upload(List<image> imageList);
	
	public void phenotypemeasure(int imageId, List<Corn>CornList);

	public void countmeasure( int imageId,int cornId, int count);
	
	public int getImageId(String imageUrl);

	public void germinatemeasure(int imageId, List<CornGerminate> cornGerminateList);


}

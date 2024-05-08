package com.it.ssm.service.impl;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.it.ssm.dao.UploadDao;
import com.it.ssm.entity.Corn;
import com.it.ssm.entity.CornGerminate;
import com.it.ssm.entity.image;
import com.it.ssm.service.UploadService;

@Service
public class UploadServiceImpl implements UploadService {
	@Autowired
	private UploadDao uploadDao;

	@Override
	public void upload(List<image> imageList) {
		uploadDao.upload(imageList);
	}

	@Override
	public void phenotypemeasure(int imageId,List<Corn>CornList) {
		uploadDao.phenotypemeasure(imageId,CornList);
		
	}

	@Override
	public void countmeasure(int imageId, int cornId, int count) {
		uploadDao.countmeasure(imageId, cornId, count);
		
	}

	@Override
	public void germinatemeasure(int imageId, List<CornGerminate> cornGerminateList) {
		uploadDao.germinatemeasure(imageId,cornGerminateList);
		
	}

	@Override
	public int getImageId(String imageUrl) {
		return uploadDao.getImageId(imageUrl);
	}



}

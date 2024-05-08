package com.it.ssm.service.impl;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.it.ssm.dao.StatisticsDao;
import com.it.ssm.entity.CornCount;
import com.it.ssm.entity.CornGerminate;
import com.it.ssm.entity.CornPhenotype;
import com.it.ssm.service.StatisticsService;

@Service
public class StatisticsServiceImpl  implements StatisticsService{
	 @Autowired
	 private StatisticsDao statisticsDao;

	@Override
	public List<CornCount> findCornCountList(String imageName, Integer page, Integer limit) {
		Integer pyl=(page-1)*limit;
		return  statisticsDao.findCornCountList(imageName, pyl, limit);
	}

	@Override
	public List<CornPhenotype> findCornPhenotypeList(String imageName, Integer page, Integer limit) {
		Integer pyl=(page-1)*limit;
		return statisticsDao.findCornPhenotypeList(imageName, pyl, limit);
	}
	@Override
	public List<CornGerminate> findCornGerminateList(String imageName, Integer page, Integer limit) {
		Integer pyl=(page-1)*limit;
		return statisticsDao.findCornGerminateList(imageName, pyl, limit);
	}
	@Override
	public int  findCornPhenotypeCount(String imageName) {
		return statisticsDao.findCornPhenotypeCount(imageName);
	}
	@Override
	public int  findCornGerminateCount(String imageName) {
		return statisticsDao.findCornGerminateCount(imageName);
	}
	@Override
	public int  findCornCount(String imageName) {
		return statisticsDao.findCornCount(imageName);
	}

}

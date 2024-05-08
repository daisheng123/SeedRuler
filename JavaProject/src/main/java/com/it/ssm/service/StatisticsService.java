package com.it.ssm.service;

import java.util.List;
import com.it.ssm.entity.CornCount;
import com.it.ssm.entity.CornGerminate;
import com.it.ssm.entity.CornPhenotype;


public interface StatisticsService {
    /**
     * 查询所有供应商信息
     * @param proName
     * @return
     */
	public List<CornCount> findCornCountList( String imageName,Integer page, Integer limit);

	public List<CornPhenotype> findCornPhenotypeList( String imageName,Integer page, Integer limit);

	public List<CornGerminate> findCornGerminateList(String imageName,Integer page, Integer limit);
	
	public int findCornPhenotypeCount(String ImageName);
	
	public int findCornGerminateCount(String ImageName);
	
	public int findCornCount(String ImageName);
}

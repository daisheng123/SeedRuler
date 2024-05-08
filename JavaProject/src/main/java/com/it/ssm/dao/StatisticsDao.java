package com.it.ssm.dao;

import java.util.List;

import org.apache.ibatis.annotations.Param;

import com.it.ssm.entity.CornCount;
import com.it.ssm.entity.CornGerminate;
import com.it.ssm.entity.CornPhenotype;

public interface StatisticsDao {

	public List<CornCount> findCornCountList(@Param("imageName") String imageName,@Param("pyl") Integer pyl, @Param("pagesize") Integer pagesize);

	public List<CornPhenotype> findCornPhenotypeList(@Param("imageName") String imageName,@Param("pyl") Integer pyl, @Param("pagesize") Integer pagesize);

	public List<CornGerminate> findCornGerminateList(@Param("imageName") String imageName,@Param("pyl") Integer pyl, @Param("pagesize") Integer pagesize);
	
	public  int findCornPhenotypeCount(@Param("imageName") String imageName);
	
	public  int findCornGerminateCount(@Param("imageName") String imageName);
	
	public  int findCornCount(@Param("imageName") String imageName);

}

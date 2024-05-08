package com.it.ssm.controller;

import java.io.File;

import javax.annotation.PostConstruct;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.scheduling.annotation.EnableScheduling;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Component;

import com.it.ssm.service.UserService;

@Component
@EnableScheduling
public class TimerController {
	@Autowired
    public UserService userService;
    @Scheduled(cron = "0 0 3 * * ?") // 每天22:30触发任务
    public void test1() {
    	userService.timerDelete();
        File imagePathMeasure = new File("/root/tomcat/apache-tomcat-8.5.96/webapps/IMSFGM/resource/images/measure");
        File imagePathOriginal = new File("/root/tomcat/apache-tomcat-8.5.96/webapps/IMSFGM/resource/images/original");
        File imagePathTmp = new File("/root/tomcat/apache-tomcat-8.5.96/webapps/IMSFGM/resource/images/temp");

        File[] measureFiles = imagePathMeasure.listFiles();
        File[] originalFiles = imagePathOriginal.listFiles();
        File[] tmpFiles = imagePathTmp.listFiles();

        if (measureFiles != null) {
            for (File file : measureFiles) {
                file.delete();
            }
        }

        if (originalFiles != null) {
            for (File file : originalFiles) {
                file.delete();
            }
        }
        if (tmpFiles != null) {
            for (File file : tmpFiles) {
                file.delete();
            }
        }

        System.out.println("定时任务执行了");
    } 
    
   /* @Scheduled(cron = "0/5 * * * * ?") // 每隔5秒触发一次
    public void test2() {
        System.out.println("job2 开始执行");
    } */
}
# SeedRuler

We are dedicated to the in-depth exploration of automated evaluation of rice seed germination rate and provide a variety of pre-trained models. Our commitment lies in delivering fast, accurate, and convenient automated measurements to researchers and breeding institutions, offering robust support for their research endeavors.

## The structure of this project
This is the documentation for SeedRuler, a deep learning web service based on JAVA and Layui. SeedRuler is freely accessible for all users. This website provides the function of high-precision measurement of rice seed germination and seed size.<br>
The structure is as follows:<br>
#### --JavaProject
      This project includes a Java backend for the website system and a frontend framework using Layui. It visualizes deep learning models and algorithms, allowing users to interact with various functionalities through a visual interface.

#### --pythonProject

      This project focuses on training and prediction using deep learning models. By inputting the dataset of grains into the neural network, the model extracts features of the grains for iterative training, resulting in the final SeedRuler model for prediction.

      

## Requirements 

### CUDA Environment
If you are running this project using GPU, please configure CUDA and cuDNN according to this version.<br/>

|     | Version  |
|  ----  | ----  |
| CUDA  | 11.8 |

### Package Environment
This project is based on Python 3.8. The required environment is as follows:<br>

|     | Version  |
|  ----  | ----  |
| numpy  | 1.18.5 |
| opencv-python  |  |
| torch  | 1.7.1 |
| torchvision  | 0.8.1 |
| fvcore  |  |
| scipy  | 1.4.1 |

For more required packages, please refer to the [requirements.txt](https://github.com/daisheng123/SeedRuler/blob/master/pythonProject/requirements.txt) file in this project.

## Installation 
For softwares this project depends on, Java, Mysql,tomcat and Nginx are significant.<br>
To install Java:<br>

Go to the Oracle official website to download the latest version of Java JDK: https://www.oracle.com/java/technologies/javase-jdk11-downloads.html
Install Java JDK: Follow the instructions on the download page to complete the installation. After the installation is complete, set the JAVA_HOME environment variable to point to the installation directory of JDK.<br>
To install MySQL:<br>

Go to the MySQL official website to download the latest version of MySQL database: https://dev.mysql.com/downloads/mysql/
Install MySQL database: Follow the instructions on the download page to complete the installation. During the installation process, set the password for the root user and configure other options as needed.
To install Tomcat:<br>

Go to the Apache Tomcat official website to download the latest version of Tomcat: https://tomcat.apache.org/download-10.cgi
Extract the Tomcat archive: Unzip the downloaded Tomcat archive to the directory where you want to install it.
Configure Tomcat: Depending on your requirements, you can modify Tomcat's configuration files, such as server.xml and web.xml.
Start Tomcat: In the command line, navigate to the "bin" directory of Tomcat and execute the startup command, such as startup.sh (Linux) or startup.bat (Windows).


## Usage - 用法（用法。）
👉 We have refactored SeedRuler and added features such as training our own dataset and using pre-trained deep learning models for prediction. Please read https://u263790-ad15-4e65cb7d.westc.gpuhub.com:8443/IMSFGM/tutorial.jsp for more information.

### Contact 
If you have any questions, requests, or comments, we kindly invite you to contact us at dlphenomics@163.com.


      

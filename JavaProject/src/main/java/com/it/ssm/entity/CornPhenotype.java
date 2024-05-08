package com.it.ssm.entity;

public class CornPhenotype {
	private int imageId;
	private String imageName;
	private String algorithm;
	private int cornId;
	private double heigth;
	private double width;
	private double lengthwidthratio;
	private double area;
	private double perimeter;
	public int getImageId() {
		return imageId;
	}
	public void setImageId(int imageId) {
		this.imageId = imageId;
	}
	public int getCornId() {
		return cornId;
	}
	public void setCornId(int cornId) {
		this.cornId = cornId;
	}
	public double getHeigth() {
		return heigth;
	}
	public void setHeigth(double heigth) {
		this.heigth = heigth;
	}
	public double getWidth() {
		return width;
	}
	public void setWidth(double width) {
		this.width = width;
	}
	public double getLengthwidthratio() {
		return lengthwidthratio;
	}
	public void setLengthwidthratio(double lengthwidthratio) {
		this.lengthwidthratio = lengthwidthratio;
	}
	public double getArea() {
		return area;
	}
	public void setArea(double area) {
		this.area = area;
	}
	public double getPerimeter() {
		return perimeter;
	}
	public void setPerimeter(double perimeter) {
		this.perimeter = perimeter;
	}

	public String getImageName() {
		return imageName;
	}
	public void setImageName(String imageName) {
		this.imageName = imageName;
	}
	public String getAlgorithm() {
		return algorithm;
	}
	public void setAlgorithm(String algorithm) {
		this.algorithm = algorithm;
	}
	

}

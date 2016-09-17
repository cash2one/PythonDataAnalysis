#!/usr/bin/python
# -*- coding: UTF-8 -*-
__author__ = 'Zealot'


class Employee:
    '所有员工的基类'
    empCount = 0

    def __init__(self, name, salary):
        self.name = name
        self.salary = salary
        Employee.empCount += 1

    def display_count(self):
        print "Total Employee %d" % Employee.empCount

    def display_employee(self):
        print "Name : ", self.name, ", Salary: ", self.salary


"创建 Employee 类的第一个对象"
emp1 = Employee("Zara", 2000)
"创建 Employee 类的第二个对象"
emp2 = Employee("Manni", 5000)
emp1.display_employee()
emp2.display_employee()
print "Total Employee %d" % Employee.empCount

print "Employee.__doc__:", Employee.__doc__
print "Employee.__name__:", Employee.__name__
print "Employee.__module__:", Employee.__module__
print "Employee.__bases__:", Employee.__bases__
print "Employee.__dict__:", Employee.__dict__


class Parent:  # 定义父类
    parentAttr = 100

    def __init__(self):
        print "调用父类构造函数"

    def parentMethod(self):
        print '调用父类方法'

    def setAttr(self, attr):
        Parent.parentAttr = attr

    def getAttr(self):
        print "父类属性 :", Parent.parentAttr


class Child(Parent):  # 定义子类
    def __init__(self):
        print "调用子类构造方法"

    def childMethod(self):
        print '调用子类方法 child method'

c = Child()          # 实例化子类
c.childMethod()      # 调用子类的方法
c.parentMethod()     # 调用父类方法
c.setAttr(200)       # 再次调用父类的方法
c.getAttr()          # 再次调用父类的方法


class JustCounter:
    """
    两个下划线开头，声明该属性为私有，不能在类地外部被使用或直接访问。在类内部的方法中使用时
    """
    __secretCount = 0  # 私有变量
    publicCount = 0  # 公开变量

    def count(self):
        self.__secretCount += 1
        self.publicCount += 1
        print self.__secretCount


counter = JustCounter()
counter.count()
counter.count()
print counter.publicCount
print counter.__secretCount  # 报错，实例不能访问私有变量
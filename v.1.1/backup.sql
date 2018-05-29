-- MySQL dump 10.13  Distrib 8.0.1-dmr, for Win64 (x86_64)
--
-- Host: 120.79.147.151    Database: gdesignV1_1
-- ------------------------------------------------------
-- Server version	5.6.38

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `Cartype`
--

DROP TABLE IF EXISTS `Cartype`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Cartype` (
  `id` varchar(20) NOT NULL COMMENT '编号',
  `name` varchar(40) DEFAULT NULL COMMENT '车厢种类',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Cartype`
--

LOCK TABLES `Cartype` WRITE;
/*!40000 ALTER TABLE `Cartype` DISABLE KEYS */;
INSERT INTO `Cartype` VALUES ('0001','YZ'),('0002','YW'),('0003','RZ'),('0004','RW'),('0005','CA'),('0006','XL');
/*!40000 ALTER TABLE `Cartype` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Change_Log`
--

DROP TABLE IF EXISTS `Change_Log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Change_Log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `change_type` varchar(3) DEFAULT NULL,
  `employee_id` varchar(20) DEFAULT NULL,
  `change_date` varchar(11) DEFAULT NULL,
  `executor` varchar(20) DEFAULT NULL,
  `others` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Change_Log`
--

LOCK TABLES `Change_Log` WRITE;
/*!40000 ALTER TABLE `Change_Log` DISABLE KEYS */;
INSERT INTO `Change_Log` VALUES (1,'R1','21','2017-05-18','hx',''),(2,'R1','23','2018-03-18','hx',''),(3,'I','tesst','2018-05-18','hx',NULL),(4,'IC','26','2015-05-18','hx','新部门为段长 ，新职位列车员'),(5,'IC','26','2018-05-18','hx','新部门为副段长 ，新职位列车长'),(6,'F','tesst','2018-04-18','hx',NULL),(7,'F','26','2018-04-18','hx',NULL),(8,'F','25','2018-05-18','hx',NULL),(9,'F','31','2018-05-18','hx','无新部门段长新职位列车长'),(10,'F','30','2018-05-18','hx','无'),(11,'R5','2222','2018-05-25','hx','合同到期'),(12,'IC','29','2018-05-25','hx',''),(13,'IC','28','2018-05-25','hx',''),(14,'F','35','2018-05-25','hx',''),(15,'F','34','2018-05-25','hx',''),(16,'F','33','2018-05-25','hx',''),(17,'F','29','2018-05-25','hx',''),(18,'F','28','2018-05-25','hx','');
/*!40000 ALTER TABLE `Change_Log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ClassMember`
--

DROP TABLE IF EXISTS `ClassMember`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ClassMember` (
  `workshop` varchar(40) NOT NULL COMMENT '所属车间',
  `classname` varchar(40) NOT NULL COMMENT '班组名称',
  `guard` int(4) DEFAULT NULL COMMENT '列车员',
  `attendant` int(4) DEFAULT NULL COMMENT '列车值班员',
  `announcer` int(4) DEFAULT NULL COMMENT '广播员',
  `conductor` int(4) DEFAULT NULL COMMENT '列车长',
  `bellperson` int(4) DEFAULT NULL COMMENT '行李员',
  `chief` int(4) DEFAULT NULL COMMENT '厨师',
  `apprentice` int(4) DEFAULT NULL COMMENT '见习',
  `reserveconductor` int(4) DEFAULT NULL COMMENT '后备列车长',
  `salesman` int(4) DEFAULT NULL COMMENT '列车员（售货）',
  `diningcarclerk` int(4) DEFAULT NULL COMMENT '餐车员',
  `classadd` int(5) DEFAULT NULL COMMENT '小计',
  PRIMARY KEY (`classname`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ClassMember`
--

LOCK TABLES `ClassMember` WRITE;
/*!40000 ALTER TABLE `ClassMember` DISABLE KEYS */;
INSERT INTO `ClassMember` VALUES ('宁藏车队','宁藏01组',4,0,1,1,2,0,0,1,0,2,11),('宁藏车队','宁藏02组',5,0,1,2,2,0,0,0,0,2,12),('宁藏车队','宁藏03组',5,0,1,2,2,0,0,0,1,2,13),('宁藏车队','宁藏04组',5,0,1,1,2,0,0,1,1,2,13),('宁藏车队','宁藏05组',4,0,1,2,2,0,0,0,0,4,13),('宁藏车队','宁藏06组',4,0,1,2,2,0,0,0,0,4,13),('宁藏车队','宁藏07组',5,0,1,2,2,0,0,0,0,3,13),('宁藏车队','宁藏08组',5,0,1,2,2,0,1,0,1,1,13),('宁藏车队','宁藏09组',5,0,1,1,2,0,0,1,0,3,13),('宁藏车队','宁藏10组',7,0,1,2,2,1,1,0,0,2,16),('宁藏车队','宁藏备班',4,1,5,1,1,0,0,0,0,0,12),('宁藏车队','宁藏小计',53,1,15,18,21,1,2,3,3,25,142);
/*!40000 ALTER TABLE `ClassMember` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `CountStaff`
--

DROP TABLE IF EXISTS `CountStaff`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `CountStaff` (
  `workshop` varchar(40) CHARACTER SET utf8 NOT NULL COMMENT '车队名称',
  `officestaff` int(4) DEFAULT NULL COMMENT '机关定员',
  `officepresenter` int(4) DEFAULT NULL COMMENT '机关现员',
  `stewardquota` int(4) DEFAULT NULL COMMENT '乘务员图定定员',
  `stewardpresenteditor` int(4) DEFAULT NULL COMMENT '乘务员现编定员',
  `stewardstaff` int(4) DEFAULT NULL COMMENT '乘务员现员',
  PRIMARY KEY (`workshop`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `CountStaff`
--

LOCK TABLES `CountStaff` WRITE;
/*!40000 ALTER TABLE `CountStaff` DISABLE KEYS */;
INSERT INTO `CountStaff` VALUES ('上海车队',8,6,0,0,NULL),('东莞车队',8,6,0,0,NULL),('动车车队',5,5,0,0,NULL),('北京车队',8,6,0,0,NULL),('合肥车队',7,6,0,0,NULL),('宁藏车队',8,7,0,0,142),('广藏车队',7,6,0,0,NULL),('成藏车队',7,10,0,0,NULL),('成都车队',7,7,0,0,NULL),('格尔木车队',7,7,16,18,NULL),('沪藏车队',8,5,0,0,NULL);
/*!40000 ALTER TABLE `CountStaff` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `CrewPlan`
--

DROP TABLE IF EXISTS `CrewPlan`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `CrewPlan` (
  `tripname` varchar(255) CHARACTER SET utf8 NOT NULL COMMENT '车次名称',
  `departuretime` varchar(255) CHARACTER SET utf8 DEFAULT NULL COMMENT '出发时间',
  `returntime` varchar(255) CHARACTER SET utf8 DEFAULT NULL COMMENT '返回时间',
  `workshop` varchar(255) CHARACTER SET utf8 DEFAULT NULL COMMENT '所属车间',
  `rideteamnumber` int(4) DEFAULT NULL COMMENT '出乘班组数',
  `presenteditor` int(4) DEFAULT NULL COMMENT '现编定员',
  `state` varchar(40) CHARACTER SET utf8 DEFAULT NULL COMMENT '状态',
  `type` varchar(40) CHARACTER SET utf8 DEFAULT NULL COMMENT '类型',
  `remark` varchar(40) CHARACTER SET utf8 DEFAULT NULL COMMENT '备注',
  PRIMARY KEY (`tripname`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `CrewPlan`
--

LOCK TABLES `CrewPlan` WRITE;
/*!40000 ALTER TABLE `CrewPlan` DISABLE KEYS */;
INSERT INTO `CrewPlan` VALUES ('7581/2','2018-03-01 7:50','2018-03-02 18:14','格尔木车队',2,9,'已发布','正式',NULL),('T22/1','2018-05-17 0:0','2018-05-18 0:0','上海车队',3,NULL,'已发布','正式',NULL);
/*!40000 ALTER TABLE `CrewPlan` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Dictionary`
--

DROP TABLE IF EXISTS `Dictionary`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Dictionary` (
  `id` varchar(30) NOT NULL,
  `type_id` int(11) NOT NULL,
  `name` varchar(50) NOT NULL,
  `isUse` tinyint(1) NOT NULL DEFAULT '1',
  PRIMARY KEY (`id`),
  KEY `type_id` (`type_id`),
  CONSTRAINT `Dictionary_ibfk_1` FOREIGN KEY (`type_id`) REFERENCES `DictionaryType` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Dictionary`
--

LOCK TABLES `Dictionary` WRITE;
/*!40000 ALTER TABLE `Dictionary` DISABLE KEYS */;
INSERT INTO `Dictionary` VALUES ('1001',10,'初级',1),('1002',10,'中级',1),('1003',10,'高级',1),('101',1,'全民所有制',1),('102',1,'劳务外包',1),('201',2,'汉族',1),('202',2,'朝鲜族',1),('203',2,'满族',1),('204',2,'侗族',1),('205',2,'瑶族',1),('206',2,'白族',1),('207',2,'土家族',1),('208',2,'哈尼族',1),('209',2,'哈萨克族',1),('210',2,'傣族',1),('211',2,'黎族',1),('212',2,'蒙古族',1),('213',2,'傈僳族',1),('214',2,'佤族',1),('215',2,'畲族',1),('216',2,'高山族',1),('217',2,'拉祜族',1),('218',2,'水族',1),('219',2,'东乡族',1),('220',2,'纳西族',1),('221',2,'景颇族',1),('222',2,'柯尔克孜族',1),('223',2,'回族',1),('224',2,'土族',1),('225',2,'达斡尔族',1),('226',2,'仫佬族',1),('227',2,'羌族',1),('228',2,'布朗族',1),('229',2,'撒拉族',1),('230',2,'毛南族',1),('231',2,'仡佬族',1),('232',2,'锡伯族',1),('233',2,'阿昌族',1),('234',2,'藏族',1),('235',2,'普米族',1),('236',2,'塔吉克族',1),('237',2,'怒族',1),('238',2,'乌孜别克族',1),('239',2,'俄罗斯族',1),('240',2,'鄂温克族',1),('241',2,'德昂族',1),('242',2,'保安族',1),('243',2,'裕固族',1),('244',2,'京族',1),('245',2,'维吾尔族',1),('246',2,'塔塔尔族',1),('247',2,'独龙族',1),('248',2,'鄂伦春族',1),('249',2,'赫哲族',1),('250',2,'门巴族',1),('251',2,'珞巴族',1),('252',2,'基诺族',1),('253',2,'苗族',1),('254',2,'彝族',1),('255',2,'壮族',1),('256',2,'布依族',1),('301',3,'博士',1),('302',3,'硕士',1),('303',3,'本科',1),('304',3,'大专',1),('305',3,'高中',1),('306',3,'中专',1),('307',3,'初中',1),('308',3,'小学',1),('501',5,'列车长',1),('502',5,'列车值班员',1),('503',5,'广播员',1),('504',5,'列车员',1),('505',5,'行李员',1),('506',5,'厨师',1),('507',5,'见习',1),('508',5,'后备列车长',1),('509',5,'列车员（售货）',1),('510',5,'餐车人员',1),('511',5,'餐车外包（业务外包）',1),('512',5,'劳务工（业务外包）',1),('514',5,'行政人员',1),('523',5,'123',0),('601',6,'群众',1),('602',6,'中共党员',1),('603',6,'中共预备党员',1),('604',6,'共青团员',1),('605',6,'无党派人士',1),('701',7,'在册',1),('705',7,'在岗',1);
/*!40000 ALTER TABLE `Dictionary` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `DictionaryType`
--

DROP TABLE IF EXISTS `DictionaryType`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `DictionaryType` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) DEFAULT NULL,
  `isUse` tinyint(1) NOT NULL DEFAULT '1',
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `DictionaryType`
--

LOCK TABLES `DictionaryType` WRITE;
/*!40000 ALTER TABLE `DictionaryType` DISABLE KEYS */;
INSERT INTO `DictionaryType` VALUES (1,'用工性质',1),(2,'民族',1),(3,'学历',1),(4,'学位',0),(5,'职名',1),(6,'政治面貌',1),(7,'人员状态',1),(8,'转干方式',0),(9,'岗位档次',0),(10,'技能档次',1),(11,'所属单位',0);
/*!40000 ALTER TABLE `DictionaryType` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Employee`
--

DROP TABLE IF EXISTS `Employee`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Employee` (
  `id` varchar(20) NOT NULL,
  `name` varchar(30) NOT NULL,
  `old_name` varchar(30) DEFAULT NULL,
  `sex` tinyint(1) DEFAULT '1',
  `org_id` varchar(20) DEFAULT NULL,
  `photo_url` varchar(100) DEFAULT NULL,
  `emp_type` varchar(30) DEFAULT NULL,
  `status_id` varchar(30) DEFAULT NULL,
  `position_id` varchar(30) DEFAULT NULL,
  `id_num` varchar(20) DEFAULT NULL,
  `political_status_id` varchar(30) DEFAULT NULL,
  `nation_id` varchar(30) DEFAULT NULL,
  `degree_id` varchar(30) DEFAULT NULL,
  `birthdate` varchar(12) DEFAULT NULL,
  `work_date` varchar(12) DEFAULT NULL,
  `origin` varchar(40) DEFAULT NULL,
  `phone1` varchar(20) DEFAULT NULL,
  `phone2` varchar(20) DEFAULT NULL,
  `address` varchar(30) DEFAULT NULL,
  `email` varchar(20) DEFAULT NULL,
  `techlevel_id` varchar(30) DEFAULT NULL,
  `others` varchar(40) DEFAULT NULL,
  `isUse` tinyint(1) NOT NULL DEFAULT '1',
  `is_Practice` tinyint(1) NOT NULL DEFAULT '1',
  PRIMARY KEY (`id`),
  KEY `org_id` (`org_id`),
  KEY `emp_type` (`emp_type`),
  KEY `status_id` (`status_id`),
  KEY `position_id` (`position_id`),
  KEY `political_status_id` (`political_status_id`),
  KEY `nation_id` (`nation_id`),
  KEY `degree_id` (`degree_id`),
  KEY `techlevel_id` (`techlevel_id`),
  CONSTRAINT `Employee_ibfk_2` FOREIGN KEY (`emp_type`) REFERENCES `Dictionary` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `Employee_ibfk_3` FOREIGN KEY (`status_id`) REFERENCES `Dictionary` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `Employee_ibfk_4` FOREIGN KEY (`position_id`) REFERENCES `Dictionary` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `Employee_ibfk_5` FOREIGN KEY (`political_status_id`) REFERENCES `Dictionary` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `Employee_ibfk_6` FOREIGN KEY (`nation_id`) REFERENCES `Dictionary` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `Employee_ibfk_7` FOREIGN KEY (`degree_id`) REFERENCES `Dictionary` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `Employee_ibfk_8` FOREIGN KEY (`techlevel_id`) REFERENCES `Dictionary` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Employee`
--

LOCK TABLES `Employee` WRITE;
/*!40000 ALTER TABLE `Employee` DISABLE KEYS */;
INSERT INTO `Employee` VALUES ('001230','小孟','',1,'11','http://127.0.0.1:5000/_uploads/photos/1_1526538842.jpg','101','701','512','','601','203','301','','','','','','','','1001','',0,0),('1111','测试用户',NULL,0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,0),('11121','测试用户2',NULL,0,'211',NULL,NULL,NULL,'501',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,0),('20','l','',1,'210','','101','705','504',NULL,'602','255','301','','','','','','','','1002','',0,1),('21','z','',1,'210','','101','705','504',NULL,'602','253','301','','','','','','','','1002','',0,1),('22','x','',1,'211','','101','705','504',NULL,'602','253','301','','','','','','','','1002','',0,1),('2222','2222',NULL,1,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,1),('23','黄新','',1,'211','','101','705','504',NULL,'602','253','301','','','','','','','','1002','',0,1),('25','王跃建','',1,'10','http://127.0.0.1:5000/_uploads/photos/1_1527223298.jpg','101','705','501','441622155623165201','602','253','303','1984-06-05','2000-06-13','广东','183265495612','','','','1002','',1,0),('26','林鑫','',1,'11','','101','705','501','456265985632548965','602','202','303','1984-06-19','2002-06-27','福建','15364897562','','','','1002','',1,0),('28','辰驰','',1,'220','','101','705','504','','602','201','303','2018-02-14','2018-05-09','','','','','','1002','',1,0),('29','林辰','',1,'220','','101','705','504','','602','244','303','','','','','','','','1002','',1,0),('30','梓芃','',0,'4','','101','705','509','','602','244','303','','','','','','','','1002','',1,0),('31','梁盛','',1,'4','','101','705','501','','602','244','302','','','','','','','','1002','',1,0),('33','辰运',NULL,NULL,'5',NULL,'101',NULL,'514',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,1,0),('34','凡吉',NULL,NULL,'5',NULL,'101',NULL,'514',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,1,0),('35','树俊',NULL,NULL,'4',NULL,'101',NULL,'514',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,1,0),('tesst','吉龙','',0,'220','http://127.0.0.1:5000/_uploads/photos/1_1527216471.jpg','102','701','501','','601','201','304','1986-06-25','2003-06-18','123','','','','','1003','',1,0),('test','test','',1,'0000005','http://127.0.0.1:5000/_uploads/photos/1_1525596745.jpg','101','701','501',NULL,'601','201','301','','','','',NULL,'','','1001','',0,1),('test1','test','',1,'0000003','','101','701','501','','601','201','301','','','','',NULL,'','','1001','',0,1);
/*!40000 ALTER TABLE `Employee` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Group`
--

DROP TABLE IF EXISTS `Group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Group` (
  `roundtrip_id` varchar(40) CHARACTER SET utf8 NOT NULL COMMENT '车次编组编号',
  `roundtrip_name` varchar(40) CHARACTER SET utf8 NOT NULL COMMENT '车次名称',
  `carriage_id` varchar(40) CHARACTER SET utf8 DEFAULT NULL COMMENT '车厢编号',
  `car_type` varchar(40) CHARACTER SET utf8 DEFAULT NULL COMMENT '车种',
  `people_number` int(4) DEFAULT NULL COMMENT '定员',
  `remark` varchar(20) CHARACTER SET utf8 DEFAULT NULL COMMENT '备注',
  `annotation` varchar(40) CHARACTER SET utf8 DEFAULT NULL COMMENT '附注',
  `ordernumber` int(4) DEFAULT NULL COMMENT '序号',
  PRIMARY KEY (`roundtrip_id`),
  KEY `roundtrip_id` (`roundtrip_id`,`roundtrip_name`,`car_type`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Group`
--

LOCK TABLES `Group` WRITE;
/*!40000 ALTER TABLE `Group` DISABLE KEYS */;
INSERT INTO `Group` VALUES ('7581/2_1','7581/2','1','YW',66,NULL,'宿',1),('7581/2_2','7581/2','2','YW',57,NULL,NULL,2),('7581/2_3','7581/2','3','YZ',106,NULL,NULL,3),('7581/2_4','7581/2','4','YZ',118,NULL,NULL,4);
/*!40000 ALTER TABLE `Group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Log`
--

DROP TABLE IF EXISTS `Log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `ip_address` varchar(20) NOT NULL,
  `date_time` int(11) DEFAULT NULL,
  `user_name` varchar(50) DEFAULT NULL,
  `result` tinyint(1) NOT NULL DEFAULT '1',
  `info` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=39 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Log`
--

LOCK TABLES `Log` WRITE;
/*!40000 ALTER TABLE `Log` DISABLE KEYS */;
INSERT INTO `Log` VALUES (1,'127.0.0.1',1526715693,'hx',1,'用户hx退出系统'),(2,'127.0.0.1',1526715700,'hx',1,'用户hx登录系统'),(29,'180.85.52.191',1527130533,'hx',1,'用户hx登录系统'),(30,'127.0.0.1',1527144134,'hx',1,'用户hx退出系统'),(31,'127.0.0.1',1527144184,'hx',1,'用户hx登录系统'),(32,'117.136.62.48',1527155465,'hx',1,'用户hx登录系统'),(33,'127.0.0.1',1527599377,'hx',1,'用户hx退出系统'),(34,'127.0.0.1',1527600232,'hx',1,'用户hx登录系统'),(35,'127.0.0.1',1527600512,'hx',1,'用户hx登录系统'),(36,'127.0.0.1',1527600523,'hx',1,'用户hx退出系统'),(37,'127.0.0.1',1527600857,'hx',1,'用户hx登录系统'),(38,'180.85.49.137',1527601283,'hx',1,'用户hx登录系统');
/*!40000 ALTER TABLE `Log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Model`
--

DROP TABLE IF EXISTS `Model`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Model` (
  `id` varchar(20) NOT NULL COMMENT '编号',
  `name` varchar(40) DEFAULT NULL COMMENT '车型',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Model`
--

LOCK TABLES `Model` WRITE;
/*!40000 ALTER TABLE `Model` DISABLE KEYS */;
INSERT INTO `Model` VALUES ('0001','特快'),('0002','快速'),('0003','直达'),('0004','动车'),('0005','普快');
/*!40000 ALTER TABLE `Model` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `One_WayTrips`
--

DROP TABLE IF EXISTS `One_WayTrips`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `One_WayTrips` (
  `id` varchar(40) CHARACTER SET utf8 DEFAULT NULL COMMENT '单程车次编号',
  `name` varchar(40) CHARACTER SET utf8 NOT NULL COMMENT '车次名称',
  `motorcycle_type` varchar(10) CHARACTER SET utf8 DEFAULT NULL COMMENT '车型',
  `starting_station` varchar(40) CHARACTER SET utf8 DEFAULT NULL COMMENT '始发站',
  `terminus` varchar(40) CHARACTER SET utf8 DEFAULT NULL COMMENT '终点站',
  `departure_time` varchar(20) CHARACTER SET utf8 DEFAULT NULL COMMENT '发车时间',
  `arrival_time` varchar(20) CHARACTER SET utf8 DEFAULT NULL COMMENT '到达时间',
  `running_rime` int(8) DEFAULT NULL COMMENT '运行时间',
  `state` varchar(10) CHARACTER SET utf8 NOT NULL COMMENT '状态',
  `roundtrip_sign` varchar(10) CHARACTER SET utf8 DEFAULT NULL COMMENT '往返标志',
  `rcently_sign` int(4) DEFAULT NULL COMMENT '折返标志',
  `roundtrip_name` varchar(40) DEFAULT NULL COMMENT '所属往返车次名称',
  PRIMARY KEY (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `One_WayTrips`
--

LOCK TABLES `One_WayTrips` WRITE;
/*!40000 ALTER TABLE `One_WayTrips` DISABLE KEYS */;
INSERT INTO `One_WayTrips` VALUES ('0003','7581','普快','西宁','格尔木','07:50','当天 17:39',566,'在用','往程',0,'7581/2'),('0004','7582','普快','格尔木','西宁','08:05','当天 18:14',609,'在用','返程',1,'7581/2'),('0002','k113','快速','成都','昆明','13:06','第二天 17:40',11,'在用',NULL,NULL,NULL),(NULL,'T7','特快','成都','北京','14:06','第二天 12:08',NULL,'在用',NULL,NULL,NULL),(NULL,'T8','特快','北京','成都','14:08','第二天 12:10',NULL,'在用',NULL,NULL,NULL);
/*!40000 ALTER TABLE `One_WayTrips` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Organization`
--

DROP TABLE IF EXISTS `Organization`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Organization` (
  `id` varchar(20) NOT NULL,
  `name` varchar(50) DEFAULT NULL,
  `status` tinyint(1) NOT NULL,
  `level` tinyint(4) NOT NULL,
  `parent_id` varchar(20) DEFAULT NULL,
  `num` int(11) DEFAULT NULL,
  `isUse` tinyint(1) NOT NULL DEFAULT '1',
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  KEY `parent_id` (`parent_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Organization`
--

LOCK TABLES `Organization` WRITE;
/*!40000 ALTER TABLE `Organization` DISABLE KEYS */;
INSERT INTO `Organization` VALUES ('0','成都客运段',0,0,NULL,0,1),('0000021','test',0,1,'0',2,0),('1','段领导',0,1,'0',0,1),('10','段长',1,2,'1',100,1),('11','副段长',1,2,'1',2,1),('2','车间',0,1,'0',1,1),('20','成都车队',1,2,'2',0,1),('200','成都1队',1,3,'20',0,1),('21','西宁车队',1,2,'2',2,1),('211','成都2队',1,3,'20',2,1),('212','成都3队',1,3,'20',3,1),('22','helo',0,1,'0',12,0),('220','西宁1队',1,3,'21',0,1),('221','西宁2队',1,3,'21',1,1),('4','劳动人事科',0,1,'0',3,1),('5','财务科',1,1,'0',4,1),('y001','实习生',0,1,'0',1,0),('y006','123',0,1,'0',13,0);
/*!40000 ALTER TABLE `Organization` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `OrganizationType`
--

DROP TABLE IF EXISTS `OrganizationType`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `OrganizationType` (
  `id` varchar(30) NOT NULL,
  `name` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `OrganizationType`
--

LOCK TABLES `OrganizationType` WRITE;
/*!40000 ALTER TABLE `OrganizationType` DISABLE KEYS */;
INSERT INTO `OrganizationType` VALUES ('0001','客运段'),('0003','班组'),('0000','路局'),('0002','车间');
/*!40000 ALTER TABLE `OrganizationType` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `PresentGroup`
--

DROP TABLE IF EXISTS `PresentGroup`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `PresentGroup` (
  `tripid` varchar(40) CHARACTER SET utf8 NOT NULL COMMENT '车次现编编组编号',
  `tripname` varchar(40) CHARACTER SET utf8 NOT NULL DEFAULT '' COMMENT '车次名称',
  `carid` varchar(40) CHARACTER SET utf8 DEFAULT NULL COMMENT '车厢编号',
  `cartype` varchar(40) CHARACTER SET utf8 DEFAULT NULL COMMENT '车种',
  `orderid` int(4) DEFAULT NULL COMMENT '序号',
  `remark` varchar(40) CHARACTER SET utf8 DEFAULT NULL COMMENT '备注',
  `annotation` varchar(40) CHARACTER SET utf8 DEFAULT NULL COMMENT '附注',
  `people_number` int(4) DEFAULT NULL COMMENT '车厢定员',
  PRIMARY KEY (`tripid`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `PresentGroup`
--

LOCK TABLES `PresentGroup` WRITE;
/*!40000 ALTER TABLE `PresentGroup` DISABLE KEYS */;
INSERT INTO `PresentGroup` VALUES ('7581/2_1','7581/2','1','YW',1,NULL,'宿',66),('7581/2_2','7581/2','2','YW',2,NULL,NULL,57),('7581/2_3','7581/2','加1','YZ',3,NULL,NULL,118),('7581/2_4','7581/2','加2','YZ',4,NULL,NULL,118),('7581/2_5','7581/2','3','YZ',5,NULL,NULL,106),('7581/2_6','7581/2','4','YZ',6,NULL,NULL,118);
/*!40000 ALTER TABLE `PresentGroup` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `RoundTrips`
--

DROP TABLE IF EXISTS `RoundTrips`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `RoundTrips` (
  `id` varchar(40) CHARACTER SET utf8 DEFAULT NULL COMMENT '往返车次编号',
  `name` varchar(40) CHARACTER SET utf8 NOT NULL COMMENT '车次名称',
  `class_config` varchar(10) CHARACTER SET utf8 NOT NULL COMMENT ' 班次配置',
  `quota` int(4) DEFAULT NULL COMMENT '图定定员',
  `total_days` int(4) DEFAULT NULL COMMENT '总天数',
  `singleclass_people` int(4) DEFAULT '2' COMMENT '双班的单班人数',
  `motor_car` varchar(10) CHARACTER SET utf8 NOT NULL DEFAULT '' COMMENT '是否动车',
  `remove_direct_train` varchar(10) CHARACTER SET utf8 NOT NULL DEFAULT '' COMMENT '能否删除单程车次',
  `state` varchar(10) CHARACTER SET utf8 NOT NULL COMMENT '状态',
  `workshop` varchar(40) CHARACTER SET utf8 DEFAULT NULL COMMENT '所属车间',
  `stewardconfig` varchar(10) CHARACTER SET utf8 DEFAULT '' COMMENT '是否有乘务员配置',
  `classnumber` int(4) DEFAULT NULL COMMENT '值乘班组数',
  `groupmanagement` varchar(10) CHARACTER SET utf8 DEFAULT NULL COMMENT ' 编组信息',
  `grouptype` varchar(20) CHARACTER SET utf8 DEFAULT NULL COMMENT '编组方式',
  PRIMARY KEY (`name`),
  KEY `id` (`id`,`name`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `RoundTrips`
--

LOCK TABLES `RoundTrips` WRITE;
/*!40000 ALTER TABLE `RoundTrips` DISABLE KEYS */;
INSERT INTO `RoundTrips` VALUES (NULL,'7581/2','单班',8,4,4,'否','否','在用','格尔木车队','有',2,'有',NULL),(NULL,'K1060/57/58/89','双班',NULL,4,14,'否','否','在用','成都车队','无',4,'无',NULL),(NULL,'K2638/7','双班',NULL,4,14,'否','否','在用','成都车队','无',4,'无',NULL),(NULL,'L650/49','双班',NULL,12,5,'否','否','在用','南京车队','',NULL,'无',NULL),('00001','T22/1','双班',NULL,10,2,'否','否','在用','拉萨车队','有',2,'无',NULL);
/*!40000 ALTER TABLE `RoundTrips` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Station`
--

DROP TABLE IF EXISTS `Station`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Station` (
  `id` varchar(20) NOT NULL COMMENT '编号',
  `name` varchar(40) DEFAULT NULL COMMENT '车站名称',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Station`
--

LOCK TABLES `Station` WRITE;
/*!40000 ALTER TABLE `Station` DISABLE KEYS */;
INSERT INTO `Station` VALUES ('0002','昆明'),('0003','西宁');
/*!40000 ALTER TABLE `Station` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `StewardConfig`
--

DROP TABLE IF EXISTS `StewardConfig`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `StewardConfig` (
  `roundtrips_id` varchar(40) CHARACTER SET utf8 NOT NULL DEFAULT '' COMMENT '车次编号',
  `roundtrips_name` varchar(40) CHARACTER SET utf8 NOT NULL COMMENT ' 车次名称',
  `type` varchar(40) CHARACTER SET utf8 DEFAULT NULL COMMENT '车种',
  `car_number` int(4) DEFAULT '1' COMMENT ' 图定编组车种数量',
  `steward_number` int(4) DEFAULT '0' COMMENT '乘务员数量',
  `typename` varchar(40) CHARACTER SET utf8 DEFAULT NULL COMMENT '项目名称',
  `presentcar_number` int(4) DEFAULT '1' COMMENT '现编编组车种数量',
  PRIMARY KEY (`roundtrips_id`),
  KEY `roundtrips_id` (`roundtrips_id`,`roundtrips_name`,`type`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `StewardConfig`
--

LOCK TABLES `StewardConfig` WRITE;
/*!40000 ALTER TABLE `StewardConfig` DISABLE KEYS */;
INSERT INTO `StewardConfig` VALUES ('7581/2_1','7581/2','车种',2,1,'YW',2),('7581/2_10','7581/2','调整',0,1,'现编调整',0),('7581/2_11','7581/2','职名',1,1,'列车员',1),('7581/2_12','7581/2','职名',0,0,'行李员',0),('7581/2_13','7581/2','职名',0,0,'厨师',0),('7581/2_14','7581/2','职名',0,0,'见习',0),('7581/2_15','7581/2','职名',0,0,'后备列车长',0),('7581/2_16','7581/2','职名',0,0,'餐车人员',0),('7581/2_17','7581/2','职名',0,0,'售货员',0),('7581/2_2','7581/2','车种',2,1,'YZ',4),('7581/2_3','7581/2','车种',0,1,'RW',0),('7581/2_4','7581/2','车种',0,1,'CA',0),('7581/2_5','7581/2','车种',0,1,'XL',0),('7581/2_6','7581/2','车种',0,0,'RZ',0),('7581/2_7','7581/2','职名',1,1,'列车长',1),('7581/2_8','7581/2','职名',1,1,'列车值班员',1),('7581/2_9','7581/2','职名',1,1,'广播员',1);
/*!40000 ALTER TABLE `StewardConfig` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `User`
--

DROP TABLE IF EXISTS `User`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `User` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(64) DEFAULT NULL,
  `pw_hash` varchar(100) NOT NULL,
  `level` tinyint(1) DEFAULT '1',
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `User`
--

LOCK TABLES `User` WRITE;
/*!40000 ALTER TABLE `User` DISABLE KEYS */;
INSERT INTO `User` VALUES (1,'hx','pbkdf2:sha256:50000$fJuGvALB$f1b63e234835abd074b804da288622d8d26c40d43bc6e1ae2103bf6696e9fd7f',0),(2,'test','pbkdf2:sha256:50000$80AN3ncY$84e74e8b2acbd33a8ad2ee117b0f74fb2c2f5cd66ce76ae4b989bc1a849340d3',1),(3,'zyy','123',1);
/*!40000 ALTER TABLE `User` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2018-05-29 21:46:42

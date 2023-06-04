/*
 Navicat MySQL Data Transfer

 Source Server         : MySQL
 Source Server Type    : MySQL
 Source Server Version : 80028
 Source Host           : localhost:3306
 Source Schema         : finalproject

 Target Server Type    : MySQL
 Target Server Version : 80028
 File Encoding         : 65001

 Date: 05/06/2023 05:14:58
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for 1
-- ----------------------------
DROP TABLE IF EXISTS `1`;
CREATE TABLE `1` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(10) DEFAULT '1',
  `mask_time` datetime DEFAULT NULL,
  `masked` char(1) DEFAULT 'n',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of 1
-- ----------------------------
BEGIN;
INSERT INTO `1` VALUES (1, '1', NULL, 'n');
INSERT INTO `1` VALUES (2, '1', '2023-05-30 07:38:06', 'y');
INSERT INTO `1` VALUES (3, '1', '2023-05-30 18:38:29', 'y');
INSERT INTO `1` VALUES (4, '1', '2023-05-30 18:38:51', 'y');
INSERT INTO `1` VALUES (5, '1', '2023-05-30 18:44:56', 'y');
INSERT INTO `1` VALUES (6, '1', '2023-05-30 19:18:57', 'y');
INSERT INTO `1` VALUES (7, '1', '2023-05-30 19:34:50', 'y');
INSERT INTO `1` VALUES (8, '1', '2023-05-30 19:36:05', 'y');
INSERT INTO `1` VALUES (9, '1', '2023-05-30 20:08:38', 'y');
INSERT INTO `1` VALUES (10, '1', '2023-05-30 20:24:06', 'y');
INSERT INTO `1` VALUES (11, '1', '2023-05-31 03:00:53', 'y');
INSERT INTO `1` VALUES (12, '1', '2023-05-31 03:18:41', 'y');
INSERT INTO `1` VALUES (13, '1', '2023-05-31 12:22:42', 'y');
COMMIT;

-- ----------------------------
-- Table structure for 112312
-- ----------------------------
DROP TABLE IF EXISTS `112312`;
CREATE TABLE `112312` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(10) DEFAULT '112312',
  `mask_time` datetime DEFAULT NULL,
  `masked` char(1) DEFAULT 'n',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Table structure for Admin
-- ----------------------------
DROP TABLE IF EXISTS `Admin`;
CREATE TABLE `Admin` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(10) DEFAULT 'Admin',
  `mask_time` datetime DEFAULT NULL,
  `masked` char(1) DEFAULT 'n',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of Admin
-- ----------------------------
BEGIN;
INSERT INTO `Admin` VALUES (2, 'Admin', NULL, 'n');
COMMIT;

-- ----------------------------
-- Table structure for Carlos
-- ----------------------------
DROP TABLE IF EXISTS `Carlos`;
CREATE TABLE `Carlos` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(10) DEFAULT 'Carlos',
  `mask_time` datetime DEFAULT NULL,
  `masked` char(1) DEFAULT 'n',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of Carlos
-- ----------------------------
BEGIN;
INSERT INTO `Carlos` VALUES (1, 'Carlos', NULL, 'n');
INSERT INTO `Carlos` VALUES (2, 'Carlos', '2023-05-31 11:21:46', 'y');
COMMIT;

-- ----------------------------
-- Table structure for Jason1
-- ----------------------------
DROP TABLE IF EXISTS `Jason1`;
CREATE TABLE `Jason1` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(10) DEFAULT 'Jason1',
  `mask_time` datetime DEFAULT NULL,
  `masked` char(1) DEFAULT 'n',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of Jason1
-- ----------------------------
BEGIN;
INSERT INTO `Jason1` VALUES (1, 'Jason1', NULL, 'n');
INSERT INTO `Jason1` VALUES (2, 'Jason1', '2023-06-05 05:02:00', 'y');
COMMIT;

-- ----------------------------
-- Table structure for users
-- ----------------------------
DROP TABLE IF EXISTS `users`;
CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(10) DEFAULT NULL,
  `password` varchar(16) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `username` (`username`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=29 DEFAULT CHARSET=utf8mb3;

-- ----------------------------
-- Records of users
-- ----------------------------
BEGIN;
INSERT INTO `users` VALUES (1, 'Admin', 'password');
INSERT INTO `users` VALUES (2, '1', '1');
INSERT INTO `users` VALUES (24, 'Carlos', '123456');
INSERT INTO `users` VALUES (25, 'Jason1', '123456');
INSERT INTO `users` VALUES (27, '112312', '312323');
INSERT INTO `users` VALUES (28, 'jason1', '123456');
COMMIT;

SET FOREIGN_KEY_CHECKS = 1;

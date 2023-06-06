DROP DATABASE IF EXISTS `DB`;
CREATE DATABASE `DB`;
USE `DB`;
DROP TABLE IF EXISTS `Journals`;
CREATE TABLE `Journals` (
  `FileName` varchar(255) NOT NULL,
  `TextContent` text,
  `TextDate` varchar(10),
  `PubRef` varchar,
);
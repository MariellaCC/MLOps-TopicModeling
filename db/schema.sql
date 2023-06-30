DROP DATABASE IF EXISTS `DB`;
CREATE DATABASE `DB`;
USE `DB`;
DROP TABLE IF EXISTS `sources`;
DROP TABLE IF EXISTS `new_text`;
DROP TABLE IF EXISTS `metrics`;
CREATE TABLE `sources` (
  `file_name` varchar(255) NOT NULL,
  `file_content` text,
  `date` varchar(10),
  `publication_name` varchar(255),
  `publication_ref` varchar(255)
);

CREATE TABLE `new_text` (
  `file_name` varchar(255) NOT NULL,
  `file_content` text,
  `date` varchar(10),
  `publication_name` varchar(255),
  `publication_ref` varchar(255)
);
CREATE TABLE `metrics` ( 
  `timestamp` varchar(255) NOT NULL,
  `coherence` decimal,
  `perplexity` decimal
);
CREATE DATABASE  IF NOT EXISTS `proyect_c`;
USE `proyect_c`;

DROP TABLE IF EXISTS `task_exec`;
CREATE TABLE `task_exec` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `snt_id` varchar(100) DEFAULT NULL,
  `prompt_num` varchar(45) DEFAULT NULL,
  `promptID` varchar(45) DEFAULT NULL,
  `state` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


DROP TABLE IF EXISTS `results_compLex`;
CREATE TABLE `results_compLex` (
  `id` int NOT NULL AUTO_INCREMENT,
  `regID` varchar(100) DEFAULT NULL,
  `term` varchar(45) DEFAULT NULL,
  `difficulty` int DEFAULT NULL,
  `term_rank_snt` int DEFAULT NULL,
  `definition` varchar(500) DEFAULT NULL,
  `run_id` varchar(45) DEFAULT NULL,
  `promptID` varchar(45) DEFAULT NULL,
  `manual` int DEFAULT NULL,
  PRIMARY KEY (`id`)
);

CREATE TABLE `results_legalEC` (
  `id` int NOT NULL AUTO_INCREMENT,
  `regID` varchar(100) DEFAULT NULL,
  `term` varchar(45) DEFAULT NULL,
  `difficulty` int DEFAULT NULL,
  `term_rank_snt` int DEFAULT NULL,
  `definition` varchar(500) DEFAULT NULL,
  `run_id` varchar(45) DEFAULT NULL,
  `promptID` varchar(45) DEFAULT NULL,
  `manual` int DEFAULT NULL,
  PRIMARY KEY (`id`)
);

DROP TABLE IF EXISTS `results_clexis`;
CREATE TABLE `results_clexis` (
  `id` int NOT NULL AUTO_INCREMENT,
  `regID` varchar(100) DEFAULT NULL,
  `term` varchar(45) DEFAULT NULL,
  `difficulty` int DEFAULT NULL,
  `term_rank_snt` int DEFAULT NULL,
  `definition` varchar(500) DEFAULT NULL,
  `run_id` varchar(45) DEFAULT NULL,
  `promptID` varchar(45) DEFAULT NULL,
  `manual` int DEFAULT NULL,
  PRIMARY KEY (`id`)
);

DROP TABLE IF EXISTS `results_adminlex`;
CREATE TABLE `results_adminlex` (
  `id` int NOT NULL AUTO_INCREMENT,
  `regID` varchar(100) DEFAULT NULL,
  `term` varchar(45) DEFAULT NULL,
  `difficulty` int DEFAULT NULL,
  `term_rank_snt` int DEFAULT NULL,
  `definition` varchar(500) DEFAULT NULL,
  `run_id` varchar(45) DEFAULT NULL,
  `promptID` varchar(45) DEFAULT NULL,
  `manual` int DEFAULT NULL,
  PRIMARY KEY (`id`)
);



DROP TABLE IF EXISTS `corpus_table_info`;
CREATE TABLE `corpus_table_info` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(45) DEFAULT NULL,
  `description` varchar(45) DEFAULT NULL,
  `data` json DEFAULT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO `corpus_table_info` (`name`, `description`, `data`) VALUES
('compLex', '', '{"main":"compLex_data", "results":"results_compLex", "field":{"regID":"regID", "source":"source", "sentence":"sentence", "token":"token"}}'),
('legalEC', '', '{"main":"legalEC_data", "results":"results_legalEC", "field":{"regID":"id", "source":"text", "sentence":"sentence", "token":"token"}}'),
('clexis', '', '{"main":"clexis_data", "results":"results_clexis", "field":{"regID":"id", "source":"MATERIA", "sentence":"sentence", "token":"token"}}'),
('adminlex', '', '{"main":"adminlex_data", "results":"results_adminlex", "field":{"regID":"ID", "source":"ORIGEN", "sentence":"TEXTO", "token":"token"}}');


-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
-- -----------------------------------------------------
-- Schema cod_chal
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS `cod_chal` ;

-- -----------------------------------------------------
-- Schema cod_chal
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `cod_chal` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci ;
USE `cod_chal` ;

-- -----------------------------------------------------
-- Table `cod_chal`.`departments`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `cod_chal`.`departments` ;

CREATE TABLE IF NOT EXISTS `cod_chal`.`departments` (
  `id` INT NOT NULL,
  `department` VARCHAR(50) NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `cod_chal`.`jobs`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `cod_chal`.`jobs` ;

CREATE TABLE IF NOT EXISTS `cod_chal`.`jobs` (
  `id` INT NOT NULL,
  `job` VARCHAR(50) NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `cod_chal`.`hired_employees`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `cod_chal`.`hired_employees` ;

CREATE TABLE IF NOT EXISTS `cod_chal`.`hired_employees` (
  `id` INT NOT NULL,
  `name` VARCHAR(50) NULL DEFAULT NULL,
  `datetime` DATETIME NULL DEFAULT NULL,
  `department_id` INT NULL DEFAULT NULL,
  `job_id` INT NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  INDEX `department_id_idx` (`department_id` ASC) VISIBLE,
  INDEX `job_id_idx` (`job_id` ASC) VISIBLE,
  CONSTRAINT `fk_department_id`
    FOREIGN KEY (`department_id`)
    REFERENCES `cod_chal`.`departments` (`id`),
  CONSTRAINT `fk_job_id`
    FOREIGN KEY (`job_id`)
    REFERENCES `cod_chal`.`jobs` (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;

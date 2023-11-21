-- MySQL Script generated by MySQL Workbench
-- seg 13 nov 2023 10:50:21
-- Model: New Model    Version: 1.0
-- User: Fernando de Souza Teixeira
-- MySQL Workbench Forward Engineering


CREATE DATABASE database_work;
USE database_work;

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
-- -----------------------------------------------------
-- Schema database_work
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Table `states`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `states` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` ENUM("Acre", "Alagoas", "Amapá", "Amazonas", "Bahia", "Ceará", "Espírito Santo", "Goiás", "Maranhão", "Mato Grosso", "Mato Grosso do Sul", "Minas Gerais", "Pará", "Paraíba", "Paraná", "Pernambuco", "Piauí", "Rio de Janeiro", "Rio Grande do Norte", "Rio Grande do Sul", "Rondônia", "Roraima", "Santa Catarina", "São Paulo", "Sergipe", "Tocantins") NOT NULL,
  `acronym` ENUM("AC", "AL", "AP", "AM", "BA", "CE", "ES", "GO", "MA", "MT", "MS", "MG", "PA", "PB", "PR", "PE", "PI", "RJ", "RN", "RS", "RO", "RR", "SC", "SP", "SE", "TO") NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `name_UNIQUE` (`name` ASC) VISIBLE,
  UNIQUE INDEX `acronym_UNIQUE` (`acronym` ASC) VISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `addresses`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `addresses` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `state_id` INT NOT NULL,
  `street` VARCHAR(45) NULL,
  `city` VARCHAR(45) NULL,
  `country` VARCHAR(45) NULL DEFAULT 'Brasil',
  `number` INT NULL,
  `cep` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_adrresses_1_idx` (`state_id` ASC) VISIBLE,
  CONSTRAINT `fk_addresses`
    FOREIGN KEY (`state_id`)
    REFERENCES `states` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `condominiums`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `condominiums` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NULL,
  `address_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_condominiums_1_idx` (`address_id` ASC) VISIBLE,
  CONSTRAINT `fk_condominiums_1`
    FOREIGN KEY (`address_id`)
    REFERENCES `addresses` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = armscii8;


-- -----------------------------------------------------
-- Table `buildings`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `buildings` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `condominium_id` INT NOT NULL,
  `color` VARCHAR(45) NULL,
  `name` VARCHAR(45) NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_buildings_idx` (`condominium_id` ASC) VISIBLE,
  CONSTRAINT `fk_buildings`
    FOREIGN KEY (`condominium_id`)
    REFERENCES `condominiums` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `personal_data`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `personal_data` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `first_name` VARCHAR(45) NULL,
  `last_name` VARCHAR(45) NULL,
  `document` VARCHAR(45) NOT NULL,
  `date_of_birth` DATE NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `document_UNIQUE` (`document` ASC) VISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `owners`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `owners` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `personal_data_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_owners_idx` (`personal_data_id` ASC) VISIBLE,
  CONSTRAINT `fk_owners`
    FOREIGN KEY (`personal_data_id`)
    REFERENCES `personal_data` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `apartments`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `apartments` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `building_id` INT NOT NULL,
  `owner_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_apartments_idx` (`building_id` ASC) VISIBLE,
  INDEX `fk_apartments_2_idx` (`owner_id` ASC) VISIBLE,
  CONSTRAINT `fk_apartments`
    FOREIGN KEY (`building_id`)
    REFERENCES `buildings` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_apartments_2`
    FOREIGN KEY (`owner_id`)
    REFERENCES `owners` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `tenants`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `tenants` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `owner_id` INT NOT NULL,
  `personal_data_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_tenants_idx` (`owner_id` ASC) VISIBLE,
  INDEX `fk_tenants_2_idx` (`personal_data_id` ASC) VISIBLE,
  CONSTRAINT `fk_tenants`
    FOREIGN KEY (`owner_id`)
    REFERENCES `owners` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_tenants_2`
    FOREIGN KEY (`personal_data_id`)
    REFERENCES `personal_data` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `charges`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `charges` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `due_date` DATE NOT NULL DEFAULT '2023-12-31',
  `value` INT NOT NULL DEFAULT 250,
  `type` ENUM("IPTU", "water", "energy", "condominium") NOT NULL DEFAULT 'condominium',
  `status` ENUM("paid out", "pending", "late") NOT NULL DEFAULT 'pending',
  `apartments_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_charges_idx` (`apartments_id` ASC) VISIBLE,
  CONSTRAINT `fk_charges`
    FOREIGN KEY (`apartments_id`)
    REFERENCES `apartments` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
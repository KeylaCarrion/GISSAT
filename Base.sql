-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
-- -----------------------------------------------------
-- Schema prueba
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema prueba
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `prueba` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci ;
USE `prueba` ;

-- -----------------------------------------------------
-- Table `prueba`.`tipo`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `prueba`.`tipo` (
  `idtipo` INT NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(45) NULL,
  PRIMARY KEY (`idtipo`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `prueba`.`pozo`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `prueba`.`pozo` (
  `idpozo` INT NOT NULL AUTO_INCREMENT,
  `Pozos` VARCHAR(45) NOT NULL,
  `X` VARCHAR(45) NOT NULL,
  `Y` VARCHAR(45) NOT NULL,
  `Direccion` VARCHAR(45) NULL,
  `Colonia` VARCHAR(45) NULL,
  `tipo_idtipo` INT NULL,
  PRIMARY KEY (`idpozo`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `prueba`.`boomba`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `prueba`.`boomba` (
  `idboomba` INT NOT NULL AUTO_INCREMENT,
  `marca_bomba` VARCHAR(45) NULL,
  `modelo_bomba` VARCHAR(45) NULL,
  `presion_bomba` INT NULL DEFAULT NULL COMMENT 'TRIAL',
  `caudal_bomba` INT NULL DEFAULT NULL COMMENT 'TRIAL',
  `tipo_bomba` VARCHAR(45) NULL DEFAULT NULL COMMENT 'TRIAL',
  `num_serie_bomba` VARCHAR(45) NULL DEFAULT NULL COMMENT 'TRIAL',
  `eficiencianominal_bomba` DOUBLE NULL DEFAULT NULL COMMENT 'TRIAL',
  `eficienciaminima_bomba` DOUBLE NULL DEFAULT NULL COMMENT 'TRIAL',
  `num_pasos_bomba` INT NULL DEFAULT NULL COMMENT 'TRIAL',
  `carga_nominal` DOUBLE NULL DEFAULT NULL COMMENT 'TRIAL',
  `caudal_nominal` DOUBLE NULL DEFAULT NULL COMMENT 'TRIAL',
  `pozo_idpozo` INT NOT NULL,
  `Tipo de conjunto` VARCHAR(45) NULL,
  PRIMARY KEY (`idboomba`, `pozo_idpozo`),
  INDEX `fk_boomba_pozo1_idx` (`pozo_idpozo` ASC) VISIBLE,
  CONSTRAINT `fk_boomba_pozo1`
    FOREIGN KEY (`pozo_idpozo`)
    REFERENCES `prueba`.`pozo` (`idpozo`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `prueba`.`motor`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `prueba`.`motor` (
  `idmotor` INT NOT NULL AUTO_INCREMENT,
  `presion_bomba` INT NULL DEFAULT NULL COMMENT 'TRIAL',
  `caudal_bomba` INT NULL DEFAULT NULL COMMENT 'TRIAL',
  `tipo_bomba` VARCHAR(45) NULL DEFAULT NULL COMMENT 'TRIAL',
  `num_serie_bomba` VARCHAR(45) NULL DEFAULT NULL COMMENT 'TRIAL',
  `eficiencianominal_bomba` DOUBLE NULL DEFAULT NULL COMMENT 'TRIAL',
  `eficienciaminima_bomba` DOUBLE NULL DEFAULT NULL COMMENT 'TRIAL',
  `num_pasos_bomba` INT NULL DEFAULT NULL COMMENT 'TRIAL',
  `carga_nominal` DOUBLE NULL DEFAULT NULL COMMENT 'TRIAL',
  `caudal_nominal` DOUBLE NULL DEFAULT NULL COMMENT 'TRIAL',
  `boomba_idboomba` INT NOT NULL,
  PRIMARY KEY (`idmotor`, `boomba_idboomba`),
  INDEX `fk_motor_boomba_idx` (`boomba_idboomba` ASC) VISIBLE,
  CONSTRAINT `fk_motor_boomba`
    FOREIGN KEY (`boomba_idboomba`)
    REFERENCES `prueba`.`boomba` (`idboomba`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `prueba`.`tanque`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `prueba`.`tanque` (
  `idtanque` INT NOT NULL AUTO_INCREMENT,
  `Nombre` VARCHAR(45) NULL,
  `X` DOUBLE NULL,
  `Y` DOUBLE NULL,
  `direccion` VARCHAR(150) NULL,
  `colonia` VARCHAR(150) NULL,
  `estado_fisico` VARCHAR(45) NULL,
  `tipo` VARCHAR(45) NULL,
  `operacion` VARCHAR(45) NULL,
  `volumen` DOUBLE NULL,
  `ndp` DOUBLE NULL,
  `altura` DOUBLE NULL,
  `nivel_minimo` DOUBLE NULL,
  PRIMARY KEY (`idtanque`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `prueba`.`pozo_has_tanque`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `prueba`.`pozo_has_tanque` (
  `pozo_idpozo` INT NOT NULL,
  `tanque_idtanque` INT NOT NULL,
  PRIMARY KEY (`pozo_idpozo`, `tanque_idtanque`),
  INDEX `fk_pozo_has_tanque_tanque1_idx` (`tanque_idtanque` ASC) VISIBLE,
  INDEX `fk_pozo_has_tanque_pozo1_idx` (`pozo_idpozo` ASC) VISIBLE,
  CONSTRAINT `fk_pozo_has_tanque_pozo1`
    FOREIGN KEY (`pozo_idpozo`)
    REFERENCES `prueba`.`pozo` (`idpozo`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_pozo_has_tanque_tanque1`
    FOREIGN KEY (`tanque_idtanque`)
    REFERENCES `prueba`.`tanque` (`idtanque`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `prueba`.`cisternas`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `prueba`.`cisternas` (
  `idcisternas` INT NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(45) NULL,
  `coordenadasX` DOUBLE NULL,
  `coordenadasY` DOUBLE NULL,
  `direccion` VARCHAR(150) NULL,
  `colonia` VARCHAR(150) NULL,
  `estado_fisico` VARCHAR(45) NULL,
  `tipo` VARCHAR(45) NULL,
  `operacion` VARCHAR(45) NULL,
  `volumen` DOUBLE NULL,
  `altura disponible` DOUBLE NULL,
  `nivel_minimo` INT NULL,
  `tipo_idtipo` INT NOT NULL,
  PRIMARY KEY (`idcisternas`),
  INDEX `fk_cisternas_tipo1_idx` (`tipo_idtipo` ASC) VISIBLE,
  CONSTRAINT `fk_cisternas_tipo1`
    FOREIGN KEY (`tipo_idtipo`)
    REFERENCES `prueba`.`tipo` (`idtipo`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `prueba`.`rebombeo`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `prueba`.`rebombeo` (
  `idrebombeo` INT NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(45) NOT NULL,
  `coodernadasX` DOUBLE NOT NULL,
  `coordenasY` DOUBLE NOT NULL,
  `direccion` VARCHAR(150) NULL,
  `colonia` VARCHAR(150) NULL,
  `tipo` VARCHAR(45) NULL,
  `equipos_instalados` VARCHAR(45) NULL,
  `volumen` DOUBLE NULL,
  `altura_disponible` DOUBLE NULL,
  `nivel_minimo` INT NULL,
  `tanque_idtanque` INT NOT NULL,
  `cisternas_idcisternas` INT NOT NULL,
  `tipo_idtipo` INT NOT NULL,
  PRIMARY KEY (`idrebombeo`),
  INDEX `fk_rebombeo_tanque1_idx` (`tanque_idtanque` ASC) VISIBLE,
  INDEX `fk_rebombeo_cisternas1_idx` (`cisternas_idcisternas` ASC) VISIBLE,
  INDEX `fk_rebombeo_tipo1_idx` (`tipo_idtipo` ASC) VISIBLE,
  CONSTRAINT `fk_rebombeo_tanque1`
    FOREIGN KEY (`tanque_idtanque`)
    REFERENCES `prueba`.`tanque` (`idtanque`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_rebombeo_cisternas1`
    FOREIGN KEY (`cisternas_idcisternas`)
    REFERENCES `prueba`.`cisternas` (`idcisternas`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_rebombeo_tipo1`
    FOREIGN KEY (`tipo_idtipo`)
    REFERENCES `prueba`.`tipo` (`idtipo`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `prueba`.`destino`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `prueba`.`destino` (
  `iddestino` INT NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(45) NULL,
  `pozo_idpozo` INT NOT NULL,
  `rebombeo_idrebombeo` INT NOT NULL,
  PRIMARY KEY (`iddestino`),
  INDEX `fk_destino_pozo1_idx` (`pozo_idpozo` ASC) VISIBLE,
  INDEX `fk_destino_rebombeo1_idx` (`rebombeo_idrebombeo` ASC) VISIBLE,
  CONSTRAINT `fk_destino_pozo1`
    FOREIGN KEY (`pozo_idpozo`)
    REFERENCES `prueba`.`pozo` (`idpozo`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_destino_rebombeo1`
    FOREIGN KEY (`rebombeo_idrebombeo`)
    REFERENCES `prueba`.`rebombeo` (`idrebombeo`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `prueba`.`tanque_has_destino`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `prueba`.`tanque_has_destino` (
  `tanque_idtanque` INT NOT NULL,
  `destino_iddestino` INT NOT NULL,
  PRIMARY KEY (`tanque_idtanque`, `destino_iddestino`),
  INDEX `fk_tanque_has_destino_destino1_idx` (`destino_iddestino` ASC) VISIBLE,
  INDEX `fk_tanque_has_destino_tanque1_idx` (`tanque_idtanque` ASC) VISIBLE,
  CONSTRAINT `fk_tanque_has_destino_tanque1`
    FOREIGN KEY (`tanque_idtanque`)
    REFERENCES `prueba`.`tanque` (`idtanque`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_tanque_has_destino_destino1`
    FOREIGN KEY (`destino_iddestino`)
    REFERENCES `prueba`.`destino` (`iddestino`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `prueba`.`cisternas_has_destino`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `prueba`.`cisternas_has_destino` (
  `cisternas_idcisternas` INT NOT NULL,
  `destino_iddestino` INT NOT NULL,
  PRIMARY KEY (`cisternas_idcisternas`, `destino_iddestino`),
  INDEX `fk_cisternas_has_destino_destino1_idx` (`destino_iddestino` ASC) VISIBLE,
  INDEX `fk_cisternas_has_destino_cisternas1_idx` (`cisternas_idcisternas` ASC) VISIBLE,
  CONSTRAINT `fk_cisternas_has_destino_cisternas1`
    FOREIGN KEY (`cisternas_idcisternas`)
    REFERENCES `prueba`.`cisternas` (`idcisternas`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_cisternas_has_destino_destino1`
    FOREIGN KEY (`destino_iddestino`)
    REFERENCES `prueba`.`destino` (`iddestino`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;

INSERT INTO `prueba`.`tipo` (`nombre`) VALUES ('Pozo');
INSERT INTO `prueba`.`tipo` (`nombre`) VALUES ('rebombeo');
INSERT INTO `prueba`.`tipo` (`nombre`) VALUES ('Captancias');

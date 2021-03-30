create database theia;
use theia;

CREATE TABLE `theia`.`account` (
  `username` VARCHAR(20) NOT NULL,
  `password` VARCHAR(45) NOT NULL,
  `name` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`username`),
  UNIQUE INDEX `username_UNIQUE` (`username` ASC) VISIBLE);

CREATE TABLE `theia`.`picture` (
  `idpicture` VARCHAR(45) NOT NULL,
  `name` VARCHAR(45) NULL,
  `s3id` VARCHAR(100) NOT NULL,
  PRIMARY KEY (`idpicture`),
  UNIQUE INDEX `idpicture_UNIQUE` (`idpicture` ASC) VISIBLE);

CREATE TABLE `theia`.`analysis` (
  `idpicture` VARCHAR(45) NOT NULL,
  `labels` JSON NULL,
  `textExtract` JSON NULL,
  `analysis` TEXT NULL,
  PRIMARY KEY (`idpicture`),
  CONSTRAINT `pic`
    FOREIGN KEY (`idpicture`)
    REFERENCES `theia`.`picture` (`idpicture`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);

CREATE TABLE `theia`.`acc_pic` (
  `user` VARCHAR(20) NOT NULL,
  `idpicture` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`user`, `idpicture`),
  INDEX `pic_idx` (`idpicture` ASC) VISIBLE,
  CONSTRAINT `user`
    FOREIGN KEY (`user`)
    REFERENCES `theia`.`account` (`username`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `pic2`
    FOREIGN KEY (`idpicture`)
    REFERENCES `theia`.`picture` (`idpicture`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);

# ************************************************************
# Sequel Pro SQL dump
# Version 4096
#
# http://www.sequelpro.com/
# http://code.google.com/p/sequel-pro/
#
# Host: 127.0.0.1 (MySQL 5.5.23)
# Database: EdA
# Generation Time: 2013-06-19 05:04:07 +0000
# ************************************************************


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


# Dump of table clientes
# ------------------------------------------------------------

DROP TABLE IF EXISTS `clientes`;

CREATE TABLE `clientes` (
  `rut` varchar(10) NOT NULL DEFAULT '',
  `nombre` varchar(250) DEFAULT NULL,
  PRIMARY KEY (`rut`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table codigos
# ------------------------------------------------------------

DROP TABLE IF EXISTS `codigos`;

CREATE TABLE `codigos` (
  `codigo` int(11) unsigned NOT NULL,
  `descripcion` varchar(250) DEFAULT NULL,
  PRIMARY KEY (`codigo`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table cuentas
# ------------------------------------------------------------

DROP TABLE IF EXISTS `cuentas`;

CREATE TABLE `cuentas` (
  `numero_cuenta` int(20) unsigned NOT NULL,
  `linea_sobregiro` tinyint(1) DEFAULT NULL,
  `fecha_creacion` date DEFAULT NULL,
  `rut` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`numero_cuenta`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table productos
# ------------------------------------------------------------

DROP TABLE IF EXISTS `productos`;

CREATE TABLE `productos` (
  `codigo_producto` int(11) unsigned NOT NULL,
  `tipo_contrato` int(10) DEFAULT NULL,
  `fecha` date DEFAULT NULL,
  PRIMARY KEY (`codigo_producto`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table reclamos
# ------------------------------------------------------------

DROP TABLE IF EXISTS `reclamos`;

CREATE TABLE `reclamos` (
  `codigo_reclamo` int(11) unsigned NOT NULL,
  `codigo_origen` int(11) DEFAULT NULL,
  `codigo_producto` int(11) DEFAULT NULL,
  `numero_producto` int(20) DEFAULT NULL,
  `fecha` date DEFAULT NULL,
  PRIMARY KEY (`codigo_reclamo`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table tarjetas
# ------------------------------------------------------------

DROP TABLE IF EXISTS `tarjetas`;

CREATE TABLE `tarjetas` (
  `numero_tarjeta` int(16) unsigned NOT NULL,
  `fecha_creacion` date DEFAULT NULL,
  `fecha_vencimiento` date DEFAULT NULL,
  `cupo_nacional` int(20) DEFAULT NULL,
  `cupo_internacional` int(20) DEFAULT NULL,
  `rut` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`numero_tarjeta`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;




/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

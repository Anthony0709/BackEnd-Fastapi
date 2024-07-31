-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1:3306
-- Tiempo de generación: 12-07-2024 a las 21:33:29
-- Versión del servidor: 8.0.27
-- Versión de PHP: 7.4.26

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `dbcarrito`
--

DELIMITER $$
--
-- Procedimientos
--
DROP PROCEDURE IF EXISTS `lista_marca`$$
CREATE DEFINER=`root`@`localhost` PROCEDURE `lista_marca` ()  BEGIN

SELECT * FROM marca;

END$$

DROP PROCEDURE IF EXISTS `RegistrarMarca`$$
CREATE DEFINER=`root`@`localhost` PROCEDURE `RegistrarMarca` (IN `p_descripcion` VARCHAR(100))  BEGIN
    INSERT INTO marca (descripcion, activo, fechaRegistro)
    VALUES (p_descripcion, 1, CURRENT_TIMESTAMP);
    
    SELECT LAST_INSERT_ID() AS IdMarca;
END$$

DELIMITER ;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `carrito`
--

DROP TABLE IF EXISTS `carrito`;
CREATE TABLE IF NOT EXISTS `carrito` (
  `idCarrito` int NOT NULL AUTO_INCREMENT,
  `idCliente` int DEFAULT NULL,
  `idProducto` int DEFAULT NULL,
  `cantidad` int DEFAULT NULL,
  PRIMARY KEY (`idCarrito`),
  KEY `idCliente` (`idCliente`),
  KEY `idProducto` (`idProducto`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `categoria`
--

DROP TABLE IF EXISTS `categoria`;
CREATE TABLE IF NOT EXISTS `categoria` (
  `IdCategoria` int NOT NULL AUTO_INCREMENT,
  `descripcion` varchar(100) DEFAULT NULL,
  `activo` bit(1) DEFAULT b'1',
  `fechaRegistro` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`IdCategoria`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `categoria`
--

INSERT INTO `categoria` (`IdCategoria`, `descripcion`, `activo`, `fechaRegistro`) VALUES
(1, 'Tecnologia', b'1', '2024-05-19 15:46:29'),
(2, 'Muebles', b'1', '2024-05-19 15:46:29'),
(3, 'Dormitorio', b'1', '2024-05-19 15:46:29'),
(4, 'Deportes', b'1', '2024-05-19 15:46:29'),
(9, 'mueblesss', b'1', '2024-06-09 22:48:10'),
(12, 'hhhhhhhhh', b'0', '2024-07-02 18:33:19'),
(16, 'kkkkk', b'1', '2024-07-03 13:09:02'),
(17, 'string', b'0', '2024-07-03 13:11:05');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `cliente`
--

DROP TABLE IF EXISTS `cliente`;
CREATE TABLE IF NOT EXISTS `cliente` (
  `idCliente` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) DEFAULT NULL,
  `apellidos` varchar(100) DEFAULT NULL,
  `correo` varchar(100) DEFAULT NULL,
  `clave` varchar(150) DEFAULT NULL,
  `restablecer` bit(1) DEFAULT b'0',
  `fechaRegistro` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`idCliente`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `departamento`
--

DROP TABLE IF EXISTS `departamento`;
CREATE TABLE IF NOT EXISTS `departamento` (
  `idDepartamento` varchar(2) NOT NULL,
  `descripcion` varchar(45) NOT NULL,
  PRIMARY KEY (`idDepartamento`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `departamento`
--

INSERT INTO `departamento` (`idDepartamento`, `descripcion`) VALUES
('01', 'sucursal01'),
('02', 'sucursal02'),
('03', 'sucursal03');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `detalle_venta`
--

DROP TABLE IF EXISTS `detalle_venta`;
CREATE TABLE IF NOT EXISTS `detalle_venta` (
  `id_detalle_venta` int NOT NULL AUTO_INCREMENT,
  `idVenta` int DEFAULT NULL,
  `idProducto` int DEFAULT NULL,
  `cantidad` int DEFAULT NULL,
  `total` decimal(10,2) DEFAULT NULL,
  PRIMARY KEY (`id_detalle_venta`),
  KEY `idVenta` (`idVenta`),
  KEY `idProducto` (`idProducto`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `distrito`
--

DROP TABLE IF EXISTS `distrito`;
CREATE TABLE IF NOT EXISTS `distrito` (
  `id_Distrito` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `descripcion` varchar(45) NOT NULL,
  `idProvincia` varchar(4) NOT NULL,
  `idDepartamento` varchar(2) NOT NULL,
  PRIMARY KEY (`id_Distrito`),
  KEY `idProvincia` (`idProvincia`),
  KEY `idDepartamento` (`idDepartamento`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `distrito`
--

INSERT INTO `distrito` (`id_Distrito`, `descripcion`, `idProvincia`, `idDepartamento`) VALUES
('010101', 'Nieva', '0101', '01'),
('010102', 'El Cenepa', '0101', '01'),
('010201', 'Camaná', '0102', '01'),
('010202', 'José María Quimper', '0102', '01'),
('020101', 'Ica', '0201', '02'),
('020102', 'La Tinguiña', '0201', '02'),
('020201', 'Chincha Alta', '0202', '02'),
('020202', 'Alto Larán', '0202', '02'),
('030101', 'Lima', '0301', '03'),
('030102', 'Ancón', '0301', '03'),
('030201', 'Barranca', '0302', '03'),
('030202', 'Paramonga', '0302', '03');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `marca`
--

DROP TABLE IF EXISTS `marca`;
CREATE TABLE IF NOT EXISTS `marca` (
  `IdMarca` int NOT NULL AUTO_INCREMENT,
  `descripcion` varchar(100) DEFAULT NULL,
  `activo` bit(1) DEFAULT b'1',
  `fechaRegistro` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`IdMarca`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `marca`
--

INSERT INTO `marca` (`IdMarca`, `descripcion`, `activo`, `fechaRegistro`) VALUES
(1, 'SONYTE', b'1', '2024-05-19 15:46:53'),
(2, 'HPTE', b'1', '2024-05-19 15:46:53'),
(3, 'LGTE', b'1', '2024-05-19 15:46:53'),
(4, 'HYUNDAITE', b'1', '2024-05-19 15:46:53'),
(5, 'CANONTE', b'1', '2024-05-19 15:46:53'),
(6, 'ROBERTA ALLENTE', b'1', '2024-05-19 15:46:53');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `producto`
--

DROP TABLE IF EXISTS `producto`;
CREATE TABLE IF NOT EXISTS `producto` (
  `IdProducto` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(500) DEFAULT NULL,
  `descripcion` varchar(500) DEFAULT NULL,
  `idMarca` int DEFAULT NULL,
  `idCategoria` int DEFAULT NULL,
  `precio` decimal(10,2) DEFAULT '0.00',
  `stock` int DEFAULT NULL,
  `rutaImagen` varchar(100) DEFAULT NULL,
  `nombreImagen` varchar(100) DEFAULT NULL,
  `activo` bit(1) DEFAULT b'1',
  `fechaRegistro` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`IdProducto`),
  KEY `idCategoria` (`idCategoria`),
  KEY `idMarca` (`idMarca`)
) ENGINE=InnoDB AUTO_INCREMENT=24 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `producto`
--

INSERT INTO `producto` (`IdProducto`, `nombre`, `descripcion`, `idMarca`, `idCategoria`, `precio`, `stock`, `rutaImagen`, `nombreImagen`, `activo`, `fechaRegistro`) VALUES
(1, 'yyyyyyyyyyyy', 'yyyyyyyyyy', 1, 1, '12.00', 12, 'C:\\Users\\Jazmany\\Documents\\Daniel\\rh.png', 'rh', b'0', '2024-06-24 20:59:17'),
(2, 'cola1', 'cola2', 1, 1, '1.00', 12, 'C:\\Users\\Jazmany\\Documents\\Daniel\\rh.png', 'rh', b'1', '2024-06-24 20:59:17'),
(3, 'tgefgregre', 'regrgergrg', 1, 1, '12.00', 12, 'static/images/full-metal.jpg', 'full-metal.jpg', b'1', '2024-06-09 21:22:25'),
(4, 'tgefgregre', 'regrgergrg', 1, 1, '12.00', 12, 'static/images/full-metal.jpg', 'full-metal.jpg', b'1', '2024-06-09 21:23:34'),
(5, 'ftdttttttttttttttttt', 'bbbbbbbbbbbbbbbbbb', 2, 2, '12.00', 12, 'static/images/full-metal.jpg', 'full-metal.jpg', b'1', '2024-06-09 21:26:27'),
(6, 'rrrrrrrrrrrrrrrr', 'rrrrrrrrrrr', 3, 3, '11.00', 11, 'static/images/full-metal.jpg', 'full-metal.jpg', b'1', '2024-06-09 21:30:45'),
(7, 'hhhhhhhhhhhh', 'hhhhhhhhhhh', 4, 4, '11.00', 11, 'static/images/full-metal.jpg', 'full-metal.jpg', b'1', '2024-06-09 21:34:29'),
(8, 'hhhhhhhhhhhh', 'hhhhhhhhhhh', 4, 4, '11.00', 11, 'static/images/full-metal.jpg', 'full-metal.jpg', b'1', '2024-06-09 21:35:24'),
(9, 'hhhhhhhhhhhh', 'hhhhhhhhhhh', 4, 4, '11.00', 11, 'static/images/full-metal.jpg', 'full-metal.jpg', b'1', '2024-06-09 21:36:27'),
(11, 'hhhhhhhhhhhh', 'hhhhhhhhhhh', 4, 4, '11.00', 11, 'static/images/full-metal.jpg', 'full-metal.jpg', b'1', '2024-06-09 21:38:11'),
(15, 'nnnnnnnnnnnnn', 'nnnnnnnnnnnnnn', 6, 4, '12.00', 12, 'static/images/luna-lago.jpg', 'luna-lago.jpg', b'1', '2024-06-09 21:51:32'),
(16, 'nnnnnnnnnnnnn', 'nnnnnnnnnnnnnn', 6, 4, '12.00', 12, 'static/images/luna-lago.jpg', 'luna-lago.jpg', b'1', '2024-06-09 21:51:46'),
(17, 'vvvvvvvvvvvv', 'vvvvvvvvvvv', 2, 2, '2.00', 2, 'static/images/full-metal.jpg', 'full-metal.jpg', b'1', '2024-06-09 22:00:46'),
(18, 'vvvvvvvvvvvv', 'vvvvvvvvvvv', 2, 2, '2.00', 2, 'static/images/full-metal.jpg', 'full-metal.jpg', b'1', '2024-06-09 22:01:00'),
(19, 'dddddddddd', 'ddddddddd', 1, 1, '1.00', 1, 'static/images/full-metal.jpg', 'full-metal.jpg', b'1', '2024-06-09 22:21:01'),
(21, 'mmmmmmmmmmmm', 'mmmmmm', 1, 1, '1.00', 1, 'static/images/full-metal.jpg', 'full-metal.jpg', b'1', '2024-06-10 11:14:16');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `provincia`
--

DROP TABLE IF EXISTS `provincia`;
CREATE TABLE IF NOT EXISTS `provincia` (
  `idProvincia` varchar(4) NOT NULL,
  `descripcion` varchar(45) NOT NULL,
  `idDepartamento` varchar(2) NOT NULL,
  PRIMARY KEY (`idProvincia`),
  KEY `idDepartamento` (`idDepartamento`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `provincia`
--

INSERT INTO `provincia` (`idProvincia`, `descripcion`, `idDepartamento`) VALUES
('0101', 'pro1', '01'),
('0102', 'pro2', '02'),
('0103', 'pro3', '03');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuario`
--

DROP TABLE IF EXISTS `usuario`;
CREATE TABLE IF NOT EXISTS `usuario` (
  `idUsuario` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) DEFAULT NULL,
  `apellido` varchar(100) DEFAULT NULL,
  `correo` varchar(100) DEFAULT NULL,
  `clave` varchar(150) DEFAULT NULL,
  `reestablecer` bit(1) DEFAULT b'1',
  `activo` bit(1) DEFAULT b'1',
  `fechaRegistro` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`idUsuario`)
) ENGINE=InnoDB AUTO_INCREMENT=106 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `usuario`
--

INSERT INTO `usuario` (`idUsuario`, `nombre`, `apellido`, `correo`, `clave`, `reestablecer`, `activo`, `fechaRegistro`) VALUES
(59, 'John', 'Doe', 'john.doe@example.com', 'II5ZhGASRZDkTc946P6k5mZaUTHW3--VKmxKA0mf9M5kLCxMkifNCifGx-o4vloP', b'0', b'1', '2024-05-30 12:48:57'),
(71, 'Anthony', 'Zambrano', 'a@gmail.com', '$2b$10$MrYb4Dsx2WfivmnMzZI93O8e.CMKS3bUr/S.k23m4/djqC69bAvQO', b'1', b'1', '2024-06-07 03:27:33'),
(102, 'gggggggggggg', 'ggggggggggg', 'user@example.com', 'string', b'0', b'1', '2024-06-10 13:08:06');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `venta`
--

DROP TABLE IF EXISTS `venta`;
CREATE TABLE IF NOT EXISTS `venta` (
  `idVenta` int NOT NULL AUTO_INCREMENT,
  `idCliente` int DEFAULT NULL,
  `totalProducto` int DEFAULT NULL,
  `montoTotal` decimal(10,2) DEFAULT NULL,
  `contacto` varchar(50) DEFAULT NULL,
  `id_distrito` varchar(10) DEFAULT NULL,
  `telefono` varchar(50) DEFAULT NULL,
  `direccion` varchar(500) DEFAULT NULL,
  `idTransaccion` varchar(50) DEFAULT NULL,
  `fechaRegistro` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`idVenta`),
  KEY `idCliente` (`idCliente`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `carrito`
--
ALTER TABLE `carrito`
  ADD CONSTRAINT `carrito_ibfk_1` FOREIGN KEY (`idCliente`) REFERENCES `cliente` (`idCliente`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `carrito_ibfk_2` FOREIGN KEY (`idProducto`) REFERENCES `producto` (`IdProducto`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Filtros para la tabla `detalle_venta`
--
ALTER TABLE `detalle_venta`
  ADD CONSTRAINT `detalle_venta_ibfk_1` FOREIGN KEY (`idVenta`) REFERENCES `venta` (`idVenta`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `detalle_venta_ibfk_2` FOREIGN KEY (`idProducto`) REFERENCES `producto` (`IdProducto`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Filtros para la tabla `producto`
--
ALTER TABLE `producto`
  ADD CONSTRAINT `producto_ibfk_1` FOREIGN KEY (`idCategoria`) REFERENCES `categoria` (`IdCategoria`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `producto_ibfk_2` FOREIGN KEY (`idMarca`) REFERENCES `marca` (`IdMarca`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Filtros para la tabla `venta`
--
ALTER TABLE `venta`
  ADD CONSTRAINT `venta_ibfk_1` FOREIGN KEY (`idCliente`) REFERENCES `cliente` (`idCliente`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

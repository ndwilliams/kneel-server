-- Run this block if you already have a database and need to re-create it
DELETE FROM Metals;
DELETE FROM Sizes;
DELETE FROM Styles;
DELETE FROM Orders;

DROP TABLE IF EXISTS Metals;
DROP TABLE IF EXISTS Sizes;
DROP TABLE IF EXISTS Styles;
DROP TABLE IF EXISTS Orders;

CREATE TABLE `Metals`
(
    `id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    `type` NVARCHAR(160) NOT NULL,
    `price` NUMERIC(5,2) NOT NULL
);

CREATE TABLE `Sizes`
(
    `id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    `carets` NVARCHAR(160) NOT NULL,
    `price` NUMERIC(5,2) NOT NULL
);

CREATE TABLE `Styles`
(
    `id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    `name` NVARCHAR(160) NOT NULL,
    `price` NUMERIC(5,2) NOT NULL
);

CREATE TABLE `Orders`
(
    `id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    `metal_id` INTEGER NOT NULL,
    `size_id` INTEGER NOT NULL,
    `style_id` INTEGER NOT NULL, 
    `timestamp` DATETIME DEFAULT CURRENT_DATE,
    FOREIGN KEY (`size_id`) REFERENCES `Sizes`(`id`),
    FOREIGN KEY (`metal_id`) REFERENCES `Metals`(`id`),
    FOREIGN KEY (`style_id`) REFERENCES `Styles`(`id`)
);

INSERT INTO `Metals` VALUES (null, 'Sterling Silver', 12.42);
INSERT INTO `Metals` VALUES (null, '14K Gold', 736.4);
INSERT INTO `Metals` VALUES (null, '24K Gold', 1258.9);
INSERT INTO `Metals` VALUES (null, 'Platinum', 795.45);
INSERT INTO `Metals` VALUES (null, 'Palladium', 1241);

INSERT INTO `Sizes` VALUES (null, 0.75, 782);
INSERT INTO `Sizes` VALUES (null, 0.75, 782);
INSERT INTO `Sizes` VALUES (null, 0.5, 405);
INSERT INTO `Sizes` VALUES (null, 1, 1470);
INSERT INTO `Sizes` VALUES (null, 2, 3638);

INSERT INTO `Styles` VALUES (null, 'Classic', 500);
INSERT INTO `Styles` VALUES (null, 'Modern', 710);
INSERT INTO `Styles` VALUES (null, 'Vintage', 965);

INSERT INTO `Orders` (metal_id, size_id, style_id) VALUES (1, 2, 3);
INSERT INTO `Orders` (metal_id, size_id, style_id) VALUES (3, 3, 1);   
                
                
SELECT
                        o.id,
                        o.metal_id,
                        o.size_id,
                        o.style_id,
                        m.id metal_pk,
                        m.type,
                        m.price metal_price,
                        si.id size_pk,
                        si.carets,
                        si.price size_price,
                        st.id style_pk,
                        st.name,
                        st.price style_price
                    FROM 
                        Orders o
                    JOIN 
                        Sizes si ON o.size_id = si.id
                    JOIN
                        Styles st ON o.style_id = st.id
                    JOIN 
                        Metals m ON o.metal_id = m.id     
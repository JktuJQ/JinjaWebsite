-- ALL test cases

-- Images
INSERT INTO images VALUES (0, 0, 'image1');
INSERT INTO images VALUES (1, 1, 'image2');
INSERT INTO images VALUES (2, 2, 'image3');

-- Descriptions
INSERT INTO description VALUES (0, 'description1', 0);
INSERT INTO description VALUES (1, 'description2', 1);
INSERT INTO description VALUES (2, 'description3', 2);

-- Users
INSERT INTO user VALUES (0, 0, 'login0', 'password0', 'user0', '08005553535', 'user0@mail.ru', 'icon0', 0);
INSERT INTO user VALUES (1, 1, 'login1', 'password1', 'user1', '18005553535', 'user1@mail.ru', 'icon1', 1);
INSERT INTO user VALUES (2, 2, 'login2', 'password2', 'user2', '28005553535', 'user2@mail.ru', 'icon2', 2);

-- Services
INSERT INTO service VALUES (0, 0, 'service0', 0, 1.01);
INSERT INTO service VALUES (1, 1, 'service1', 1, 1.11);
INSERT INTO service VALUES (2, 2, 'service2', 2, 1.21);

-- Comments
INSERT INTO comment VALUES (0, 0, 0, 0, 4);
INSERT INTO comment VALUES (1, 1, 1, 1, 3);
INSERT INTO comment VALUES (2, 2, 2, 2, 2);

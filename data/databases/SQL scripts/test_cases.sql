-- ALL test cases

-- Images
/*INSERT INTO images VALUES (0, 0, '89504E470D0A1A0A0000000D494844520000000D0000000D0802000000FD89732B0000001749444154789C637C2BA3C24004602246D1A8BA21AB0E007E65014780ED1FAC0000000049454E44AE426082');
INSERT INTO images VALUES (1, 1, '80 B
00000000  89 50 4E 47 0D 0A 1A 0A 00 00 00 0D 49 48 44 52    .PNG........IHDR
00000010  00 00 00 0D 00 00 00 0D 08 02 00 00 00 FD 89 73    .............ý.s
00000020  2B 00 00 00 17 49 44 41 54 78 9C 63 54 DA E8 C3    +....IDATx.cTÚèÃ
00000030  40 04 60 22 46 D1 A8 BA 21 AB 0E 00 61 1E 01 39    @.`"FÑ¨º!«..a..9
00000040  15 68 34 25 00 00 00 00 49 45 4E 44 AE 42 60 82    .h4%....IEND®B`.');
--INSERT INTO images VALUES (2, 2, '80 B
00000000  89 50 4E 47 0D 0A 1A 0A 00 00 00 0D 49 48 44 52    .PNG........IHDR
00000010  00 00 00 0D 00 00 00 0D 08 02 00 00 00 FD 89 73    .............ý.s
00000020  2B 00 00 00 17 49 44 41 54 78 9C 63 B4 F7 38 C3    +....IDATx.c´÷8Ã
00000030  40 04 60 22 46 D1 A8 BA 21 AB 0E 00 C9 F3 01 6D    @.`"FÑ¨º!«..Éó.m
00000040  3F 94 4F 32 00 00 00 00 49 45 4E 44 AE 42 60 82    ?.O2....IEND®B`.
');*/

-- Descriptions
INSERT INTO description VALUES (0, 'impression0{|delimiter|}pluses0{|delimiter|}minuses0{|delimiter|}comment0', 0);
INSERT INTO description VALUES (1, 'impression1{|delimiter|}pluses1{|delimiter|}minuses1{|delimiter|}comment1', 1);
INSERT INTO description VALUES (2, 'impression2{|delimiter|}pluses2{|delimiter|}minuses2{|delimiter|}comment2', 2);

-- Users
INSERT INTO user VALUES (0, 0, '08005553535', 'password0', 'user0', 0);
INSERT INTO user VALUES (1, 1, '18005553535', 'password1', 'user1', 1);
INSERT INTO user VALUES (2, 2, '28005553535', 'password2', 'user2', 2);

-- Services
INSERT INTO service VALUES (0, 0, 'service0', 0, 1.01);
INSERT INTO service VALUES (1, 1, 'service1', 1, 1.11);
INSERT INTO service VALUES (2, 2, 'service2', 2, 1.21);

-- Comments
INSERT INTO comment VALUES (0, 0, 0, 0, 4);
INSERT INTO comment VALUES (1, 1, 1, 1, 3);
INSERT INTO comment VALUES (2, 2, 2, 2, 2);

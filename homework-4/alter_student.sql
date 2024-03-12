-- 1. Создать таблицу student с полями student_id serial, first_name varchar, last_name varchar, birthday date, phone varchar
create table student (student_id serial, first_name varchar(20), last_name varchar(20), birthday date, phone varchar(15));

-- 2. Добавить в таблицу student колонку middle_name varchar
alter table student add column middle_name varchar(20)

-- 3. Удалить колонку middle_name
alter table student drop column middle_name;

-- 4. Переименовать колонку birthday в birth_date
alter table student rename column birthday to birth_date;

-- 5. Изменить тип данных колонки phone на varchar(32)
alter table student alter column phone varchar(32);

-- 6. Вставить три любых записи с автогенерацией идентификатора
insert into student (first_name, last_name, birth_date, phone) values ('vasya', 'pupkin', '2000-01-01', '88008880000');
insert into student (first_name, last_name, birth_date, phone) values ('petya', 'petrov', '2000-02-02', '89008880000');
insert into student (first_name, last_name, birth_date, phone) values ('sasha', 'sashov', '2000-03-03', '88008880000');
-- 7. Удалить все данные из таблицы со сбросом идентификатор в исходное состояние
truncate table student;
alter sequence student_student_id_seq restart with 1;
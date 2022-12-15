--domains
create domain valid_num as int
check (value > 0 and value is not null);

create domain valid_cost as decimal
check (value > 0 and value is not null)

create domain valid_text as text
check (value is not null);

drop domain valid_num cascade;
drop domain valid_text cascade;
drop domain valid_cost cascade;

--tables
create table cinemas(
	cinema_name text primary key,
	cinema_district valid_text,
	cinema_location valid_text,
	cinema_category valid_text,
	cinema_capacity valid_num
);

create table films(
	film_name text primary key,
	film_production valid_text,
	film_producer valid_text,
	film_genre valid_text,
	film_rental_price valid_cost
);

create table sessions(
	session_id serial primary key,
	session_time time not null,
    session_date date not null,
	cinema_name valid_text,
	film_name valid_text,
	session_free_seats valid_num,
	session_cost valid_cost,
	unique (session_time, session_date, cinema_name, film_name)
);

create table tickets(
	ticket_id serial primary key,
	session_id valid_num,
	ticket_row valid_num,
	ticket_place valid_num,
	unique (session_id, ticket_row, ticket_place)
);

--indexes
create unique index key_cinema 
on cinemas (cinema_name);

create unique index key_film 
on films (film_name);

create unique index key_session 
on sessions (session_id);

create unique index key_ticket 
on tickets (ticket_id);

drop index key_cinema;
drop index key_film;
drop index key_session;
drop index key_ticket;

--triggers
--триггер на заполнение таблицы обновление таблицы sessions (покупка билетов)

create trigger tr_ticket  before insert on tickets 
for each row execute function f_insert_ticket();

create or replace function f_insert_ticket()
	returns trigger as 
$$
begin					
	update sessions 
	set session_free_seats = session_free_seats - 1
	where new.session_id = session_id;
	return (new);
end;
$$ language plpgsql;

drop trigger tr_session on tickets

--вспомогательные функции
--определение вместимости кинотеатра	
create or replace function f_capacity(cinema_category text) returns int as $$
declare 
	num int;
begin	
	if cinema_category = 'Кинотеатр' then num = 500;
	end if;
	if cinema_category = 'Кинотеатр 3D' then num = 600; 
	end if;
	if cinema_category = 'Автокинотеатр' then num = 300;
	end if;
	return num;
end;
$$ language plpgsql;

drop function f_capacity(text)

--определение вместимости для сеанса	
create or replace function f_cap_session(cinema text) returns int as $$
declare 
	capacity int;
begin
	capacity = (select cinema_capacity from cinemas as c
				where c.cinema_name = cinema);
	return capacity;
end;
$$ language plpgsql;

drop function f_cap_session(text)

--определение цены билета
create or replace function f_cost(cinema text, film text) returns int as $$
declare
	ticket_cost int;
	category text;
begin
	category = (select cinema_category from cinemas
				where cinema_name = cinema);
	if category = 'Кинотеатр' then ticket_cost = 100;
	end if;
	if category = 'Кинотеатр 3D' then ticket_cost = 150; 
	end if;
	if category = 'Автокинотеатр' then ticket_cost = 50;
	end if;
	ticket_cost = ticket_cost + (select film_rental_price from films as f
								 where f.film_name = film);
	return ticket_cost;
end;
$$ language plpgsql; 

drop function f_cost(text, text)

--insert data
insert into cinemas(
values
	('Звезда', 'Санкт-Петербург', 'ул. Савушкина, д. 6', 'Кинотеатр', f_capacity('Кинотеатр')),
	('Cinema park', 'Москва', 'пр. Мира, д. 2', 'Кинотеатр 3D', f_capacity('Кинотеатр 3D')),
	('Мираж', 'Выборг', 'пр. Ленина, д. 15', 'Кинотеатр', f_capacity('Кинотеатр')),
	('Кино', 'Новгород', 'ул. Мартынова, д. 63', 'Автокинотеатр', f_capacity('Автокинотеатр'))
);

insert into films(
values
	('Человек-паук 3', '20 centry', 'Раян Гослинг', 'Триллер', 300),
	('Колобок', 'Нева', 'Алексей Лыганов', 'Мультфильм', 150),
	('Начало', '20 centry', 'Береза Кирилл', 'Фантастика', 200),
	('Алёша Попович и Тугарин Змей', 'Мельница', 'Тарантино', 'Мультфильм', 200),
	('Гарри Поттер', 'WB', 'Алексей Артюх', 'Приключения', 250),
	('Властелин колец', '20 centry', 'Джо Байден', 'Приключения', 190)
);

insert into sessions(
values
	(default, '01:15', '2022.12.22', 'Звезда', 'Человек-паук 3', f_cap_session('Звезда'), f_cost('Звезда', 'Человек-паук 3')),
	(default, '15:10', '2022.10.12', 'Звезда', 'Колобок', f_cap_session('Звезда'), f_cost('Звезда', 'Колобок')),
	(default, '21:30', '2022.11.25', 'Cinema park', 'Гарри Поттер', f_cap_session('Cinema park'), f_cost('Cinema park', 'Гарри Поттер')),
	(default, '19:00', '2022.11.05', 'Cinema park', 'Властелин колец', f_cap_session('Cinema park'), f_cost('Cinema park', 'Властелин колец')),
	(default, '18:20', '2022.11.25', 'Cinema park', 'Человек-паук 3', f_cap_session('Cinema park'), f_cost('Cinema park', 'Человек-паук 3')),
	(default, '09:00', '2022.11.05', 'Cinema park', 'Колобок', f_cap_session('Cinema park'), f_cost('Cinema park', 'Колобок')),
	(default, '12:40', '2022.11.05', 'Мираж', 'Начало', f_cap_session('Мираж'), f_cost('Мираж', 'Начало')),
	(default, '19:25', '2022.09.25', 'Мираж', 'Алёша Попович и Тугарин Змей', f_cap_session('Мираж'), f_cost('Мираж', 'Алёша Попович и Тугарин Змей')),
	(default, '08:00', '2022.10.05', 'Мираж', 'Колобок', f_cap_session('Мираж'), f_cost('Мираж', 'Колобок')),
	(default, '10:30', '2022.12.15', 'Кино', 'Колобок', f_cap_session('Кино'), f_cost('Мираж', 'Колобок'))
);

insert into tickets(
values
	(default, 1, 4, 16),
	(default, 1, 5, 15),
	(default, 2, 5, 11),
	(default, 3, 5, 15),
	(default, 4, 5, 14),
	(default, 5, 6, 15),
	(default, 6, 3, 10),
	(default, 7, 10, 20),
	(default, 8, 5, 12),
	(default, 9, 2, 4),
	(default, 10, 15, 6),
	(default, 10, 5, 1)
);
--
select * from cinemas;
select * from films;
select * from sessions;
select * from tickets;

---запросы

--репертуар кинотеатра (по названию кинотеатра);
select cinema_category from cinemas
where cinema_name = 'Звезда'

--адрес и район кинотеатра (по названию кинотеатра);
select cinema_district, cinema_location from cinemas
where cinema_name = 'Звезда'

--число мест (свободных) на данный сеанс (название кинотеатра и сеанс);
select session_free_seats from sessions
where (cinema_name = 'Cinema park' and session_time = '21:30' 
	and session_date = '2022.11.25' and film_name = 'Гарри Поттер')
	
--цена билетов на данный сеанс (название кинотеатра и сеанс);
select session_cost from sessions
where (cinema_name = 'Cinema park' and session_time = '21:30' 
	and session_date = '2022.11.25' and film_name = 'Гарри Поттер')

--жанр, производство и режиссер данного фильма (по названию);
select film_genre, film_producer from films
where film_name = 'Гарри Поттер'

--вместимость данного кинотеатра (по названию кинотеатра).
select cinema_capacity from cinemas
where cinema_name = 'Звезда'

--манипуляция

--открытие нового кинотеатра,
insert into cinemas(
values
	('Меркурий', 'Санкт-Петербург', 'ул. Станюковича, д. 7', 'Кинотеатр', f_capacity('Кинотеатр'))
);

--снятие фильма с проката;
delete from films
where film_name = 'Колобок'

--изменение репертуара кинотеатра.	
update cinemas
set cinema_category = 'Кинотеатр 3D', cinema_capacity = f_capacity('Кинотеатр 3D')
where cinema_name = 'Звезда'

--справки
select film_name, session_time, session_date, session_cost from sessions
where cinema_name = 'Звезда'

select film_name, s.cinema_name, session_cost from sessions as s
inner join cinemas as c on c.cinema_name = s.cinema_name
where cinema_district = 'Москва'

-------
drop table cinemas cascade;
drop table films cascade;
drop table tickets cascade;
drop table sessions cascade;
-------

set role employee
set role postgres
set role admin

select * from daily_checkin;
select * from daily_checkin where id = 1;

-- insert first row data
insert into daily_checkin (id, username, project, hours, timestamp) VALUES (1, 'foo', 'tm', '10.0', '2024-03-02 15:50:00');

-- select used in app query
select username as user, project, hours, to_char(timestamp, 'YYYY-mm-dd HH:SS')  from daily_checking where username = 'foo';
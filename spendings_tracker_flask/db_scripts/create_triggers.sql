--user_incomes
--functions
create or replace function f_trg_user_incomes_tmstp() returns trigger as
$BODY$
begin
	new.last_changes_timestamp = now();
	return new;
end;
$BODY$ language plpgsql

create or replace function f_trg_user_incomes_hist() returns trigger as
$BODY$
declare
	_oper_type varchar(1);
begin
	if tg_op = 'UPDATE' then
		_oper_type = 'U';
		
		insert into user_incomes_hist(id_income, id_user, income_amount, income_timestamp, income_user_note, hist_oper, hist_timestamp)
		values(old.id_income, old.id_user, old.income_amount, old.income_timestamp, old.income_user_note, _oper_type, now());
		
		return new;
		
	elsif tg_op = 'DELETE' then
		_oper_type = 'D';
		
		insert into user_incomes_hist(id_income, id_user, income_amount, income_timestamp, income_user_note, hist_oper, hist_timestamp)
		values(old.id_income, old.id_user, old.income_amount, old.income_timestamp, old.income_user_note, _oper_type, now());
	
		return old;
	end if;
end;
$BODY$ language plpgsql

--triggers
create trigger trg_user_incomes_tmstp
 before insert or update
 on user_incomes
 for each row
 execute procedure f_trg_user_incomes_tmstp();
 
create trigger trg_user_incomes_hist
 before delete or update
 on user_incomes
 for each row
 execute procedure f_trg_user_incomes_hist();
	
	
--user_spendings
--trigger functions
create or replace function f_trg_user_spendings_tmstp() returns trigger as
$BODY$
begin
	new.last_changes_timestamp = now();
	return new;
end;
$BODY$ language plpgsql

create or replace function f_trg_user_spendings_hist() returns trigger as
$BODY$
declare
	_oper_type varchar(1);
begin
	if tg_op = 'UPDATE' then
		_oper_type = 'U';
		
		insert into user_spendings_hist(id_spending, id_user, spending_amount, spending_timestamp, spending_user_note, hist_oper, hist_timestamp)
		values(old.id_spending, old.id_user, old.spending_amount, old.spending_timestamp, old.spending_user_note, _oper_type, now());
	
		return new;
	elsif tg_op = 'DELETE' then
		_oper_type = 'D';
		
		insert into user_spendings_hist(id_spending, id_user, spending_amount, spending_timestamp, spending_user_note, hist_oper, hist_timestamp)
		values(old.id_spending, old.id_user, old.spending_amount, old.spending_timestamp, old.spending_user_note, _oper_type, now());
	
		return old;
	end if;
end;
$BODY$ language plpgsql

--triggers
create trigger trg_user_spendings_tmstp
 before insert or update
 on user_spendings
 for each row
 execute procedure f_trg_user_spendings_tmstp();
 
create trigger trg_user_spendings_hist
 before delete or update
 on user_spendings
 for each row
 execute procedure f_trg_user_spendings_hist();
 
 
--users
--trigger functions
create or replace function f_trg_user_create_tmstp() returns trigger as
$BODY$
begin
	new.created_date = now();
	return new;
end;
$BODY$ language plpgsql

create or replace function f_trg_user_ud() returns trigger as
$BODY$
declare
	_oper_type varchar(1);
begin
	if tg_op = 'UPDATE' then
		_oper_type = 'U';
		
		insert into users_hist(id_user, username, created_date, hashed_pwd, hist_operation, hist_timestamp)
		values (old.id_user, old.username, old.created_date, old.hashed_pwd, _oper_type, now());
	
		return new;
	elsif tg_op = 'DELETE' then
		_oper_type = 'D';
		
		insert into users_hist(id_user, username, created_date, hashed_pwd, hist_operation, hist_timestamp)
		values (old.id_user, old.username, old.created_date, old.hashed_pwd, _oper_type, now());

		return old;
	end if;
end;
$BODY$ language plpgsql

--triggers
create trigger trg_user_ud
 before update or delete
 on users
 for each row
 execute procedure f_trg_user_ud();

create trigger trg_user_create_tmstp
 before insert
 on users
 for each row
 execute procedure f_trg_user_create_tmstp();
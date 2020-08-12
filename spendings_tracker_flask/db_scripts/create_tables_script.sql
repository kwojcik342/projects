create table if not exists users(
	 id_user serial primary key
	,username varchar(50) UNIQUE NOT NULL
	,hashed_pwd varchar
	,created_date timestamp
);

create table if not exists users_hist(
	 id_user_hist serial primary key
	,id_user int
	,username varchar(50)
	,hashed_pwd varchar
	,created_date date
	,hist_operation varchar(1)
	,hist_timestamp timestamp
);



create table if not exists user_incomes(
	 id_income serial primary key
	,id_user int not null
	,income_amount numeric(16,2) not null
	,income_timestamp timestamp not null
	,income_user_note varchar(1000)
	,last_changes_timestamp timestamp
	,foreign key (id_user) references users(id_user)
);

create table if not exists user_incomes_hist(
	 id_income_hist serial primary key
	,id_income int
	,id_user int
	,income_amount numeric(16,2)
	,income_timestamp timestamp
	,income_user_note varchar(1000)
	,hist_operation varchar(1)
	,hist_timestamp timestamp
);



create table if not exists user_spendings(
	 id_spending serial primary key
	,id_user int not null
	,spending_amount numeric(16,2) not null
	,spending_timestamp timestamp not null
	,spending_user_note varchar(1000)
	,last_changes_timestamp timestamp
	,foreign key (id_user) references users(id_user)
);

create table if not exists user_spendings_hist(
	 id_spending_hist serial primary key
	,id_spending int
	,id_user int
	,spending_amount numeric(16,2)
	,spending_timestamp timestamp
	,spending_user_note varchar(1000)
	,hist_operation varchar(1)
	,hist_timestamp timestamp
);
create schema user;

create table user.contact_info(
    user_id VARCHAR(50) NOT NULL,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    gender ENUM,
    email_address VARCHAR(254) NOT NULL,
    birth_date DATE NOT NULL,
    phone VARCHAR(30) NOT NULL,
    primary key (user_id)
);

create table user.address(
    user_id VARCHAR(50) NOT NULL,
    address_line1 VARCHAR(254),
    address_line2 VARCHAR(254),
    city VARCHAR(254),
    state VARCHAR(254),
    zipcode VARCHAR(10),
    country VARCHAR(3),
    primary key (user_id),
    foreign key (user_id) references contact_info(user_id)
);

create table user.payment(
    user_id VARCHAR(50) NOT NULL,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    card_number VARCHAR(50) NOT NULL,
    cvn VARCHAR(7) NOT NULL,
    exp_month VARCHAR(2) NOT NULL,
    exp_year VARCHAR(2) NOT NULL,
    card_type VARCHAR(10) NOT NULL
)
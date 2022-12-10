create schema event;

create table event.event(
    event_id varchar(50) not null,
    organizer_id varchar(50) not null,
    date date not null,
    start_time TIME not null,
    end_time TIME not null,
    description varchar(50) not null,
    event_category varchar(50) not null,
    capacity: int not null,
    image_url: varchar(100)
    primary key (event_id),
    foreign key (organizer_id) references organizer(org_id)
)

create table event.location(
    event_id varchar(50) not null,
    address_line1 varchar(50) not null,
    address_line2 varchar(50),
    city varchar(50) not null,
    zipcode varchar(5) not null,
    state varchar(50) not null,
    country varchar(50) not null,
    primary key (event_id),
    foreign key(event_id) references event(event_id)
)

create table event.transcation(
    transaction_id int not null auto_increment,
    user_id varchar(50) not null,
    event_id varchar(50) not null,
    ticket_type varchar(50) not null,
    num_tickets int not null,
    primary key (transaction_id),
    foreign key (event_id) references event(event_id),
    foreign key (user_id) references user.contact_info(user_id)
)

create table event.tickets(
    event_id varchar(50) not null,
    ticket_type varchar(50) not null,
    ticket_price money,
    currency varchar(50),
    num_available int
    primary key(event_id, ticket_type),
    foreign key(event_id) references event(event_id)
)

create table event.attendees(
	event_id varchar(50) not null,
    primary key(event_id, ticket_type),
    foreign key(attendee_id) references attendee.contact_info(attendee_id)
)

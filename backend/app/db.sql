CREATE EXTENSION pgcrypto;
CREATE TABLE user (
    uuid UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email_address TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    created_on DATE DEFAULT CURRENT_DATE
);

CREATE TABLE category (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE manufacture (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE mount (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE item (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    consumable BOOLEAN NOT NULL,
    category SERIAL REFERENCES category(id),
    manufacture SERIAL REFERENCES manufacture(id),
    mount_id SERIAL REFERENCES mount(id),
    release_date DATE
);

CREATE TABLE loan_item (
    id SERIAL PRIMARY KEY,
    user_uuid UUID NOT NULL REFERENCES user(uuid),
    item_id SERIAL NOT NULL REFERENCES item(id),
    loan_date DATE NOT NULL,
    due_date DATE NOT NULL,
    return_date DATE
);

CREATE TABLE button (
    id SERIAL PRIMARY KEY,
    user_uuid UUID NOT NULL REFERENCES user(uuid),
    item_id SERIAL NOT NULL REFERENCES item(id),
    request_date DATE DEFAULT CURRENT_DATE
)

CREATE EXTENSION pgcrypto;
CREATE TABLE user (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    password_hash TEXT NOT NULL,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    email_address TEXT NOT NULL UNIQUE,
    created_on DATE NOT NULL,
);

CREATE TABLE mount (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE item (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    category TEXT, NOT NULL,
    manufacture TEXT NOT NULL,
    release_date DATE, NOT NULL,
    consumable BOOLEAN, NOT NULL,
    mount_id SERIAL REFERENCES mount(id)
);

CREATE TABLE loan_item (
    id SERIAL PRIMARY KEY,
    user_id SERIAL NOT NULL REFERENCES user(id),
    item_id SERIAL NOT NULL REFERENCES item(id),
    loan_date DATE NOT NULL,
    due_date DATE NOT NULL,
    return_date DATE
);

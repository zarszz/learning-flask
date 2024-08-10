-- Create the Users table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) NOT NULL UNIQUE,
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    role_id INTEGER REFERENCES roles(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create the Roles table
CREATE TABLE roles (
    id SERIAL PRIMARY KEY,
    role_name VARCHAR(50) NOT NULL UNIQUE
);

-- Create the Requests table
CREATE TABLE requests (
    id SERIAL PRIMARY KEY,
    requester_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    status VARCHAR(50) NOT NULL DEFAULT 'pending',
    current_approval_level INTEGER DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create the Approval Levels table
CREATE TABLE approval_levels (
    id SERIAL PRIMARY KEY,
    request_id INTEGER REFERENCES requests(id) ON DELETE CASCADE,
    level INTEGER NOT NULL,
    approver_role_id INTEGER REFERENCES roles(id) ON DELETE SET NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'pending',
    approved_by INTEGER REFERENCES users(id) ON DELETE SET NULL,
    approved_at TIMESTAMP,
    UNIQUE (request_id, level)  -- Ensure that each request has unique levels
);

-- Create the Approval History table
CREATE TABLE approval_history (
    id SERIAL PRIMARY KEY,
    request_id INTEGER REFERENCES requests(id) ON DELETE CASCADE,
    approver_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
    level INTEGER NOT NULL,
    status VARCHAR(50) NOT NULL,
    comment TEXT,
    action_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Add triggers to update the updated_at field on each table
CREATE OR REPLACE FUNCTION update_timestamp_column()
RETURNS TRIGGER AS $$
BEGIN
   NEW.updated_at = NOW();
   RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_users_updated_at BEFORE UPDATE
ON users FOR EACH ROW EXECUTE PROCEDURE update_timestamp_column();

CREATE TRIGGER update_requests_updated_at BEFORE UPDATE
ON requests FOR EACH ROW EXECUTE PROCEDURE update_timestamp_column();

CREATE TRIGGER update_approval_levels_updated_at BEFORE UPDATE
ON approval_levels FOR EACH ROW EXECUTE PROCEDURE update_timestamp_column();

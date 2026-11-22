
-- Create a separate database for Keycloak
CREATE DATABASE keycloak;

-- Connect back to the application database
\connect capstone_db

-- Create the application schema
CREATE SCHEMA IF NOT EXISTS capstone;

-- Create candidates table
CREATE TABLE IF NOT EXISTS capstone.candidates (
    candidate_id TEXT PRIMARY KEY,
    full_name TEXT NOT NULL,
    email TEXT NOT NULL,
    phone_number TEXT NOT NULL DEFAULT '',
    status TEXT NOT NULL DEFAULT 'PENDING'
        CHECK (status IN ('PENDING', 'VERIFIED', 'REJECTED')),
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Create candidate ownership mapping table
CREATE TABLE IF NOT EXISTS capstone.candidate_user_mapping (
    candidate_id TEXT PRIMARY KEY,
    keycloak_user_id TEXT NOT NULL,
    CONSTRAINT fk_candidate_user_mapping_candidate
        FOREIGN KEY (candidate_id)
        REFERENCES capstone.candidates(candidate_id)
        ON DELETE CASCADE
);

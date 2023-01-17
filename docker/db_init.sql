CREATE DATABASE oidccontroller;
CREATE USER oidccontrolleradminuser PASSWORD 'oidccontrolleradminpass';
CREATE USER oidccontrolleruser PASSWORD 'oidccontrollerpass';
ALTER DATABASE oidccontroller OWNER TO oidccontrolleradminuser;
\connect oidccontroller 
CREATE EXTENSION IF NOT EXISTS pgcrypto;
REVOKE ALL ON SCHEMA public
FROM PUBLIC;
GRANT USAGE ON SCHEMA public TO oidccontrolleradminuser;
GRANT USAGE ON SCHEMA public TO oidccontrolleruser;
GRANT ALL ON SCHEMA public TO oidccontrolleradminuser;
ALTER DEFAULT PRIVILEGES FOR USER oidccontrolleradminuser IN SCHEMA public
GRANT SELECT,
    INSERT,
    UPDATE,
    DELETE ON TABLES TO oidccontrolleruser;
ALTER DEFAULT PRIVILEGES FOR USER oidccontrolleradminuser IN SCHEMA public
GRANT USAGE,
    SELECT ON SEQUENCES TO oidccontrolleruser;
ALTER DEFAULT PRIVILEGES FOR USER oidccontrolleradminuser IN SCHEMA public
GRANT EXECUTE ON FUNCTIONS TO oidccontrolleruser;
CREATE USER 'THARINDU'@'localhost' IDENTIFIED BY 'Tha15270';
GRANT ALL PRIVILEGES ON llm_agent.* TO 'THARINDU'@'localhost';
FLUSH PRIVILEGES;

select user, host from mysql.user;

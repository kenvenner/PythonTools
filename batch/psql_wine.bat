psql -h localhost -d wine -U postgres -p 5432 -v "ON_ERROR_STOP=1" -f ..\Postgres\wine\%1%

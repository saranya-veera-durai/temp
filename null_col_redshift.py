CREATE TABLE example_table (
    id INT,
    name VARCHAR(255),
    age INT,
    address VARCHAR(255),
    phone VARCHAR(255)
);

INSERT INTO example_table (id, name, age, address, phone) VALUES
(1, 'John', 30, NULL, NULL),
(2, 'Jane', NULL, NULL, NULL),
(3, NULL, 25, NULL, NULL),
(4, NULL, NULL, NULL, NULL);

CREATE OR REPLACE PROCEDURE find_all_null_columns(table_name VARCHAR)
AS $$
DECLARE
    col_name VARCHAR;
    sql_query TEXT;
BEGIN
    -- Create a temporary table to hold column names with all NULL values
    CREATE TEMP TABLE temp_null_columns (column_name VARCHAR);

    -- Loop through all columns of the table
    FOR col_name IN
        SELECT column_name
        FROM information_schema.columns
        WHERE table_name = table_name
          AND table_schema = 'public'
    LOOP
        -- Construct the SQL query to check if the column contains only NULLs
        sql_query := format(
            'INSERT INTO temp_null_columns (column_name) 
             SELECT %L 
             WHERE NOT EXISTS (SELECT 1 FROM %I WHERE %I IS NOT NULL)',
            col_name,
            table_name,
            col_name
        );
        
        -- Execute the query
        EXECUTE sql_query;
    END LOOP;

    -- Output the results
    SELECT * FROM temp_null_columns;
END;
$$ LANGUAGE plpgsql;
CALL find_all_null_columns('example_table');

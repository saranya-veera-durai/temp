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

SELECT column_name
FROM information_schema.columns
WHERE table_name = 'example_table'
AND column_name IN ('name', 'age', 'address', 'phone')
AND column_name NOT IN (
    SELECT 'name' FROM example_table WHERE name IS NOT NULL
    UNION ALL
    SELECT 'age' FROM example_table WHERE age IS NOT NULL
    UNION ALL
    SELECT 'address' FROM example_table WHERE address IS NOT NULL
    UNION ALL
    SELECT 'phone' FROM example_table WHERE phone IS NOT NULL
);





-------------------------------------------------------------------------------------------------------------







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
SET @table_name = 'example_table';

DELIMITER $$

CREATE PROCEDURE FindAllNullColumns(IN tableName VARCHAR(255))
BEGIN
    DECLARE done INT DEFAULT 0;
    DECLARE colName VARCHAR(255);
    DECLARE columns CURSOR FOR 
        SELECT COLUMN_NAME 
        FROM INFORMATION_SCHEMA.COLUMNS 
        WHERE TABLE_NAME = tableName 
        AND TABLE_SCHEMA = DATABASE();
    
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = 1;

    DROP TEMPORARY TABLE IF EXISTS temp_null_columns;
    CREATE TEMPORARY TABLE temp_null_columns (column_name VARCHAR(255));

    OPEN columns;
    read_loop: LOOP
        FETCH columns INTO colName;
        IF done THEN
            LEAVE read_loop;
        END IF;

        SET @query = CONCAT('INSERT INTO temp_null_columns (column_name) 
                             SELECT ''', colName, ''' 
                             FROM ', tableName, ' 
                             GROUP BY 1 
                             HAVING COUNT(', colName, ') = 0');
        PREPARE stmt FROM @query;
        EXECUTE stmt;
        DEALLOCATE PREPARE stmt;
    END LOOP;

    CLOSE columns;

    SELECT * FROM temp_null_columns;
END $$

DELIMITER ;

CALL FindAllNullColumns('example_table');


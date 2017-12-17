# -*- coding: utf-8 -*-

from __future__ import unicode_literals

CURRENT_DBD_VERSION = '3.1'

SQL_DBD_PRE_INIT = """
    CREATE TABLE dbd$schemas (
         id              INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL
        ,name            VARCHAR                           NOT NULL
        ,fulltext_engine VARCHAR                               NULL
        ,version         VARCHAR                               NULL
        ,description     VARCHAR                               NULL
    );
"""

SQL_DBD_DOMAINS_TABLE_INIT = """
    CREATE TABLE dbd$domains (
         id                  INTEGER PRIMARY KEY AUTOINCREMENT        DEFAULT(NULL)     NULL
        ,name                VARCHAR                           UNIQUE DEFAULT(NULL)     NULL               
        ,description         VARCHAR                                  DEFAULT(NULL)     NULL               
        ,data_type_id        INTEGER                                                NOT NULL               
        ,length              INTEGER                                  DEFAULT(NULL)     NULL               
        ,char_length         INTEGER                                  DEFAULT(NULL)     NULL               
        ,precision           INTEGER                                  DEFAULT(NULL)     NULL               
        ,scale               INTEGER                                  DEFAULT(NULL)     NULL               
        ,width               INTEGER                                  DEFAULT(NULL)     NULL               
        ,align               CHAR                                     DEFAULT(NULL)     NULL               
        ,show_null           BOOLEAN                                  DEFAULT(NULL)     NULL               
        ,show_lead_nulls     BOOLEAN                                  DEFAULT(NULL)     NULL               
        ,thousands_separator BOOLEAN                                  DEFAULT(NULL)     NULL               
        ,summable            BOOLEAN                                  DEFAULT(NULL)     NULL               
        ,case_sensitive      BOOLEAN                                  DEFAULT(NULL)     NULL               
        ,uuid                VARCHAR                           UNIQUE               NOT NULL COLLATE NOCASE
    );
    
    CREATE INDEX "idx.FZX832TFV" ON dbd$domains(data_type_id);
    CREATE INDEX "idx.4AF9IY0XR" ON dbd$domains(uuid);
"""

SQL_DBD_TABLES_TABLE_INIT = """
    CREATE TABLE dbd$tables (
         id            INTEGER PRIMARY KEY AUTOINCREMENT        DEFAULT(NULL)     NULL
        ,schema_id     INTEGER                                  DEFAULT(NULL)     NULL  
        ,name          VARCHAR                           UNIQUE                   NULL  
        ,description   VARCHAR                                  DEFAULT(NULL)     NULL  
        ,can_add       BOOLEAN                                  DEFAULT(NULL)     NULL  
        ,can_edit      BOOLEAN                                  DEFAULT(NULL)     NULL  
        ,can_delete    BOOLEAN                                  DEFAULT(NULL)     NULL  
        ,temporal_mode VARCHAR                                  DEFAULT(NULL)     NULL 
        ,means         VARCHAR                                  DEFAULT(NULL)     NULL         
        ,uuid          VARCHAR                           UNIQUE               NOT NULL COLLATE NOCASE 
    );  
    
    CREATE INDEX "idx.GCOFIBEBJ" ON dbd$tables(name);
    CREATE INDEX "idx.2J02T9LQ7" ON dbd$tables(uuid);
"""

SQL_DBD_TABLES_INIT = """
    CREATE TABLE dbd$fields (
         id                 INTEGER PRIMARY KEY AUTOINCREMENT        DEFAULT(NULL)     NULL
        ,table_id           INTEGER                                                NOT NULL             
        ,position           INTEGER                                                NOT NULL             
        ,name               VARCHAR                                                NOT NULL             
        ,russian_short_name VARCHAR                                                NOT NULL  
        ,description        VARCHAR                                  DEFAULT(NULL)     NULL 
        ,domain_id          INTEGER                                                NOT NULL     
        ,can_input          BOOLEAN                                  DEFAULT(NULL)     NULL   
        ,can_edit           BOOLEAN                                  DEFAULT(NULL)     NULL   
        ,show_in_grid       BOOLEAN                                  DEFAULT(NULL)     NULL   
        ,show_in_details    BOOLEAN                                  DEFAULT(NULL)     NULL
        ,is_mean            BOOLEAN                                  DEFAULT(NULL)     NULL 
        ,autocalculated     BOOLEAN                                  DEFAULT(NULL)     NULL 
        ,required           BOOLEAN                                  DEFAULT(NULL)     NULL 
        ,uuid               VARCHAR                           UNIQUE               NOT NULL COLLATE NOCASE
    );
    
    CREATE INDEX "idx.7UAKR6FT7" ON dbd$fields(table_id);
    CREATE INDEX "idx.7HJ6KZXJF" ON dbd$fields(position);
    CREATE INDEX "idx.74RSETF9N" ON dbd$fields(name);
    CREATE INDEX "idx.6S0E8MWZV" ON dbd$fields(domain_id);
    CREATE INDEX "idx.88KWRBHA7" ON dbd$fields(uuid);
    
    
    CREATE TABLE dbd$constraints (
         id               INTEGER PRIMARY KEY AUTOINCREMENT        DEFAULT(NULL)     NULL
        ,table_id         INTEGER                                                NOT NULL                          
        ,name             VARCHAR                                  DEFAULT(NULL)     NULL                       
        ,constraint_type  CHAR                                     DEFAULT(NULL)     NULL       
        ,reference        INTEGER                                  DEFAULT(NULL)     NULL 
        ,unique_key_id    INTEGER                                  DEFAULT(NULL)     NULL 
        ,has_value_edit   BOOLEAN                                  DEFAULT(NULL)     NULL 
        ,cascading_delete BOOLEAN                                  DEFAULT(NULL)     NULL 
        ,expression       VARCHAR                                  DEFAULT(NULL)     NULL
        ,uuid             VARCHAR                           UNIQUE               NOT NULL COLLATE NOCASE 
    );
    
    CREATE INDEX "idx.6F902GEQ3" ON dbd$constraints(table_id);
    CREATE INDEX "idx.6SRYJ35AJ" ON dbd$constraints(name);
    CREATE INDEX "idx.62HLW9WGB" ON dbd$constraints(constraint_type);
    CREATE INDEX "idx.5PQ7Q3E6J" ON dbd$constraints(reference);
    CREATE INDEX "idx.92GH38TZ4" ON dbd$constraints(unique_key_id);
    CREATE INDEX "idx.6IOUMJINZ" ON dbd$constraints(uuid);


    CREATE TABLE dbd$constraint_details (
         id            INTEGER PRIMARY KEY AUTOINCREMENT DEFAULT(NULL)     NULL
        ,constraint_id INTEGER                                         NOT NULL          
        ,position      INTEGER                                         NOT NULL               
        ,field_id      INTEGER                                         NOT NULL  
    );
    
    CREATE INDEX "idx.5CYTJWVWR" ON dbd$constraint_details(constraint_id);
    CREATE INDEX "idx.507FDQDMZ" ON dbd$constraint_details(position);
    CREATE INDEX "idx.4NG17JVD7" ON dbd$constraint_details(field_id);


    CREATE TABLE dbd$indices (
         id       INTEGER PRIMARY KEY AUTOINCREMENT        DEFAULT(NULL)     NULL
        ,table_id INTEGER                                  NOT NULL          NULL                  
        ,name     VARCHAR                                  DEFAULT(NULL)     NULL                   
        ,local    BOOLEAN                                  DEFAULT(0)        NULL                  
        ,kind     CHAR                                     DEFAULT(NULL)     NULL                      
        ,uuid     VARCHAR                           UNIQUE               NOT NULL COLLATE NOCASE   
    );
    
    CREATE INDEX "idx.12XXTJUYZ" ON dbd$indices(table_id);
    CREATE INDEX "idx.6G0KCWN0R" ON dbd$indices(name);
    CREATE INDEX "idx.FQH338PQ7" ON dbd$indices(uuid);


    CREATE TABLE dbd$index_details (
         id         INTEGER PRIMARY KEY AUTOINCREMENT DEFAULT(NULL)     NULL
        ,index_id   INTEGER                                         NOT NULL
        ,position   INTEGER                                         NOT NULL
        ,field_id   INTEGER                           DEFAULT(NULL)     NULL
        ,expression VARCHAR                           DEFAULT(NULL)     NULL
        ,descend    BOOLEAN                           DEFAULT(NULL)     NULL              
    );
    
    CREATE INDEX "idx.H1KFOWTCB" ON dbd$index_details(index_id);
    CREATE INDEX "idx.BQA4HXWNF" ON dbd$index_details(field_id);
    

    CREATE TABLE dbd$data_types (
         id      INTEGER PRIMARY KEY AUTOINCREMENT        NOT NULL
        ,type_id VARCHAR                           UNIQUE NOT NULL
    );

    INSERT INTO dbd$data_types(type_id) VALUES ('STRING');
    INSERT INTO dbd$data_types(type_id) VALUES ('SMALLINT');
    INSERT INTO dbd$data_types(type_id) VALUES ('INTEGER');
    INSERT INTO dbd$data_types(type_id) VALUES ('WORD');
    INSERT INTO dbd$data_types(type_id) VALUES ('BOOLEAN');
    INSERT INTO dbd$data_types(type_id) VALUES ('FLOAT');
    INSERT INTO dbd$data_types(type_id) VALUES ('CURRENCY');
    INSERT INTO dbd$data_types(type_id) VALUES ('BCD');
    INSERT INTO dbd$data_types(type_id) VALUES ('FMTBCD');
    INSERT INTO dbd$data_types(type_id) VALUES ('DATE');
    INSERT INTO dbd$data_types(type_id) VALUES ('TIME');
    INSERT INTO dbd$data_types(type_id) VALUES ('DATETIME');
    INSERT INTO dbd$data_types(type_id) VALUES ('TIMESTAMP');
    INSERT INTO dbd$data_types(type_id) VALUES ('BYTES');
    INSERT INTO dbd$data_types(type_id) VALUES ('VARBYTES');
    INSERT INTO dbd$data_types(type_id) VALUES ('BLOB');
    INSERT INTO dbd$data_types(type_id) VALUES ('MEMO');
    INSERT INTO dbd$data_types(type_id) VALUES ('GRAPHIC');
    INSERT INTO dbd$data_types(type_id) VALUES ('FMTMEMO');
    INSERT INTO dbd$data_types(type_id) VALUES ('FIXEDCHAR');
    INSERT INTO dbd$data_types(type_id) VALUES ('WIDESTRING');
    INSERT INTO dbd$data_types(type_id) VALUES ('LARGEINT');
    INSERT INTO dbd$data_types(type_id) VALUES ('COMP');
    INSERT INTO dbd$data_types(type_id) VALUES ('ARRAY');
    INSERT INTO dbd$data_types(type_id) VALUES ('FIXEDWIDECHAR');
    INSERT INTO dbd$data_types(type_id) VALUES ('WIDEMEMO');
    INSERT INTO dbd$data_types(type_id) VALUES ('CODE');
    INSERT INTO dbd$data_types(type_id) VALUES ('RECORDID');
    INSERT INTO dbd$data_types(type_id) VALUES ('SET');
    INSERT INTO dbd$data_types(type_id) VALUES ('PERIOD');
    INSERT INTO dbd$data_types(type_id) VALUES ('BYTE');
""" % {'dbd_version': CURRENT_DBD_VERSION}

SQL_DBD_VIEWS_INIT = """
    CREATE VIEW dbd$view_fields 
    AS
    SELECT
         sch.name                AS "schema"
        ,tab.name                AS "table"
        ,fld.position            AS "position"
        ,fld.name                AS "name"
        ,fld.russian_short_name  AS "russian_short_name"
        ,fld.description         AS "description"
        ,type.type_id            AS "type_id"
        ,dom.length              AS "length"
        ,dom.char_length         AS "char_length"
        ,dom.width               AS "width"
        ,dom.align               AS "align"
        ,dom.precision           AS "precision"
        ,dom.scale               AS "scale"
        ,dom.show_null           AS "show_null"
        ,dom.show_lead_nulls     AS "show_lead_nulls"
        ,dom.thousands_separator AS "thousands_separator"
        ,dom.summable            AS "summable"
        ,dom.case_sensitive      AS "case_sensitive"
        ,fld.can_input           AS "can_input"
        ,fld.can_edit            AS "can_edit"
        ,fld.show_in_grid        AS "show_in_grid"
        ,fld.show_in_details     AS "show_in_details"
        ,fld.is_mean             AS "is_mean"
        ,fld.autocalculated      AS "autocalculated"
        ,fld.required            AS "required"
    FROM dbd$fields              AS fld
    INNER JOIN dbd$tables     AS tab
        ON fld.table_id = tab.id
    INNER JOIN dbd$domains    AS dom
        ON fld.domain_id = dom.id
    INNER JOIN dbd$data_types AS type
        ON dom.data_type_id = type.id
    LEFT JOIN dbd$schemas     AS sch
        ON tab.schema_id = sch.id
    ORDER BY
         bd$tables.name
        ,bd$fields.position;
    
    
    CREATE VIEW dbd$view_domains 
    AS
    SELECT
         dom.id
        ,dom.name
        ,dom.description
        ,type.type_id
        ,dom.length
        ,dom.char_length
        ,dom.width
        ,dom.align
        ,dom.summable
        ,dom.precision
        ,dom.scale
        ,dom.show_null
        ,dom.show_lead_nulls
        ,dom.thousands_separator
        ,dom.case_sensitive "case_sensitive"
    FROM dbd$domains          AS dom
    INNER JOIN dbd$data_types AS type
        ON dom.data_type_id = type.id
    ORDER BY dom.id;
    
    
    CREATE VIEW dbd$view_constraints 
    AS
    SELECT
         con.id              AS "constraint_id"
        ,con.constraint_type AS "constraint_type"
        ,det.position        AS "position"
        ,sch.name            AS "schema"
        ,tab.name            AS "table_name"
        ,fld.name            AS "field_name"
        ,ref.name            AS "reference"
    FROM dbd$constraint_details AS det
    INNER JOIN dbd$constraints  AS con
        ON det.constraint_id = con.id
    INNER JOIN dbd$tables       AS tab
        ON con.table_id = tab.id
    LEFT JOIN dbd$tables        AS ref
        ON con.reference = ref.id
    LEFT JOIN dbd$fields        AS fld
        ON det.field_id = fld.id
    LEFT JOIN dbd$schemas       AS sch
        ON tab.schema_id = sch.id
    ORDER BY
         constraint_id
        ,position;
    
    
    CREATE VIEW dbd$view_indices 
    AS
    SELECT
         ind.id         AS "index_id"
        ,ind.name       AS "index_name"
        ,sch.name       AS "schema"
        ,tab.name       AS "table_name"
        ,ing.local
        ,ing.kind
        ,det.position
        ,fld.name       AS "field_name"
        ,det.expression
        ,det.descend
    FROM dbd$index_details AS det
    INNER JOIN dbd$indices AS ind
        ON det.index_id = ind.id
    INNER JOIN dbd$tables  AS tab
        ON ind.table_id = tab.id
    LEFT JOIN dbd$fields   AS fld
        ON det.field_id = fld.id
    LEFT JOIN dbd$schemas  AS sch
        ON tab.schema_id = sch.id
    ORDER BY
         dbd$tables.name
        ,dbd$indices.name
        ,dbd$index_details.position;
"""

BEGIN_TRANSACTION = """
    PRAGMA FOREIGN_KEYS = ON;
    BEGIN TRANSACTION;
"""

COMMIT = """
COMMIT;
"""

SQL_DBD_Init = BEGIN_TRANSACTION + SQL_DBD_PRE_INIT + SQL_DBD_DOMAINS_TABLE_INIT + \
    SQL_DBD_TABLES_TABLE_INIT + SQL_DBD_TABLES_INIT + SQL_DBD_VIEWS_INIT + COMMIT
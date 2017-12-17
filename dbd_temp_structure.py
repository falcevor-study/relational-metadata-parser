from __future__ import unicode_literals

CURRENT_DBD_VERSION = '3.1'

SQL_DBD_PRE_INIT = """\
    CREATE TEMPORARY TABLE schemas (
         name            VARCHAR UNIQUE NOT NULL
        ,fulltext_engine VARCHAR            NULL
        ,version         VARCHAR            NULL
        ,description     VARCHAR            NULL
    );
"""

SQL_DBD_DOMAINS_TABLE_INIT = """
    CREATE TEMPORARY TABLE domains (
         name                VARCHAR UNIQUE DEFAULT(NULL)     NULL
        ,description         VARCHAR        DEFAULT(NULL)     NULL
        ,data_type_name      VARCHAR                      NOT NULL    
        ,length              INTEGER        DEFAULT(NULL)     NULL
        ,char_length         INTEGER        DEFAULT(NULL)     NULL
        ,precision           INTEGER        DEFAULT(NULL)     NULL
        ,scale               INTEGER        DEFAULT(NULL)     NULL
        ,width               INTEGER        DEFAULT(NULL)     NULL
        ,align               CHAR           DEFAULT(NULL)     NULL
        ,show_null           BOOLEAN        DEFAULT(NULL)     NULL
        ,show_lead_nulls     BOOLEAN        DEFAULT(NULL)     NULL
        ,thousands_separator BOOLEAN        DEFAULT(NULL)     NULL
        ,summable            BOOLEAN        DEFAULT(NULL)     NULL
        ,case_sensitive      BOOLEAN        DEFAULT(NULL)     NULL
        ,uuid                VARCHAR UNIQUE               NOT NULL
    );
"""

SQL_DBD_TABLES_TABLE_INIT = """
    CREATE TEMPORARY TABLE tables (
         schema_name   VARCHAR                      NOT NULL      
        ,name          VARCHAR UNIQUE               NOT NULL  
        ,description   VARCHAR        DEFAULT(NULL)     NULL   
        ,can_add       BOOLEAN        DEFAULT(NULL)     NULL       
        ,can_edit      BOOLEAN        DEFAULT(NULL)     NULL      
        ,can_delete    BOOLEAN        DEFAULT(NULL)     NULL    
        ,temporal_mode VARCHAR        DEFAULT(NULL)     NULL 
        ,means         VARCHAR        DEFAULT(NULL)     NULL      
        ,uuid          VARCHAR UNIQUE               NOT NULL
    );
"""

SQL_DBD_TABLES_INIT = """
    CREATE TEMPORARY TABLE fields (
         table_name         VARCHAR                      NOT NULL             
        ,position           INTEGER                      NOT NULL             
        ,name               VARCHAR                      NOT NULL                 
        ,russian_short_name VARCHAR                      NOT NULL   
        ,description        VARCHAR        DEFAULT(NULL)     NULL    
        ,domain_name        VARCHAR                      NOT NULL            
        ,can_input          BOOLEAN        DEFAULT(NULL)     NULL      
        ,can_edit           BOOLEAN        DEFAULT(NULL)     NULL       
        ,show_in_grid       BOOLEAN        DEFAULT(NULL)     NULL   
        ,show_in_details    BOOLEAN        DEFAULT(NULL)     NULL
        ,is_mean            BOOLEAN        DEFAULT(NULL)     NULL        
        ,autocalculated     BOOLEAN        DEFAULT(NULL)     NULL 
        ,required           BOOLEAN        DEFAULT(NULL)     NULL      
        ,uuid               VARCHAR UNIQUE               NOT NULL
    );

    CREATE TEMPORARY TABLE constraints (
         id               INTEGER                      NOT NULL -- Синтетический временный идентификатор.
        ,table_name       VARCHAR                      NOT NULL                         
        ,name             VARCHAR        DEFAULT(NULL)     NULL                          
        ,constraint_type  CHAR           DEFAULT(NULL)     NULL                  
        ,reference        VARCHAR        DEFAULT(NULL)     NULL        
        ,unique_key_name  VARCHAR        DEFAULT(NULL)     NULL    
        ,has_value_edit   BOOLEAN        DEFAULT(NULL)     NULL   
        ,cascading_delete BOOLEAN        DEFAULT(NULL)     NULL 
        ,expression       VARCHAR        DEFAULT(NULL)     NULL
        ,uuid             VARCHAR UNIQUE               NOT NULL
    );

    CREATE TEMPORARY TABLE constraint_details (
         constraint_id   INTEGER NOT NULL          
        ,position        INTEGER NOT NULL               
        ,field_name      VARCHAR NOT NULL
    );

    CREATE TEMPORARY TABLE indices (
         id         INTEGER                        NOT NULL -- Синтетический временный идентификатор.
        ,table_name VARCHAR                        NOT NULL                          
        ,name       VARCHAR        DEFAULT(NULL)       NULL                       
        ,local      BOOLEAN        DEFAULT(0)      NOT NULL                  
        ,kind       CHAR           DEFAULT(NULL)       NULL   
        ,uuid       VARCHAR UNIQUE                 NOT NULL
    );

    CREATE TEMPORARY TABLE index_details (
         index_id   INTEGER               NOT NULL                     
        ,position   INTEGER               NOT NULL                          
        ,field_name VARCHAR DEFAULT(NULL)     NULL                    
        ,expression VARCHAR DEFAULT(NULL)     NULL           
        ,descend    BOOLEAN DEFAULT(NULL)     NULL              
    );
"""

SQL_TMP_INIT = SQL_DBD_PRE_INIT + SQL_DBD_DOMAINS_TABLE_INIT + \
    SQL_DBD_TABLES_TABLE_INIT + SQL_DBD_TABLES_INIT

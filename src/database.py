import cassandra
from cassandra.auth import PlainTextAuthProvider
from cassandra.cloud import Cloud
import pandas as pd
from src.logger import logging

class CassandraOperations():
    def __init__(self):
        self.client_id = "yzxUsYaTHOhluQtEecGTmLdF"
        self.client_secret = "FBKwnBx5A8,O.,xYTkOZ1c7i.OCwqX9-C2Zk+zpLCX04.Q2shO-Ecl.+G2eUg+8n_SOM51,shWgkzDg1FExX2iqPDxyy9zFOk6e-DP1wsOmBx_Lx6GZ3fgnB9vUTJWp2"
        self.secure_connect_bundle = "C:\Users\HP\Downloads\secure-connect-thyroid.zip"
    
    def database_connection(self):
        auth_provider = PlainTextAuthProvider(self.client_id, self.client_secret)
        cloud_config = {'secure_connect_bundle': self.secure_connect_bundle}
        cloud = Cloud(cloud = cloud_config, auth_provider= auth_provider)
        session = cloud.connect()
        logging.info("Connection has been established to the database")
        return session

    def table_creation(self):
        session = self.database_connection()

        integer = 'int'
        var = 'varchar'
        age = 'age'
        sex = 'sex'
        on_thyroxine = 'on_thyroxine'
        query_on_thyroxine = 'query_on_thyroxine'
        on_antithyroid_medication = 'on_antithyroid_medication'
        sick = 'sick'
        pregnant = 'pregnant'
        thyroid_surgery = 'thyroid_surgery'
        I131_treatment = 'I131_treatment'
        query_hypothyroid = 'query_hypothyroid'
        query_hyperthyroid = 'query_hyperthyroid'
        lithium = 'lithium'
        goitre = 'goitre'
        tumor = 'tumor'
        hypopituitary = 'hypopituitary'
        psych = 'psych'
        TSH_measured = 'TSH_measured'
        TSH = 'TSH'
        T3_measured = 'T3_measured'
        T3 = 'T3'
        TT4_measured = 'TT4_measured'
        TT4 = 'TT4'
        T4U_measured = 'T4U_measured'
        T4U = 'T4U'
        FTI_measured = 'FTI_measured'
        FTI = 'FTI'
        TBG_measured = 'TBG_measured'
        TBG = 'TBG'
        referral_source = 'referral_source'
        Class = 'Class'
        
        session.execute(f" CREATE TABLE THYROID ({age} {integer} PRIMARY KEY, {sex} {var}, {on_thyroxine} {var}, {query_on_thyroxine} {var}, {on_antithyroid_medication} {var}, {sick} {var}, {pregnant} {var}, {thyroid_surgery} {var}, {I131_treatment} {var}, {query_hypothyroid} {var}, {query_hyperthyroid} {var}, {lithium} {var}, {goitre} {var}, {tumor} {var}, {hypopituitary} {var}, {psych} {var}, {TSH_measured} {var},{TSH} {var}, {T3_measured} {var}, {T3} {var}, {TT4_measured} {var}, {TT4} {var}, {T4U_measured} {var}, {T4U} {var}, {FTI_measured} {var}, {FTI} {var}, {TBG_measured} {var}, {TBG} {var}, {referral_source} {var}, {Class} {var});")

        logging.info("Table has been created")

        session.shutdown()


    def data_insertion(self):
        session = self.database_connection()
        df = pd.read_csv('input_data.csv')
        
        age = 'age'
        sex = 'sex'
        on_thyroxine = 'on_thyroxine'
        query_on_thyroxine = 'query_on_thyroxine'
        on_antithyroid_medication = 'on_antithyroid_medication'
        sick = 'sick'
        pregnant = 'pregnant'
        thyroid_surgery = 'thyroid_surgery'
        I131_treatment = 'I131_treatment'
        query_hypothyroid = 'query_hypothyroid'
        query_hyperthyroid = 'query_hyperthyroid'
        lithium = 'lithium'
        goitre = 'goitre'
        tumor = 'tumor'
        hypopituitary = 'hypopituitary'
        psych = 'psych'
        TSH_measured = 'TSH_measured'
        TSH = 'TSH'
        T3_measured = 'T3_measured'
        T3 = 'T3'
        TT4_measured = 'TT4_measured'
        TT4 = 'TT4'
        T4U_measured = 'T4U_measured'
        T4U = 'T4U'
        FTI_measured = 'FTI_measured'
        FTI = 'FTI'
        TBG_measured = 'TBG_measured'
        TBG = 'TBG'
        referral_source = 'referral_source'
        Class = 'Class'

        for i, row in df.iterrows():
            query = f"INSERT into THYROID ({age}, {sex}, {on_thyroxine}, {query_on_thyroxine}, {on_antithyroid_medication}, {sick}, {pregnant}, {thyroid_surgery}, {I131_treatment}, {query_hypothyroid},{query_hyperthyroid}, {lithium}, {goitre}, {tumor}, {hypopituitary},{psych}, {TSH_measured}, {TSH}, {T3_measured}, {T3}, {TT4_measured}, {TT4}, {T4U_measured}, {T4U},{FTI_measured}, {FTI}, {TBG_measured}, {TBG},{referral_source}, {Class}) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            session.execute(query, tuple(row))
        
        session.shutdown()
    

    def exporting_data(self):
        session = self.database_connection()
        main_list = []
        for i in session.execute("select * from THYROID;"):
            main_list.append(i)
        
        df = pd.DataFrame(main_list)
        df.to_csv("input_file.csv")
        session.shutdown()

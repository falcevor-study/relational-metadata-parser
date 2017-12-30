from db_replication.replication import Replicator

replicator = Replicator('Northwind')
replicator.create_empty_database()
replicator.transfer_data()

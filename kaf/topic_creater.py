from confluent_kafka.admin import AdminClient, NewTopic
from confluent_kafka import KafkaException
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def create_topic(topic_name, num_partitions=1, replication_factor=1, retention_ms=60000):  # 這邊的retention_ms是資料留存時間
    admin_client = AdminClient({'bootstrap.servers': '10.0.1.138:9092'})
    
    try:
        topic_metadata = admin_client.list_topics(timeout=10).topics
        if topic_name in topic_metadata:
            logging.info(f"'{topic_name}' already exists. Deleting ---->")
            admin_client.delete_topics([topic_name])
            logging.info(f"'{topic_name}' deleted. Recreating ---->")
    except KafkaException as e:
        logging.info(f"Failed to list/delete '{e}'")


    topic = NewTopic(topic_name, num_partitions=num_partitions, replication_factor=replication_factor, config={'retention.ms': str(retention_ms)})
    try:
        fs = admin_client.create_topics([topic]) # 這邊接出一個fs可以查看建立的狀況，
        for topic, future in fs.items():
            try:
                future.result()
                logging.info(f"Topic '{topic}' created successfully. Got {num_partitions} partitions.")
            except KafkaException as e:
                logging.info(f"Failed to create topic '{topic}': {e}")
    except KafkaException as e:
        logging.info(f"Failed to create topic '{topic_name}': {e}")
    #  先前分區一直是[0]的根本原因是因為，沒有先刪除掉，並且kafka的機制是，沒辦法在建立的topic上改動partitioon
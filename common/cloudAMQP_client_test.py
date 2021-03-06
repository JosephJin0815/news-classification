from cloudAMQP_client import CloudAMQPClient

CLOUDAMQP_URL = "amqp://jamkyqms:HFH8eLsHiLjAWiiJKw2FTsJWmCoyK15J@gull.rmq.cloudamqp.com/jamkyqms"
QUEUE_NAME = "test"

def test_basic():
    client = CloudAMQPClient(CLOUDAMQP_URL, QUEUE_NAME)

    sentMsg = {'test': 'test'}
    client.sendMessage(sentMsg)

    receivedMsg = client.getMessage()
    assert sentMsg == receivedMsg

    print('test_basic passed.')

if __name__ == "__main__":
    test_basic()

import firebase_admin
import time
from firebase_admin import credentials, messaging

cred = credentials.Certificate('serviceAccountKey1.json') 
default_app = firebase_admin.initialize_app(cred)



def send_notif(data):

        start  = time.time()

        print("yes")
        # The topic name can be optionally prefixed with "/topics/".
        topic = 'security_alert'

        # See documentation on defining a message payload.
        message = messaging.Message(
            notification = messaging.Notification(
                    title = data,
                    body = data,
                ),
            android=messaging.AndroidConfig( priority='high', 
                                            notification=messaging.AndroidNotification( sound='default' ), ),
            data={
                'score': '850',
                'time': '2:45',
            },
            topic=topic,
        )

        # Send a message to the devices subscribed to the provided topic.
        response = messaging.send(message)
        # Response is a message ID string.
        print('Successfully sent message:', response)

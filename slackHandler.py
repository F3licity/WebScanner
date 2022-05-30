import logging
import os

# Import WebClient from Python SDK (github.com/slackapi/python-slack-sdk)
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

logger = logging.getLogger(__name__)

"""WebClient instantiates a client that can call API methods"""


class SlackHandler:
    def __init__(self, channel_id):
        self.channel_id = channel_id

    def send_message(self, message):
        """TODO"""
        client = WebClient(token=os.environ.get("SLACK_BOT_TOKEN"))

        # ID of channel you want to post message to
        # channel_id = "C03EHJN9BM0"

        try:
            # message = {
            #     "type": "section",
            #     "text": {
            #         "type": "mrkdwn",
            #         "text": "Hello this is a message from the Webscanner <example.com|Fred Enriquez>\n\n<https://example.com|View request>",
            #     },
            # }
            # Call the conversations.list method using the WebClient
            result = client.chat_postMessage(
                channel=self.channel_id,
                text=message
                # blocks=[message]
                # You could also use a blocks[] array to send richer content
            )
            # Print result, which includes information about the message (like TS)
            print(result)

        except SlackApiError as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    sh = SlackHandler("C03EHJN9BM0")
    sh.send_message("hello there!")

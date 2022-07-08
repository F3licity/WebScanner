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

    def send_message(self, message, brokenLinks=[]):
        """Send message on Slack using blocks with rich markdown type of text.

        Args:
            message: the text to be sent to slack
            brokenLinks: a list of broken links coming from the webscanner
        """
        client = WebClient(token=os.environ.get("SLACK_BOT_TOKEN"))

        try:
            blocks = [
                {"type": "section", "text": {"type": "mrkdwn", "text": message}},
                {"type": "divider"},
            ]
            if len(brokenLinks) > 0:
                broken_links_list = ""
                for brokenLink in brokenLinks:
                    broken_links_list += f" * {brokenLink[0]} : {brokenLink[1]} \n"
                blocks.append(
                    {
                        "type": "section",
                        "text": {"type": "mrkdwn", "text": broken_links_list},
                    }
                )

            client.chat_postMessage(
                channel=self.channel_id,
                blocks=blocks,
                text="This is the WebScanner app sending a message on Slack.",
            )

        except SlackApiError as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    sh = SlackHandler("")
    sh.send_message("hello there!")

import slack
import json
from .wx import metar


# Event Handlers
@slack.RTMClient.run_on(event='hello')
def hello(**payload):
    print('Successfully Connected')


@slack.RTMClient.run_on(event='message')
def msg_handler(**payload):
    data = payload['data']
    web_client = payload['web_client']

    self_user_id = web_client.auth_test().data['user_id']

    channel_id = data['channel']
    thread_ts = data['ts']
    subtype = data['subtype'] if 'subtype' in data else None
    user = data['user'] if 'user' in data else None
    text = data['text'] if 'text' in data else None

    print(f'({subtype}) {channel_id} - [{thread_ts}] - {user}: {text}')  # Debugging

    if text is not None:
        split_str = text.split()

        if split_str[0] == '!m':
            post_msg(
                wclient=web_client,
                channel=channel_id,
                thread_ts=None,
                message_body=metar(split_str[1]),
            )


def build_rtm_client(token):
    """
    Return an RTM client
    :param token:
    :return:
    """
    return slack.RTMClient(token=token)


def post_msg(wclient, channel, thread_ts, message_body):
    post_parms = {
        'channel': channel
    }
    if thread_ts is not None:
        post_parms['thread_ts'] = thread_ts

    wclient.chat_postMessage(
        **post_parms,
        **message_body
    )
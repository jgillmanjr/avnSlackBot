from botlib import build_rtm_client
import creds





def main():
    rclient = build_rtm_client(creds.bot_token)
    rclient.start()


if __name__ == '__main__':
    main()

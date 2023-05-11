from bot import Bot
import os


def main():
    bot = Bot()
    bot.create_group('music', 'Music related commands')

    bot.run(os.getenv('TOKEN'), reconnect=True)


if __name__ == '__main__':
    main()

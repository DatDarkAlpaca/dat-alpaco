import os
from bot import Bot
from dotenv import load_dotenv
from utils.logger import create_default_logger_file


def prepare_workspace():
    if not os.path.isdir('../res'):
        os.mkdir('../res')

    if not os.path.isfile('../res/client.log'):
        file = open('../res/client.log', 'w')
        file.close()

    if not os.path.isfile('../res/config.yaml'):
        create_default_logger_file()


def main():
    os.chdir(os.path.dirname(__file__))
    load_dotenv()

    prepare_workspace()
    return

    bot = Bot()
    bot.create_group('music', 'Music related commands')

    bot.run(os.getenv('TOKEN'), reconnect=True)


if __name__ == '__main__':
    main()

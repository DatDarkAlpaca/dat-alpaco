from src.bot import Bot
from fnmatch import fnmatch
from os import walk


def load_cogs(bot: Bot):
    file_pattern = '*.py'
    any_cogs_found = False

    for path, subdirectories, files in walk('./cogs'):
        for cog in files:
            if cog.startswith('_'):
                continue
            if fnmatch(cog, file_pattern):
                cog_path = path.replace('\\', '.').replace('./', '') + '.' + cog[:-3]
                try:
                    bot.load_extension(cog_path)
                    bot.logger.info(f"The cog '{cog[:-3]}' has been successfully loaded.")
                    any_cogs_found = True
                except Exception as e:
                    bot.logger.error(f"The cog '{cog[:-3]}' couldn't be loaded! | {e}")

    if not any_cogs_found:
        bot.logger.info('Not cogs were detected.')
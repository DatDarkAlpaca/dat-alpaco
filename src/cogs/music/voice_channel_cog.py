import wavelink
from discord import VoiceClient
from discord.utils import get
from discord.ext import commands
from discord.commands import ApplicationContext, SlashCommandGroup

from src.utils.context_utils import respond_ephemeral


class VoiceChannelCog(commands.Cog):
    voice_channel = SlashCommandGroup(name='vc', description='Voice channel related commands')

    def __init__(self, bot):
        self.bot = bot
        self.lock_status = {}

    @voice_channel.command(description="Joins the user's current voice channel")
    async def join(self, ctx):
        channel = ctx.author.voice.channel
        if not channel:
            return await respond_ephemeral(ctx, 'You need to be in a voice channel to do that.')

        # Lock mechanism:
        controller_uid = self.lock_status.get(ctx.guild_id)
        if controller_uid:
            if not controller_uid == ctx.author.id:
                return await respond_ephemeral(ctx, f"I'm currently locked by: {self.bot.get_user(controller_uid)}.")

        current_vc: VoiceClient = get(ctx.bot.voice_clients, guild=ctx.guild)
        if not current_vc:
            await respond_ephemeral(ctx, 'Entering your voice chat.')
            return await channel.connect(cls=wavelink.Player)

        if channel == current_vc.channel:
            await respond_ephemeral(ctx, "I'm already connected to your voice channel.")
            return None

        await respond_ephemeral(ctx, "Moved to your voice channel.")
        await current_vc.move_to(channel)
        return current_vc

    @voice_channel.command(description="Leaves the voice channel, if I'm in one.")
    async def leave(self, ctx: ApplicationContext):
        vc: wavelink.Player | None = ctx.voice_client
        if not vc:
            return await respond_ephemeral(ctx, "I'm not connected to any voice channel.")

        # Locking mechanism:
        controller_uid = self.lock_status.get(ctx.guild_id)
        if controller_uid:
            if not controller_uid == ctx.user.id:
                return await respond_ephemeral(ctx, f"I'm currently locked by: {self.bot.get_user(controller_uid)}.")

        await vc.disconnect()
        await respond_ephemeral(ctx, 'Leaving your voice chat.')

    @voice_channel.command(description="Locks the audio player so that people can't mess with it.")
    async def lock(self, ctx: ApplicationContext):
        gid = ctx.guild_id
        uid = ctx.user.id

        controller_uid = self.lock_status.get(gid)
        if controller_uid:
            return await respond_ephemeral(ctx, f"I'm already locked by: {self.bot.get_user(controller_uid)}.")

        self.lock_status[gid] = uid
        await respond_ephemeral(ctx, f"I have been successfully locked.")

    @voice_channel.command(description="Unlocks the audio player so that people can use it again.")
    async def unlock(self, ctx: ApplicationContext):
        gid = ctx.guild_id
        uid = ctx.user.id

        controller_uid = self.lock_status.get(gid)
        if not controller_uid:
            return await respond_ephemeral(ctx, f"I'm currently unlocked.")

        if controller_uid != uid:
            return await respond_ephemeral(ctx, f"Denied! I'm locked by: {self.bot.get_user(controller_uid)}, not you.")

        self.lock_status[gid] = None
        await respond_ephemeral(ctx, f"I have been successfully unlocked.")

    # Helpers:
    async def connect_and_get_voice_client(self, ctx):
        vc: wavelink.Player = ctx.voice_client
        if not vc:
            vc = await self.join(ctx)
            if not vc:
                return None
        return vc

    @staticmethod
    async def get_voice_channel(ctx):
        vc: wavelink.Player = ctx.voice_client
        if not vc:
            await respond_ephemeral(ctx, 'I need to be connected to a voice channel before executing this command')
            return None

        return vc


def setup(bot):
    bot.add_cog(VoiceChannelCog(bot))

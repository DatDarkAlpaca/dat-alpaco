import wavelink
from discord.ext import commands
from discord.commands import SlashCommandGroup
from discord import Option, AutocompleteContext, utils

from src.utils.context_utils import single_embed, respond_ephemeral


# Presets:
def get_equalizer_presets(_: AutocompleteContext) -> list:
    return ['Boost', 'Flat', 'Metal', 'Piano']


def get_channel_mix_presets(_: AutocompleteContext) -> list:
    return ['Full Left', 'Full Right', 'Mono', 'Only Left', 'Only Right', 'Switch']


class FilterSongCog(commands.Cog):
    filter = SlashCommandGroup(name='filter', description='Filter related commands')

    def __init__(self, bot):
        self.bot = bot
        self.current_filter = {}

    @filter.command(description='Resets the current filters')
    async def reset(self, ctx):
        vc: wavelink.Player = await self.bot.get_cog('VoiceChannelCog').connect_and_get_voice_client(ctx)
        if not vc:
            return

        new_filter = wavelink.Filter()
        self.current_filter[ctx.guild.id] = new_filter
        await vc.set_filter(new_filter)

        await single_embed(ctx, f"{ctx.user.mention} has reset all filters!")

    @filter.command(description='Applies an equalizer filter from a list of presets')
    async def equalizer(self, ctx,
                        preset: Option(str, autocomplete=utils.basic_autocomplete(get_equalizer_presets))):
        vc: wavelink.Player = await self.bot.get_cog('VoiceChannelCog').connect_and_get_voice_client(ctx)
        if not vc:
            return

        if preset == 'Boost':
            equalizer = wavelink.Equalizer(bands=[]).boost()
        elif preset == 'Flat':
            equalizer = wavelink.Equalizer(bands=[]).flat()
        elif preset == 'Metal':
            equalizer = wavelink.Equalizer(bands=[]).metal()
        elif preset == 'Piano':
            equalizer = wavelink.Equalizer(bands=[]).piano()
        else:
            return await respond_ephemeral(ctx, 'This filter preset does not exist.')

        current_filter = self.current_filter.get(ctx.guild.id)
        if current_filter:
            new_filter = wavelink.Filter(current_filter, equalizer=equalizer)
        else:
            new_filter = wavelink.Filter(equalizer=equalizer)
            self.current_filter[ctx.guild.id] = new_filter

        await vc.set_filter(new_filter)
        await single_embed(ctx, f"{ctx.user.mention} enabled an equalizer mix filter! To reset, use the command:"
                                f"`/filter reset`")

    @filter.command(description='Applies a karaoke filter to the player')
    async def karaoke(self, ctx,
                      level: Option(float, default=1.0, description='Default: 1.0'),
                      mono_level: Option(float, default=1.0, description='Default: 1.0'),
                      filter_band: Option(float, default=220.0, description='Default: 220.0'),
                      filter_width: Option(float, default=100.0, description='Default: 100.0')):

        vc: wavelink.Player = await self.bot.get_cog('VoiceChannelCog').connect_and_get_voice_client(ctx)
        if not vc:
            return

        karaoke = wavelink.Karaoke(level=level,
                                   mono_level=mono_level,
                                   filter_band=filter_band,
                                   filter_width=filter_width)

        current_filter = self.current_filter.get(ctx.guild.id)
        if current_filter:
            new_filter = wavelink.Filter(current_filter, karaoke=karaoke)
        else:
            new_filter = wavelink.Filter(karaoke=karaoke)
            self.current_filter[ctx.guild.id] = new_filter

        await vc.set_filter(new_filter)
        await single_embed(ctx, f"{ctx.user.mention} enabled a karaoke filter! To reset, use the command:"
                                f"`/filter reset`")

    @filter.command(description='Applies a timescale filter to the player')
    async def timescale(self, ctx,
                        speed: Option(float, default=1.0, description='Default: 1.0'),
                        pitch: Option(float, default=1.0, description='Default: 1.0'),
                        rate: Option(float, default=1.0, description='Default: 1.0')):

        vc: wavelink.Player = await self.bot.get_cog('VoiceChannelCog').connect_and_get_voice_client(ctx)
        if not vc:
            return

        timescale = wavelink.Timescale(speed=speed, pitch=pitch, rate=rate)

        current_filter = self.current_filter.get(ctx.guild.id)
        if current_filter:
            new_filter = wavelink.Filter(current_filter, timescale=timescale)
        else:
            new_filter = wavelink.Filter(timescale=timescale)
            self.current_filter[ctx.guild.id] = new_filter

        await vc.set_filter(new_filter)
        await single_embed(ctx, f"{ctx.user.mention} enabled a timescale filter! To reset, use the command:"
                                f"`/filter reset`")

    @filter.command(description='Applies a tremolo filter to the player')
    async def tremolo(self, ctx,
                      frequency: Option(float, default=2.0, description='Default: 2.0'),
                      depth: Option(float, default=0.5, description='Default: 0.5')):

        vc: wavelink.Player = await self.bot.get_cog('VoiceChannelCog').connect_and_get_voice_client(ctx)
        if not vc:
            return

        tremolo = wavelink.Tremolo(frequency=frequency, depth=depth)

        current_filter = self.current_filter.get(ctx.guild.id)
        if current_filter:
            new_filter = wavelink.Filter(current_filter, tremolo=tremolo)
        else:
            new_filter = wavelink.Filter(tremolo=tremolo)
            self.current_filter[ctx.guild.id] = new_filter

        await vc.set_filter(new_filter)
        await single_embed(ctx, f"{ctx.user.mention} enabled a tremolo filter! To reset, use the command:"
                                f"`/filter reset`")

    @filter.command(description='Applies a vibrato filter to the player')
    async def vibrato(self, ctx,
                      frequency: Option(float, default=2.0, description='Default: 2.0'),
                      depth: Option(float, default=0.5, description='Default: 0.5')):

        vc: wavelink.Player = await self.bot.get_cog('VoiceChannelCog').connect_and_get_voice_client(ctx)
        if not vc:
            return

        vibrato = wavelink.Vibrato(frequency=frequency, depth=depth)

        current_filter = self.current_filter.get(ctx.guild.id)
        if current_filter:
            new_filter = wavelink.Filter(current_filter, vibrato=vibrato)
        else:
            new_filter = wavelink.Filter(vibrato=vibrato)
            self.current_filter[ctx.guild.id] = new_filter

        await vc.set_filter(new_filter)
        await single_embed(ctx, f"{ctx.user.mention} enabled a vibrato filter! To reset, use the command:"
                                f"`/filter reset`")

    @filter.command(description='Applies a rotation filter to the player')
    async def rotation(self, ctx, speed: Option(float, default=5.0, description='Default: 5.0')):
        vc: wavelink.Player = await self.bot.get_cog('VoiceChannelCog').connect_and_get_voice_client(ctx)
        if not vc:
            return

        rotation = wavelink.Rotation(speed=speed)

        current_filter = self.current_filter.get(ctx.guild.id)
        if current_filter:
            new_filter = wavelink.Filter(current_filter, rotation=rotation)
        else:
            new_filter = wavelink.Filter(rotation=rotation)
            self.current_filter[ctx.guild.id] = new_filter

        await vc.set_filter(new_filter)
        await single_embed(ctx, f"{ctx.user.mention} enabled a rotation filter! To reset, use the command:"
                                f"`/filter reset`")

    @filter.command(description='Applies a distortion filter to the player')
    async def distortion(self, ctx,
                         sin_offset: Option(float, default=0.0, description='Default: 0.0'),
                         sin_scale: Option(float, default=1.0, description='Default: 1.0'),
                         cos_offset: Option(float, default=0.0, description='Default: 0.0'),
                         cos_scale: Option(float, default=1.0, description='Default: 1.0'),
                         tan_offset: Option(float, default=0.0, description='Default: 0.0'),
                         tan_scale: Option(float, default=1.0, description='Default: 1.0'),
                         offset: Option(float, default=0.0, description='Default: 0.0'),
                         scale: Option(float, default=1.0, description='Default: 1.0'),):

        vc: wavelink.Player = await self.bot.get_cog('VoiceChannelCog').connect_and_get_voice_client(ctx)
        if not vc:
            return

        distortion = wavelink.Distortion(sin_offset=sin_offset, sin_scale=sin_scale, cos_offset=cos_offset,
                                         cos_scale=cos_scale, tan_offset=tan_offset, tan_scale=tan_scale,
                                         offset=offset, scale=scale)

        current_filter = self.current_filter.get(ctx.guild.id)
        if current_filter:
            new_filter = wavelink.Filter(current_filter, distortion=distortion)
        else:
            new_filter = wavelink.Filter(distortion=distortion)
            self.current_filter[ctx.guild.id] = new_filter

        await vc.set_filter(new_filter)
        await single_embed(ctx, f"{ctx.user.mention} enabled a distortion filter! To reset, use the command:"
                                f"`/filter reset`")

    # Channel Mix:
    @filter.command(description='Applies a channel mix filter to the player')
    async def channel_mix(self, ctx,
                          left_to_left: Option(float, default=1.0, description='Default: 1.0'),
                          left_to_right: Option(float, default=1.0, description='Default: 1.0'),
                          right_to_left: Option(float, default=1.0, description='Default: 1.0'),
                          right_to_right: Option(float, default=1.0, description='Default: 1.0')):
        vc: wavelink.Player = await self.bot.get_cog('VoiceChannelCog').connect_and_get_voice_client(ctx)
        if not vc:
            return

        channel_mix = wavelink.ChannelMix(left_to_left=left_to_left, left_to_right=left_to_right,
                                          right_to_left=right_to_left, right_to_right=right_to_right)

        current_filter = self.current_filter.get(ctx.guild.id)
        if current_filter:
            new_filter = wavelink.Filter(current_filter, channel_mix=channel_mix)
        else:
            new_filter = wavelink.Filter(channel_mix=channel_mix)
            self.current_filter[ctx.guild.id] = new_filter

        await vc.set_filter(new_filter)
        await single_embed(ctx, f"{ctx.user.mention} enabled a channel mix filter! To reset, use the command:"
                                f"`/filter reset`")

    @filter.command(description='Applies a channel mix filter from a list of presets')
    async def channel_mix_preset(self, ctx,
                                 preset: Option(str, autocomplete=utils.basic_autocomplete(get_channel_mix_presets))):
        vc: wavelink.Player = await self.bot.get_cog('VoiceChannelCog').connect_and_get_voice_client(ctx)
        if not vc:
            return

        if preset == 'Full Left':
            channel_mix = wavelink.ChannelMix().full_left()
        elif preset == 'Full Right':
            channel_mix = wavelink.ChannelMix().full_right()
        elif preset == 'Mono':
            channel_mix = wavelink.ChannelMix().mono()
        elif preset == 'Only Left':
            channel_mix = wavelink.ChannelMix().only_left()
        elif preset == 'Only Right':
            channel_mix = wavelink.ChannelMix().only_right()
        elif preset == 'Switch':
            channel_mix = wavelink.ChannelMix().switch()
        else:
            return await respond_ephemeral(ctx, 'This filter preset does not exist.')

        current_filter = self.current_filter.get(ctx.guild.id)
        if current_filter:
            new_filter = wavelink.Filter(current_filter, channel_mix=channel_mix)
        else:
            new_filter = wavelink.Filter(channel_mix=channel_mix)
            self.current_filter[ctx.guild.id] = new_filter

        await vc.set_filter(new_filter)
        await single_embed(ctx, f"{ctx.user.mention} enabled a channel mix filter! To reset, use the command:"
                                f"`/filter reset`")

    @filter.command(description='Applies a low pass filter to the player')
    async def low_pass(self, ctx, smoothing: Option(float, default=20.0, description='Default: 20.0')):
        vc: wavelink.Player = await self.bot.get_cog('VoiceChannelCog').connect_and_get_voice_client(ctx)
        if not vc:
            return

        low_pass = wavelink.LowPass(smoothing=smoothing)

        current_filter = self.current_filter.get(ctx.guild.id)
        if current_filter:
            new_filter = wavelink.Filter(current_filter, low_pass=low_pass)
        else:
            new_filter = wavelink.Filter(low_pass=low_pass)
            self.current_filter[ctx.guild.id] = new_filter

        await vc.set_filter(new_filter)
        await single_embed(ctx, f"{ctx.user.mention} enabled a low pass filter! To reset, use the command:"
                                f"`/filter reset`")


def setup(bot):
    bot.add_cog(FilterSongCog(bot))

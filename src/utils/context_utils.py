from discord import Embed


async def respond_ephemeral(ctx, message: str, delete_after: int = 7):
    await ctx.respond(message, delete_after=delete_after, ephemeral=True)


async def single_embed(ctx, description: str):
    embed = Embed(description=description, color=0x38f2ff)
    await ctx.send_response(embed=embed)

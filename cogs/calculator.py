# -----------------------------------------------------------
# This is a discord bot by ArikSquad and you are viewing the source code of it.
#
# This file is not protected by any license
#
# -----------------------------------------------------------
from __future__ import division

import discord
from discord.ext import commands
from simpcalc import simpcalc


# noinspection PyUnusedLocal
class InteractiveView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.expr = ""
        self.calc = simpcalc.Calculate()
        self.response = None

    async def on_timeout(self) -> None:
        for child in self.children:
            child.disabled = True
        await self.response.edit(view=self)

    @discord.ui.button(style=discord.ButtonStyle.blurple, label="1", row=0)
    async def one(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.expr += "1"
        await interaction.message.edit(content=f"```\n{self.expr}\n```")
        await interaction.response.defer()

    @discord.ui.button(style=discord.ButtonStyle.blurple, label="2", row=0)
    async def two(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.expr += "2"
        await interaction.message.edit(content=f"```\n{self.expr}\n```")
        await interaction.response.defer()

    @discord.ui.button(style=discord.ButtonStyle.blurple, label="3", row=0)
    async def three(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.expr += "3"
        await interaction.message.edit(content=f"```\n{self.expr}\n```")
        await interaction.response.defer()

    @discord.ui.button(style=discord.ButtonStyle.green, label="+", row=0)
    async def plus(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.expr += "+"
        await interaction.message.edit(content=f"```\n{self.expr}\n```")
        await interaction.response.defer()

    @discord.ui.button(style=discord.ButtonStyle.blurple, label="4", row=1)
    async def last(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.expr += "4"
        await interaction.message.edit(content=f"```\n{self.expr}\n```")
        await interaction.response.defer()

    @discord.ui.button(style=discord.ButtonStyle.blurple, label="5", row=1)
    async def five(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.expr += "5"
        await interaction.message.edit(content=f"```\n{self.expr}\n```")
        await interaction.response.defer()

    @discord.ui.button(style=discord.ButtonStyle.blurple, label="6", row=1)
    async def six(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.expr += "6"
        await interaction.message.edit(content=f"```\n{self.expr}\n```")
        await interaction.response.defer()

    @discord.ui.button(style=discord.ButtonStyle.green, label="/", row=1)
    async def divide(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.expr += "/"
        await interaction.message.edit(content=f"```\n{self.expr}\n```")
        await interaction.response.defer()

    @discord.ui.button(style=discord.ButtonStyle.blurple, label="7", row=2)
    async def seven(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.expr += "7"
        await interaction.message.edit(content=f"```\n{self.expr}\n```")
        await interaction.response.defer()

    @discord.ui.button(style=discord.ButtonStyle.blurple, label="8", row=2)
    async def eight(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.expr += "8"
        await interaction.message.edit(content=f"```\n{self.expr}\n```")
        await interaction.response.defer()

    @discord.ui.button(style=discord.ButtonStyle.blurple, label="9", row=2)
    async def nine(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.expr += "9"
        await interaction.message.edit(content=f"```\n{self.expr}\n```")
        await interaction.response.defer()

    @discord.ui.button(style=discord.ButtonStyle.green, label="*", row=2)
    async def multiply(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.expr += "*"
        await interaction.message.edit(content=f"```\n{self.expr}\n```")
        await interaction.response.defer()

    @discord.ui.button(style=discord.ButtonStyle.blurple, label=".", row=3)
    async def dot(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.expr += "."
        await interaction.message.edit(content=f"```\n{self.expr}\n```")
        await interaction.response.defer()

    @discord.ui.button(style=discord.ButtonStyle.blurple, label="0", row=3)
    async def zero(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.expr += "0"
        await interaction.message.edit(content=f"```\n{self.expr}\n```")
        await interaction.response.defer()

    @discord.ui.button(style=discord.ButtonStyle.green, label="=", row=3)
    async def equal(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            self.expr = await self.calc.calculate(self.expr)
        except simpcalc.BadArgument:
            await interaction.response.defer()
            return await interaction.message.edit(content=f"```\nNot possible...\n```")
        await interaction.message.edit(content=f"```\n{self.expr}\n```")
        await interaction.response.defer()

    @discord.ui.button(style=discord.ButtonStyle.green, label="-", row=3)
    async def minus(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.expr += "-"
        await interaction.message.edit(content=f"```\n{self.expr}\n```")
        await interaction.response.defer()

    @discord.ui.button(style=discord.ButtonStyle.green, label="(", row=4)
    async def left_bracket(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.expr += "("
        await interaction.message.edit(content=f"```\n{self.expr}\n```")
        await interaction.response.defer()

    @discord.ui.button(style=discord.ButtonStyle.green, label=")", row=4)
    async def right_bracket(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.expr += ")"
        await interaction.message.edit(content=f"```\n{self.expr}\n```")
        await interaction.response.defer()

    @discord.ui.button(style=discord.ButtonStyle.red, label="C", row=4)
    async def clear(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.expr = ""
        await interaction.message.edit(content=f"```\n{self.expr}\n```")
        await interaction.response.defer()

    @discord.ui.button(style=discord.ButtonStyle.danger, label="DEL", row=4)
    async def delete(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.expr = self.expr[:-1]
        await interaction.message.delete()


class Calculator(commands.Cog, description="Calculator"):
    EMOJI = "🧮"

    def __init__(self, bot):
        self.bot = bot

    # Calculate using buttons
    @commands.command(name="calculate", help="Calculator simulator", aliases=["calc", "calculator"],
                      brief='You can do calculations using this command')
    async def interactive_calc(self, ctx: commands.Context):
        view = InteractiveView()
        await ctx.send("```\n```", view=view)


async def setup(bot):
    await bot.add_cog(Calculator(bot))

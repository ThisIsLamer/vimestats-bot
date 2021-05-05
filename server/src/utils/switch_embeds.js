async function start(client, embeds, msg, emojis=["◀", "▶"], option={author: true, time: 150000, page: 0, footer: "[Время вышло]"}) {
    const message = await msg.channel.send(embeds[option.page]);
    
    const filter = (reaction, user) => {
        if (option.author) return (reaction.emoji === emojis[0] || reaction.emoji === emojis[1]) && user.id === msg.author.id;
        return reaction.emoji === emojis[0] || reaction.emoji === emojis[1];
    }
    const collector = await message.createReactionCollector(filter, { time: option.time });
    for (let i of emojis) {
        await message.react(i);
    }

    await collector.on('collect', async (reaction, user) => {
        if (reaction.emoji === emojis[0]) {
            if (option.page <= 0) return;
            else option.page -= 1;
        } else {
            if (option.page >= embeds.length-1) return;
            else option.page += 1;
        }

        await reaction.users.remove(user);
        await collector.resetTimer();
        await message.edit(embeds[option.page]);
    })

    await collector.on("end", async collected => {
        await message.edit(embeds[option.page].setFooter(option.footer))
        await message.reactions.removeAll();
    })
}

module.exports = {start}
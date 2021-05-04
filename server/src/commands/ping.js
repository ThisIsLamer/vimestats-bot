const { get_player_nick } = require(process.cwd() + "/src/vimeapi.js");

module.exports = {
    name: "ping",
    description: "test command",
    async execute(client, message, args) {
        console.log(await get_player_nick(args[0]));
        await message.channel.send("pong");
    }
}
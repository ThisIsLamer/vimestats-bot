module.exports = {
    name: "ping",
    description: "test command",
    async execute(client, message, args) {
        console.log(process.cwd());
        await message.channel.send("pong");
    }
}
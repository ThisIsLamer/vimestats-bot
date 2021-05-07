module.exports = {
    name: "error",
    description: "Событие срабатывает при появлении ошибки",
    command: false,
    async execute(client, err, logger, logging) {
        if (logging) {
            if (err) logger.error(err);
        }
    }
}
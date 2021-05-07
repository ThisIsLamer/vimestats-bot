module.exports = {
    name: "ready",
    description: "Событие срабатывает, когда клиент готов начать работу",
    command: false,
    async execute(client, logger, logging) {
        if (logging) logger.log("Клиент готов начать работу")
    }
}
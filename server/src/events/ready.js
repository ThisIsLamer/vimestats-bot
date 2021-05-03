module.exports = {
    name: "ready",
    description: "Событие срабатывает, когда клиент готов начать работу",
    async execute(client, logger, logging) {
        if (logging) logger.log("Клиент готов начать работу")
    }
}
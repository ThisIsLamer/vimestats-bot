const fs = require("fs");

module.exports = {
    name: "import_modules",
    description: "Утилита позволяющая создавать коллекцию комманд",
    // параметр value принимает путь до папки с нужными модулями
    execute(client, value, logger, logging=true) {
        // берём все файлы название которых оканчивается на .js
        const files = fs.readdirSync(value).filter(file => file.endsWith(".js"));
        // импортируем все файлы в коллекцию. {name: module}
        for (const file of files) {
            if (logging) logger.log(`Модуль [${value}/${file}] - загружен`);
            const props = require(`${process.cwd()}/${value}/${file}`);
            client.commands.set(props.name, props);
        }
    }
}
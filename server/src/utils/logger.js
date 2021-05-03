// формирование текста для вывода по заданным параметрам
function preparation(lvl, text, settings) {
    let level, date, module, body;

    if (settings.level) level = `[${lvl}]`;
    if (settings.date) date = `[${new Date().toLocaleString()}]`;
    if (settings.module) module = `[${"Testing"}]`;
    if (settings.body) body = text;
    
    return `${date} ${module} : ${level} - ${body}`;
}

// параметры вывода логов в консоль
function consoleOutput(lvl, text, settings) {
    // разукрашиваем текст в консоли
    if (lvl === "debug" || lvl === "log") console.log(preparation(lvl, text, settings), "\x1b[0m")      // стандартный
    if (lvl === "error") console.log("\x1b[32m", preparation(lvl, text, settings), "\x1b[0m");           // зелёный
    if (lvl === "warn") console.log("\x1b[33m", preparation(lvl, text, settings), "\x1b[0m");            // жёлтый
    if (lvl === "fatal") console.log("\x1b[31m",preparation(lvl, text, settings), "\x1b[0m");            // красный
}

module.exports = {
    name: "logger",
    description: "Утилита позволяющая логировать ошибки, исключения, и т.д.",
    // параметры логирования
    settings: {level: true, date: true, module: true, body: true, file: true, console: true},

    // уровни логирования
    debug(value) {if (this.settings.console) consoleOutput("debug", value, this.settings)},
    log(value) {if (this.settings.console) consoleOutput("log", value, this.settings)},
    error(value) {if (this.settings.console) consoleOutput("error", value, this.settings)},
    warn(value) {if (this.settings.console) consoleOutput("warn", value, this.settings)},
    fatal(value) {if (this.settings.console) consoleOutput("fatal", value, this.settings)},

    // параметры записи логов вв файл
    writingFile() {
        
    },
}
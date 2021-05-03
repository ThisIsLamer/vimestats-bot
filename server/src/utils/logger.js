const fs = require("fs");

// создаём log файл по дате
const date = new Date().toLocaleString().replace(":", "-").replace(":", "-");
const filename = process.cwd() + `/logs/${date}.log`;
fs.open(filename, "a", err => {if (err) console.error(err)});

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
function console_output(lvl, text, settings) {
    // разукрашиваем текст в консоли
    if (lvl === "debug" || lvl === "log") console.log(preparation(lvl, text, settings), "\x1b[0m")      // стандартный
    if (lvl === "error") console.log("\x1b[32m", preparation(lvl, text, settings), "\x1b[0m");           // зелёный
    if (lvl === "warn") console.log("\x1b[33m", preparation(lvl, text, settings), "\x1b[0m");            // жёлтый
    if (lvl === "fatal") console.log("\x1b[31m",preparation(lvl, text, settings), "\x1b[0m");            // красный
}

function writing_to_file(lvl, text, settings, recording) {
    if (recording) fs.appendFile(filename, preparation(lvl, text, settings) + "\n", err => {if (err) console.error(err)});
}

module.exports = {
    name: "logger",
    description: "Утилита позволяющая логировать ошибки, исключения, и т.д.",
    // параметры логирования
    settings: {level: true, date: true, module: true, body: true, file: true, console: true},

    // уровни логирования
    debug(value, recording=true) {if (this.settings.console) {
        console_output("debug", value, this.settings);
        writing_to_file("debug", value, this.settings, recording);
    }},
    log(value, recording=true) {if (this.settings.console) {
        console_output("log", value, this.settings);
        writing_to_file("log", value, this.settings, recording);
    }},
    error(value, recording=true) {if (this.settings.console) {
        console_output("error", value, this.settings);
        writing_to_file("error", value, this.settings, recording);
    }},
    warn(value, recording=true) {if (this.settings.console) {
        console_output("warn", value, this.settings);
        writing_to_file("warn", value, this.settings, recording);
    }},
    fatal(value, recording=true) {if (this.settings.console) {
        console_output("fatal", value, this.settings);
        writing_to_file("fatal", value, this.settings, recording);
    }},
}
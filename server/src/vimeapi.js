const fetch = require("node-fetch");

const config = require(process.cwd() + "/src/config.json");
const token = config.VIMEAPI.TOKEN;

async function get_request(url) {
    await fetch(url)
        .then(async res => this.responce = await res.json());
    return this.responce;
}

module.exports = {
    // получить игрока по нику
    async get_player_nick(nick) {
        const user = await get_request(`https://api.vimeworld.ru/user/name/${nick}?token=${token}`);
        if (user.length === 0) return {error: {code: -1}};
        else return user;
    },
    // получить игрока по id
    async get_player_id(id) {
        const user = await get_request(`https://api.vimeworld.ru/user/${id}?token=${token}`);
        if (user.length === 0) return {error: {code: -1}};
        else return user;
    },
    // получить друзей игрока по id
    async get_player_friends(id) {
        return await get_request(`https://api.vimeworld.ru/user/${id}/friends?token=${token}`);
    },
    // получить статус игрока по id
    async get_player_status(id) {
        return await get_request(`https://api.vimeworld.ru/user/${id}/session?token=${token}`);
    },
    // получить статистику игрока, значение в параметре games указывается через запятую ahh,lk,bd
    async get_player_stats(id, games=null) {
        if (games === null) return await get_request(`https://api.vimeworld.ru/user/${id}/stats?token=${token}`);
        else return await get_request(`https://api.vimeworld.ru/user/${id}/stats?games=${games}?token=${token}`);
    },
    // получить достижения игрока
    async get_player_achievements(id) {
        return await get_request(`https://api.vimeworld.ru/user/${id}/achievements?token=${token}`);
    },
    // поиск гильдии по названию и тегу
    async guild_search(query) {
        const guilds = await get_request(`https://api.vimeworld.ru/guild/search?query=${query}?token=${token}`);
        if (guilds.length === 0) return {error: {code: -1}};
        else return guilds;
    },
    // поиск гильдии по id
    async get_guild(id) {
        return await get_request(`https://api.vimeworld.ru/guild/get?id=${id}?token=${token}`);
    },
    async get_leaderboard(mode, records) {
        return await get_request(`https://api.vimeworld.ru/leaderboard/get/${mode}/wins?size=${records}`);
    },
    // получить количество онлайн игроков
    async get_online() {
        return await get_request(`https://api.vimeworld.ru/online?token=${token}`);
    },
    // получить список онлайн стримов
    async get_streams() {
        return await get_request(`https://api.vimeworld.ru/online/streams?token=${token}`);
    },
    // список онлайн модераторов
    async get_staff_online() {
        return await get_request(`https://api.vimeworld.ru/online/staff?token=${token}`);
    },
    // Переведённые названия игр, статистики, рангов
    async get_locale(parts=null, name="ru") {
        return await get_request(`https://api.vimeworld.ru/locale/ru?parts=game_stats?token=${token}`);
    },
    // получить голову игрока
    async get_player_head(nick) {
        return `http://skin.vimeworld.ru/head/${nick}.png`
    },
    async get_player_page(nick) {
        return `https://vimetop.ru/player/${nick}`;
    }
}
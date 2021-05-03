const fs = require("fs");
const logger = require("../utils/logger");

const prefix_database_file = process.cwd() + "/src/database/prefix_database.json";


function put_prefix(guild_id, prefix) {
    fs.readFile(prefix_database_file, "utf8", (err, data) => {
        if (err) logger.error(err);
        else {
            obj = JSON.parse(data);
            obj.prefix[guild_id] = prefix;
            json = JSON.stringify(obj);
            fs.writeFile(prefix_database_file, json, "utf8", ()=>{});
        }
    })
}

async function get_prefix(guild_id, pref="!") {
    let prefix = pref;
    fs.readFile(prefix_database_file, "utf8", async (err, data) => {
        if (err) logger.error(err);
        else {
            obj = await JSON.parse(data).prefix[guild_id];
            if (obj != undefined) {
                this.prefix = obj;
            }            
        }
    })
    return new Promise((resolve) => {
        resolve(prefix);
    });
}

function check_guild(guild_id) {
    let channel;
    const data = fs.readFileSync(prefix_database_file, "utf8");
    const guild_ids = Object.keys(JSON.parse(data).prefix);
  
    if (guild_ids.includes(guild_id)) {
        channel = guild_ids[guild_ids.indexOf(guild_id)];
    }

    return channel;
}

module.exports = {put_prefix, get_prefix, check_guild}
const express = require('express');
const { hostname } = require('os');
const { lookup } = require('dns').promises;

const app = express();
const port = 3000;

(async () => {
    async function _getIpAddress() {
        return (await lookup(hostname())).address
    }

    app.get('/', async (req, res) => {
        ipAddress = await _getIpAddress()
        res.send(`Hostname: ${hostname()}.<br/>IP Address: ${ipAddress}`)
    })

    app.listen(port, () => {
        console.log(`Listening on port ${port}`)
    })
})();
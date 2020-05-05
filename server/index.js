const https = require('https')
const fs = require('fs')
const express = require('express');
const { hostname, networkInterfaces } = require('os');

const app = express();
const port = process.env.WEB_PORT || 3000;
const certificates_path = process.env.SSL_CERTIFICATES_PATH || '.'

const privateKey = fs.readFileSync(`${certificates_path}/key.pem`, 'utf8')
const certificate = fs.readFileSync(`${certificates_path}/cert.pem`, 'utf8')
const credentials = {
    key: privateKey,
    cert: certificate
}

function _getIpAddress() {
    let ifaces = networkInterfaces()

    let ips = ''

    for (iface in ifaces) {
        ifaces[iface].forEach((ifaceProp) => {
            if (ifaceProp.family !== 'IPv4' || ifaceProp.internal !== false) {
                // skip over internal (i.e. 127.0.0.1) and non-ipv4 addresses
                return
            }

            ips += `${ifaceProp.address}, `
            return
        })
    }

    ips = ips.substr(0, ips.length - 2)

    return ips
}

app.get('/healthcheck', (req, res) => {
    console.log(`Got incoming request for healthcheck from: ${req.ip}`)
    res.sendStatus(200)
})

app.get('/', async (req, res) => {
    console.log(`Got incoming request for server details from: ${req.ip}`)
    ipAddress = _getIpAddress()
    res.send(`Hostname: ${hostname()}.<br/>IP Address: ${ipAddress}`)
})

const httpsServer = https.createServer(credentials, app)
httpsServer.listen(port, () => {
    console.log(`Listening on port ${port}`)
})
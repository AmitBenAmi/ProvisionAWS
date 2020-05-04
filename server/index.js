const express = require('express');
const { hostname, networkInterfaces } = require('os');

const app = express();
const port = process.env.WEB_PORT || 3000;

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

app.get('/', async (req, res) => {
    ipAddress = _getIpAddress()
    res.send(`Hostname: ${hostname()}.<br/>IP Address: ${ipAddress}`)
})

app.listen(port, () => {
    console.log(`Listening on port ${port}`)
})
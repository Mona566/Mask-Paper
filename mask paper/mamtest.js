const { composeAPI } = require('@iota/core');
const { asciiToTrytes, trytesToAscii } = require('@iota/converter')
const { createChannel, createMessage, parseMessage, mamAttach, mamFetch } = require('@iota/mam.js');
const crypto = require('crypto');
const fs = require('fs');
const moment = require('moment');
const MQTT = require('mqtt')

const IOTA = require('iota.lib.js');


// Setup the details for the channel.
const mode = 'public';
const sideKey = '';
let channelState;

const publish = async function(packet) {
    console.log('publishing message... ')
    console.log(packet)

    // Try and load the channel state from json file
    try {
       const currentState = fs.readFileSync('./channelState.json');
       if (currentState) {
           channelState = JSON.parse(currentState.toString());
        }
    } catch (e) { }

   // If we couldn't load the details then create a new channel.
   if (!channelState) {
      channelState = createChannel(generateSeed(81), 2, mode)
   }


    // Create a MAM message using the channel state.
    const mamMessage = createMessage(channelState, asciiToTrytes(JSON.stringify(packet)));

    console.log('Root:', mamMessage.root);

    // Store the channel state.
    try {
        fs.writeFileSync('./channelState.json', JSON.stringify(channelState, undefined, "\t"));
    } catch (e) {
        console.error(e)
    }

    const api = composeAPI({ provider: "https://nodes.devnet.iota.org" });
    // Attach the message.
    console.log('Attaching to tangle, please wait...')
    await mamAttach(api, mamMessage, 3, 9);
    console.log(`You can view the mam channel here https://explorer.iota.org/legacy-devnet/streams/0/${mamMessage.root}/${mode}/`);
}


function generateSeed(length) {
    const charset = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ9';
    let seed = '';
    while (seed.length < length) {
        const byte = crypto.randomBytes(1)
        if (byte[0] < 243) {
            seed += charset.charAt(byte[0] % 27);
        }
    }
    return seed;
}


/// mqtt part ///
var mqtt_subscriber = MQTT.connect({
    host: 'localhost',
    port: 1883})

mqtt_subscriber.on('connect', function() {
    mqtt_subscriber.subscribe('data', function(err) {
	if(!err) {
	    console.log('connected and subscribed to mqtt sensors/data stream');
	}
    })
})



mqtt_subscriber.on('message', function(topic, message) {
    obj = JSON.parse(message);
    const root = publish(obj);
})

process.on('uncaughtException', function (exception) {
    console.log(exception);
});


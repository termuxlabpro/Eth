const fs = require('fs');
const { randomBytes } = require('crypto');
const { ec } = require('elliptic');
const { keccak256 } = require('js-sha3');
const { exec } = require('child_process');
const readline = require('readline');

// Create a new elliptic curve instance for secp256k1
const ecInstance = new ec('secp256k1');

// ANSI color codes
const colors = {
    reset: "\x1b[0m",
    green: "\x1b[32m",
    red: "\x1b[31m",
    cyan: "\x1b[36m",
};

// Function to display banner
const displayBanner = () => {
    console.clear();
    const bannerArt = [
        `${colors.green}████████╗██╗     ██████╗ `,
        "╚══██╔══╝██║     ██╔══██╗",
        "   ██║   ██║     ██████╔╝",
        "   ██║   ██║     ██╔═══╝ ",
        "   ██║   ███████╗██║     ",
        "   ╚═╝   ╚══════╝╚═╝     ",
        `${colors.cyan}╔═══════════════════════════════╗`,
        `${colors.cyan}║         T . L . P            ║`,
        `${colors.cyan}║     Multi-Chain Wallet         ║`,
        `${colors.cyan}╚═══════════════════════════════╝`,
        `${colors.green}📺 YouTube : https://youtube.com/@termuxlabpro`,
        `${colors.green}💬 Telegram: https://t.me/termuxlabpro`,
        `${colors.green}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n`
    ];
    for (const line of bannerArt) {
        console.log(line);
    }
};

// Function to generate a random Ethereum private key and corresponding address
const generateWallet = () => {
    const privateKey = randomBytes(32);
    const keyPair = ecInstance.keyFromPrivate(privateKey);
    const publicKey = keyPair.getPublic().encode('hex');
    const address = '0x' + keccak256(Buffer.from(publicKey.slice(2), 'hex')).slice(-40);
    
    return { privateKey: privateKey.toString('hex'), address }; // Return private key and address
};

// Function to generate address from a given private key
const addressFromPrivateKey = (privateKeyHex) => {
    const keyPair = ecInstance.keyFromPrivate(privateKeyHex);
    const publicKey = keyPair.getPublic().encode('hex');
    const address = '0x' + keccak256(Buffer.from(publicKey.slice(2), 'hex')).slice(-40);
    return address;
};

// Function to check balance using separate API keys for each chain
const checkBalance = (address, apiKeys) => {
    const chains = [
        { id: 'eth', name: 'Ethereum', apiKey: apiKeys.Etherscan },
        { id: 'bsc', name: 'BSC', apiKey: apiKeys.BSCScan },
        { id: 'polygon', name: 'Polygon', apiKey: apiKeys.PolygonScan },
    ];

    chains.forEach(({ id, name, apiKey }) => {
        exec(`python3 check_balance.py ${address} ${apiKey} ${id}`, (error, stdout, stderr) => {
            if (error) {
                console.error(`Error executing Python script: ${stderr}`);
                return;
            }
            console.log(stdout);
        });
    });
};

// Function to prompt for API keys for each chain
const promptForApiKeys = (callback) => {
    const rl = readline.createInterface({
        input: process.stdin,
        output: process.stdout
    });

    const apiKeys = {};

    const askForApiKey = (chain) => {
        rl.question(`Please enter your ${chain} API key: `, (apiKey) => {
            apiKeys[chain] = apiKey;
            if (chain === 'Etherscan') {
                askForApiKey('BSCScan');
            } else if (chain === 'BSCScan') {
                askForApiKey('PolygonScan');
            } else {
                rl.close();
                callback(apiKeys);
            }
        });
    };

    askForApiKey('Etherscan'); // Start the chain asking with Etherscan
};

// Function to create a loading animation
const loadingAnimation = () => {
    const frames = ['⣷', '⣯', '⡿', '⣿'];
    let index = 0;

    return setInterval(() => {
        process.stdout.write(`\rLoading... ${frames[index++]}`);
        index %= frames.length;
    }, 250);
};

// Main wallet generation function
const startWalletGeneration = (apiKeys) => {
    const loading = loadingAnimation();

    // Generate wallets and check balances at set intervals
    setInterval(() => {
        const { privateKey, address } = generateWallet();
        console.log(`\n${colors.cyan}Generated Private Key: ${privateKey}${colors.reset}`);
        console.log(`${colors.cyan}Wallet Address: ${address}${colors.reset}`);
        checkBalance(address, apiKeys);
    }, 1000); // Repeat every 1 second

    // Clear loading animation after 5 seconds
    setTimeout(() => {
        clearInterval(loading);
        process.stdout.write('\r'); // Clear the loading line
    }, 5000);
};

// Main logic
const main = () => {
    displayBanner(); // Display the banner first
    promptForApiKeys((apiKeys) => {
        startWalletGeneration(apiKeys);
    });
};

main();

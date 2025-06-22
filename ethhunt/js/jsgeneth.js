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
    console.clear(); // Clear the terminal
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

// Function to check balance using separate API keys for each chain
const checkBalance = (address, apiKeys, privateKey) => {
    const chains = [
        { id: 'eth', name: 'Ethereum', apiKey: apiKeys.Etherscan },
        { id: 'bsc', name: 'BSC', apiKey: apiKeys.BSCScan },
        { id: 'polygon', name: 'Polygon', apiKey: apiKeys.PolygonScan },
    ];

    const balanceResults = {
        Eth: 0,
        Bsc: 0,
        Pol: 0
    };

    const balancePromises = chains.map(({ id, name, apiKey }) => {
        return new Promise((resolve) => {
            exec(`python3 check_balance.py ${address} ${apiKey} ${id}`, (error, stdout, stderr) => {
                if (error) {
                    console.error(`Error executing Python script for ${name}: ${stderr}`);
                    resolve();
                    return;
                }

                // Assuming the Python script returns balance in a specific format
                const balanceMatch = stdout.match(/Balance: (\d+\.\d+)/);
                if (balanceMatch) {
                    const balance = parseFloat(balanceMatch[1]);
                    balanceResults[name] = balance;
                }
                resolve();
            });
        });
    });

    Promise.all(balancePromises).then(() => {
        // Output the results in the desired format
        console.log(`\n${colors.green}Generated Private Key: ${privateKey}${colors.reset}`);
        console.log(`${colors.green}Wallet Address: ${address}${colors.reset}`);
        console.log(`Balance ➤`);
        console.log(`Eth: ${balanceResults.Eth}`);
        console.log(`Bsc: ${balanceResults.Bsc}`);
        console.log(`Pol: ${balanceResults.Pol}`);
    });
};

// Function to prompt for API keys for each chain
const promptForApiKeys = (callback) => {
    const rl = readline.createInterface({
        input: process.stdin,
        output: process.stdout
    });

    const apiKeys = {};

    // Function to ask for the API key for a specific chain
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
        checkBalance(address, apiKeys, privateKey);
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

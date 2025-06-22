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
    cyan: "\x1b[36m",
};

// API keys file path
const apiKeysFilePath = './api_keys.json';
// Output file for valid wallets
const validWalletsFilePath = './valid_wallets.txt';

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

// Function to check the balances using separate API keys for each chain
const checkBalances = (address, apiKeys) => {
    const chains = [
        { id: 'eth', name: 'Ethereum', apiKey: apiKeys.Etherscan },
        { id: 'bsc', name: 'BSC', apiKey: apiKeys.BSCScan },
        { id: 'polygon', name: 'Polygon', apiKey: apiKeys.PolygonScan },
    ];

    let balanceResults = {
        Eth: 0,
        Bsc: 0,
        Pol: 0
    };

    const promises = chains.map(({ id, name, apiKey }) => {
        return new Promise((resolve, reject) => {
            exec(`python3 check_balance.py ${address} ${apiKey} ${id}`, (error, stdout, stderr) => {
                if (error) {
                    console.error(`Error executing Python script: ${stderr}`);
                    reject(error);
                }
                
                const balanceMatch = stdout.match(/Main Balance for address (.+): (.+) ETH/);
                if (balanceMatch) {
                    const balance = parseFloat(balanceMatch[2]);
                    balanceResults[name] = balance;
                }
                resolve();
            });
        });
    });

    Promise.all(promises).then(() => {
        console.log(`\n${colors.green}Generated Private Key: ${address}${colors.reset}`);
        console.log(`${colors.green}Wallet Address: ${address}${colors.reset}`);
        console.log(`Balance ➤`);
        console.log(`Eth: ${balanceResults.Eth}`);
        console.log(`Bsc: ${balanceResults.Bsc}`);
        console.log(`Pol: ${balanceResults.Pol}`);
        
        // If any balance is greater than 0, save the wallet details
        if (balanceResults.Eth > 0 || balanceResults.Bsc > 0 || balanceResults.Pol > 0) {
            const walletDetails = `Address: ${address}\nPrivate Key: ${privateKey}\nBalances: ETH: ${balanceResults.Eth}, BSC: ${balanceResults.Bsc}, POLYGON: ${balanceResults.Pol}\n\n`;
            fs.appendFileSync(validWalletsFilePath, walletDetails);
            console.log(`${colors.green}Wallet details saved to ${validWalletsFilePath}${colors.reset}`);
        }
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
                // Save the API keys to a JSON file
                fs.writeFileSync(apiKeysFilePath, JSON.stringify(apiKeys, null, 2));
                callback(apiKeys);
            }
        });
    };

    askForApiKey('Etherscan'); // Start the chain asking with Etherscan
};

// Function to load API keys from the JSON file
const loadApiKeys = () => {
    if (fs.existsSync(apiKeysFilePath)) {
        const apiKeys = JSON.parse(fs.readFileSync(apiKeysFilePath));
        return apiKeys;
    }
    return null; // Return null if the file does not exist
};

// Main wallet generation function
const startWalletGeneration = (apiKeys) => {
    // Generate wallets and check balances at set intervals
    setInterval(() => {
        const { privateKey, address } = generateWallet();
        checkBalances(address, apiKeys);
    }, 1000); // Repeat every 1 second
};

// Main logic
const main = () => {
    displayBanner(); // Display the banner first

    // Load API keys from the file if they exist
    const apiKeys = loadApiKeys();

    if (apiKeys) {
        console.log(`${colors.green}Loaded API keys from file.${colors.reset}`);
        startWalletGeneration(apiKeys);
    } else {
        console.log(`${colors.green}No API keys found. Please enter them.${colors.reset}`);
        promptForApiKeys((apiKeys) => {
            startWalletGeneration(apiKeys);
        });
    }
};

main();

import { ethers } from "https://cdn.jsdelivr.net/npm/ethers@6.8.1/+esm";

const provider = window.enkrypt?.providers?.ethereum;

document.getElementById("connectWalletBtn").addEventListener("click", async () => {
  if (!provider) {
    alert("🦉 Enkrypt Wallet not found. Please install it.");
    return;
  }

  try {
    const accounts = await provider.request({ method: "eth_requestAccounts" });
    const address = accounts[0];

    // Update DOM
    document.getElementById("walletAddress").value = address;
    document.getElementById("walletShort").textContent = address.slice(0, 6) + "..." + address.slice(-4);
    document.getElementById("connectedDisplay").classList.remove("hidden");

    console.log("✅ Connected: ", address);
  } catch (err) {
    console.error("❌ Connection failed", err);
    alert("❌ Failed to connect to wallet.");
  }
});


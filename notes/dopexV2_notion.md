---
noteId: "1db502d0499911eea4f8db847f52532e"
tags: []

---

# rDPX V2 RI

rDPX V2 is a new system which involves a series of changes and additions to the current utility of the rDPX token.

## *Glossary*

1. ***Backing Reserve*** - ******The reserve of tokens which back the amount of dpxETH in supply, there are 2 token reserves: rDPX Backing Reserve and ETH Backing Reserve
2. ***Treasury Reserve*** - The reserve of tokens held by the treasury for decaying bonds and discounts provided on the bonding process.
3. ***Core Contract*** - The contract that handles the PSM, backing reserve and bonding processes
4. ***AMO*** - Algorithmic Market Operations Controller
5. ***APP*** - Atlantic Perpetual Put Option

rDPX V2 introduces a new synthetic coin dpxETH which is pegged to ETH. dpxETH will be used to earn boosted yields on ETH and will be a staple collateral token for future Dopex Options Products.

The rDPX bonding process represents the method in which new dpxETH tokens can be minted. When a user bonds with the rDPX V2 contract they receive a receipt token. A receipt token represents ETH and dpxETH LP on curve.

Via the bonding process new dpxETH is minted and its backing is maintained via a rDPX and ETH reserve (the Backing Reserves). These backing reserves are controlled via AMOs. To ensure a safe and controllable way to scale rDPX V2 and dpxETH together we have decided incorporate the AMO ideology from Frax Finance (https://docs.frax.finance/amo/overview).

## ***Bonding** Mechanism*

There are 3 ways a user can bond on the Bonding contract; regular bonding, delegate bonding or using a decaying bond.

### Regular bonding:

*Assumptions: ETH @ $2000, rDPX @ $20*

- To mint a bond carrying approx. 1 Receipt Token you will deposit 25 rDPX (25%) & 0.75 ETH (75%) + the premium for the size of the rDPX provided for an rDPX Atlantic Perpetual PUT option which is 25% out of the money. You receive a discount on the rDPX & ETH provided.
- Discount is calculated in the following way: `Discount = (Discount Factor *
sqrt(rDPX Treasury Reserve)` where the discount factor is a value set by governance.
- During the bonding process a series of actions are performed by the contract:
    - The full amount of rDPX and 33% of the ETH provided (33% of 75% = 25%) is sent to the [Backing Reserve](https://www.notion.so/rDPX-V2-RI-b45b5b402af54bcab758d62fb7c69cb4?pvs=21) and used to mint dpxETH which is then paired with the rest of the ETH to LP on curve.
    - 50% of the rDPX provided for bonding is burnt from the [Treasury Reserve](https://www.notion.so/rDPX-V2-RI-b45b5b402af54bcab758d62fb7c69cb4?pvs=21) and another 50% is sent as emissions to veDPX holders. These percentages are variable and can be controlled by governance.
    - The discount provided on the rDPX and ETH is covered by the [Treasury Reserve](https://www.notion.so/rDPX-V2-RI-b45b5b402af54bcab758d62fb7c69cb4?pvs=21), the same amount of rDPX (in ETH value) is sent to the [Backing Reserve](https://www.notion.so/rDPX-V2-RI-b45b5b402af54bcab758d62fb7c69cb4?pvs=21).
    - Finally a reLP process is applied on the Uniswap V2 liquidity added by the Uniswap V2 AMO. This is toggleable and hence may or may not be used on every bond execution depending on the market conditions of rDPX. reLP is the process by which part of the Uniswap V2 liquidity is removed, then the ETH received is swapped to rDPX. This essentially increases the price of rDPX and also increases the [Backing Reserve](https://www.notion.so/rDPX-V2-RI-b45b5b402af54bcab758d62fb7c69cb4?pvs=21) of rDPX.
        - rDPX to remove:  `((amount_lp * 4) / rdpx_supply) * lp_rdpx_reserves * base_relp_percent` where `base_relp_percent = Math.sqrt(reserves_rdpx) * relp_factor`
        - A higher `relp_factor` leads to higher target rDPX price.
- After the bonding process is complete a bond (ERC721 token) will be minted to the user which can be redeemed after a variable maturity (initially to be set at 5 days) for the receipt tokens.

![diagram-export-14_08_2023, 12 46 56 AM.png](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/d8496b9d-aafe-463d-bc41-c2b6aa9204e5/diagram-export-14_08_2023_12_46_56_AM.png)

### Delegate bonding:

Delegate bonding is a system wherein users come in with ETH deposit it in a pool (via the [Core Contract](https://www.notion.so/rDPX-V2-RI-b45b5b402af54bcab758d62fb7c69cb4?pvs=21)) and set a fee for the usage of their ETH. Now users holding rDPX can use this pool of ETH to bond (using the regular bonding mechanism). This way users only with rDPX and users only with ETH both can come together and bond to receive their share of receipt tokens.

### Bonding via rDPX Decaying Bond:

*Assumptions: ETH @ $2000, rDPX @ $20*

- Each decaying bond carries a particular amount of rDPX in it. This amount is decided when these decaying bonds are minted to users. rDPX Decaying bonds can be minted to users as rebates for losses incurred on the Dopex Options Protocol or for incentives.
- For an example lets take the amount of rDPX in the decaying bond used as 25 rDPX then to mint a bond carrying 1 Receipt token you will deposit 0.75 ETH (75%) + the premium for the size of the rDPX provided (in the decaying bond in this case being 25 rDPX) for an rDPX Atlantic Perpetual PUT option which is 25% out of the money.
- The full amount of rDPX is provided by the [Treasury Reserve](https://www.notion.so/rDPX-V2-RI-b45b5b402af54bcab758d62fb7c69cb4?pvs=21) and 33% of the ETH provided by the user (33% of 75% = 25%) is sent to the [Backing Reserve](https://www.notion.so/rDPX-V2-RI-b45b5b402af54bcab758d62fb7c69cb4?pvs=21) and used to mint dpxETH which is then paired with the rest of the ETH to LP on curve.
- After the bonding process is complete a bond (ERC721 token) will be minted to the user which can be redeemed after a variable maturity (initially to be set at 5 days) for the receipt tokens.

## *Atlantic Perpetual PUTS Options*

A perpetual options pools for rDPX options the [Core Contract](https://www.notion.so/rDPX-V2-RI-b45b5b402af54bcab758d62fb7c69cb4?pvs=21) uses for the bonding process. The liquidity for this will be provided via the open market and will be incentivized via DPX. The [Core Contract](https://www.notion.so/rDPX-V2-RI-b45b5b402af54bcab758d62fb7c69cb4?pvs=21) pays this pool LPs funding every week. The APP contract follows a epoch system where each epoch is 1 week long. Funding is distributed per epoch basis to the perpetual options minted. The APP contract admin needs to calculate the funding needs to be called for every strike before the epoch ends. The funding is calculated based on the amount of options active for a given strike using BlackScholes with the duration as the start of the epoch until the end of the epoch. The funding payments comes from the 30% of CRV which goes to the Core Contract in the dpxETH/ETH LP staking. IV is adjusted accordingly to pay the users a target APY derived from the total CRV earned. Note that the funding has to be paid at the start of each epoch. Users depositing into this APP contract can redeem their deposit when collateral is available (when the core contract buys options collateral is locked until the Core Contract settles or forfeits options).

## *Receipt Token*

The rDPX V2 bonds hold receipt tokens in them, a receipt token represent dpxETH/ETH LP tokens on curve. These LP tokens are staked in curve gauges with boosted rewards. Boosted rewards come from pointing the CVX held by the Dopex Team and Partners to the curve gauge. Rewards earned from this will be distributed in a variable manner, initially 70% of the rewards go directly to receipt token stakers and 30% go to the [Core Contract](https://www.notion.so/rDPX-V2-RI-b45b5b402af54bcab758d62fb7c69cb4?pvs=21) which can be used to pay funding for the PUT options bought during the bonding process, to compound CVX to boost the rewards further etc. This way receipt tokens receive boosted yield. Receipt tokens staked with Dopex also earn additional incentives in the form of DPX, decaying bonds etc.

### Redemption

Redemption of the receipt token will depend on the current ratio of the [Backing Reserve](https://www.notion.so/rDPX-V2-RI-b45b5b402af54bcab758d62fb7c69cb4?pvs=21) in rDPX and ETH and a variable redemption fee is charged to redeem receipt tokens. For eg. if 1 receipt token represents 1 ETH/dpxETH LP token which carries 0.5 ETH and 0.5 dpxETH, then during redemption the LP token is removed from the curve pool, the 0.5 dpxETH is burnt and 0.5 eth + the current ratio of backing is returned to the user with the redemption fee charged.

## *AMO*

Diving deeper into the Frax ecosystem, All Frax AMOs hold 4 key properties: Recollateralize, Decollateralize, Market Operations and FXS1559. CR here is collateral ratio of FXS and the peg token (for frxETH peg token is ETH)

- *Decollateralize* - the portion of the strategy which lowers the CR
- *Market operations* - the portion of the strategy that is run in equilibrium and doesn't change the CR
- *Recollateralize* - the portion of the strategy which increases the CR
- *FXS1559* - a formalized accounting of the balance sheet of the AMO which defines exactly how much FXS can be burned with profits above the target CR

We modify this approach to AMOs by separating out the Decollateralize and Recollateralize into the Treasury singleton [PSM](https://www.notion.so/rDPX-V2-RI-b45b5b402af54bcab758d62fb7c69cb4?pvs=21). Further the FXS1559 would be the mechanism by which rDPX would be burned with profits above the CR this too would remain a part of the [Core Contract](https://www.notion.so/rDPX-V2-RI-b45b5b402af54bcab758d62fb7c69cb4?pvs=21). The AMO contracts in rDPX V2 will solely be responsible to perform market operations. The 2 initial AMOs that we will begin with is the Uniswap V2 and Uniswap V3 AMOs.

### Uniswap V2 AMO

This AMO will be responsible for adding / removing liquidity on a Uniswap V2 rDPX/ETH pool. To be based on Camelot.

### Uniswap V3 AMO

This AMO will be responsible for adding / removing liquidity on a Uniswap V3 rDPX/ETH pool and compounding the fees earned by providing the liquidity. To be based on Camelot.

## *Peg Stability Module (PSM)*

The peg stability module is part of the [Core Contract](https://www.notion.so/rDPX-V2-RI-b45b5b402af54bcab758d62fb7c69cb4?pvs=21) that ensures that the peg of dpxETH to ETH on the curve pool is maintained. It is entirely controlled via the [Core Contract](https://www.notion.so/rDPX-V2-RI-b45b5b402af54bcab758d62fb7c69cb4?pvs=21) managers and It encompasses 3 functions:

- ***upperDepeg*** (if dpxETH > 1 ETH)**:** Mints new dpxETH to sell on the curve pool to bring back the peg to 1 ETH.
- ***lowerDepeg*** (if dpxETH < 1 ETH)**:** The backing reserves are used to buy and burn dpxETH from the curve pool to bring back the peg to 1 ETH.
- ***settle:*** When any rDPX APPs can be exercised, they are exercised to bring back the peg and back the backing reserves more in ETH.

## *System Parameters*

System parameters are different parameters that are set by governance and are changed to ensure the stability of the system:

- veDPX Bonding Fee: Paid by the [Treasury Reserve](https://www.notion.so/rDPX-V2-RI-b45b5b402af54bcab758d62fb7c69cb4?pvs=21) as emissions to veDPX holders. Initially to be set to 12.5% of the total bonded value.
- Reward Distribution Percentages: The rewards earned from the dpxETH/ETH curve LP staking are distributed to receipt token stakers and the [Core Contract](https://www.notion.so/rDPX-V2-RI-b45b5b402af54bcab758d62fb7c69cb4?pvs=21). The percentages of distribution is variable. Initially to be set to 70% to stakers and 30% to Treasury.
- Discount Factor: The factor that determines the discount on the bonds based on the [Treasury Reserve](https://www.notion.so/rDPX-V2-RI-b45b5b402af54bcab758d62fb7c69cb4?pvs=21) of rDPX.
- rDPX V2 Bond Maturity: The bond maturity of the rDPX V2 Bond. Initially to be set to 5 days.
- Redemption Fee: % of the total value of the receipt token charged to users when redeeming the receipt token. Initially to be set to 5%.

## *Launch Details*

The Bootstrap Phase:

- Deploy all contracts on arbitrum mainnet awaiting public announcement.
- Before publicly announcing the Dopex Treasury funds and Partners partake in the bonding process to ensure a sufficient amount of dpxETH is in circulation and the backing reserves of rDPX and ETH will be used to provide liquidity on the Uniswap V2 pool via the Uniswap V2 AMO.
- Following this rDPX V2 is made public.

## *Contracts Architecture*

1. rDPX V2 Core: This contract features several modules: 
    - The bonding module is incharge of the different bonding processes. A rDPX Bond contract which is ERC721 is used to handle bond balances for users.
    - The peg stability module will This contract will be incharge of maintaining the peg of the dpxETH.
    - The backing reserves module will allow using the reserves by the different AMOs. This module should allow different tokens to be used as reserves although the primary backing reserves should remain rDPX and ETH.
    - The burn module will allow burning of rDPX via profits from the AMOs.
2. RdpxV2ReceiptToken: ERC4626 like contract that stores dpxETH/ETH Curve LP and stakes the same into the curve gauge, allows redemption of the receipt tokens via the Treasury contract. Rewards emitted from the curve gauge are sent to the Staking LP and Treasury in the variable ratios (initially 70% of rewards are sent to staking contract and 30% to treasury)
3. RdpxV2ReceiptTokenStaking: Receipt token can be staked here to earn boosted yield from curve and DPX incentives.
4. AtlanticPerpetualPool: This contract is ERC721 which mints option tokens as NFTs to the Core contract.
5. AtlanticPerpetualPoolLP: Contract to add liquidity to the APP.
6. AtlanticPerpetualPoolStaking: The staking contract will allow users to stake their APP LP tokens for reward emissions.
7. rDPX Decaying Bonds contract: This is an ERC721 contract that mints decaying bonds to users which store a virtual amount of rDPX (to be fulfilled by the Treasury Reserves). These bonds are minted to users as rebates for losses incurred on Dopex Option Products and can also be used to emit indirect rDPX. The term `decaying` is used as the bond expires after a period of time.
8. Uniswap V2 AMO contract encompasses uniswap v2 functions to add/remove liquidity and swap
9. Uniswap V3 AMO contract encompasses uniswap v3 functions to add/remove liquidity, swap and compound fees
10. reLP Contract: Contract that does the reLP strategy using the uniswap v2 AMO
11. dpxETH/ETH Oracle
12. rDPX/ETH Oracle


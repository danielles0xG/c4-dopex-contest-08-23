---
noteId: "09ea20f048ea11eea4f8db847f52532e"
tags: []

---


/** 
 *  SourceUnit: /Users/danielguerrero/workspace/BOUNTY/c4-dopex-contest-08-23/contracts/core/RdpxV2Core.sol
*/
            
////// SPDX-License-Identifier-FLATTEN-SUPPRESS-WARNING: UNLICENSED

pragma solidity 0.8.19;

/// @title Lighter version of the Openzeppelin Pausable contract
/// @author witherblock
/// @notice Helps pause a contract to block the execution of selected functions
/// @dev Difference from the Openzeppelin version is changing the modifiers to internal fns and requires to reverts
abstract contract Pausable {
  /**
   * @dev Emitted when the pause is triggered by `account`.
   */
  event Paused(address account);

  /**
   * @dev Emitted when the pause is lifted by `account`.
   */
  event Unpaused(address account);

  bool private _paused;

  /**
   * @dev Initializes the contract in unpaused state.
   */
  constructor() {
    _paused = false;
  }

  /**
   * @dev Returns true if the contract is paused, and false otherwise.
   */
  function paused() public view virtual returns (bool) {
    return _paused;
  }

  /**
   * @dev Internal function to make a function callable only when the contract is not paused.
   *
   * Requirements:
   *
   * - The contract must not be paused.
   */
  function _whenNotPaused() internal view {
    if (paused()) revert ContractPaused();
  }

  /**
   * @dev Internal function to make a function callable only when the contract is paused.
   *
   * Requirements:
   *
   * - The contract must be paused.
   */
  function _whenPaused() internal view {
    if (!paused()) revert ContractNotPaused();
  }

  /**
   * @dev Triggers stopped state.
   *
   * Requirements:
   *
   * - The contract must not be paused.
   */
  function _pause() internal virtual {
    _whenNotPaused();
    _paused = true;
    emit Paused(msg.sender);
  }

  /**
   * @dev Returns to normal state.
   *
   * Requirements:
   *
   * - The contract must be paused.
   */
  function _unpause() internal virtual {
    _whenPaused();
    _paused = false;
    emit Unpaused(msg.sender);
  }

  error ContractPaused();
  error ContractNotPaused();
}




/** 
 *  SourceUnit: /Users/danielguerrero/workspace/BOUNTY/c4-dopex-contest-08-23/contracts/core/RdpxV2Core.sol
*/
            
//SPDX-License-Identifier: UNLICENSED
pragma solidity 0.8.19;

interface IReLP {
  function reLP(uint256 amount) external;
}




/** 
 *  SourceUnit: /Users/danielguerrero/workspace/BOUNTY/c4-dopex-contest-08-23/contracts/core/RdpxV2Core.sol
*/
            
//SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.19;

interface IRdpxV2ReceiptToken {
  function deposit(uint256 _amount) external returns (uint256);
}




/** 
 *  SourceUnit: /Users/danielguerrero/workspace/BOUNTY/c4-dopex-contest-08-23/contracts/core/RdpxV2Core.sol
*/
            
////// SPDX-License-Identifier-FLATTEN-SUPPRESS-WARNING: UNLICENSED
pragma solidity 0.8.19;

interface IRdpxV2Core {
  // ================================ STRUCTS ================================ //

  /// @dev Peripheral addresses for the RdpxV2Core contract
  struct Addresses {
    address dopexAMMRouter;
    address dpxEthCurvePool;
    address rdpxDecayingBonds;
    address perpetualAtlanticVault;
    address perpetualAtlanticVaultLP;
    address rdpxReserve;
    address rdpxV2ReceiptToken;
    address feeDistributor;
    address reLPContract;
    address receiptTokenBonds;
  }

  /// @dev Peripheral addresses for the RdpxV2Core pricing oracles
  struct PricingOracleAddresses {
    address rdpxPriceOracle;
    address dpxEthPriceOracle;
  }

  /// @dev Struct containing the variables for delegate's position
  struct Delegate {
    address owner;
    uint256 amount;
    uint256 fee;
    uint256 activeCollateral;
  }

  /// @dev Struct containing the variables for a bond
  struct Bond {
    uint256 amount;
    uint256 maturity;
    uint256 timestamp;
  }

  /// @dev Struct containing the the rdpxV2Core reserve asset data
  struct ReserveAsset {
    address tokenAddress;
    uint256 tokenBalance;
    string tokenSymbol;
  }

  /// @dev Struct containing the return values for _bondWithDelegate
  struct BondWithDelegateReturnValue {
    uint256 delegateReceiptTokenAmount;
    uint256 bondAmountForUser;
    uint256 rdpxRequired;
    uint256 wethRequired;
  }

  // ================================ FUNCTIONS ================================ //
  function sync() external;

  // ================================ EVENTS ================================ //

  /// @notice Emitted when rdpxV2Core reserves are synced
  event LogSync();

  /// @notice Emitted when funds are withdrawn in an emergency
  /// @param sender msg.sender
  event LogEmergencyWithdraw(address sender, address[] tokens);

  /// @notice Emitted when addresses are set
  /// @param addresses The Addresses struct
  event LogSetAddresses(Addresses addresses);

  /// @notice Emitted when pricing oracle addresses are set
  /// @param pricingOracleAddresses The pricingOracleAddresses struct
  event LogSetPricingOracleAddresses(
    PricingOracleAddresses pricingOracleAddresses
  );

  /// @notice Emitted when the bond discount factor is set
  /// @param bondDiscountFactor The Bond Discount Factor
  event LogSetBondDiscountFactor(uint256 bondDiscountFactor);

  /// @notice Emitted when the reLP factor is set
  /// @param reLpFactor The reLP factor
  event LogSetReLpFactor(uint256 reLpFactor);

  /// @notice Emitted when the put option requirement is changed
  /// @param putOptionRequirement The put option requirement
  event LogSetputOptionsRequired(bool putOptionRequirement);

  /// @notice Emitted when the slippage tolerance is set
  /// @param slippageTolerance The Slippage tolerance
  event LogSetSlippageTolerance(uint256 slippageTolerance);

  /// @notice Emitted when the bond maturity is set
  /// @param bondMaturity The Bond Maturity
  event LogSetBondMaturity(uint256 bondMaturity);

  /// @notice Emitted when a bond is minted
  /// @param rdpxPaid the amount of rdpx paid
  /// @param alphaTokenPaid the amount of alphaTokenPaid
  /// @param receiptTokenAmount the amount of receipt tokens received
  event LogBond(
    uint256 rdpxPaid,
    uint256 alphaTokenPaid,
    uint256 receiptTokenAmount
  );

  /// @notice Emitted when a bond is minted via delegation
  /// @param to the address to which the bond is minted
  /// @param delegateIds array of the delegate ids
  /// @param amounts array of amounts used from the delegates
  /// @param rdpxBondId the bond id of the rdpx decaying bond
  /// @param userReceiptTokenAmount the amount of receipt tokens received by the user
  /// @param delegateReceiptTokenAmounts the amount of receipt tokens received by the delegates
  event LogBondWithDelegate(
    address to,
    uint256[] delegateIds,
    uint256[] amounts,
    uint256 rdpxBondId,
    uint256 userReceiptTokenAmount,
    uint256[] delegateReceiptTokenAmounts
  );

  /// @notice Emitted when the rdpxV2Core settles the perp-vault options
  /// @param optionIds the optionIds
  event LogSettle(uint256[] optionIds);

  /// @notice Emitted when the rdpxV2Core pays funding
  /// @param epoch the epoch for which to pay funding for
  /// @param funding the amount of funding to pay
  event LogProvideFunding(uint256 epoch, uint256 funding);

  /// @notice Emitted when someone delegates
  /// @param amount the amount to delegate
  event LogAddToDelegate(uint256 amount, uint256 fees, uint256 delegateId);

  /// @notice Emitted when a delegate withdraws
  /// @param delegateId the delegate id
  /// @param amount the amount withdrawn
  event LogDelegateWithdraw(uint256 delegateId, uint256 amount);

  /// @notice Emitted when upper depeg fn is called
  /// @param amount The amount of dpxEth minted
  /// @param wethReceived The amount of alpha token received
  event LogUpperDepeg(uint256 amount, uint256 wethReceived);

  /// @notice Emitted when lower depeg fn is called
  /// @param rdpxAmount The amount of rdpx used
  /// @param wethAmount The amount of weth used
  /// @param dpxEthReceived The amount of dpxEth received
  event LogLowerDepeg(
    uint256 rdpxAmount,
    uint256 wethAmount,
    uint256 dpxEthReceived
  );

  /// @notice Emitted when a new asset is added to the rdpxV2Core
  /// @param asset the address of the asset
  /// @param assetSymbol the symbol of the asset
  event LogAssetAddedTotokenReserves(address asset, string assetSymbol);

  /// @notice Emitted when a new asset is removed from the rdpxV2Core
  /// @param assetSymbol the symbol of the asset
  event LogAssetRemovedFromtokenReserves(string assetSymbol, uint256 index);

  /// @notice Emitted when rdpx burn percentage is set
  /// @param rdpxBurnPercentage the percentage of rdpx to burn
  event LogSetRdpxBurnPercentage(uint256 rdpxBurnPercentage);

  /// @notice Emitted when rdpx fee percentage is set
  /// @param rdpxFeePercentage the percentage of rdpx to burn
  event LogSetRdpxFeePercentage(uint256 rdpxFeePercentage);

  /// @notice Emitted when isReLpActive is set
  /// @param isReLPActive the boolean value of isReLpActive
  event LogSetIsReLPActive(bool isReLPActive);

  /// @notice Emitted when a bond is redeemed
  /// @param to the address to which the receipt tokens are sent
  /// @param amount the amount of receipt tokens redeemed
  event LogRedeem(address to, uint256 amount);
}




/** 
 *  SourceUnit: /Users/danielguerrero/workspace/BOUNTY/c4-dopex-contest-08-23/contracts/core/RdpxV2Core.sol
*/
            
////// SPDX-License-Identifier-FLATTEN-SUPPRESS-WARNING: UNLICENSED
pragma solidity 0.8.19;

interface IRdpxReserve {
  function withdraw(uint256 _amount) external;

  function rdpxReserve() external view returns (uint256);
}




/** 
 *  SourceUnit: /Users/danielguerrero/workspace/BOUNTY/c4-dopex-contest-08-23/contracts/core/RdpxV2Core.sol
*/
            
//SPDX-License-Identifier: UNLICENSED
pragma solidity 0.8.19;

interface IDpxEthOracle {
  /// @notice Gets the price of dpxETH in ETH
  /// @return price
  function getDpxEthPriceInEth() external view returns (uint256);

  /// @notice Gets the price of ETH in dpxETH
  /// @return price
  function getEthPriceInDpxEth() external view returns (uint256);
}




/** 
 *  SourceUnit: /Users/danielguerrero/workspace/BOUNTY/c4-dopex-contest-08-23/contracts/core/RdpxV2Core.sol
*/
            
//SPDX-License-Identifier: UNLICENSED
pragma solidity 0.8.19;

interface IRdpxEthOracle {
  function getRdpxPriceInEth() external view returns (uint256);

  function getEthPriceInRdpx() external view returns (uint256);

  function getLpPriceInEth() external view returns (uint256);
}




/** 
 *  SourceUnit: /Users/danielguerrero/workspace/BOUNTY/c4-dopex-contest-08-23/contracts/core/RdpxV2Core.sol
*/
            
////// SPDX-License-Identifier-FLATTEN-SUPPRESS-WARNING: UNLICENSED
pragma solidity 0.8.19;

interface IPerpetualAtlanticVault {
  // ================================ VIEWS ================================ //

  /**
   * @notice Returns the funding duration
   * @return uint256 the funding duration
   **/
  function fundingDuration() external view returns (uint256);

  /**
   * @notice Returns the funding rate for a specified epoch
   * @param  _epoch The epoch to get the funding rate for
   * @return uint256 the funding rate
   **/
  function fundingRates(uint256 _epoch) external view returns (uint256);

  /**
   * @notice Returns the price of the underlying in ETH in 1e8 precision
   * @return uint256 the current underlying price
   **/
  function getUnderlyingPrice() external view returns (uint256);

  /**
   * @notice Returns the volatility from the volatility oracle
   * @param  _strike Strike of the option
   * @return uint256 Volatility for given strike
   **/
  function getVolatility(uint256 _strike) external view returns (uint256);

  /**
   * @notice Calculate premium for an option
   * @param  _strike Strike price of the option
   * @param  _amount Amount of options (1e18 precision)
   * @param  timeToExpiry Time to expiry of the option in seconds
   * @param  _price in 1e8 precision
   * @return premium in collateralToken in collateral precision
   **/
  function calculatePremium(
    uint256 _strike,
    uint256 _amount,
    uint256 timeToExpiry,
    uint256 _price
  ) external view returns (uint256 premium);

  /**
   * @notice Calculate Pnl
   * @param  price price of the underlying asset
   * @param  strike strike price of the option
   * @param  amount amount of options
   * @return uint256 the PnL calculated
   **/
  function calculatePnl(
    uint256 price,
    uint256 strike,
    uint256 amount
  ) external pure returns (uint256);

  /**
   * @notice Get the timestamp for next funding payment
   * @dev    Calculates funding timestamp based on genesis timestamp from deployment,
   *         the preset fundingDuration, and the current pointer
   * @return timestamp the next funding timestamp
   **/
  function nextFundingPaymentTimestamp()
    external
    view
    returns (uint256 timestamp);

  /**
   * @dev Function to round up a value to the roundingPrecision.
   * @param _strike the strike
   * @return strike rounded up to the nearest roundingPrecision
   **/
  function roundUp(uint256 _strike) external view returns (uint256 strike);

  /// @dev the pointer to the lattest funding payment timestamp
  function latestFundingPaymentPointer() external view returns (uint256);

  // ================================ TREASURY FUNCTIONS ================================ //

  /**
   * @notice Purchases options for the current epoch
   * @param  amount Amount of options to purchase
   * @param  to address to send the purchased options to
   **/
  function purchase(
    uint256 amount,
    address to
  ) external returns (uint256 premium, uint256 tokenId);

  /** 
  * @notice   The function asset settles the options by transferring rdpx 
              from the rdpxV2Core and transfers eth to the rdpx rdpxV2Core 
              contract at the option strike price. Will also the burn the 
              option tokens from the user.
  * @param    optionIds The Ids of the option to settle
  * @return   ethAmount The amount of eth transferred to the rdpx rdpxV2Core
  * @return   rdpxAmount The amount of rdpx transferred from the rdpx rdpxV2Core
  **/
  function settle(
    uint256[] memory optionIds
  ) external returns (uint256, uint256);

  /**
   * @notice function for rdpxV2Core to pay funding to option writers
   * @return uint256 the total funding for the ongoing epoch
   **/
  function payFunding() external returns (uint256);

  /**
   * @notice function to transfer funding into the LP in a drip-vested manner
   * @dev    addProceeds() is invoked to update totalCollateral in LP
   **/
  function updateFunding() external;

  /*==== EVENTS ====*/

  /// @notice Emitted when addresses are set
  /// @param addresses The Addresses struct
  event AddressesSet(Addresses addresses);

  /// @notice Emitted when funds are withdrawn in an emergency
  /// @param sender msg.sender
  /// @param tokens Array of tokens that were withdrawn
  event EmergencyWithdraw(address sender, address[] tokens);

  /// @notice Emitted when a purchase is made on the vault by the rdpxV2Core
  /// @param strike The strike of the option
  /// @param amount The amount of options purchased
  /// @param premium The premium paid by the rdpxV2Core
  /// @param to Address the options were sent to
  /// @param sender Address of the rdpxV2Core
  event Purchase(
    uint256 strike,
    uint256 amount,
    uint256 premium,
    address indexed to,
    address indexed sender
  );

  /// @notice Emitted on when settle is called by the rdpxV2Core
  /// @param ethAmount Amount of ETH received by the rdpxV2Core
  /// @param rdpxAmount Amount of rDPX received by the rdpxV2Core
  /// @param tokenIds Array of token ids that were settled
  event Settle(uint256 ethAmount, uint256 rdpxAmount, uint256[] tokenIds);

  /// @notice Emitted when funding is paid
  /// @param sender msg.sender
  /// @param amount amount paid
  /// @param latestFundingPaymentPointer latest funding payment pointer
  event PayFunding(
    address sender,
    uint256 amount,
    uint256 latestFundingPaymentPointer
  );

  /// @notice Emitted when calculate funding is called
  /// @param sender msg.sender
  /// @param amount amount of options
  /// @param strike strike of the option
  /// @param fundingAmount funding amount
  /// @param latestFundingPaymentPointer latest funding payment pointer
  event CalculateFunding(
    address sender,
    uint256 amount,
    uint256 strike,
    uint256 fundingAmount,
    uint256 latestFundingPaymentPointer
  );

  /// @notice Emitted when funding paymentPointer is updated
  /// @param latestFundingPaymentPointer latest funding payment pointer
  event FundingPaymentPointerUpdated(uint256 latestFundingPaymentPointer);

  /// @notice Emitted when funding is paid
  /// @param sender msg.sender
  /// @param amount amount paid
  /// @param latestFundingPaymentPointer latest funding payment pointer
  event FundingPaid(
    address sender,
    uint256 amount,
    uint256 latestFundingPaymentPointer
  );

  /*==== STRUCTS ====*/

  /// @dev Struct of all addresses used by the vault
  struct Addresses {
    address optionPricing;
    address assetPriceOracle;
    address volatilityOracle;
    address feeDistributor;
    address rdpx;
    address perpetualAtlanticVaultLP;
    address rdpxV2Core;
  }

  /// @dev Struct of a option position
  struct OptionPosition {
    uint256 strike;
    uint256 amount;
    uint256 positionId;
  }
}




/** 
 *  SourceUnit: /Users/danielguerrero/workspace/BOUNTY/c4-dopex-contest-08-23/contracts/core/RdpxV2Core.sol
*/
            
////// SPDX-License-Identifier-FLATTEN-SUPPRESS-WARNING: UNLICENSED
pragma solidity 0.8.19;

////import { IERC20Metadata } from "@openzeppelin/contracts/token/ERC20/extensions/IERC20Metadata.sol";

interface IDpxEthToken is IERC20Metadata {
  function mint(address to, uint256 amount) external;

  function burn(uint256 _amount) external;
}




/** 
 *  SourceUnit: /Users/danielguerrero/workspace/BOUNTY/c4-dopex-contest-08-23/contracts/core/RdpxV2Core.sol
*/
            
////// SPDX-License-Identifier-FLATTEN-SUPPRESS-WARNING: UNLICENSED
pragma solidity 0.8.19;

/**
 * @dev Interface of the rDPX decaying bonds contract.
 */

interface IRdpxDecayingBonds {
  function burn(uint256 bondId) external;

  function bonds(uint256 bondId) external returns (address, uint256, uint256);

  function decreaseAmount(uint256 bondId, uint256 amount) external;

  function ownerOf(uint256 tokenId) external view returns (address);
}




/** 
 *  SourceUnit: /Users/danielguerrero/workspace/BOUNTY/c4-dopex-contest-08-23/contracts/core/RdpxV2Core.sol
*/
            
////// SPDX-License-Identifier-FLATTEN-SUPPRESS-WARNING: UNLICENSED
pragma solidity ^0.8.9;

interface IStableSwap {
  function add_liquidity(uint256[2] calldata amounts, uint256 min_mint_amount)
    external
    returns (uint256);

  function balances() external view returns (uint256[] memory);

  function remove_liquidity_one_coin(
    uint256 _token_amount,
    int128 i,
    uint256 min_amount
  ) external returns (uint256);

  function get_virtual_price() external view returns (uint256);

  function coins(uint256) external view returns (address);

  function balances(uint256) external view returns (uint256);

  function get_dy(
    int128 i,
    int128 j,
    uint256 dx
  ) external view returns (uint256);

  function exchange(
    int128 i,
    int128 j,
    uint256 _dx,
    uint256 _min_dy
  ) external returns (uint256);
}




/** 
 *  SourceUnit: /Users/danielguerrero/workspace/BOUNTY/c4-dopex-contest-08-23/contracts/core/RdpxV2Core.sol
*/
            
////// SPDX-License-Identifier-FLATTEN-SUPPRESS-WARNING: UNLICENSED

pragma solidity 0.8.19;

interface IUniswapV2Router {
  function factory() external view returns (address);

  function WETH() external view returns (address);

  function addLiquidity(
    address tokenA,
    address tokenB,
    uint256 amountADesired,
    uint256 amountBDesired,
    uint256 amountAMin,
    uint256 amountBMin,
    address to,
    uint256 deadline
  ) external returns (uint256 amountA, uint256 amountB, uint256 liquidity);

  function addLiquidityETH(
    address token,
    uint256 amountTokenDesired,
    uint256 amountTokenMin,
    uint256 amountETHMin,
    address to,
    uint256 deadline
  )
    external
    payable
    returns (uint256 amountToken, uint256 amountETH, uint256 liquidity);

  function removeLiquidity(
    address tokenA,
    address tokenB,
    uint256 liquidity,
    uint256 amountAMin,
    uint256 amountBMin,
    address to,
    uint256 deadline
  ) external returns (uint256 amountA, uint256 amountB);

  function removeLiquidityETH(
    address token,
    uint256 liquidity,
    uint256 amountTokenMin,
    uint256 amountETHMin,
    address to,
    uint256 deadline
  ) external returns (uint256 amountToken, uint256 amountETH);

  function removeLiquidityWithPermit(
    address tokenA,
    address tokenB,
    uint256 liquidity,
    uint256 amountAMin,
    uint256 amountBMin,
    address to,
    uint256 deadline,
    bool approveMax,
    uint8 v,
    bytes32 r,
    bytes32 s
  ) external returns (uint256 amountA, uint256 amountB);

  function removeLiquidityETHWithPermit(
    address token,
    uint256 liquidity,
    uint256 amountTokenMin,
    uint256 amountETHMin,
    address to,
    uint256 deadline,
    bool approveMax,
    uint8 v,
    bytes32 r,
    bytes32 s
  ) external returns (uint256 amountToken, uint256 amountETH);

  function swapExactTokensForTokens(
    uint256 amountIn,
    uint256 amountOutMin,
    address[] calldata path,
    address to,
    uint256 deadline
  ) external returns (uint256[] memory amounts);

  function swapTokensForExactTokens(
    uint256 amountOut,
    uint256 amountInMax,
    address[] calldata path,
    address to,
    uint256 deadline
  ) external returns (uint256[] memory amounts);

  function swapExactETHForTokens(
    uint256 amountOutMin,
    address[] calldata path,
    address to,
    uint256 deadline
  ) external payable returns (uint256[] memory amounts);

  function swapTokensForExactETH(
    uint256 amountOut,
    uint256 amountInMax,
    address[] calldata path,
    address to,
    uint256 deadline
  ) external returns (uint256[] memory amounts);

  function swapExactTokensForETH(
    uint256 amountIn,
    uint256 amountOutMin,
    address[] calldata path,
    address to,
    uint256 deadline
  ) external returns (uint256[] memory amounts);

  function swapETHForExactTokens(
    uint256 amountOut,
    address[] calldata path,
    address to,
    uint256 deadline
  ) external payable returns (uint256[] memory amounts);

  function quote(
    uint256 amountA,
    uint256 reserveA,
    uint256 reserveB
  ) external pure returns (uint256 amountB);

  function getAmountsOut(
    uint256 amountIn,
    address[] calldata path
  ) external view returns (uint256[] memory amounts);

  function getAmountsIn(
    uint256 amountOut,
    address[] calldata path
  ) external view returns (uint256[] memory amounts);
}




/** 
 *  SourceUnit: /Users/danielguerrero/workspace/BOUNTY/c4-dopex-contest-08-23/contracts/core/RdpxV2Core.sol
*/
            
////// SPDX-License-Identifier-FLATTEN-SUPPRESS-WARNING: UNLICENSED
pragma solidity 0.8.19;

////import { IERC20Metadata } from "@openzeppelin/contracts/token/ERC20/extensions/IERC20Metadata.sol";

interface IERC20WithBurn is IERC20Metadata {
  function burn(uint256 amount) external;
}




/** 
 *  SourceUnit: /Users/danielguerrero/workspace/BOUNTY/c4-dopex-contest-08-23/contracts/core/RdpxV2Core.sol
*/
            
////// SPDX-License-Identifier-FLATTEN-SUPPRESS-WARNING: UNLICENSED
pragma solidity 0.8.19;

////import { ERC721 } from "@openzeppelin/contracts/token/ERC721/ERC721.sol";
////import { ERC721Enumerable } from "@openzeppelin/contracts/token/ERC721/extensions/ERC721Enumerable.sol";
////import { Pausable } from "../helper/Pausable.sol";
////import { AccessControl } from "@openzeppelin/contracts/access/AccessControl.sol";
////import { ERC721Burnable } from "@openzeppelin/contracts/token/ERC721/extensions/ERC721Burnable.sol";
////import { Counters } from "@openzeppelin/contracts/utils/Counters.sol";

contract RdpxV2Bond is
  ERC721,
  ERC721Enumerable,
  Pausable,
  AccessControl,
  ERC721Burnable
{
  using Counters for Counters.Counter;

  Counters.Counter private _tokenIdCounter;

  bytes32 public constant MINTER_ROLE = keccak256("MINTER_ROLE");

  constructor() ERC721("rDPX V2 Bond", "rDPXV2Bond") {
    _setupRole(DEFAULT_ADMIN_ROLE, msg.sender);
    _setupRole(MINTER_ROLE, msg.sender);
  }

  function pause() public onlyRole(DEFAULT_ADMIN_ROLE) {
    _pause();
  }

  function unpause() public onlyRole(DEFAULT_ADMIN_ROLE) {
    _unpause();
  }

  function mint(
    address to
  ) public onlyRole(MINTER_ROLE) returns (uint256 tokenId) {
    tokenId = _tokenIdCounter.current();
    _tokenIdCounter.increment();
    _mint(to, tokenId);
  }

  function _beforeTokenTransfer(
    address from,
    address to,
    uint256 tokenId,
    uint256 batchSize
  ) internal override(ERC721, ERC721Enumerable) {
    _whenNotPaused();
    super._beforeTokenTransfer(from, to, tokenId, batchSize);
  }

  // The following functions are overrides required by Solidity.

  function supportsInterface(
    bytes4 interfaceId
  )
    public
    view
    override(ERC721, ERC721Enumerable, AccessControl)
    returns (bool)
  {
    return super.supportsInterface(interfaceId);
  }
}




/** 
 *  SourceUnit: /Users/danielguerrero/workspace/BOUNTY/c4-dopex-contest-08-23/contracts/core/RdpxV2Core.sol
*/
            
//SPDX-License-Identifier: UNLICENSED
pragma solidity 0.8.19;

/// @title ContractWhitelist
/// @author witherblock
/// @notice A helper contract that lets you add a list of whitelisted contracts that should be able to interact with restricited functions
abstract contract ContractWhitelist {
  /// @dev contract => whitelisted or not
  mapping(address => bool) public whitelistedContracts;

  /*==== SETTERS ====*/

  /// @dev add to the contract whitelist
  /// @param _contract the address of the contract to add to the contract whitelist
  function _addToContractWhitelist(address _contract) internal {
    require(isContract(_contract), "Address must be a contract");
    require(!whitelistedContracts[_contract], "Contract already whitelisted");

    whitelistedContracts[_contract] = true;

    emit AddToContractWhitelist(_contract);
  }

  /// @dev remove from  the contract whitelist
  /// @param _contract the address of the contract to remove from the contract whitelist
  function _removeFromContractWhitelist(address _contract) internal {
    require(whitelistedContracts[_contract], "Contract not whitelisted");

    whitelistedContracts[_contract] = false;

    emit RemoveFromContractWhitelist(_contract);
  }

  // modifier is eligible sender modifier
  function _isEligibleSender() internal view {
    // the below condition checks whether the caller is a contract or not
    if (msg.sender != tx.origin)
      require(whitelistedContracts[msg.sender], "Contract must be whitelisted");
  }

  /*==== VIEWS ====*/

  /// @dev checks for contract or eoa addresses
  /// @param addr the address to check
  /// @return bool whether the passed address is a contract address
  function isContract(address addr) public view returns (bool) {
    uint256 size;
    assembly {
      size := extcodesize(addr)
    }
    return size > 0;
  }

  /*==== EVENTS ====*/

  event AddToContractWhitelist(address indexed _contract);

  event RemoveFromContractWhitelist(address indexed _contract);
}


/** 
 *  SourceUnit: /Users/danielguerrero/workspace/BOUNTY/c4-dopex-contest-08-23/contracts/core/RdpxV2Core.sol
*/

//SPDX-License-Identifier: UNLICENSED
pragma solidity 0.8.19;

// Contracts
////import { AccessControl } from "@openzeppelin/contracts/access/AccessControl.sol";
////import { ERC721Holder } from "@openzeppelin/contracts/token/ERC721/utils/ERC721Holder.sol";
////import { ContractWhitelist } from "../helper/ContractWhitelist.sol";
////import { Pausable } from "../helper/Pausable.sol";
////import { RdpxV2Bond } from "./RdpxV2Bond.sol";

// Interfaces
////import { IERC20WithBurn } from "../interfaces/IERC20WithBurn.sol";
////import { IUniswapV2Router } from "../uniswap_V2/IUniswapV2Router.sol";
////import { IStableSwap } from "../interfaces/IStableSwap.sol";
////import { IRdpxDecayingBonds } from "../decaying-bonds/IRdpxDecayingBonds.sol";
////import { IDpxEthToken } from "../dpxETH/IDpxEthToken.sol";
////import { IPerpetualAtlanticVault } from "../perp-vault/IPerpetualAtlanticVault.sol";
////import { IRdpxEthOracle } from "../interfaces/IRdpxEthOracle.sol";
////import { IDpxEthOracle } from "../oracles/IDpxEthOracle.sol";
////import { IRdpxReserve } from "../reserve/IRdpxReserve.sol";
////import { IRdpxV2Core } from "./IRdpxV2Core.sol";
////import { IRdpxV2ReceiptToken } from "../interfaces/IRdpxV2ReceiptToken.sol";
////import { IReLP } from "../interfaces/IReLP.sol";

// Libraries
////import { EnumerableSet } from "@openzeppelin/contracts/utils/structs/EnumerableSet.sol";
////import { SafeERC20 } from "@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol";
////import { Math } from "@openzeppelin/contracts/utils/math/Math.sol";

/// @title Rdpx V2 Core contract
/// @author Dopex
/// @notice The Rdpx V2 Corecontracts handles the bonding mechanism and peg of DpxEth
contract RdpxV2Core is
  IRdpxV2Core,
  AccessControl,
  ContractWhitelist,
  ERC721Holder,
  Pausable
{
  using EnumerableSet for EnumerableSet.AddressSet;
  using SafeERC20 for IERC20WithBurn;
  using SafeERC20 for IDpxEthToken;

  // ================================ STATE VARIABLES ================================ //

  /// @notice Addresses used by the contract
  Addresses public addresses;

  /// @notice The pricing oracle addresses
  PricingOracleAddresses public pricingOracleAddresses;

  /* Inital tokens in the reserve
     index0: ZERO address
     index1: weth
     index2: rdpx
     index3: dpxEth
     index4: crv
  */

  /// @notice Array containg the reserve assets
  ReserveAsset[] public reserveAsset;

  /// @notice Array that contains the addresses of the AMO
  address[] public amoAddresses;

  /// @notice Token address that dpxEth is pegged to
  address public weth;

  /// @notice Array that contains the symbol of the reserve tokens
  string[] public reserveTokens;

  /// @notice Mapping that contains the index for a specific token in the reserves
  mapping(string => uint256) public reservesIndex;

  /// @dev Bond id => Bond
  mapping(uint256 => Bond) public bonds;

  /// @dev Option id => owned or not (boolean)
  mapping(uint256 => bool) public optionsOwned;

  /// @dev Funding paid for epoch
  mapping(uint256 => bool) public fundingPaidFor;

  /// @notice Precision used for prices, percentages and other calculations
  uint256 public constant DEFAULT_PRECISION = 1e8;

  /// @notice rDPX Ratio required when bonding
  uint256 public constant RDPX_RATIO_PERCENTAGE = 25 * DEFAULT_PRECISION;

  /// @notice ETH Ratio required when bonding
  uint256 public constant ETH_RATIO_PERCENTAGE = 75 * DEFAULT_PRECISION;

  /// @notice The % of rdpx to burn while bonding
  uint256 public rdpxBurnPercentage = 50 * DEFAULT_PRECISION;

  /// @notice The % of rdpx sent to fee distributor while bonding
  uint256 public rdpxFeePercentage = 50 * DEFAULT_PRECISION;

  /// @notice The slippage tolernce in swaps in 1e8 precision
  uint256 public slippageTolerance = 5e5; // 0.5%

  /// @notice Liquidity slippage tolerance
  uint256 public liquiditySlippageTolerance = 5e5; // 0.5%

  /// @notice Bond maturity
  uint256 public bondMaturity;

  /// @notice rDPX LP bond discount factor
  uint256 public bondDiscountFactor;

  /// @notice Total weth delegated
  uint256 public totalWethDelegated;

  /// @notice Whether reLP is active or not
  bool public isReLPActive;

  /// @notice Whether put options are requred
  bool public putOptionsRequired;

  /// @notice Delegates array
  Delegate[] public delegates;

  // ================================ CONSTRUCTOR ================================ //
  constructor(address _weth) {
    _setupRole(DEFAULT_ADMIN_ROLE, msg.sender);
    weth = _weth;

    // add Zero asset to reserveAsset
    ReserveAsset memory zeroAsset = ReserveAsset({
      tokenAddress: address(0),
      tokenBalance: 0,
      tokenSymbol: "ZERO"
    });
    reserveAsset.push(zeroAsset);
    putOptionsRequired = true;
  }

  // ================================ ADMIN FUNCTIONS ================================ //

  /**
   * @notice Pauses the vault for emergency cases
   * @dev    Can only be called by the owner
   **/
  function pause() external onlyRole(DEFAULT_ADMIN_ROLE) {
    _pause();
  }

  /**
   * @notice Unpauses the vault
   * @dev    Can only be called by the owner
   **/
  function unpause() external onlyRole(DEFAULT_ADMIN_ROLE) {
    _unpause();
  }

  /**
   * @notice Transfers all funds to msg.sender
   * @dev    Can only be called by the owner
   * @param  tokens The list of erc20 tokens to withdraw
   **/
  function emergencyWithdraw(
    address[] calldata tokens
  ) external onlyRole(DEFAULT_ADMIN_ROLE) {
    _whenPaused();
    IERC20WithBurn token;

    for (uint256 i = 0; i < tokens.length; i++) {
      token = IERC20WithBurn(tokens[i]);
      token.safeTransfer(msg.sender, token.balanceOf(address(this)));
    }

    emit LogEmergencyWithdraw(msg.sender, tokens);
  }

  /**
   * @notice Sets the rdpx burn percentage
   * @dev    Can only be called by admin
   * @param  _rdpxBurnPercentage the burn percentage to set in 1e8 precision
   **/
  function setRdpxBurnPercentage(
    uint256 _rdpxBurnPercentage
  ) external onlyRole(DEFAULT_ADMIN_ROLE) {
    _validate(_rdpxBurnPercentage > 0, 3);
    rdpxBurnPercentage = _rdpxBurnPercentage;
    emit LogSetRdpxBurnPercentage(_rdpxBurnPercentage);
  }

  /**
   * @notice Sets the rdpx fee percentage
   * @dev    Can only be called by admin
   * @param  _rdpxFeePercentage the fee percentage to set in 1e8 precision
   **/
  function setRdpxFeePercentage(
    uint256 _rdpxFeePercentage
  ) external onlyRole(DEFAULT_ADMIN_ROLE) {
    _validate(_rdpxFeePercentage > 0, 3);
    rdpxFeePercentage = _rdpxFeePercentage;
    emit LogSetRdpxFeePercentage(_rdpxFeePercentage);
  }

  /**
   * @notice Sets whether reLP is true or false
   * @dev    Can only be called by admin
   * @param  _isReLPActive the value to set
   */
  function setIsreLP(bool _isReLPActive) external onlyRole(DEFAULT_ADMIN_ROLE) {
    isReLPActive = _isReLPActive;
    emit LogSetIsReLPActive(_isReLPActive);
  }

  /**
   * @notice Sets whether put options are required or not
   * @dev    Can only be called by admin
   * @param  _putOptionsRequired the value to set
   */
  function setPutOptionsRequired(
    bool _putOptionsRequired
  ) external onlyRole(DEFAULT_ADMIN_ROLE) {
    putOptionsRequired = _putOptionsRequired;
    emit LogSetputOptionsRequired(_putOptionsRequired);
  }

  /**
   * @notice Update the bond maturity
   * @dev    Can only be called by admin
   * @param  _bondMaturity bond maturity
   **/
  function setBondMaturity(
    uint256 _bondMaturity
  ) external onlyRole(DEFAULT_ADMIN_ROLE) {
    _validate(_bondMaturity > 0, 3);
    bondMaturity = _bondMaturity;
    emit LogSetBondMaturity(_bondMaturity);
  }

  /**
   * @notice Adds a asset to the reserves tokens
   * @dev    Can only be called by admin
   **/
  function addAssetTotokenReserves(
    address _asset,
    string memory _assetSymbol
  ) external onlyRole(DEFAULT_ADMIN_ROLE) {
    require(_asset != address(0), "RdpxV2Core: asset cannot be 0 address");

    for (uint256 i = 1; i < reserveAsset.length; i++) {
      require(
        reserveAsset[i].tokenAddress != _asset,
        "RdpxV2Core: asset already exists"
      );
    }

    ReserveAsset memory asset = ReserveAsset({
      tokenAddress: _asset,
      tokenBalance: 0,
      tokenSymbol: _assetSymbol
    });
    reserveAsset.push(asset);
    reserveTokens.push(_assetSymbol);

    reservesIndex[_assetSymbol] = reserveAsset.length - 1;

    emit LogAssetAddedTotokenReserves(_asset, _assetSymbol);
  }

  /**
   * @notice Removes a asset from the reserves tokens
   * @dev    Can only be called by admin
   **/
  function removeAssetFromtokenReserves(
    string memory _assetSymbol
  ) external onlyRole(DEFAULT_ADMIN_ROLE) {
    uint256 index = reservesIndex[_assetSymbol];
    _validate(index != 0, 18);

    // remove the asset from the mapping
    reservesIndex[_assetSymbol] = 0;

    // add new index for the last element
    reservesIndex[reserveTokens[reserveTokens.length - 1]] = index;

    // update the index of reserveAsset with the last element
    reserveAsset[index] = reserveAsset[reserveAsset.length - 1];

    // remove the last element
    reserveAsset.pop();
    reserveTokens.pop();

    emit LogAssetRemovedFromtokenReserves(_assetSymbol, index);
  }

  /**
   * @notice Update contract addresses
   * @dev    Can only be called by admin
   * @param  _dopexAMMRouter dopex AMM router address
   * @param  _dpxEthCurvePool DpxEth curve pool address
   * @param  _rdpxDecayingBonds rdpx decaying bonds address
   * @param  _perpetualAtlanticVault perpetual atlantic vault address
   * @param  _perpetualAtlanticVaultLP perpetual atlantic vault LP address
   * @param  _rdpxReserve rdpx reserve address
   * @param  _rdpxV2ReceiptToken rdpxV2ReceiptToken contract address
   * @param  _feeDistributor fee distributor address
   **/
  function setAddresses(
    address _dopexAMMRouter,
    address _dpxEthCurvePool,
    address _rdpxDecayingBonds,
    address _perpetualAtlanticVault,
    address _perpetualAtlanticVaultLP,
    address _rdpxReserve,
    address _rdpxV2ReceiptToken,
    address _feeDistributor,
    address _reLPContract,
    address _receiptTokenBonds
  ) external onlyRole(DEFAULT_ADMIN_ROLE) {
    _validate(_dopexAMMRouter != address(0), 17);
    _validate(_dpxEthCurvePool != address(0), 17);
    _validate(_rdpxDecayingBonds != address(0), 17);
    _validate(_perpetualAtlanticVault != address(0), 17);
    _validate(_perpetualAtlanticVaultLP != address(0), 17);
    _validate(_rdpxReserve != address(0), 17);
    _validate(_rdpxV2ReceiptToken != address(0), 17);
    _validate(_feeDistributor != address(0), 17);
    _validate(_reLPContract != address(0), 17);
    _validate(_receiptTokenBonds != address(0), 17);

    addresses = Addresses({
      dopexAMMRouter: _dopexAMMRouter,
      dpxEthCurvePool: _dpxEthCurvePool,
      rdpxDecayingBonds: _rdpxDecayingBonds,
      perpetualAtlanticVault: _perpetualAtlanticVault,
      perpetualAtlanticVaultLP: _perpetualAtlanticVaultLP,
      rdpxReserve: _rdpxReserve,
      rdpxV2ReceiptToken: _rdpxV2ReceiptToken,
      feeDistributor: _feeDistributor,
      reLPContract: _reLPContract,
      receiptTokenBonds: _receiptTokenBonds
    });
    IERC20WithBurn(weth).approve(
      addresses.perpetualAtlanticVault,
      type(uint256).max
    );
    IERC20WithBurn(weth).approve(addresses.dopexAMMRouter, type(uint256).max);
    IERC20WithBurn(weth).approve(addresses.dpxEthCurvePool, type(uint256).max);
    IERC20WithBurn(weth).approve(
      addresses.rdpxV2ReceiptToken,
      type(uint256).max
    );
    emit LogSetAddresses(addresses);
  }

  /**
   * @notice Update token contract addresses
   * @dev    Can only be called by admin
   * @param  _rdpxPriceOracle rdpx price oracle address
   * @param  _dpxEthPriceOracle DpxEth price oracle address
   **/
  function setPricingOracleAddresses(
    address _rdpxPriceOracle,
    address _dpxEthPriceOracle
  ) external onlyRole(DEFAULT_ADMIN_ROLE) {
    _validate(_rdpxPriceOracle != address(0), 17);
    _validate(_dpxEthPriceOracle != address(0), 17);

    pricingOracleAddresses = PricingOracleAddresses({
      rdpxPriceOracle: _rdpxPriceOracle,
      dpxEthPriceOracle: _dpxEthPriceOracle
    });

    emit LogSetPricingOracleAddresses(pricingOracleAddresses);
  }

  /**
   * @notice Adds a AMO contract to the AMO address array
   * @dev    Can only be called by admin
   * @param  _addr the address to add to the AMO address array
   */
  function addAMOAddress(address _addr) external onlyRole(DEFAULT_ADMIN_ROLE) {
    _validate(_addr != address(0), 17);
    amoAddresses.push(_addr);
  }

  /**
   * @notice Removes a AMO contract from the AMO address array
   * @dev    Can only be called by admin
   * @param  _index the index of the address to remove from the AMO address array
   */
  function removeAMOAddress(
    uint256 _index
  ) external onlyRole(DEFAULT_ADMIN_ROLE) {
    _validate(_index < amoAddresses.length, 18);
    amoAddresses[_index] = amoAddresses[amoAddresses.length - 1];
    amoAddresses.pop();
  }

  /**
   * @notice Approve a contract to spend a certain amount of tokens
   * @dev    Can only be called by admin
   * @param  _token the address of the token to approve
   * @param  _spender the address of the contract to approve
   * @param  _amount the amount to approve
   */
  function approveContractToSpend(
    address _token,
    address _spender,
    uint256 _amount
  ) external onlyRole(DEFAULT_ADMIN_ROLE) {
    _validate(_token != address(0), 17);
    _validate(_spender != address(0), 17);
    _validate(_amount > 0, 17);
    IERC20WithBurn(_token).approve(_spender, _amount);
  }

  /**
   * @notice Adds a contract to the contract whitelist
   * @dev    Can only be called by admin
   * @param  _addr the address to add to the contract whitelist
   **/
  function addToContractWhitelist(
    address _addr
  ) external onlyRole(DEFAULT_ADMIN_ROLE) {
    _addToContractWhitelist(_addr);
  }

  /**
   * @notice Removes a contract from the contract whitelist
   * @dev    Can only be called by admin
   * @param  _addr the address to remove from the contract whitelist
   **/
  function removeFromContractWhitelist(
    address _addr
  ) external onlyRole(DEFAULT_ADMIN_ROLE) {
    _removeFromContractWhitelist(_addr);
  }

  /**
   * @notice Set the rDPX LP bond discount factor
   * @dev    Can only be called by admin
   * @param  _bondDiscountFactor the bond discount factor
   **/
  function setBondDiscount(
    uint256 _bondDiscountFactor
  ) external onlyRole(DEFAULT_ADMIN_ROLE) {
    _validate(_bondDiscountFactor > 0, 3);
    bondDiscountFactor = _bondDiscountFactor;

    emit LogSetBondDiscountFactor(_bondDiscountFactor);
  }

  /**
   * @notice Set the slippage tolerance
   * @dev    Can only be called by admin
   * @param  _slippageTolerance the slipage tolerance
   **/
  function setSlippageTolerance(
    uint256 _slippageTolerance
  ) external onlyRole(DEFAULT_ADMIN_ROLE) {
    _validate(_slippageTolerance > 0, 3);
    slippageTolerance = _slippageTolerance;

    emit LogSetSlippageTolerance(_slippageTolerance);
  }

  // ================================ INTERNAL FUNCTIONS ================================ //

  /**
   * @notice Purchase rdpx put options
   * @param _amount amount of rdpx to purchase
   * @return premium amount of premium paid
   */
  function _purchaseOptions(
    uint256 _amount
  ) internal returns (uint256 premium) {
    /**
     * Purchase options and store ERC721 option id
     * Note that the amount of options purchased is the amount of rDPX received
     * from the user to sufficiently collateralize the underlying DpxEth stored in the bond
     **/
    uint256 optionId;

    (premium, optionId) = IPerpetualAtlanticVault(
      addresses.perpetualAtlanticVault
    ).purchase(_amount, address(this));

    optionsOwned[optionId] = true;
    reserveAsset[reservesIndex["WETH"]].tokenBalance -= premium;
  }

  /**
   * @notice issue bonds
   * @param  _to The address to send the bond to
   * @param  _amount The bond amount
   * @return bondId The bond id
   **/
  function _issueBond(
    address _to,
    uint256 _amount
  ) internal returns (uint256 bondId) {
    bondId = RdpxV2Bond(addresses.receiptTokenBonds).mint(_to);
    bonds[bondId] = Bond({
      amount: _amount,
      maturity: block.timestamp + bondMaturity,
      timestamp: block.timestamp
    });
  }

  /**
   * @notice Swaps _amount of token a to token b
   * @param _amount amount to swap
   * @param _ethToDpxEth whether to swap ETH to dpxETH or dpxETH to ETH
   * @param validate whether to validate the swap
   * @param minAmount minimum amount of token b to receive
   * @return amountOut amount of token b received
   */
  function _curveSwap(
    uint256 _amount,
    bool _ethToDpxEth,
    bool validate,
    uint256 minAmount
  ) internal returns (uint256 amountOut) {
    IStableSwap dpxEthCurvePool = IStableSwap(addresses.dpxEthCurvePool);

    // First compute a reverse swapping of dpxETH to ETH to compute the amount of ETH required
    address coin0 = dpxEthCurvePool.coins(0);
    (uint256 a, uint256 b) = coin0 == weth ? (0, 1) : (1, 0);

    // validate the swap for peg functions
    if (validate) {
      uint256 ethBalance = IStableSwap(addresses.dpxEthCurvePool).balances(a);
      uint256 dpxEthBalance = IStableSwap(addresses.dpxEthCurvePool).balances(
        b
      );
      _ethToDpxEth
        ? _validate(
          ethBalance + _amount <= (ethBalance + dpxEthBalance) / 2,
          14
        )
        : _validate(
          dpxEthBalance + _amount <= (ethBalance + dpxEthBalance) / 2,
          14
        );
    }

    // calculate minimum amount out
    uint256 minOut = _ethToDpxEth
      ? (((_amount * getDpxEthPrice()) / 1e8) -
        (((_amount * getDpxEthPrice()) * slippageTolerance) / 1e16))
      : (((_amount * getEthPrice()) / 1e8) -
        (((_amount * getEthPrice()) * slippageTolerance) / 1e16));

    // Swap the tokens
    amountOut = dpxEthCurvePool.exchange(
      _ethToDpxEth ? int128(int256(a)) : int128(int256(b)),
      _ethToDpxEth ? int128(int256(b)) : int128(int256(a)),
      _amount,
      minAmount > 0 ? minAmount : minOut
    );
  }

  /**
   * @notice Deposits ETH and dpxETH to the ReceiptToken contract
   * @param  _to The address to send the bond to
   * @param  _amount The amount of ETH to add liquidity with
   * @return receiptTokenAmount The amount of receipt token received
   **/
  function _stake(
    address _to,
    uint256 _amount
  ) internal returns (uint256 receiptTokenAmount) {
    reserveAsset[reservesIndex["WETH"]].tokenBalance -= _amount / 2;

    IDpxEthToken(reserveAsset[reservesIndex["DPXETH"]].tokenAddress).mint(
      address(this),
      _amount / 2
    );

    // deposit into the rdpxV2ReceiptToken contract
    receiptTokenAmount = IRdpxV2ReceiptToken(addresses.rdpxV2ReceiptToken)
      .deposit(_amount / 2);

    // mint receipt token bonds
    _issueBond(_to, receiptTokenAmount);
  }

  /**
   * @notice Calculate the amounts received by delegate and delegatee after accounting for
   *         delegate fee.
   * @dev    Mint receipt tokens based on its respective share with a discount % in 1e8 precision.
   *         The delegate fee is the percentage of the discount received by the delegatee
   *         that is cut for them.
   * @param  _wethRequired The wethRequired to bond
   * @param  _rdpxRequired The rdpxRequired to bond
   * @param  _amount The bond amount
   * @param  _delegateFee The delegate fee
   * @return amount1 The amount received by the delegate
   * @return amount2 The amount received by the delegatee
   **/
  function _calculateAmounts(
    uint256 _wethRequired,
    uint256 _rdpxRequired,
    uint256 _amount,
    uint256 _delegateFee
  ) internal view returns (uint256 amount1, uint256 amount2) {
    // Commented below for better clarity
    uint256 rdpxRequiredInWeth = (_rdpxRequired * getRdpxPrice()) / 1e8;

    // amount required for delegatee
    amount1 = ((rdpxRequiredInWeth * _amount) /
      (rdpxRequiredInWeth + _wethRequired));

    // account for delegate fee
    amount1 = (amount1 * (100e8 - _delegateFee)) / 1e10;

    amount2 = _amount - amount1;
  }

  /**
   * @notice Transfers rdpx or burns the equivalent in rDPX Decaying bonds
   * @param  _rdpxAmount The rdpx amount
   * @param  _wethAmount The weth amount
   * @param  _bondAmount The bond amount
   * @param  _bondId The bond id of the rdpx decaying bond
   **/
  function _transfer(
    uint256 _rdpxAmount,
    uint256 _wethAmount,
    uint256 _bondAmount,
    uint256 _bondId
  ) internal {
    if (_bondId != 0) {
      (, uint256 expiry, uint256 amount) = IRdpxDecayingBonds(
        addresses.rdpxDecayingBonds
      ).bonds(_bondId);

      _validate(amount >= _rdpxAmount, 1);
      _validate(expiry >= block.timestamp, 2);
      _validate(
        IRdpxDecayingBonds(addresses.rdpxDecayingBonds).ownerOf(_bondId) ==
          msg.sender,
        9
      );

      IRdpxDecayingBonds(addresses.rdpxDecayingBonds).decreaseAmount(
        _bondId,
        amount - _rdpxAmount
      );

      IRdpxReserve(addresses.rdpxReserve).withdraw(_rdpxAmount);

      reserveAsset[reservesIndex["RDPX"]].tokenBalance += _rdpxAmount;
    } else {
      // Transfer rDPX and ETH token from user
      IERC20WithBurn(reserveAsset[reservesIndex["RDPX"]].tokenAddress)
        .safeTransferFrom(msg.sender, address(this), _rdpxAmount);

      // burn the rdpx
      IERC20WithBurn(reserveAsset[reservesIndex["RDPX"]].tokenAddress).burn(
        (_rdpxAmount * rdpxBurnPercentage) / 1e10
      );

      // transfer the rdpx to the fee distributor
      IERC20WithBurn(reserveAsset[reservesIndex["RDPX"]].tokenAddress)
        .safeTransfer(
          addresses.feeDistributor,
          (_rdpxAmount * rdpxFeePercentage) / 1e10
        );

      // calculate extra rdpx to withdraw to compensate for discount
      uint256 rdpxAmountInWeth = (_rdpxAmount * getRdpxPrice()) / 1e8;
      uint256 discountReceivedInWeth = _bondAmount -
        _wethAmount -
        rdpxAmountInWeth;
      uint256 extraRdpxToWithdraw = (discountReceivedInWeth * 1e8) /
        getRdpxPrice();

      // withdraw the rdpx
      IRdpxReserve(addresses.rdpxReserve).withdraw(
        _rdpxAmount + extraRdpxToWithdraw
      );

      reserveAsset[reservesIndex["RDPX"]].tokenBalance +=
        _rdpxAmount +
        extraRdpxToWithdraw;
    }
  }

  /**
   * @notice Internal function to bond with delegates
   * @param  _amount The amount of DpxEth to bond
   * @param  rdpxBondId The bond id
   * @param  delegateId The id of the delegate position being used
   * @return  returnValues {
    uint256 delegateReceiptTokenAmount;
    uint256 bondAmountForUser;
    uint256 rdpxRequired;
    uint256 wethRequired;
  }
   **/
  function _bondWithDelegate(
    uint256 _amount,
    uint256 rdpxBondId,
    uint256 delegateId
  ) internal returns (BondWithDelegateReturnValue memory returnValues) {
    // Compute the bond cost
    (uint256 rdpxRequired, uint256 wethRequired) = calculateBondCost(
      _amount,
      rdpxBondId
    );

    // update ETH token reserve
    reserveAsset[reservesIndex["WETH"]].tokenBalance += wethRequired;

    Delegate storage delegate = delegates[delegateId];

    // update delegate active collateral
    _validate(delegate.amount - delegate.activeCollateral >= wethRequired, 5);
    delegate.activeCollateral += wethRequired;

    // update total weth delegated
    totalWethDelegated -= wethRequired;

    // Calculate the amount of bond token to mint for the delegate and user based on the fee
    (uint256 amount1, uint256 amount2) = _calculateAmounts(
      wethRequired,
      rdpxRequired,
      _amount,
      delegate.fee
    );

    // update user amounts
    // ETH token amount remaining after LP for the user
    uint256 bondAmountForUser = amount1;

    // Mint bond token for delegate
    // ETH token amount remaining after LP for the delegate
    uint256 delegateReceiptTokenAmount = _stake(delegate.owner, amount2);

    returnValues = BondWithDelegateReturnValue(
      delegateReceiptTokenAmount,
      bondAmountForUser,
      rdpxRequired,
      wethRequired
    );
  }

  /**
   * @dev    Internal function to validate checks
   * @param  _clause the boolean clause to validate
   * @param  _errorCode error code for error mapping below
   **/
  function _validate(bool _clause, uint256 _errorCode) internal pure {
    if (!_clause) revert RdpxV2CoreError(_errorCode);
  }

  // ================================ CORE ================================ //

  /**
   * @notice Settles the options
   * @dev    Can only be called by admin
   * @param  optionIds the ids of the option to be settled
   * @return amountOfWeth the amount of eth received
   * @return rdpxAmount the amount of rdpx sent out
   */
  function settle(
    uint256[] memory optionIds
  )
    external
    onlyRole(DEFAULT_ADMIN_ROLE)
    returns (uint256 amountOfWeth, uint256 rdpxAmount)
  {
    _whenNotPaused();
    (amountOfWeth, rdpxAmount) = IPerpetualAtlanticVault(
      addresses.perpetualAtlanticVault
    ).settle(optionIds);
    for (uint256 i = 0; i < optionIds.length; i++) {
      optionsOwned[optionIds[i]] = false;
    }

    reserveAsset[reservesIndex["WETH"]].tokenBalance += amountOfWeth;
    reserveAsset[reservesIndex["RDPX"]].tokenBalance -= rdpxAmount;

    emit LogSettle(optionIds);
  }

  /**
   * @notice Calculates and sends the funding amount to the vault
   * @dev    Can only be called by admin
   * @return fundingAmount the amount of funding paid
   **/
  function provideFunding()
    external
    onlyRole(DEFAULT_ADMIN_ROLE)
    returns (uint256 fundingAmount)
  {
    _whenNotPaused();
    uint256 pointer = IPerpetualAtlanticVault(addresses.perpetualAtlanticVault)
      .latestFundingPaymentPointer();
    _validate(fundingPaidFor[pointer] == false, 16);

    fundingAmount = IPerpetualAtlanticVault(addresses.perpetualAtlanticVault)
      .payFunding();

    reserveAsset[reservesIndex["WETH"]].tokenBalance -= fundingAmount;

    fundingPaidFor[pointer] = true;

    emit LogProvideFunding(pointer, fundingAmount);
  }

  /**
   * @notice The Bonding function to bond with delegates
   * @param  _to The address to send the bond to
   * @param  _amounts The amounts of DpxEth to lock in the bond
   * @param  _delegateIds the id of the delegate position's being used
   * @param  rdpxBondId The bond id
   * @return receiptTokenAmount The amount of receipt tokens recieved
   * @return delegateTokenAmounts The amount of receipt tokens recieved for each delegate
   **/
  function bondWithDelegate(
    address _to,
    uint256[] memory _amounts,
    uint256[] memory _delegateIds,
    uint256 rdpxBondId
  ) public returns (uint256 receiptTokenAmount, uint256[] memory) {
    _whenNotPaused();
    // Validate amount
    _validate(_amounts.length == _delegateIds.length, 3);

    uint256 userTotalBondAmount;
    uint256 totalBondAmount;

    uint256[] memory delegateReceiptTokenAmounts = new uint256[](
      _amounts.length
    );

    for (uint256 i = 0; i < _amounts.length; i++) {
      // Validate amount
      _validate(_amounts[i] > 0, 4);

      BondWithDelegateReturnValue
        memory returnValues = BondWithDelegateReturnValue(0, 0, 0, 0);

      returnValues = _bondWithDelegate(
        _amounts[i],
        rdpxBondId,
        _delegateIds[i]
      );

      delegateReceiptTokenAmounts[i] = returnValues.delegateReceiptTokenAmount;

      userTotalBondAmount += returnValues.bondAmountForUser;
      totalBondAmount += _amounts[i];

      // purchase options
      uint256 premium;
      if (putOptionsRequired) {
        premium = _purchaseOptions(returnValues.rdpxRequired);
      }

      // transfer the required rdpx
      _transfer(
        returnValues.rdpxRequired,
        returnValues.wethRequired - premium,
        _amounts[i],
        rdpxBondId
      );
    }

    // Mint bond token for user
    receiptTokenAmount = _stake(_to, userTotalBondAmount);

    // reLP
    if (isReLPActive) IReLP(addresses.reLPContract).reLP(totalBondAmount);

    emit LogBondWithDelegate(
      _to,
      _delegateIds,
      _amounts,
      rdpxBondId,
      receiptTokenAmount,
      delegateReceiptTokenAmounts
    );

    return (receiptTokenAmount, delegateReceiptTokenAmounts);
  }

  /**
   * @notice The primary bonding function
   * @param  _amount The amount of DpxEth to bond for
   * @param  rdpxBondId The bond id
   * @param  _to The address to send the bond to
   * @return receiptTokenAmount the amount of receipt tokens received
   **/
  function bond(
    uint256 _amount,
    uint256 rdpxBondId,
    address _to
  ) public returns (uint256 receiptTokenAmount) {
    _whenNotPaused();
    // Validate amount
    _validate(_amount > 0, 4);

    // Compute the bond cost
    (uint256 rdpxRequired, uint256 wethRequired) = calculateBondCost(
      _amount,
      rdpxBondId
    );

    IERC20WithBurn(weth).safeTransferFrom(
      msg.sender,
      address(this),
      wethRequired
    );

    // update weth reserve
    reserveAsset[reservesIndex["WETH"]].tokenBalance += wethRequired;

    // purchase options
    uint256 premium;
    if (putOptionsRequired) {
      premium = _purchaseOptions(rdpxRequired);
    }

    _transfer(rdpxRequired, wethRequired - premium, _amount, rdpxBondId);

    // Stake the ETH in the ReceiptToken contract
    receiptTokenAmount = _stake(_to, _amount);

    // reLP
    if (isReLPActive) IReLP(addresses.reLPContract).reLP(_amount);

    emit LogBond(rdpxRequired, wethRequired, receiptTokenAmount);
  }

  /**
   * @notice Lets users delegate WETH
   * @param  _amount The amount of WETH to delegate
   * @param  _fee The fee to charge for the delegated WETH
   * @return uint256 the ID of the delegate
   **/
  function addToDelegate(
    uint256 _amount,
    uint256 _fee
  ) external returns (uint256) {
    _whenNotPaused();
    // fee less than 100%
    _validate(_fee < 100e8, 8);
    // amount greater than 0.01 WETH
    _validate(_amount > 1e16, 4);
    // fee greater than 1%
    _validate(_fee >= 1e8, 8);

    IERC20WithBurn(weth).safeTransferFrom(msg.sender, address(this), _amount);

    Delegate memory delegatePosition = Delegate({
      amount: _amount,
      fee: _fee,
      owner: msg.sender,
      activeCollateral: 0
    });
    delegates.push(delegatePosition);

    // add amount to total weth delegated
    totalWethDelegated += _amount;

    emit LogAddToDelegate(_amount, _fee, delegates.length - 1);
    return (delegates.length - 1);
  }

  /**
   * @notice Lets the delegate withdraw unused WETH
   * @param  delegateId The ID of the delegate
   * @return amountWithdrawn The amount of WETH withdrawn
   **/
  function withdraw(
    uint256 delegateId
  ) external returns (uint256 amountWithdrawn) {
    _whenNotPaused();
    _validate(delegateId < delegates.length, 14);
    Delegate storage delegate = delegates[delegateId];
    _validate(delegate.owner == msg.sender, 9);

    amountWithdrawn = delegate.amount - delegate.activeCollateral;
    _validate(amountWithdrawn > 0, 15);
    delegate.amount = delegate.activeCollateral;

    IERC20WithBurn(weth).safeTransfer(msg.sender, amountWithdrawn);

    emit LogDelegateWithdraw(delegateId, amountWithdrawn);
  }

  /**
   * @notice Syncs asset reserves with contract balances
   **/
  function sync() external {
    for (uint256 i = 1; i < reserveAsset.length; i++) {
      uint256 balance = IERC20WithBurn(reserveAsset[i].tokenAddress).balanceOf(
        address(this)
      );

      if (weth == reserveAsset[i].tokenAddress) {
        balance = balance - totalWethDelegated;
      }
      reserveAsset[i].tokenBalance = balance;
    }

    emit LogSync();
  }

   /**
   * @notice Withdraws DSC from a matured bond
   * @param  id bond ID
   * @param  to the address to send the DSC too
   * @return receiptTokenAmount the amount of receipt Tokens to transfer
   **/
  function redeem(
    uint256 id,
    address to
  ) external returns (uint256 receiptTokenAmount) {
    // Validate bond ID
    _validate(bonds[id].timestamp > 0, 6);
    // Validate if bond has matured
    _validate(block.timestamp > bonds[id].maturity, 7);

    _validate(
      msg.sender == RdpxV2Bond(addresses.receiptTokenBonds).ownerOf(id),
      9
    );

    // Burn the bond token
    // Note requires an approval of the bond token to this contract
    RdpxV2Bond(addresses.receiptTokenBonds).burn(id);

    // transfer receipt tokens to user
    receiptTokenAmount = bonds[id].amount;
    IERC20WithBurn(addresses.rdpxV2ReceiptToken).safeTransfer(
      to,
      receiptTokenAmount
    );

    emit LogRedeem(to, receiptTokenAmount);
  }

  // ================================ REPEG FUNCTIONS ================================ //

  /**
   * @notice Lets users mint DpxEth at a 1:1 ratio when DpxEth pegs above 1.01 of the ETH token
   * @param  _amount The amount of DpxEth to mint
   * @param minOut The minimum amount out
   **/
  function upperDepeg(
    uint256 _amount,
    uint256 minOut
  ) external onlyRole(DEFAULT_ADMIN_ROLE) returns (uint256 wethReceived) {
    _isEligibleSender();

    _validate(getDpxEthPrice() > 1e8, 10);

    IDpxEthToken(reserveAsset[reservesIndex["DPXETH"]].tokenAddress).mint(
      address(this),
      _amount
    );

    // Swap DpxEth for ETH token
    wethReceived = _curveSwap(_amount, false, true, minOut);

    reserveAsset[reservesIndex["WETH"]].tokenBalance += wethReceived;

    emit LogUpperDepeg(_amount, wethReceived);
  }

  /**
   * @notice Rdpx V2 Core can redeem Rdpx/ETH lp tokens ot buy back and burn DpxEth
   * @dev    uintParams are used to avoid reaching stack depth
   * @param  _rdpxAmount The amount of rdpx to use
   * @param  _wethAmount The amount of weth to use
   * @param minamountOfWeth min ETH token receive when swapping rdpx to ETH token
   * @param  minOut min amount out
   **/
  function lowerDepeg(
    uint256 _rdpxAmount,
    uint256 _wethAmount,
    uint256 minamountOfWeth,
    uint256 minOut
  ) external onlyRole(DEFAULT_ADMIN_ROLE) returns (uint256 dpxEthReceived) {
    _isEligibleSender();
    _validate(getDpxEthPrice() < 1e8, 13);

    uint256 amountOfWethOut;

    if (_rdpxAmount != 0) {
      address[] memory path;
      path = new address[](2);
      path[0] = reserveAsset[reservesIndex["RDPX"]].tokenAddress;
      path[1] = weth;

      amountOfWethOut = IUniswapV2Router(addresses.dopexAMMRouter)
        .swapExactTokensForTokens(
          _rdpxAmount,
          minamountOfWeth,
          path,
          address(this),
          block.timestamp + 10
        )[path.length - 1];

      reserveAsset[reservesIndex["RDPX"]].tokenBalance -= _rdpxAmount;
    }

    // update Reserves
    reserveAsset[reservesIndex["WETH"]].tokenBalance -= _wethAmount;

    dpxEthReceived = _curveSwap(
      _wethAmount + amountOfWethOut,
      true,
      true,
      minOut
    );

    IDpxEthToken(reserveAsset[reservesIndex["DPXETH"]].tokenAddress).burn(
      dpxEthReceived
    );

    emit LogLowerDepeg(_rdpxAmount, _wethAmount, dpxEthReceived);
  }

  // ================================ VIEWS/GETTERS ================================ //

  /**
   * @notice Returns the reserve token info for a given token
   * @param _token token to get reserves of
   * @return tokenAddress token address
   * @return tokenBalance reserves of the token
   * @return tokenSymbol token symbol
   */
  function getReserveTokenInfo(
    string memory _token
  ) public view returns (address, uint256, string memory) {
    ReserveAsset memory asset = reserveAsset[reservesIndex[_token]];

    _validate(
      keccak256(abi.encodePacked(asset.tokenSymbol)) ==
        keccak256(abi.encodePacked(_token)),
      19
    );

    return (asset.tokenAddress, asset.tokenBalance, asset.tokenSymbol);
  }

  /**
   * @notice Calculate the cost of bonding
   * @param  _amount amount of bonding
   * @param _rdpxBondId id of rdpx bond
   * @return rdpxRequired amount of rDPX required
   * @return wethRequired amount of ETH token required
   **/
  function calculateBondCost(
    uint256 _amount,
    uint256 _rdpxBondId
  ) public view returns (uint256 rdpxRequired, uint256 wethRequired) {
    uint256 rdpxPrice = getRdpxPrice();

    if (_rdpxBondId == 0) {
      uint256 bondDiscount = (bondDiscountFactor *
        Math.sqrt(IRdpxReserve(addresses.rdpxReserve).rdpxReserve()) *
        1e2) / (Math.sqrt(1e18)); // 1e8 precision

      _validate(bondDiscount < 100e8, 14);

      rdpxRequired =
        ((RDPX_RATIO_PERCENTAGE - (bondDiscount / 2)) *
          _amount *
          DEFAULT_PRECISION) /
        (DEFAULT_PRECISION * rdpxPrice * 1e2);

      wethRequired =
        ((ETH_RATIO_PERCENTAGE - (bondDiscount / 2)) * _amount) /
        (DEFAULT_PRECISION * 1e2);
    } else {
      // if rdpx decaying bonds are being used there is no discount
      rdpxRequired =
        (RDPX_RATIO_PERCENTAGE * _amount * DEFAULT_PRECISION) /
        (DEFAULT_PRECISION * rdpxPrice * 1e2);

      wethRequired =
        (ETH_RATIO_PERCENTAGE * _amount) /
        (DEFAULT_PRECISION * 1e2);
    }

    uint256 strike = IPerpetualAtlanticVault(addresses.perpetualAtlanticVault)
      .roundUp(rdpxPrice - (rdpxPrice / 4)); // 25% below the current price

    uint256 timeToExpiry = IPerpetualAtlanticVault(
      addresses.perpetualAtlanticVault
    ).nextFundingPaymentTimestamp() - block.timestamp;
    if (putOptionsRequired) {
      wethRequired += IPerpetualAtlanticVault(addresses.perpetualAtlanticVault)
        .calculatePremium(strike, rdpxRequired, timeToExpiry, 0);
    }
  }

  /**
   * @notice Returns the price of a rDPX/ETH Lp token against the ETH token
   * @dev    Price is in 1e8 Precision
   * @return uint256 LP price
   **/
  function getLpPrice() public view returns (uint256) {
    return
      IRdpxEthOracle(pricingOracleAddresses.rdpxPriceOracle).getLpPriceInEth();
  }

  /**
   * @notice Returns the price of dpxETH against ETH
   * @dev    Price is in 1e8 Precision
   * @return dpxEthPrice dpxETH price
   **/
  function getDpxEthPrice() public view returns (uint256 dpxEthPrice) {
    return
      IDpxEthOracle(pricingOracleAddresses.dpxEthPriceOracle)
        .getDpxEthPriceInEth();
  }

  /**
   * @notice Returns the price of ETH token against the DpxEth
   * @dev    Price is in 1e8 Precision
   * @return ethPrice ethToken price
   **/
  function getEthPrice() public view returns (uint256 ethPrice) {
    return
      IDpxEthOracle(pricingOracleAddresses.dpxEthPriceOracle)
        .getEthPriceInDpxEth();
  }

  /**
   * @notice Returns the price of rDPX against ETH
   * @dev    Price is in 1e8 Precision
   * @return rdpxPriceInEth rDPX price in ETH
   **/
  function getRdpxPrice() public view returns (uint256) {
    return
      IRdpxEthOracle(pricingOracleAddresses.rdpxPriceOracle)
        .getRdpxPriceInEth();
  }

  /**
   * @notice Viewer for returning length of uint256[] delegates
   * @return uint256 length of delegates array
   **/
  function getDelegatesLength() external view returns (uint256) {
    return delegates.length;
  }

  /**
   * @notice Returns the details of a delegate position
   * @param _delegateId id of the delegate position
   * @return delegate address of the delegate
   * @return amount amount of WETH delegated
   * @return fee fee of the delegate
   * @return activeCollateral active collateral of the delegate
   **/
  function getDelegatePosition(
    uint256 _delegateId
  )
    public
    view
    returns (
      address delegate,
      uint256 amount,
      uint256 fee,
      uint256 activeCollateral
    )
  {
    Delegate memory delegatePosition = delegates[_delegateId];
    return (
      delegatePosition.owner,
      delegatePosition.amount,
      delegatePosition.fee,
      delegatePosition.activeCollateral
    );
  }

  // ================================ CUSTOM ERROR ================================ //
  /**
  * @dev  Custom Error used to validate checks within the contract's functions.
          The uint256 error code corresponds to an error message.
  **/
  error RdpxV2CoreError(uint256);
}

// ERROR CODES
// E1: "Insufficient bond amount",
// E2: "Bond has expired",
// E3: "Invalid parameters",
// E4: "Invalid amount",
// E5: "Not enough ETH available from the delegate",
// E6: "Invalid bond ID",
// E7: "Bond has not matured",
// E8: "Fee cannot be more than 100",
// E9: "msg.sender is not the owner",
// E10: "Price is not above the upper peg",
// E11: "Amount greater that max permissible amount",
// E12: "Price is not lower than first lower peg",
// E13: "Amount greater than max permissible amount"
// E14: "Invalid delegate Id"
// E15: "Invalid amount"
// E16: "Funding already paid for the epoch"
// E17: "Zero address"
// E18: "Asset not found"
// E19: "Token not found"


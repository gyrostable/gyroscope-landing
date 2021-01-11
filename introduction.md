---
layout: default
permalink: /introduction
body_class: post
---

# Gyroscope Explained:<br> from TradFi Currency Pegs to Non-custodial Stablecoins

{:.logo}
!["Spinning Gyroscope"](figures/spinning_top.png)

Following our work on modeling stablecoins [here](https://medium.com/coinmonks/stablecoins-2-0-economic-foundations-for-defi-b9ab38500b87) and [here](https://medium.com/coinmonks/insights-from-modeling-stablecoins-a30e732aef1b), we recently proposed ways to make more robust non-custodial stablecoins in our [Gyroscope paper](litepaper). This blog post is an intro to those ideas. The design insights are relatively simple, though their optimization is not. At the heart of the Gyroscope design is a community-owned reserve fund, which we call the gyroscopic buffer, that supports a currency peg through an algorithmic minting and redemption process.

<blockquote class="twitter-tweet" style="min-height: 520px;"><p lang="en" dir="ltr">🚨 Introducing Gyroscope 🚨. A new resilient <a href="https://twitter.com/hashtag/stablecoin?src=hash&amp;ref_src=twsrc%5Etfw">#stablecoin</a> design that aims to be the nearest feasible neighbour to a risk-free crypto asset. Our gyroscopic stablecoin mechanism uses AMMs and a growing gyroscopic buffer to maintain stability.<a href="https://t.co/Ao4jUXeMH8">https://t.co/Ao4jUXeMH8</a> <a href="https://t.co/StKvZmvcSk">pic.twitter.com/StKvZmvcSk</a></p>&mdash; Gyroscope (@GyroStable) <a href="https://twitter.com/GyroStable/status/1347573355818459136?ref_src=twsrc%5Etfw">January 8, 2021</a></blockquote> <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script> 

## TradFi Currency Pegs

Our ideas are far from a new concept altogether. The core design is similar to how traditional currency pegs work in traditional finance (TradFi). With a traditional currency peg, a central bank pegs currency X to currency Y. They hold a reserve of currency Y, with which they may intervene in the X/Y foreign exchange market to maintain the pegged exchange rate. When the supply of currency X is completely collateralized by reserves in Y, the peg is effectively unbreakable unless policy itself changes. This is comparable to currency boards like the Hong Kong Dollar and custodial stablecoins like USDC.

More interesting is the case where Y reserves may undercollateralize the supply of X (or may generally be variable). A peg can be maintained in this setting as well. Here the mechanism is a currency game: the peg is maintainable as long as enough people (1) don’t need to sell the currency X at once and (2) don’t expect that too many other people will sell currency X. This currency game can lead to speculative attacks on the peg (e.g., George Soros’s infamous attack on the British pound). A well-designed currency peg needs to be robust to this. The game theory typically works here by (1) making it so people commonly don’t need to redeem currency X for Y (i.e., X is useful to people directly as a currency), and (2) by making speculative attacks, which would profit from a depegging, economically infeasible.

The international economics literature demonstrates that pegged currencies can be stable for extended periods of time, though they are far from riskless. History provides many examples with which to learn how currency pegs work and also break.


## Applying this to non-custodial stablecoins
We envision a stablecoin inspired by TradFi currency peg mechanisms that replaces the central bank’s role of maintaining the peg with algorithms that manage reserves, issuance, and redemption. This sounds great, but is not easy to realize. When doing this non-custodially, there are two key differences when compared with TradFi currency pegs that make this even more difficult.

## The Portfolio Problem:

First, USD reserves can’t be held on-chain. So if we’re creating non-custodial stablecoin X that is pegged to target currency Y, the reserves backing the currency peg can’t be in Y. In particular, reserves have to be held in other on-chain assets, which are inherently risky. So on top of the currency peg game, this introduces a portfolio problem. In effect, the system has to maintain the peg using a volatile reserve, and the stablecoin’s strength is limited by the reserve portfolio.

## The Attack Problem:

Second, on-chain speculative attacks are in a different league than TradFi speculative attacks. Transactions can interact with an on-chain reserve with great speed, the implementation is open-source and algorithmic, and the on-chain setting is pseudo-anonymous. For these reasons, a DeFi mechanism needs to be more robust to speculative attacks and extra thought needs to go into structuring the underlying game toward long-term peg incentives.

This is what we explore and propose new solutions for in the Gyroscope paper.  For the Portfolio Problem, we develop methods for stratifying complex DeFi portfolio risks, similar to designing watertight compartments in a ship to ensure a breach in one compartment does not make the whole thing sink. For the Attack Problem, we  develop new AMM designs that shift incentives toward long-term peg stability.

<figure class="image titanic">
  <img src="figures/titanic.png" alt="Titanic analogy">
  <figcaption>(Titanic analogy) how to prevent cascading failure from DeFi risks.</figcaption>
</figure>


In the gyroscopic design, the reserve is community-owned and supports the stablecoin through transparent on-chain rules, including putting proceeds from supply expansion toward the common good (e.g., toward maintaining stability vs. solely rewarding early adopters). The resulting game can be thought of as a game of communal insurance, which we suggest can be stable over much more flexible settings than existing non-custodial stability mechanisms. This flexibility also enables exciting future directions for this technology--e.g., the ability for arbitrary targets, including on-chain crypto-economy metrics vs. pegged USD exchange rate, and the ability for on-chain economic policy, including universal basic income ‘funded’ by a growing ecosystem through partially collateralized supply increases.

## The difference compared to current stablecoins

Currency peg mechanisms, of the nature described above, are notably absent from the non-custodial design space. Non-custodial stablecoins today mainly use very different mechanisms that set up different games and vulnerabilities. For instance, Dai and Synthetix work using leverage market mechanisms, which require demand for speculative leverage. Basis and Empty Set Dollar essentially work as leverage markets on near-future growth of their respective systems and require speculators to bet on an ever increasing level of demand. Both will commonly evaporate in times of crisis, as on Black Thursday, which risks the stablecoin’s collapse (we’ve explored this further [here](https://medium.com/coinmonks/insights-from-modeling-stablecoins-a30e732aef1b)). Among stablecoins today, the closest comparison is probably with Celo Dollars, which can be reinterpreted along the lines of a currency peg as described above (compared to seigniorage shares), but so far only in an ad hoc way.

In addition to creating new stablecoins based on gyroscopic mechanisms, we also suggest that existing designs can benefit from their use as complementary stability mechanisms. For instance, when Dai is trading above target when demand for speculative leverage evaporates, a gyroscopic mechanism could provide the functionality to mint new Dai in exchange for a dollar’s worth of a particular portfolio that funds a gyroscopic buffer. This would provide greater flexibility to Dai and increase its attractiveness as a leveraging market (Dai’s primary mechanism) as speculators will know that they can deleverage at the expected Dai price during crises.

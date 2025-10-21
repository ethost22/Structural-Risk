# Structural Risk – Summary Report
This project produces Monte Carlo simulations of expected value (EV) versus expected growth rate (EGR) investment strategies; this work expands upon an earlier paper in decision theory and environmental policy (Osterman 2025, the "technical report" in the repository), putting it in a computational context.

## Background:

Longtermism is a philosophical position emerging from the tradition of classical utilitarianism, effective altruism, and contemporary rationalist communities. It is broadly committed to maximizing “total value” in the universe in the long term, often through the implementation of speculative technologies such as artificial general intelligence. In recent years, longtermist ideas have had an increasing influence on policy, particularly through their uptake by technology and investment leaders in Silicon Valley (cf. Godfrey-Smith 2022; Torres 2024).

Longtermists are optimistic about technological progress and comparatively unconcerned about environmental degradation (cf. Read and Torres 2023). In a longer technical report (Osterman 2025), I examine the mathematical formalism underlying longtermist policy reasoning—the expected value (EV) framework—and argue that it is inadequate for the kinds of policy evaluations which longtermists want to make. The discussion begins with the observation (dating back to Bernoulli circa 1713) that (naïve) EV calculations lead to paradoxical prescriptions: for instance, EV calculations recommend taking gambles with negligible probabilities of success given that the potential payoffs are sufficiently large, despite the fact that gambles of this kind are ruinous (they incur too much “structural risk”) in the long run.

As an alternative, I propose the use of the Kelly criterion, or expected growth rate (EGR) strategy, a formalism derived from information theory and later applied to gambling theory and financial mathematics (cf. Thorp 2006). Unlike EV maximization, the EGR strategy dampens shocks from undesirable outcomes, ensuring long-run survival at the cost of forfeiting maximum short-term expectation. Under this model, many longtermist-style policies—particularly those that trade immediate environmental stability for speculative future payoffs—are shown to simply be mathematically unsound investment strategies which (ironically) fail to adequately account for the long run over which their investments must develop.

## Computational Implementation:

The accompanying code implements a Monte Carlo simulation comparing the expected value (EV) and expected growth rate (EGR) strategies over repeated stochastic rounds of investment. Two simulated agents begin with identical portfolios and face sequential investment opportunities defined by:

•	upside, the potential gain multiplier,

•	downside, the potential loss multiplier, and

•	p the probability of success.

Player 1 invests according to EV maximization (all-in when the edge is positive, since EV increases linearly with proportion invested when edge > 0, and 0 otherwise); Player 2 invests according to EGR optimization (proportionally to the edge afforded to the player, bounded between 0 and 1). Player portfolios are updated each round according to the outcome of the gamble. The game terminates when one or more players goes bankrupt or after 200 rounds of play have transpired. Various risk-averse (‘clamp”) parameters are tested, which specify a fraction of the initial recommendation to invest. Using Monte Carlo methods, the simulation is repeated 10,000 times per parameter value in order to estimate the average terminal portfolio value for each strategy. 

## Results:

A characteristic output of the model is shown below:

<img width="651" height="247" alt="Screenshot 2025-10-21 at 2 45 15 AM" src="https://github.com/user-attachments/assets/329f607c-5b98-4a62-8678-484051d6c9d1" />

Figure 1: characteristic output of the simulation for EV and EGR strategies. Average EV portfolio value approaches 0 as the clamp parameter approaches 1 (i.e., as we relax precautionary or conservative safeguards against risk).

Across all experimental conditions, we note the following:

•	The expected value (EV) strategy proves to be excessively risk-seeking and repeatedly courts ruination, converging toward an average portfolio value of 0 as conservative adjustments (in the form of the clamp parameter) are minimized.

•	The expected growth rate (EGR) strategy consistently outperforms EV, maintaining positive long-run growth.

•	When “clamped” (i.e., constrained to invest a fixed fraction of the recommended amount), EV performance improves but never surpasses EGR (for the same clamp value). In the context of the model, a “clamped” or “fractional” EGR strategy of about 0.7 appears to maximize long-term portfolio value across stochastic regimes (round types).

## Discussion:

The simulation corroborates the theoretical analysis in Osterman 2025: maximizing expected value prioritizes short-term upside at the cost of structural fragility, while maximizing the expected growth rate produces robust, sustainable outcomes over time. Consider, for example, Figure 2 below:

![Figure 2](https://github.com/user-attachments/assets/46bfb46f-ba6a-45f6-abc4-cbd1d1af411d)

Figure 2: a characteristic graphical output of one run of the simulation. 

In the first few rounds of play, although the players have an edge, enticing both to make an investment, it does not pay off; both players consistently incur losses until ~ t = 7. By investing proportional to the edge, however, the EGR strategy dampens the shock to its portfolio, leaving it with greater resources going forward. The EV strategy, making no such adjustment, quickly fritters away its portfolio, leaving it to oscillate around some low value from which it is unable to recover. It eventually depletes its resources entirely, ending the simulation. Note that clamp here = 0.6—a conservative adjustment to both strategies.

Figure 3 provides another interesting example of the instability of EV:

![Plot](https://github.com/user-attachments/assets/cc3bcaa5-e7af-44e2-9464-06ea0510003e)

Figure 3: 6 subplots for clamp parameters = [0.5, 0.6, 0.7, 0.8, 0.9, 1.0]

In the case where clamp = 1.0 (i.e., no conservative adjustment) EV quickly takes the lead over EGR; EGR dampens both negative shocks and short term gains, meaning that, in the event that both strategies win multiple rounds to start, EV will generically outperform EGR. But just as quickly as resources are won by EV, they are lost again. Similar behavior can be seen for clamp = 0.7, 0.8 above. EV is thus shown to be, once again, a remarkably volatile strategy; short term success of the strategy is no predictor of stability, and so strategies of this kind are unsuitable for long run, future-facing policy.

## Works Cited:

Godfrey-Smith, Peter: Is Longtermism Such a Big Deal? (2022)

Osterman, Ethan: Structural Risk: Decision Theory in the Long Run (preprint 2025)

Read and Torres: Radical Longtermism and the Seduction of Endless Growth (2023)

Thorp, Edward: The Kelly Criterion in Blackjack, Sports Betting, and the Stock Market (2006)

Torres, Émile: Go West, Weird Man (2024)



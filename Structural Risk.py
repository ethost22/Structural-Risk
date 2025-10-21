#The aim of this project is to implement some ideas in a previous technical report computationally.
#Namely, it presents two investment strategies; expected value and expected growth rate (the "Kelly strategy")
#and observes how they develop over time. The application of this simple technical result to
#environmental policy is developed at length in the aforementioned report.

#The simulation occurs over multiple rounds of play. Player 1 invests to maximize the expected value,
#while Player 2 invests to maximize the expected growth rate. Each player chooses a percentage of their
#portfolio to invest in the current round.

import random
import matplotlib.pyplot as plt
import timeit
import csv

def edge(upside, downside, p):
    #Simple calculation of "edge" in the procedure. The equation is derived by
    #setting p * upside - (1-p) * downside = 0
    return (p / downside) - ((1-p) / upside)

#defining the two strategies
#EXPECTED VALUE:
def ev(upside, downside, p):
    #the expected value of an investment is given by f(d) = p(1+d) + (1-p)(1-d)
    #i.e., the weighted sum of the fractional increase to the player's portfolio
    #on a win (as represented by the first term) and the fractional decrease to the
    #player's portfolio on a loss (as represented by the second term).

    #Because the function is linear wrt d, expected value is maximized in one of two ways:
    # 1) if the player has an edge (p > 0.5), set d to 1, i.e., "all in".
    # 2) if the house has an edge (p < 0.5), set d to 0, i.e., invest nothing.

    e = edge(upside, downside, p)
    frac = 0
    if e > 0:
        frac = 1
    return frac

#EXPECTED GROWTH RATE:
def egr(upside, downside, p):
    #The Kelly strategy is equivalent to betting proportionally to the "edge" afforded
    #to the player. A longer discussion and derivation of the relevant math is given
    #in my paper "Structural Risk"
    e = edge(upside, downside, p)
    frac = e
    if e > 1:
        frac = 1
    elif e < 0:
        frac = 0
    return frac

#defining each round of play
def sim_round():
    #every round has a random risk profile, which the gambler is
    #assumed to have perfect knowledge of.
    #Upsides are bounded from simple doubling to a 5x ROI
    upside = random.uniform(1, 2)
    downside = random.random()
    #throttle the minimal downside to 0.1 to avoid divide by zero / exponentiation
    if downside < 0.1:
        downside = 0.1
    #the probability of a win is determined randomly
    p = random.random()

    return upside, downside, p

def sim_round_static():
    #for convenience, rounds can also be deterministic
    return 2, 1, 0.6

def sim_round_dynamic():
    #another alternative round structure, with static downsides and
    #random upsides and win probability. p is bounded on [0.2, 0.8]
    upside = random.uniform(1, 5)
    downside = 1
    p = random.random()
    if p < 0.2:
        p = 0.2
    elif p > 0.8:
        p = 0.8
    return upside, downside, p

def visualize(P1, P2, t):
    #a simple function to plot a visualization of two strategies' portfolios over time
    plt.plot( t, P1, label = "expected value strategy")
    plt.plot(t, P2, label = "expected growth rate strategy")
    plt.legend()
    plt.xlabel("Time")
    plt.ylabel("Portfolio Value")
    plt.title("Two Investment Strategies wrt Time")
    plt.show()
    return

def vis_suplots(m, clamp):
    #a function to plot multiple subplots at different clamp values
    n = len(m)

    for i in range(0, n):
        font1 = {'family': 'serif', 'color': 'black', 'size': 8}
        plt.rc('font', size=5)
        plt.subplot(2, 3, i+1)
        plt.plot(m[i][2], m[i][0], label = "EV")
        plt.plot(m[i][2], m[i][1], label = "EGR")
        plt.xlabel("T")
        plt.ylabel("V")
        plt.title(f"Clamp: {clamp[i]}", fontdict = font1, loc="left")
        plt.yticks(rotation=75)
    plt.legend(loc='upper right', bbox_to_anchor=(1, -0.2), ncols=2)
    plt.tight_layout(pad=1.0)
    plt.show()

def round_select(n):
    #a simple function which takes an integer and returns one of three round types
    if n == 0:
        return sim_round()
    elif n == 1:
        return sim_round_static()
    elif n == 2:
        return sim_round_dynamic()
    return

#the code for a single trial, in which player portfolio over time is tracked
def single_trial(n = 0, clamp = 0.8):

    #initializing player portfolios. Pn_report was used for bug fixing.
    #Pn_portfolio stores consecutive portfolio values for a given strategy,
    #allowing for graphical visualization
    P1_current = 200
    P2_current = 200
    time_current = 0
    P1_portfolio = [P1_current]
    P2_portfolio = [P2_current]
    time_sequence = [time_current]
    #P1_report = []
    #P2_report = []

    #keep playing until somebody is bankrupt
    check = True
    count = 0

    while check == True:
        #determining the character of the investment for the given round in accordance
        #with the round type, as determined by the round_select() function
        w, l, p = round_select(n)

        #in order to allow the simulation to run for a bit, clamp
        #player investments to a fraction of the actual suggestion
        #This is a conservative strategy which minimizes risk of
        #immediate ruin. Setting the clamp to ~ 0.8 allows for
        #a good number of rounds before extinction.
        P1_invest = P1_current * ev(w, l, p) * clamp
        P2_invest = P2_current * egr(w, l, p) * clamp
        #P1_report.append(ev(w, l, p))
        #P2_report.append(egr(w, l, p))

        #Determining the outcome of the investment
        diceroll = random.random()

        #we check to see the outcome of our investment; if diceroll is below
        #the probability threshold, we have a win. Otherwise we have a loss.
        if diceroll < p:
            P1_current += P1_invest
            P2_current += P2_invest
        else:
            P1_current -= P1_invest
            P2_current -= P2_invest

        #Adding the resulting portfolio values to our running tally; plus
        #updating the time sequence. Note that the list.append() method
        #is computationally expensive; it would be worth rewriting using
        #different methods. A preliminary attempt to optimize by
        #preallocating list sizes of 200 proves to be almost two simes slower
        #(~26 seconds rather than ~16), presumably because this
        #necessitated 200 "turns" for each game, whereas in the .append()
        #version, we are able to stop the simulation as soon as one
        #of the strategies runs out of resources.
        P1_portfolio.append(P1_current)
        P2_portfolio.append(P2_current)
        time_current += 1
        time_sequence.append(time_current)

        #We end the simulation when the remaining portfolio of one or more strategies
        #is vanishingly small, i.e., less than 1.
        #This is because the clamp parameters makes it such that a decayed portfolio
        #approaches 0 asymptotically, since it can never be allowed to invest *all*
        #of its contents.
        if P1_current < 1 or P2_current < 1:
            check = False
        elif count > 200:
            check = False

        count += 1

    #print(P1_report, P2_report)
    return (P1_portfolio, P2_portfolio, time_sequence)

def repeatable_trial(n = 0, clamp = 0.8):
    #This is essentially the same as single_trial(), but removes the
    #list appendices, since in the context of the full Monte Carlo simulation, all
    #that we are concerned with is the final result of each run. This should
    #increase computational efficiency marginally.

    #initializing portfolios
    P1_portfolio = 200
    P2_portfolio = 200

    check = True
    count = 0

    while check == True:
        #generating round parameters
        w, l, p = round_select(n)

        #determining investment values
        P1_invest = P1_portfolio * ev(w, l, p) * clamp
        P2_invest = P2_portfolio * egr(w, l, p) * clamp

        #determining outcome
        diceroll = random.random()

        # we check to see the outcome of our investment; if diceroll is below
        # the probability threshold, we have a win. Otherwise we have a loss.
        if diceroll < p:
            P1_portfolio += P1_invest
            P2_portfolio += P2_invest
        else:
            P1_portfolio -= P1_invest
            P2_portfolio -= P2_invest

        if P1_portfolio < 1 or P2_portfolio < 1:
            check = False
        elif count > 200:
            check = False

        count += 1

    return [P1_portfolio, P2_portfolio]


def monte_carlo(n=0, clamp = 0.8):
    #Monte Carlo methods can be used to get a statistical approximation of the average
    #result of a given strategy (ev vs. egr). We do this by keeping a running total
    #of final portfolio values across trials and summing them, with an eye towards
    #generating an average.
    P1_final = 0
    P2_final = 0
    N = 10000

    for i in range(0, N):
        #grab the final value for each strategy and add it to a running total
        temp = repeatable_trial(n, clamp)
        P1_final += temp[0]
        P2_final += temp[1]

    #we report the average final value for each strategy
    #by dividing the sum of all final values by the number
    #of runs, here represented as N.
    return P1_final / N, P2_final / N

def clamp_iteration(low = 2, high = 10):
    #We can gather data for each clamp parameter and round type
    #into a three-dimensional matrix of
    # 1) parameter value
    # 2) ev average result, and
    # 3) egr average result
    #For all three round types; hence a list of three matrices,
    #each composed of three rows (sublists)
    matrix = [[[],[],[]],[[],[],[]],[[],[],[]]]
    for i in range(0, 3):
        for j in range(low, high):
            clamp = j * 0.1
            temp = monte_carlo(i, clamp)
            matrix[i][0].append(clamp)
            matrix[i][1].append(temp[0])
            matrix[i][2].append(temp[1])
    return matrix

def print_matrix(low = 2, high = 10):
    #a function to print out the data in a more easily readable format
    out = clamp_iteration(low, high)
    #first layer: compiling data by round type
    for i in range(0, 3):
        print(f"Type {i} Results:")
        #second layer: rows per type
        for j in range(0, 3):
            data_type = ["clamp", "ev", "egr"]
            temp = out[i][j]
            temp2 = []

            for k in range(0, len(temp)):
                #converting the values to scientific notation (for the portfolios)
                #or 1 decimal point (for the clamp parameters)
                if j > 0:
                    temp2.append("{:.2e}".format(temp[k]))
                else:
                    temp2.append("{:.1f}".format(temp[k]))
            #outputs the row header along with the data in the row
            print(f"{data_type[j]}: {temp2}")
        print()
    return

def matrix_as_csv(low = 2, high = 10):
    #an alternate method to output the data as a csv file
    #out is set to the matrix output of our "clamp" parameter sweep
    out = clamp_iteration(low, high)
    #we want to put the data into a "cleaned" matrix with the data
    #processed in scientific notation, and removing the redundant
    #instances of the clamp parameters.
    #note that matrix = [[[], [], []], [[], [], []], [[], [], []]]
    cleaned = [[[],[]],[[],[]],[[],[]]]

    #processing the data into scientfic notation
    for i in range(0, 3):
        for j in range(1, 3):
            #we need to grab the EV and EGR data for each round type
            #and convert it into scientific notation
            for k in range(0, len(out[i][j])):
                out[i][j][k] = "{:.2e}".format(out[i][j][k])
            #we need to adjust the j value by -1 since the cleaned
            #matrix has removed the first row, which stored the 
            #clamp values.
            cleaned[i][j-1] = out[i][j]

    with open("monte_carlo_risk.csv", "w", newline = "") as csvfile:
        writer = csv.writer(csvfile)
        #the first row is our clamp parameters, which are constant across
        #all stochastic regimes
        for i in range(0, len(out[0][0])):
            out[0][0][i] = "{:.1f}".format(out[0][0][i])
        writer.writerow(["clamp"] + out[0][0])
        for i in range(0, 3):
            #having written out our clamp parameters, we need to output the
            #simulation data
            writer.writerow([f"EV type {i}"] + cleaned[i][0])
            writer.writerow([f"EGR type {i}"] + cleaned[i][1])

    return

def main():
    #outputs a set of graphs as well as a matrix of results for both strategies
    #under various clamp parameters and under different round paradigms.
    # Key finding: as clamp parameter approaches 1 (i.e., minimally conservative
    # adjustment against risk of ruin), ev approaches 0, whereas egr does not)
    #the following two lines run one round and print a graph
    to_plot = []
    for i in range(5, 11):
        temp = single_trial(2, i * 0.1)
        to_plot.append(temp)
    vis_suplots(to_plot, [0.5, 0.6, 0.7, 0.8, 0.9, 1.0])

    #The following line packages the simulation across various clamp parameter values.
    #One easy way to save some computation time is to just choose a  lower
    #bound greater than 2. The lower clamp values are particularly expensive because
    #neither strategy is likely to terminate within the relevant time-frame,
    #necessitating the maximum 200 turns per round each time.
    #e.g., using (6, 10) here instead of the default (2, 10) takes only ~3 seconds
    #as compared with ~16. (7, 10) takes ~1.5 seconds. (8, 10) takes under a second.
    #print_matrix(6, 11)

    #the following line reports as a CSV
    matrix_as_csv(6, 11)
    return

if __name__ == "__main__":
    #packaging the code into a single main() function; includes
    #runtime tracking for purposes of further optimization.
    #deterministic seed for repeatability
    random.seed(0)
    start = timeit.default_timer()
    main()
    stop = timeit.default_timer()
    print(f"Runtime: {stop - start}")

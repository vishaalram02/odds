const computeBets = (numPlayers: number, bookOdds: Array<number>, trueOdds: Array<number>, dividend: number) => {
    const revenueRates = Array(numPlayers).fill(0).map((_, i) => [dividend * trueOdds[i] / bookOdds[i], i]);
    revenueRates.sort((a, b) => b[0] - a[0]);

    let bets: Array<number> = Array(numPlayers).fill(0);
    let reserve = 1;

    for(let i = 0; i < numPlayers; i++) {
        let revenueRate = revenueRates[i][0];
        let player = revenueRates[i][1];

        if (revenueRate < reserve) break;

        bets[player] = 1;

        const A = trueOdds.filter((_, i) => !bets[i]).reduce((a, b) => a + b, 0);
        const B = bookOdds.filter((_, i) => bets[i]).reduce((a, b) => a + b, 0);

        reserve = dividend * A / (dividend - B);
    }

    
    for(let i = 0; i < numPlayers; i++) {
        if(bets[i] === 0) continue;

        const A = trueOdds.filter((_, i) => !bets[i]).reduce((a, b) => a + b, 0);
        const B = bookOdds.filter((_, i) => bets[i]).reduce((a, b) => a + b, 0);

        bets[i] = trueOdds[i] - bookOdds[i] * A / (dividend - B);
    }

    return bets;
}

const test = () => {
    const numPlayers = 7;
    const trueOdds = [
        0.003247, // Horse 1
        0.003247, // Horse 2
        0.003247, // Horse 3
        0.01623,  // Horse 4
        0.2273,   // Horse 5
        0.1623,   // Horse 6
        0.5844    // Horse 7
    ];

    const bookOdds = [
        0.025,    // Horse 1
        0.0375,   // Horse 2
        0.0625,   // Horse 3
        0.125,    // Horse 4
        0.25,     // Horse 5
        0.3125,   // Horse 6
        0.1875    // Horse 7
    ];

    const dividend = 0.8;

    const bets = computeBets(numPlayers, bookOdds, trueOdds, dividend);
    console.log(bets);
}

test();
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

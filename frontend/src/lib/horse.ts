export const computeBets = (
	numPlayers: number,
	trueOdds: Array<number>,
	bookOdds: Array<number>,
	dividend: number
) => {

    const calcRevenue = (trueOdds: number, bookOdds: number) => {
        if(trueOdds === 0) return 0;
        if(bookOdds === 0) return 0;
        return (dividend * trueOdds) / bookOdds;
    }

	const revenueRates = Array(numPlayers)
		.fill(0)
		.map((_, i) => [calcRevenue(trueOdds[i], bookOdds[i]), i]);
	revenueRates.sort((a, b) => b[0] - a[0]);

	const bets: Array<number> = Array(numPlayers).fill(0);
    const horses = new Set<number>();
	let reserve = 1;

	for (let i = 0; i < numPlayers; i++) {
		const revenueRate = revenueRates[i][0];
		const player = revenueRates[i][1];

		if (revenueRate <= reserve) break;

        horses.add(player);

		const A = trueOdds.filter((_, i) => !horses.has(i)).reduce((a, b) => a + b, 0);
		const B = bookOdds.filter((_, i) => horses.has(i)).reduce((a, b) => a + b, 0);

		reserve = (dividend * A) / (dividend - B);
	}

	for (let i = 0; i < numPlayers; i++) {
		if (!horses.has(i)) continue;

		const A = trueOdds.filter((_, i) => !horses.has(i)).reduce((a, b) => a + b, 0);
		const B = bookOdds.filter((_, i) => horses.has(i)).reduce((a, b) => a + b, 0);

		bets[i] = trueOdds[i] - (bookOdds[i] * A) / (dividend - B);
	}

	return bets;
};

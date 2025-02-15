<script lang="ts">
    import {
        BOOK_LIST,
        type GameData
    } from "$lib";
    import { computeBets } from "$lib/horse";
    export let game: GameData;
    export let modifyMGM: boolean;

    let fairBook = "draftkings";
    let targetBook = "betmgm";
    let bankRoll = 25000;
    const TIME_OFFSET = 3600 * 2;

    let bookEdges: Record<string, number> = {};
    let impliedProbs: Record<string, Record<string, number>> = {};
    let filteredOdds: Array<{player: string, odds: Record<string, number>}> = [];
    let latestOdds: Array<{player: string, odds: Record<string, number>}> = [];
    let betValues: Array<number> = [];
    let scaledBets: Array<number> = [];

    const impliedProb = (odds: number) => {
        return 100 / (odds + 100);
    }

    const computeTableData = (modifyMGM: boolean, fairBook: string, targetBook: string) => {
        const currentTime = Math.floor(Date.now() / 1000);
        const cutoffTime = Math.min(currentTime, game.commence_time - TIME_OFFSET);
        
        const latestHistory = game.first_basket
            .filter(h => h.timestamp <= cutoffTime)
            .sort((a, b) => b.timestamp - a.timestamp)[0];
        
        if (!latestHistory) return [];

        latestOdds = [];
        for(const player of game.players) {
            const playerOdds: Record<string, number> = {};
            for(const [book, odds] of Object.entries(latestHistory.odds)) {
                let adjustedOdds = odds[player];
                if (modifyMGM && book === 'betmgm' && adjustedOdds) {
                    const newImpliedProbability = 1 + adjustedOdds / 200 - Math.sqrt(adjustedOdds ** 2 + 400 * adjustedOdds) / 200;
                    adjustedOdds = 100 / newImpliedProbability - 100;
                }
                playerOdds[book] = Math.round(adjustedOdds);
            }
            latestOdds.push({player, odds: playerOdds});
        }

        bookEdges = getBookEdges();
        impliedProbs = getImpliedProbs();
        filteredOdds = latestOdds.filter(player => 
            player.odds[fairBook] || player.odds[targetBook]
        ); 
        betValues = computeBetValues(targetBook);
        scaledBets = betValues.map(bet => Math.round(bet * bankRoll));
    }

    $: computeTableData(modifyMGM, fairBook, targetBook);

    const getBookEdges = () => {
        const bookEdges: Record<string, number> = {};
        for(const book of BOOK_LIST) {
            bookEdges[book] = latestOdds.reduce((acc, player) => acc + (player.odds[book] ? impliedProb(player.odds[book]) : 0), 0);
        }
        return bookEdges;
    }

    const getImpliedProbs = () => {
        const impliedProbs: Record<string, Record<string, number>> = {};
        for(const book of BOOK_LIST) {
            impliedProbs[book] = {};
            for(const player of latestOdds) {
                impliedProbs[book][player.player] = player.odds[book] ? impliedProb(player.odds[book]) / bookEdges[book] : 0;
            }
        }
        return impliedProbs;
    }

    const computeBetValues = (targetBook: string) => {
        const fairOdds = filteredOdds.map(player => impliedProbs[fairBook][player.player] || 0);
        const targetOdds = filteredOdds.map(player => impliedProbs[targetBook][player.player] || 0);

        return computeBets(filteredOdds.length, fairOdds, targetOdds, 1 / bookEdges[targetBook]);
    }

</script>

<div class="controls">
    <label>
        Bank Roll: $
        <input 
            type="number" 
            bind:value={bankRoll}
            min="0"
            step="100"
        />
    </label>
    <div>
        Fair Edge: {Math.round(bookEdges[fairBook] * 100 - 100)}%
    </div>
    <div>
        Target Edge: {Math.round(bookEdges[targetBook] * 100 - 100)}%
    </div>
</div>

<table>
    <thead>
        <tr>
            <th>Player</th>
            <th colspan="1">
                <select bind:value={fairBook}>
                    {#each BOOK_LIST as book}
                        <option value={book}>{book}</option>
                    {/each}
                </select>
            </th>
            <th>Implied</th>
            <th colspan="1">
                <select bind:value={targetBook}>
                    {#each BOOK_LIST as book}
                        <option value={book}>{book}</option>
                    {/each}
                </select>
            </th>
            <th>Implied</th>
            <th>Bet Size</th>
        </tr>
    </thead>
    <tbody>
        {#each filteredOdds as {player, odds}, i}
            {@const fairOdds = odds[fairBook] || 0}
            {@const targetOdds = odds[targetBook] || 0}
            <tr>
                <td>{player}</td>
                <td class="odds">{fairOdds ? (fairOdds > 0 ? '+' : '') + fairOdds : '-'}</td>
                <td>{fairOdds > 0 ? Math.round(impliedProbs[fairBook][player] * 1000) / 10 + '%' : '-'}</td>
                <td class="odds">{targetOdds ? (targetOdds > 0 ? '+' : '') + targetOdds : '-'}</td>
                <td>{targetOdds > 0 ? Math.round(impliedProbs[targetBook][player] * 1000) / 10 + '%' : '-'}</td>
                <td>${scaledBets[i]}</td>
            </tr>
        {/each}
    </tbody>
</table>

<style>
    select {
        padding: 0.25rem;
        border-radius: 4px;
    }

    table {
        width: 100%;
        border-collapse: collapse;
        margin-top: 1rem;
        font-size: 0.9rem;
    }

    th, td {
        padding: 0.5rem;
        text-align: left;
        border-bottom: 1px solid #ddd;
    }

    th {
        background-color: #f5f5f5;
    }

    th select {
        width: 100%;
        padding: 0.25rem;
        border-radius: 4px;
        border: 1px solid #ddd;
    }

    .odds {
        font-family: monospace;
        font-weight: bold;
    }

    .controls {
        margin-top: 3rem;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 1rem;
    }
    
    input {
        padding: 0.25rem;
        border-radius: 4px;
        border: 1px solid #ddd;
        width: 120px;
    }
    
    label {
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
</style>
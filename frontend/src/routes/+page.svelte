<script lang="ts">
    import { onMount } from "svelte";
    import type { GameData, PlayerChartData } from "$lib";
    import PlayerChart from "../components/PlayerChart.svelte";

    const date = "2025-02-05"
    let gameData: GameData[] = [];
    let selectedGame: GameData | null = null;
    let selectedPlayer: string | null = null;

    // Function to get the most recent odds for each player from each sportsbook
    function getLatestOdds(game: GameData): Array<{player: string, odds: Record<string, number>}> {
        const latestHistory = game.first_basket[game.first_basket.length - 1];

        const latestOdds: Array<{player: string, odds: Record<string, number>}> = [];
        for(const player of game.players) {
            const playerOdds: Record<string, number> = {};
            for(const [book, odds] of Object.entries(latestHistory.odds)) {
                playerOdds[book] = odds[player];
            }
            latestOdds.push({player, odds: playerOdds});
        }
        return latestOdds;
    }

    // Function to get historical odds data for a specific player
    function getPlayerHistory(game: GameData, player: string) {
        const playerHistory: PlayerChartData[] = [];
        for (const history of game.first_basket) {
            const date = new Date(history.timestamp * 1000);
            const bookOdds: Record<string, number> = {};
            for (const [book, odds] of Object.entries(history.odds)) {
                bookOdds[book] = odds[player];
            }
            playerHistory.push({
                date,
                odds: bookOdds
            });
        }
        return playerHistory;
    }

    onMount(() => {
        fetch(`/api/first-basket?date=${date}`)
            .then(res => res.json())
            .then(data => {
                for (const entry of Object.entries(data)) {
                    const [id, game]: [string, any] = entry;
                    const currentGame: GameData = {
                        id: id,
                        home_team: game.home_team,
                        away_team: game.away_team,
                        players: new Set(),
                        first_basket: game.first_basket,
                    }
                    for (const history of currentGame.first_basket) {
                        for (const odds of Object.values(history.odds)) {
                            for (const player of Object.keys(odds)) {
                                currentGame.players.add(player);
                            }
                        }
                    }
                    gameData.push(currentGame);
                }
                if (gameData.length > 0) {
                    selectedGame = gameData[0];
                }
                gameData = [...gameData];
            });
    });

    $: chartData = selectedGame && selectedPlayer ? getPlayerHistory(selectedGame, selectedPlayer) : [];
    $: latestOdds = selectedGame ? getLatestOdds(selectedGame) : [];

</script>

<div class="container mx-auto p-4">
    {#if gameData.length > 0}
        <div class="mb-6">
            <!-- svelte-ignore a11y_label_has_associated_control -->
            <label class="block text-sm font-medium mb-2">Select Game:</label>
            <select 
                class="w-full p-2 border rounded"
                bind:value={selectedGame}
            >
                {#each gameData as game}
                    <option value={game}>
                        {game.away_team} @ {game.home_team}
                    </option>
                {/each}
            </select>
        </div>

        {#if selectedGame}
            <div class="mb-6">
                <!-- svelte-ignore a11y_label_has_associated_control -->
                <label class="block text-sm font-medium mb-2">Select Player:</label>
                <select 
                    class="w-full p-2 border rounded"
                    bind:value={selectedPlayer}
                >
                    <option value={null}>Select a player...</option>
                    {#each Array.from(selectedGame.players) as player}
                        <option value={player}>{player}</option>
                    {/each}
                </select>
            </div>

            {#if selectedPlayer && chartData.length > 0}
                <div class="mb-6">
                    <h2 class="text-xl font-bold mb-4">Odds History for {selectedPlayer}</h2>
                    <div class="h-[400px]">
                        <PlayerChart chartData={chartData} />
                    </div>
                </div>
            {/if}

            <div class="mb-6">
                <h2 class="text-xl font-bold mb-4">Latest Odds</h2>
                <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                    {#each latestOdds as {player, odds}}
                        <div class="border rounded p-4">
                            <h3 class="font-bold mb-2">{player}</h3>
                            <div class="space-y-1">
                                {#each Object.entries(odds) as [book, odd]}
                                    <div class="flex justify-between">
                                        <span>{book}:</span>
                                        <span>{odd}</span>
                                    </div>
                                {/each}
                            </div>
                        </div>
                    {/each}
                </div>
            </div>
        {/if}
    {:else}
        <p>Loading...</p>
    {/if}
</div>

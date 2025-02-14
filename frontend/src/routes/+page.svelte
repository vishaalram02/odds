<script lang="ts">
    import { onMount } from "svelte";
    import type { GameData, PlayerChartData } from "$lib";
    import PlayerChart from "../components/PlayerChart.svelte";

    // Function to generate date options (7 days including today)
    function getDateOptions(): string[] {
        const dates: string[] = [];
        // Create date in EST/EDT
        const today = new Date(new Date().toLocaleString("en-US", { timeZone: "America/New_York" }));

        for (let i = 0; i < 7; i++) {
            const date = new Date(today);
            date.setDate(date.getDate() - i);
            const formattedDate = date.toISOString().split('T')[0];
            dates.push(formattedDate);
        }
        return dates;
    }

    const dateOptions = getDateOptions();
    console.log(dateOptions)
    const today = dateOptions[0];
    let date: string | undefined = undefined;
    let gameData: GameData[] = [];
    let selectedGameId: string | null = null;
    let previousGameId: string | null = null;
    let selectedPlayer: string | null = null;

    // Helper to get current game
    $: currentGame = gameData.find(game => game.id === selectedGameId) || null;

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

    function handleKeydown(event: KeyboardEvent) {
        // Handle game switching with left/right arrows
        if (event.key === 'ArrowLeft' || event.key === 'ArrowRight') {
            event.preventDefault();
            if (gameData.length === 0) return;
            
            const currentIndex = gameData.findIndex(game => game.id === selectedGameId);
            if (currentIndex === -1) return;
            
            if (event.key === 'ArrowLeft') {
                const newIndex = currentIndex <= 0 ? gameData.length - 1 : currentIndex - 1;
                selectedGameId = gameData[newIndex].id;
            } else {
                const newIndex = currentIndex >= gameData.length - 1 ? 0 : currentIndex + 1;
                selectedGameId = gameData[newIndex].id;
            }
            return;
        }

        // Handle player switching with up/down arrows
        if (!currentGame || !Array.from(currentGame.players).length) return;
        
        const players = Array.from(currentGame.players);
        const currentIndex = selectedPlayer ? players.indexOf(selectedPlayer) : -1;
        
        if (event.key === 'ArrowUp') {
            event.preventDefault();
            const newIndex = currentIndex <= 0 ? players.length - 1 : currentIndex - 1;
            selectedPlayer = players[newIndex];
        } else if (event.key === 'ArrowDown') {
            event.preventDefault();
            const newIndex = currentIndex === players.length - 1 ? 0 : currentIndex + 1;
            selectedPlayer = players[newIndex];
        }
    }

    onMount(() => {
        fetchData();
    });

    $: if(date) {
        fetchData();
    }

    const fetchData = () => {
        fetch(`/api/first-basket?date=${date}`)
            .then(res => res.json())
            .then(data => {
                gameData = [];
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
                        selectedGameId = gameData[0].id;
                    }
                    gameData = [...gameData];
            });
    }

    $: chartData = currentGame && selectedPlayer ? getPlayerHistory(currentGame, selectedPlayer) : [];
    $: latestOdds = currentGame ? getLatestOdds(currentGame) : [];

    $: if(selectedGameId !== previousGameId) {
        previousGameId = selectedGameId;
        selectedPlayer = null;
    }

</script>

<svelte:window on:keydown={handleKeydown}/>

<div class="container mx-auto p-4">
    <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
        <div>
            <!-- svelte-ignore a11y_label_has_associated_control -->
            <label class="block text-sm font-medium mb-2">Select Date:</label>
            <select 
                class="w-full p-2 border rounded"
                bind:value={date}
            >
                {#each dateOptions as dateOption}
                    <option value={dateOption}>
                        {dateOption}
                    </option>
                {/each}
            </select>
        </div>

        {#if gameData.length > 0}
            <div>
                <!-- svelte-ignore a11y_label_has_associated_control -->
                <label class="block text-sm font-medium mb-2">Select Game:</label>
                <select 
                    class="w-full p-2 border rounded"
                    bind:value={selectedGameId}
                >
                    {#each gameData as game}
                        <option value={game.id}>
                            {game.away_team} @ {game.home_team}
                        </option>
                    {/each}
                </select>
            </div>

            {#if currentGame}
                <div>
                    <!-- svelte-ignore a11y_label_has_associated_control -->
                    <label class="block text-sm font-medium mb-2">Select Player:</label>
                    <select 
                        class="w-full p-2 border rounded"
                        bind:value={selectedPlayer}
                    >
                        <option value={null}>Select a player...</option>
                        {#each Array.from(currentGame.players) as player}
                            <option value={player}>{player}</option>
                        {/each}
                    </select>
                </div>
            {/if}
        {/if}
    </div>

    {#if selectedPlayer && chartData.length > 0}
        <div class="mb-6">
            <h2 class="text-xl font-bold mb-4">Odds History for {selectedPlayer}</h2>
            <div class="h-[400px]">
                {#key chartData}
                    <PlayerChart chartData={chartData} />
                {/key}
            </div>
        </div>
    {/if}

    {#if today === date && gameData.length > 0}
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
    {:else if gameData.length === 0}
        <div class="mb-6">
            <h2 class="text-xl font-bold mb-4">No games found for {date}</h2>
        </div>
    {/if}
</div>

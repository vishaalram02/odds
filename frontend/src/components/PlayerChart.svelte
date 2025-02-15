<script lang="ts">
	import {
		Chart as ChartJS,
		LineElement,
		PointElement,
		LinearScale,
		Title,
		Tooltip,
		Legend,
		CategoryScale,
        type ChartOptions,
        type ChartData
	} from 'chart.js';
    import type { PlayerChartData } from '$lib';
    import Line from "./Line.svelte"

    export let chartData: PlayerChartData[];
    export let modifyMGM: boolean;

	// Register necessary Chart.js components
	ChartJS.register(LineElement, PointElement, LinearScale, Title, Tooltip, Legend, CategoryScale);

    const books = ["draftkings", "betmgm", "fanduel", "bovada"]
    const colors = ["rgba(75,192,192,1)", "rgba(255,206,86,1)", "rgba(255,159,64,1)", "rgba(153,102,255,1)"]

    // Reactive data based on toggle
    $: data = {
        datasets: books.map((book, index) => ({
            label: book,
            data: chartData.map(data => {
                let odds = data.odds[book];
                // If toggle is on and it's MGM, add 2 to the odds
                if (modifyMGM && book === 'betmgm' && odds) {
					const newImpliedProbability = 1 + odds / 200 - Math.sqrt(odds ** 2 + 400 * odds) / 200
                    odds = 100 / newImpliedProbability - 100;
                }
                return {
                    x: data.date.toISOString(),
                    y: odds ?? null
                }
            }),
            borderColor: colors[index],
            fill: false,
            tension: 0.4,
            // Add strikethrough for MGM when toggle is on
            borderDash: modifyMGM && book === 'betmgm' ? [5, 5] : []
        }))
    } as unknown as ChartData<'line', number[], string>

	const options: ChartOptions<'line'> = {
		responsive: true,
		maintainAspectRatio: false,
		scales: {
			x: {
				type: 'time',
				time: {
					displayFormats: {
						hour: 'HH:mm'
					},
					unit: 'hour'
				}
			},
			y: { beginAtZero: true }
		}
	};
</script>

<div class="toggle-container">
    <label>
        <input type="checkbox" bind:checked={modifyMGM}>
        MGM Promo
    </label>
</div>

<Line {data} {options} />

<style>
    .toggle-container {
        margin-bottom: 1rem;
    }

    label {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        cursor: pointer;
    }

    input[type="checkbox"] {
        cursor: pointer;
    }
</style>

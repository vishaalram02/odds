<script lang="ts">
	import {
		Chart as ChartJS,
		LineElement,
		PointElement,
		LinearScale,
		Title,
		Tooltip,
		Legend,
		CategoryScale
	} from 'chart.js';
    import type { PlayerChartData } from '$lib';
    import Line from "./Line.svelte"

    export let chartData: PlayerChartData[];

	// Register necessary Chart.js components
	ChartJS.register(LineElement, PointElement, LinearScale, Title, Tooltip, Legend, CategoryScale);

    const books = ["draftkings", "betmgm", "fanduel", "bovada"]

    const data = {
        labels: chartData.map(data => data.date),
        datasets: books.map(book => ({
            label: book,
            data: chartData.map(data => {
                return {
                    x: data.date,
                    y: data.odds[book] ?? null
                }
            }),
            borderColor: 'rgba(75,192,192,1)',
            fill: false,
            tension: 0.4
        }))
    }

	

	// Chart options
	const options = {
		responsive: true,
		maintainAspectRatio: false,
		scales: {
			y: { beginAtZero: true }
		}
	};
</script>

<Line {data} {options} />

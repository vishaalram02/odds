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
    const colors = ["rgba(75,192,192,1)", "rgba(255,206,86,1)", "rgba(255,159,64,1)", "rgba(153,102,255,1)"]

    const data = {
        datasets: books.map((book, index) => ({
            label: book,
            data: chartData.map(data => {
                return {
                    x: data.date.toISOString(),
                    y: data.odds[book] ?? null
                }
            }),
            borderColor: colors[index],
            fill: false,
            tension: 0.4
        }))
    }

	const options = {
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

<Line {data} {options} />

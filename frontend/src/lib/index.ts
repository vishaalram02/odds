// place files you want to import through the `$lib` alias in this folder.


export interface PlayerChartData {
    date: Date
    odds: Record<string, number>
}

interface FirstBasketHistory {
    timestamp: number;
    odds: Record<string, Record<string, number>>;
}

export interface GameData {
    id: string;
    home_team: string;
    away_team: string;
    players: Set<string>;
    first_basket: Array<FirstBasketHistory>;
}
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
    commence_time: number;
}

export const BOOK_LIST = ["draftkings", "betmgm", "fanduel", "bovada", "betrivers"]

export function getDateOptions(): string[] {
    const dates: string[] = [];
    // Create date in EST/EDT
    const today = new Date(new Date().toLocaleString("en-US", { timeZone: "America/New_York" }));

    for (let i = 0; i < 10; i++) {
        const date = new Date(today);
        date.setDate(date.getDate() - i);
        const formattedDate = date.toISOString().split('T')[0];
        dates.push(formattedDate);
    }
    return dates;
}
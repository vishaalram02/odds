import { json } from '@sveltejs/kit';
import type { RequestHandler } from './$types';

const BACKEND_URL = "https://vishaalram02--first-basket-first-basket-web.modal.run";

export const GET: RequestHandler = async ({ url }) => {
    const date = url.searchParams.get('date');
    
    const response = await fetch(`${BACKEND_URL}?date=${date}`);
    const data = await response.json();
    
    return json(data);
};
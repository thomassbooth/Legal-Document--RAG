export async function getUserHistory(userId: number) {
    try {
        const response = await fetch(`http://${process.env.NEXT_PUBLIC_WEBSOCKET_URL as string || "localhost:8000"}/user-history/${userId}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
        });

        if (!response.ok) {
            throw new Error(`Error: ${response.status}`);
        }

        const data = await response.json();

        return data
        console.log(data);
    } catch (error) {
        console.error('Error fetching user history:', error);
    }
}
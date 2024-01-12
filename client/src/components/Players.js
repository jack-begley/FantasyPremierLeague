import axios from 'axios';
import React, { useEffect, useState } from 'react';

const Players = () => {
    const [playerData, setPlayerData] = useState(null);

    useEffect(() => {
        // replace 'surname' with the player's surname you're interested in
        const playerSurname = 'salah';
        // Issue is here: Some issue with the request - could be related to the response in my method in gameweekSummary.py but hard to tell.
        axios.get(`http://localhost:3000/playerinfo?surname=${playerSurname}`)
            .then(response => {
                setPlayerData(response.data);
                console.log('Response Headers:', JSON.stringify(response.headers, null, 2)); // Log response headers here
            })
            .catch(error => {
                if (error.response) {
                    // The request was made and the server responded with a status code
                    // that falls out of the range of 2xx
                    console.log("Data", error.response.data);
                    console.log("Status", error.response.status);
                    console.log("Headers", error.response.headers);
                } else if (error.request) {
                    // The request was made but no response was received
                    // `error.request` is an instance of XMLHttpRequest in the browser and an instance of
                    // http.ClientRequest in Node.js
                    console.log("Request", error.request);
                } else {
                    // Something happened in setting up the request that triggered an Error
                    console.log('Error', error.message);
                }
            });
    }, []);

    return (
        <div>
            {playerData && (
                <div>
                    {/* Display player data here */}
                    <p>{`Player name: ${playerData.first_name} ${playerData.second_name}`}</p>
                    <p>{`Form: ${playerData.form}`}</p>
                    {/* Add more data as needed */}
                </div>
            )}
        </div>
    );
};

export default Players;
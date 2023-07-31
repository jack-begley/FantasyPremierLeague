import axios from 'axios';
import React, { useEffect, useState } from 'react';

const Players = () => {
    const [playerData, setPlayerData] = useState(null);

    useEffect(() => {
        // replace 'surname' with the player's surname you're interested in
        const playerSurname = 'salah';
        axios.get(`http://localhost:5000/playerinfo?surname=${playerSurname}`)
            .then(response => {
                setPlayerData(response.data);
            })
            .catch(error => console.error(`Error: ${error}`));
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
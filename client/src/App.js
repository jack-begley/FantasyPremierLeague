import React, { useEffect, useState } from 'react';

function App() {
    const [message, setMessage] = useState('');

    useEffect(() => {
        fetch('/')
            .then(res => res.json())
            .then(data => setMessage(data.message));
    }, []);

    return (
        <div className="App">
            <header className="App-header">
                <div>Hello!</div>
                {message}
            </header>
        </div>
    );
}

export default App;
import React, { useEffect, useState } from 'react';
import { BrowserRouter as Router, Route, Routes, Link, useLocation } from 'react-router-dom';
import './App.css';
import Players from './components/Players.js';
import Team from './components/Team.js';
import Compare from './components/Compare.js';

const MobileMenu = ({ menuItems }) => {
    const [isMenuOpen, setIsMenuOpen] = useState(false);

    const handleMenuToggle = () => {
        setIsMenuOpen(!isMenuOpen);
    };

    return (
        <div className={`mobile-menu ${isMenuOpen ? 'open' : ''}`}>
            <div className={`menu-items ${isMenuOpen ? 'open' : ''}`}>
                <MenuListItem icon="person" label="Players" path="/players" />
                <MenuListItem icon="groups" label="Teams" path="/teams" />
                <MenuListItem icon="compare_arrows" label="Compare" path="/compare" />
            </div>
            <div className={`burger-icon ${isMenuOpen ? 'open' : ''}`} onClick={handleMenuToggle}>
                <div className="bar1"></div>
                <div className="bar2"></div>
                <div className="bar3"></div>
            </div>
        </div>
    );
};

const toSentenceCase = (str) => {
    return str.replace(/\b\w/g, (char) => char.toUpperCase());
};


const Breadcrumb = () => {
    const location = useLocation();
    const pathSegments = location.pathname.split('/').filter(Boolean);

    return (
        <div className="breadcrumb">
            {pathSegments.map((segment, index) => {
                const path = `/${pathSegments.slice(0, index + 1).join('/')}`;
                const label = toSentenceCase(segment.replace(/-/g, ' '));

                return (
                    <React.Fragment key={index}>
                        {index > 0 && <span className="breadcrumb-separator">{'>'}</span>}
                        {index === pathSegments.length - 1 ? (
                            <span className="breadcrumb-segment">{label}</span>
                        ) : (
                            <Link to={path} className="breadcrumb-link">
                                {label}
                            </Link>
                        )}
                    </React.Fragment>
                );
            })}
        </div>
    );
};

const MenuListItem = ({ icon, label, path }) => {
    const location = useLocation();

    return (
        <Link to={path} className={`listItem ${location.pathname === path ? 'active' : ''}`}>
            <i className="material-icons icons">{icon}</i>
            {label}
        </Link>
    );
};

function App() {
    const [pagecontent, setMessage] = useState('');

    useEffect(() => {
        fetch('/')
            .then(res => res.json())
            .then(data => setMessage(data.pagecontent));
    }, []);

    return (
        <Router>
            <div className="App">
                <header className="App-header headerContainer">
                    <img src="/logo.png" alt="Logo" className="logo" />
                    <nav className="desktop-menu">
                        <div className="list">
                            <MenuListItem icon="person" label="Players" path="/players" />
                            <MenuListItem icon="groups" label="Teams" path="/teams" />
                            <MenuListItem icon="compare_arrows" label="Compare" path="/compare" />
                        </div>
                    </nav>
                    <nav className="mobile-menu">
                        <MobileMenu />
                    </nav>
                </header>
                <Breadcrumb></Breadcrumb>
                <Routes>
                    <Route path="/players" element={<Players />} />
                    <Route path="/teams" element={<Team />} />
                    <Route path="/compare" element={<Compare />} />
                </Routes>
                <p>{pagecontent}</p>
            </div>
        </Router>
    );
}

export default App;




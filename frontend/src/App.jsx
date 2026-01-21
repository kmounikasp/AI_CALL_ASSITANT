import React, { useState, useEffect, useRef } from 'react';
import { Mic, Send, AlertCircle, ShoppingCart, MessageSquare, PieChart, Activity } from 'lucide-react';

const App = () => {
    const [messages, setMessages] = useState([]);
    const [sentiment, setSentiment] = useState('Neutral');
    const [suggestion, setSuggestion] = useState('Waiting for input...');
    const [keywords, setKeywords] = useState([]);
    const [recs, setRecs] = useState([]);
    const [inputText, setInputText] = useState('');
    const [isActive, setIsActive] = useState(false);
    const [isListening, setIsListening] = useState(false);
    const [summary, setSummary] = useState(null);
    const [sessionId] = useState(`session_${Math.floor(Math.random() * 10000)}`);

    const ws = useRef(null);
    const recognitionRef = useRef(null);

    useEffect(() => {
        // Initialize Web Speech API
        if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
            const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
            recognitionRef.current = new SpeechRecognition();
            recognitionRef.current.continuous = true;
            recognitionRef.current.interimResults = false;
            recognitionRef.current.lang = 'en-US';

            recognitionRef.current.onresult = (event) => {
                const transcript = event.results[event.results.length - 1][0].transcript;
                if (ws.current && ws.current.readyState === WebSocket.OPEN) {
                    ws.current.send(transcript);
                }
            };

            recognitionRef.current.onerror = (event) => {
                console.error("Speech Recognition Error", event.error);
                setIsListening(false);
            };

            recognitionRef.current.onend = () => {
                if (isListening) recognitionRef.current.start();
            };
        }
    }, [isListening]);

    const startCall = () => {
        setIsActive(true);
        setSummary(null);
        setMessages([]);
        ws.current = new WebSocket(`ws://localhost:8000/ws/audio/${sessionId}`);

        ws.current.onmessage = (event) => {
            const data = JSON.parse(event.data);
            if (data.transcript) {
                setMessages(prev => [...prev.slice(-10), data.transcript]);
                setSentiment(data.sentiment);
                setSuggestion(data.suggestion);
                setKeywords(prev => Array.from(new Set([...prev, ...data.keywords])));
                setRecs(data.recommendations);
            }
        };
    };

    const endCall = async () => {
        if (ws.current) ws.current.close();
        if (recognitionRef.current) recognitionRef.current.stop();
        setIsActive(false);
        setIsListening(false);

        // Fetch Summary
        try {
            const resp = await fetch(`http://localhost:8000/call/${sessionId}/summary`);
            const data = await resp.json();
            setSummary(data.summary);
        } catch (err) {
            console.error("Failed to fetch summary", err);
        }
    };

    const sendMessage = () => {
        if (ws.current && inputText.trim()) {
            ws.current.send(inputText);
            setInputText('');
        }
    };

    const toggleListening = () => {
        if (isListening) {
            recognitionRef.current.stop();
            setIsListening(false);
        } else {
            recognitionRef.current.start();
            setIsListening(true);
        }
    };

    return (
        <div className="dashboard">
            <header className="header">
                <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
                    <Activity color="#6366f1" />
                    <h1>AI Sales Assistant</h1>
                </div>
                <div style={{ display: 'flex', gap: '1rem' }}>
                    {!isActive ? (
                        <button onClick={startCall}>Start New Call</button>
                    ) : (
                        <button style={{ background: 'var(--negative)' }} onClick={endCall}>End Call</button>
                    )}
                </div>
            </header>

            {/* Left Sidebar: Recommendations */}
            <aside className="sidebar-left">
                <div className="title"><ShoppingCart size={16} /> Product Recs</div>
                {recs.length === 0 ? (
                    <p style={{ color: 'var(--text-muted)', fontSize: '0.8rem' }}>No recommendations yet.</p>
                ) : (
                    recs.map(r => (
                        <div key={r.id} className="card recommendation-item">
                            <h4>{r.name}</h4>
                            <p style={{ fontSize: '0.8rem', margin: '0.5rem 0' }}>{r.description}</p>
                            {r.tags.map(t => <span key={t} className="tag">{t}</span>)}
                        </div>
                    ))
                )}
            </aside>

            {/* Main Content: Live Feed */}
            <main className="main-content">
                <div className="title"><MessageSquare size={16} /> Live Transcription</div>
                <div style={{ height: 'calc(100% - 150px)', overflowY: 'auto', paddingBottom: '100px' }}>
                    {messages.map((m, i) => (
                        <div key={i} className="transcript-bubble">{m}</div>
                    ))}
                    {summary && (
                        <div className="card" style={{ border: '2px dashed var(--primary)', marginTop: '2rem' }}>
                            <h3 style={{ marginBottom: '1rem', color: 'var(--primary)' }}>Post-Call Summary</h3>
                            <div style={{ whiteSpace: 'pre-wrap', lineHeight: '1.6' }}>{summary}</div>
                        </div>
                    )}
                </div>

                {isActive && (
                    <div className="input-area">
                        <Mic
                            size={20}
                            color={isListening ? "var(--negative)" : "var(--text-muted)"}
                            className={isListening ? "pulse" : ""}
                            style={{ cursor: 'pointer' }}
                            onClick={toggleListening}
                        />
                        <input
                            placeholder={isListening ? "Listening..." : "Simulate customer speech..."}
                            value={inputText}
                            onChange={(e) => setInputText(e.target.value)}
                            onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
                            disabled={isListening}
                        />
                        <button onClick={sendMessage} disabled={isListening}><Send size={16} /></button>
                    </div>
                )}
            </main>

            {/* Right Sidebar: Sentiment & Coaching */}
            <aside className="sidebar-right">
                <div className="title"><Activity size={16} /> Live Sentiment</div>
                <div className="card" style={{ textAlign: 'center', padding: '1.5rem' }}>
                    <span className={`badge badge-${sentiment.toLowerCase()}`}>
                        {sentiment}
                    </span>
                </div>

                <div className="title" style={{ marginTop: '2rem' }}><AlertCircle size={16} /> Sales Coaching</div>
                <div className="card suggestion-box">
                    {suggestion}
                </div>

                <div className="title" style={{ marginTop: '2rem' }}><PieChart size={16} /> Key Focus Areas</div>
                <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.5rem' }}>
                    {keywords.map(k => (
                        <span key={k} className="tag" style={{ background: 'var(--card)', border: '1px solid var(--primary)' }}>{k}</span>
                    ))}
                </div>
            </aside>
        </div>
    );
};

export default App;

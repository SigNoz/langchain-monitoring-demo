import './App.css';
import { useState, useRef, useEffect } from 'react';
import ReactMarkdown from "react-markdown";
import Select from 'react-select';


const cityOptions = [
  { value: "new york", label: "New York" },
  { value: "los angeles", label: "Los Angeles" },
  { value: "chicago", label: "Chicago" },
  { value: "san francisco", label: "San Francisco" },
  { value: "miami", label: "Miami" },
  { value: "paris", label: "Paris" },
  { value: "tokyo", label: "Tokyo" },
  { value: "sydney", label: "Sydney" },
  { value: "dubai", label: "Dubai" },
  { value: "london", label: "London" },
];


function App() {
  const [response, setResponse] = useState('');
  const [loading, setLoading] = useState(false);
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [departureCity, setDepartureCity] = useState(null);
  const [arrivalCity, setArrivalCity] = useState(null);
  const chatContainerRef = useRef(null);

  useEffect(() => {
    if (chatContainerRef.current) {
      chatContainerRef.current.scrollTop = chatContainerRef.current.scrollHeight;
    }
  }, [messages]);

  const handlePlanClick = async () => {
    const departure = departureCity ? departureCity.value : '';
    const arrival = arrivalCity ? arrivalCity.value : '';
    const checkin = document.getElementById('checkin').value;
    const checkout = document.getElementById('checkout').value;

    const queryParams = new URLSearchParams({
      departure,
      arrival,
      check_in: checkin,
      check_out: checkout,
    }).toString();

    setLoading(true);
    try {
      const res = await fetch(`http://localhost:8001/query?${queryParams}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      });

      const data = await res.json();
      setResponse(data.response);
      setMessages([]);
    } catch (error) {
      console.error('Error fetching data:', error);
      setResponse('An error occurred while fetching the data.');
    } finally {
      setLoading(false);
    }
  };

  const handleSendMessage = async () => {
    if (!inputValue.trim()) return;

    const newMessage = { role: 'user', content: inputValue };
    setMessages((prev) => [...prev, newMessage]);
    setInputValue('');

    try {
      const queryParams = new URLSearchParams({ query: inputValue }).toString();
      const res = await fetch(`http://localhost:8001/query?${queryParams}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      });

      const data = await res.json();
      setMessages((prev) => [
        ...prev,
        { role: 'assistant', content: data.response },
      ]);
    } catch (error) {
      console.error('Error sending message:', error);
      setMessages((prev) => [
        ...prev,
        { role: 'assistant', content: 'An error occurred while fetching the response.' },
      ]);
    }
  };

  return (
    <div className="App" style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', fontFamily: 'Arial, sans-serif', color: '#333' }}>
      <header className="App-header" style={{ width: '100%', maxWidth: '1200px', padding: '20px', boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)', borderRadius: '10px', backgroundColor: '#f9f9f9' }}>
        <h1 style={{ textAlign: 'center', color: '#000', marginBottom: '20px' }}>Trip Planning Agent</h1>
        <form style={{ textAlign: 'center', marginBottom: '20px' }}>
          <div style={{ marginBottom: '15px' }}>
            <label htmlFor="departure" style={{ display: 'block', marginBottom: '5px', fontWeight: 'bold', color: '#000' }}>Departure:</label>
            <Select
              id="departure"
              options={cityOptions}
              placeholder="Select a city"
              isSearchable
              onChange={(selectedOption) => setDepartureCity(selectedOption)}
              styles={{
                control: (base) => ({ ...base, height: '40px', fontSize: '16px' }),
                singleValue: (base) => ({ ...base, color: '#000' }),
                option: (base, state) => ({
                  ...base,
                  color: state.isSelected ? '#fff' : '#000',
                  backgroundColor: state.isSelected ? '#3498db' : '#fff',
                  fontSize: '14px', // Reduced font size for options
                }),
              }}
            />
          </div>
          <div style={{ marginBottom: '15px' }}>
            <label htmlFor="arrival" style={{ display: 'block', marginBottom: '5px', fontWeight: 'bold', color: '#000' }}>Arrival:</label>
            <Select
              id="arrival"
              options={cityOptions}
              placeholder="Select a city"
              isSearchable
              onChange={(selectedOption) => setArrivalCity(selectedOption)}
              styles={{
                control: (base) => ({ ...base, height: '40px', fontSize: '16px' }),
                singleValue: (base) => ({ ...base, color: '#000' }),
                option: (base, state) => ({
                  ...base,
                  color: state.isSelected ? '#fff' : '#000',
                  backgroundColor: state.isSelected ? '#3498db' : '#fff',
                  fontSize: '14px', // Reduced font size for options
                }),
              }}
            />
          </div>
          <div style={{ marginBottom: '15px' }}>
            <label htmlFor="checkin" style={{ display: 'block', marginBottom: '5px', fontWeight: 'bold', color: '#000' }}>Check-in Date:</label>
            <input type="date" id="checkin" name="checkin" style={{ width: '100%', height: '40px', fontSize: '16px', padding: '5px', borderRadius: '5px', border: '1px solid #ccc' }} />
          </div>
          <div style={{ marginBottom: '15px' }}>
            <label htmlFor="checkout" style={{ display: 'block', marginBottom: '5px', fontWeight: 'bold', color: '#000' }}>Check-out Date:</label>
            <input type="date" id="checkout" name="checkout" style={{ width: '100%', height: '40px', fontSize: '16px', padding: '5px', borderRadius: '5px', border: '1px solid #ccc' }} />
          </div>
          <button type="button" onClick={handlePlanClick} style={{ width: '100%', height: '40px', fontSize: '16px', borderRadius: '5px', border: 'none', backgroundColor: '#3498db', color: '#fff', cursor: 'pointer', fontWeight: 'bold' }}>Plan</button>
        </form>
        {loading && (
          <div style={{ marginTop: '20px', textAlign: 'center' }}>
            <div className="spinner" style={{ border: '4px solid #f3f3f3', borderTop: '4px solid #3498db', borderRadius: '50%', width: '40px', height: '40px', animation: 'spin 1s linear infinite', margin: '0 auto' }}></div>
          </div>
        )}
        <div style={{ display: 'flex', marginTop: '20px' }}>
          {response && (
            <div style={{ flex: 1, marginRight: '10px', padding: '15px', borderRadius: '5px', backgroundColor: '#ecf0f1', boxShadow: '0 2px 4px rgba(0, 0, 0, 0.1)' }}>
              <h2 style={{ color: '#000', marginBottom: '10px' }}>Your Trip Plan Details:</h2>
              <ReactMarkdown components={{
                p: ({ node, ...props }) => <p style={{ color: '#000', textAlign: 'left', fontSize: '18px' }} {...props} />, // Increased font size
                li: ({ node, ...props }) => <li style={{ color: '#000', textAlign: 'left', fontSize: '18px' }} {...props} />, // Increased font size
                ul: ({ node, ...props }) => <ul style={{ color: '#000', textAlign: 'left', fontSize: '18px' }} {...props} />, // Increased font size
                ol: ({ node, ...props }) => <ol style={{ color: '#000', textAlign: 'left', fontSize: '18px' }} {...props} />, // Increased font size
                strong: ({ node, ...props }) => <strong style={{ color: '#000', textAlign: 'left', fontSize: '18px' }} {...props} />, // Increased font size
                em: ({ node, ...props }) => <em style={{ color: '#000', textAlign: 'left', fontSize: '18px' }} {...props} />, // Increased font size
                blockquote: ({ node, ...props }) => <blockquote style={{ color: '#000', textAlign: 'left', fontSize: '18px' }} {...props} />, // Increased font size
                h1: ({ node, ...props }) => <h1 style={{ color: '#000', textAlign: 'left', fontSize: '18px' }} {...props} />, // Increased font size
                h2: ({ node, ...props }) => <h2 style={{ color: '#000', textAlign: 'left', fontSize: '18px' }} {...props} />, // Increased font size
                h3: ({ node, ...props }) => <h3 style={{ color: '#000', textAlign: 'left', fontSize: '18px' }} {...props} />, // Increased font size
                h4: ({ node, ...props }) => <h4 style={{ color: '#000', textAlign: 'left', fontSize: '18px' }} {...props} />, // Increased font size
                h5: ({ node, ...props }) => <h5 style={{ color: '#000', textAlign: 'left', fontSize: '18px' }} {...props} />, // Increased font size
                h6: ({ node, ...props }) => <h6 style={{ color: '#000', textAlign: 'left', fontSize: '18px' }} {...props} /> // Increased font size
              }}>{response}</ReactMarkdown>
            </div>
          )}
          {response && (
            <div style={{ flex: 1, marginLeft: '10px', padding: '15px', borderRadius: '5px', backgroundColor: '#ecf0f1', boxShadow: '0 2px 4px rgba(0, 0, 0, 0.1)' }}>
              <h2 style={{ color: '#000', marginBottom: '10px' }}>Chat with the Agent:</h2>
              <div
                ref={chatContainerRef}
                style={{ maxHeight: '70vh', overflowY: 'auto', border: '1px solid #ccc', padding: '10px', borderRadius: '5px', backgroundColor: '#fff' }}
              >
                {messages.map((msg, index) => (
                  <div key={index} style={{ marginBottom: '20px', textAlign: 'left' }}> {/* Added textAlign: 'left' for left alignment */}
                    <div style={{ fontWeight: 'bold', color: msg.role === 'user' ? '#000' : '#000', fontSize: '16px', marginBottom: '10px' }}>
                      {msg.role === 'user' ? 'You:' : 'Agent:'}
                    </div>
                    {msg.role === 'assistant' ? (
                      <ReactMarkdown components={{
                        p: ({ node, ...props }) => <p style={{ color: '#000', textAlign: 'left', fontSize: '16px' }} {...props} />, // Adjusted font size
                        li: ({ node, ...props }) => <li style={{ color: '#000', textAlign: 'left', fontSize: '16px' }} {...props} />, // Adjusted font size
                        ul: ({ node, ...props }) => <ul style={{ color: '#000', textAlign: 'left', fontSize: '16px' }} {...props} />, // Adjusted font size
                        ol: ({ node, ...props }) => <ol style={{ color: '#000', textAlign: 'left', fontSize: '16px' }} {...props} />, // Adjusted font size
                        strong: ({ node, ...props }) => <strong style={{ color: '#000', textAlign: 'left', fontSize: '16px' }} {...props} />, // Adjusted font size
                        em: ({ node, ...props }) => <em style={{ color: '#000', textAlign: 'left', fontSize: '16px' }} {...props} />, // Adjusted font size
                        blockquote: ({ node, ...props }) => <blockquote style={{ color: '#000', textAlign: 'left', fontSize: '16px' }} {...props} />, // Adjusted font size
                        h1: ({ node, ...props }) => <h1 style={{ color: '#000', textAlign: 'left', fontSize: '16px' }} {...props} />, // Adjusted font size
                        h2: ({ node, ...props }) => <h2 style={{ color: '#000', textAlign: 'left', fontSize: '16px' }} {...props} />, // Adjusted font size
                        h3: ({ node, ...props }) => <h3 style={{ color: '#000', textAlign: 'left', fontSize: '16px' }} {...props} />, // Adjusted font size
                        h4: ({ node, ...props }) => <h4 style={{ color: '#000', textAlign: 'left', fontSize: '16px' }} {...props} />, // Adjusted font size
                        h5: ({ node, ...props }) => <h5 style={{ color: '#000', textAlign: 'left', fontSize: '16px' }} {...props} />, // Adjusted font size
                        h6: ({ node, ...props }) => <h6 style={{ color: '#000', textAlign: 'left', fontSize: '16px' }} {...props} /> // Adjusted font size
                      }}>{msg.content}</ReactMarkdown>
                    ) : (
                      <div style={{ color: '#000', fontSize: '16px' }}>{msg.content}</div> // Adjusted font size
                    )}
                  </div>
                ))}
              </div>
              <div style={{ display: 'flex', marginTop: '10px' }}>
                <input
                  type="text"
                  value={inputValue}
                  onChange={(e) => setInputValue(e.target.value)}
                  placeholder="Type your message here..."
                  style={{ flex: 1, height: '40px', fontSize: '16px', padding: '0 10px', borderRadius: '5px', border: '1px solid #ccc' }}
                />
                <button
                  onClick={handleSendMessage}
                  style={{ height: '40px', fontSize: '16px', marginLeft: '10px', padding: '0 20px', borderRadius: '5px', border: 'none', backgroundColor: '#3498db', color: '#fff', cursor: 'pointer', fontWeight: 'bold' }}
                >
                  Send
                </button>
              </div>
            </div>
          )}
        </div>
      </header>
    </div>
  );
}

export default App;

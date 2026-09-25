import { useState } from 'react'
import './App.css'

function App() {
  const [message, setMessage] = useState('')
  const [messages, setMessages] = useState([
    {
      role: 'assistant',
      content:
        'Hello! Give me a GitHub repository or reconnaissance request to get started.',
    },
  ])
  const [loading, setLoading] = useState(false)

  async function sendMessage(event) {
    event.preventDefault()

    const trimmedMessage = message.trim()

    if (!trimmedMessage || loading) {
      return
    }

    setMessages((currentMessages) => [
      ...currentMessages,
      {
        role: 'user',
        content: trimmedMessage,
      },
    ])

    setMessage('')
    setLoading(true)

    try {
      const response = await fetch('http://127.0.0.1:8000/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: trimmedMessage,
        }),
      })

      if (!response.ok) {
        let errorMessage =
          `The reconnaissance backend returned an error (${response.status}).`

        try {
          const errorData = await response.json()

          if (errorData.detail) {
            errorMessage = errorData.detail
          }
        } catch {
          // Keep the default error message when the response is not JSON.
        }

        throw new Error(errorMessage)
      }

      const data = await response.json()

      setMessages((currentMessages) => [
        ...currentMessages,
        {
          role: 'assistant',
          content: data.response,
        },
      ])
    } catch (error) {
      setMessages((currentMessages) => [
        ...currentMessages,
        {
          role: 'assistant',
          content:
            error.message ||
            'I could not connect to the reconnaissance backend. Please check that the FastAPI server is running.',
        },
      ])
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="app">
      <header className="app-header">
        <div>
          <h1>GitHub Reconnaissance</h1>
          <p>AI-powered repository intelligence</p>
        </div>

        <div className="status">
          <span className="status-dot"></span>
          Backend Ready
        </div>
      </header>

      <main className="chat-container">
        <section className="welcome-card">
          <h2>GitHub Recon Chatbot</h2>
          <p>
            Analyze GitHub repositories, discover technologies, inspect APIs
            and domains, and review potential security findings.
          </p>

          <div className="example-prompts">
            <button
              type="button"
              onClick={() => setMessage('Analyze microsoft/vscode')}
            >
              Analyze microsoft/vscode
            </button>

            <button
              type="button"
              onClick={() =>
                setMessage('Find technologies in microsoft/vscode')
              }
            >
              Find technologies in a repository
            </button>

            <button
              type="button"
              onClick={() =>
                setMessage('Inspect security findings in microsoft/vscode')
              }
            >
              Inspect repository security findings
            </button>
          </div>
        </section>

        <section className="chat-box">
          <div className="messages">
            {messages.map((item, index) => (
              <div
                className={`message ${
                  item.role === 'user'
                    ? 'user-message'
                    : 'assistant-message'
                }`}
                key={`${item.role}-${index}`}
              >
                <strong>
                  {item.role === 'user' ? 'You' : 'Recon Assistant'}
                </strong>
                <p>{item.content}</p>
              </div>
            ))}

            {loading && (
              <div className="message assistant-message">
                <strong>Recon Assistant</strong>
                <p>Analyzing your request...</p>
              </div>
            )}
          </div>

          <form className="chat-input" onSubmit={sendMessage}>
            <input
              type="text"
              value={message}
              onChange={(event) => setMessage(event.target.value)}
              placeholder="Ask about a GitHub repository..."
              aria-label="Chat message"
              disabled={loading}
            />

            <button type="submit" disabled={loading || !message.trim()}>
              {loading ? 'Sending...' : 'Send'}
            </button>
          </form>
        </section>
      </main>
    </div>
  )
}

export default App
import React, { useState, useEffect } from 'react';
import {useTypingSession} from '../../hooks/useTypingSession'
import TypingEngine from './TypingEngine';
import TypingStats from './TypingStats';

const TypingSession = ({
  text,
  onComplete,
  autoStart = false,
  showStats = true,
  sessionOptions = {},
  ...engineProps
}) => {
  const [sessionStarted, setSessionStarted] = useState(autoStart);
  
  const {
    sessionId,
    isSessionActive,
    isStarted,
    isComplete,
    stats,
    currentWPM,
    currentAccuracy,
    totalErrors,
    startSession,
    reset,
    getSessionStats,
    handleKeyPress,
    sessionData
  } = useTypingSession(text, {
    onSessionComplete: onComplete,
    onSessionStart: () => setSessionStarted(true),
    ...sessionOptions
  });

  // Auto-iniciar si está configurado
  useEffect(() => {
    if (autoStart && !sessionStarted) {
      startSession();
    }
  }, [autoStart, sessionStarted, startSession]);

  return (
    <div className="typing-session">
      <div className="session-header">
        <h3>Sesión de Transcripción</h3>
        <div className="session-id">ID: {sessionId}</div>
        <div className="session-status">
          Estado: {isComplete ? 'Completada' : isSessionActive ? 'En progreso' : 'Inactiva'}
        </div>
      </div>

      {!sessionStarted && !autoStart && (
        <div className="session-controls">
          <button onClick={startSession} className="start-button">
            Iniciar Sesión
          </button>
        </div>
      )}

      {sessionStarted && (
        <>
          <TypingEngine
            text={text}
            onComplete={(data) => {
              // El hook maneja la completación
            }}
            onError={(error) => {
              console.debug('Typing error:', error);
            }}
            onProgress={(progress) => {
              // Actualizar progreso
            }}
            showStats={false}
            {...engineProps}
          />

          {showStats && (
            <div className="session-stats">
              <TypingStats
                stats={getSessionStats()}
                isComplete={isComplete}
                isStarted={isStarted}
                showDetailed={true}
              />
              
              <div className="session-metrics">
                <div className="metric">
                  <label>Velocidad actual:</label>
                  <span>{currentWPM} WPM</span>
                </div>
                <div className="metric">
                  <label>Precisión actual:</label>
                  <span>{currentAccuracy}%</span>
                </div>
                <div className="metric">
                  <label>Errores totales:</label>
                  <span>{totalErrors}</span>
                </div>
                <div className="metric">
                  <label>Intentos:</label>
                  <span>{sessionData.attempts}</span>
                </div>
              </div>
            </div>
          )}

          <div className="session-controls">
            <button onClick={reset} className="reset-button">
              Reiniciar Sesión
            </button>
            <button onClick={() => startSession()} className="restart-button">
              Nueva Sesión
            </button>
          </div>
        </>
      )}

      <style jsx>{`
        .typing-session {
          padding: 20px;
          background: white;
          border-radius: 12px;
          box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }

        .session-header {
          display: flex;
          justify-content: space-between;
          align-items: center;
          margin-bottom: 20px;
          padding-bottom: 10px;
          border-bottom: 2px solid #f0f0f0;
        }

        .session-header h3 {
          margin: 0;
          color: #333;
        }

        .session-id {
          font-size: 0.8rem;
          color: #999;
        }

        .session-status {
          padding: 4px 12px;
          border-radius: 12px;
          font-size: 0.8rem;
          font-weight: 500;
        }

        .session-controls {
          display: flex;
          justify-content: center;
          gap: 12px;
          margin-top: 20px;
        }

        .start-button {
          padding: 10px 32px;
          background: #007bff;
          color: white;
          border: none;
          border-radius: 8px;
          font-size: 1rem;
          cursor: pointer;
          transition: background 0.2s;
        }

        .start-button:hover {
          background: #0056b3;
        }

        .reset-button {
          padding: 8px 24px;
          background: #6c757d;
          color: white;
          border: none;
          border-radius: 6px;
          cursor: pointer;
          transition: background 0.2s;
        }

        .reset-button:hover {
          background: #5a6268;
        }

        .restart-button {
          padding: 8px 24px;
          background: #28a745;
          color: white;
          border: none;
          border-radius: 6px;
          cursor: pointer;
          transition: background 0.2s;
        }

        .restart-button:hover {
          background: #218838;
        }

        .session-stats {
          margin-top: 20px;
          padding: 20px;
          background: #f8f9fa;
          border-radius: 8px;
        }

        .session-metrics {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
          gap: 12px;
          margin-top: 16px;
        }

        .metric {
          display: flex;
          flex-direction: column;
          padding: 10px;
          background: white;
          border-radius: 6px;
          box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        }

        .metric label {
          font-size: 0.8rem;
          color: #666;
          margin-bottom: 4px;
        }

        .metric span {
          font-size: 1.2rem;
          font-weight: 600;
          color: #333;
        }
      `}</style>
    </div>
  );
};

export default TypingSession;

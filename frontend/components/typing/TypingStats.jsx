import React from 'react';

const TypingStats = ({ 
  stats,
  isComplete,
  isStarted,
  showDetailed = false,
  className = ''
}) => {
  if (!isStarted) {
    return (
      <div className={`typing-stats ${className}`}>
        <div className="stats-placeholder">
          Presiona cualquier tecla para comenzar
        </div>
      </div>
    );
  }

  const {
    accuracy = 100,
    wpm = 0,
    charactersTyped = 0,
    correctCharacters = 0,
    errorCount = 0,
    elapsedTime = 0,
    progress = 0
  } = stats;

  // Formatear tiempo
  const formatTime = (ms) => {
    const seconds = Math.floor(ms / 1000);
    const minutes = Math.floor(seconds / 60);
    const remainingSeconds = seconds % 60;
    return `${minutes}:${remainingSeconds.toString().padStart(2, '0')}`;
  };

  // Obtener barra de precisión
  const accuracyBar = () => {
    const color = accuracy >= 90 ? '#28a745' : accuracy >= 70 ? '#ffc107' : '#dc3545';
    return (
      <div className="accuracy-bar-container">
        <div 
          className="accuracy-bar"
          style={{
            width: `${accuracy}%`,
            backgroundColor: color,
            transition: 'width 0.3s ease'
          }}
        />
      </div>
    );
  };

  // Obtener barra de progreso
  const progressBar = () => {
    return (
      <div className="progress-bar-container">
        <div 
          className="progress-bar"
          style={{
            width: `${Math.min(progress, 100)}%`,
            backgroundColor: isComplete ? '#28a745' : '#007bff',
            transition: 'width 0.3s ease'
          }}
        />
      </div>
    );
  };

  return (
    <div className={`typing-stats ${className}`}>
      <div className="stats-grid">
        <div className="stat-item">
          <label>Precisión</label>
          <div className="stat-value">{accuracy}%</div>
          {accuracyBar()}
        </div>

        <div className="stat-item">
          <label>Velocidad</label>
          <div className="stat-value">{wpm} <span className="unit">WPM</span></div>
        </div>

        <div className="stat-item">
          <label>Tiempo</label>
          <div className="stat-value">{formatTime(elapsedTime)}</div>
        </div>

        <div className="stat-item">
          <label>Caracteres</label>
          <div className="stat-value">
            {correctCharacters}/{charactersTyped}
            <span className="unit"> correctos</span>
          </div>
        </div>

        {errorCount > 0 && (
          <div className="stat-item error">
            <label>Errores</label>
            <div className="stat-value">{errorCount}</div>
          </div>
        )}

        <div className="stat-item progress">
          <label>Progreso</label>
          <div className="stat-value">{Math.round(progress)}%</div>
          {progressBar()}
        </div>

        {isComplete && (
          <div className="stat-item complete">
            <div className="completion-badge">✅ Completado</div>
          </div>
        )}
      </div>

      {showDetailed && stats.summary && (
        <div className="detailed-stats">
          <h4>Resumen Detallado</h4>
          <div className="summary-grid">
            <div className="summary-item">
              <span>Promedio WPM:</span>
              <strong>{stats.summary.averageWPM || 0}</strong>
            </div>
            <div className="summary-item">
              <span>Pico WPM:</span>
              <strong>{stats.summary.peakWPM || 0}</strong>
            </div>
            <div className="summary-item">
              <span>Precisión promedio:</span>
              <strong>{stats.summary.averageAccuracy || 0}%</strong>
            </div>
            <div className="summary-item">
              <span>Consistencia:</span>
              <strong>{stats.summary.consistency || 0}%</strong>
            </div>
            <div className="summary-item">
              <span>Total caracteres:</span>
              <strong>{stats.summary.totalCharacters || 0}</strong>
            </div>
            <div className="summary-item">
              <span>Muestras:</span>
              <strong>{stats.summary.samples || 0}</strong>
            </div>
          </div>
        </div>
      )}

      <style jsx>{`
        .typing-stats {
          padding: 12px;
          background: white;
          border-radius: 8px;
        }

        .stats-placeholder {
          text-align: center;
          color: #6c757d;
          font-size: 0.9rem;
          padding: 10px;
        }

        .stats-grid {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
          gap: 12px;
        }

        .stat-item {
          padding: 8px;
          background: #f8f9fa;
          border-radius: 6px;
          text-align: center;
        }

        .stat-item label {
          display: block;
          font-size: 0.7rem;
          color: #6c757d;
          margin-bottom: 4px;
          text-transform: uppercase;
          letter-spacing: 0.5px;
        }

        .stat-value {
          font-size: 1.2rem;
          font-weight: 600;
          color: #333;
        }

        .stat-value .unit {
          font-size: 0.7rem;
          font-weight: 400;
          color: #6c757d;
          margin-left: 2px;
        }

        .stat-item.error .stat-value {
          color: #dc3545;
        }

        .stat-item.complete {
          background: #e6f4ea;
        }

        .completion-badge {
          font-size: 0.9rem;
          font-weight: 500;
          color: #1e8e3e;
        }

        .accuracy-bar-container,
        .progress-bar-container {
          width: 100%;
          height: 4px;
          background: #e9ecef;
          border-radius: 2px;
          overflow: hidden;
          margin-top: 4px;
        }

        .accuracy-bar,
        .progress-bar {
          height: 100%;
          border-radius: 2px;
          transition: width 0.3s ease;
        }

        .detailed-stats {
          margin-top: 16px;
          padding-top: 16px;
          border-top: 1px solid #e9ecef;
        }

        .detailed-stats h4 {
          margin: 0 0 12px 0;
          font-size: 0.9rem;
          color: #495057;
        }

        .summary-grid {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
          gap: 8px;
        }

        .summary-item {
          display: flex;
          justify-content: space-between;
          padding: 4px 8px;
          background: #f8f9fa;
          border-radius: 4px;
          font-size: 0.85rem;
        }

        .summary-item span {
          color: #6c757d;
        }

        .summary-item strong {
          color: #333;
        }

        @media (max-width: 600px) {
          .stats-grid {
            grid-template-columns: repeat(2, 1fr);
            gap: 8px;
          }
          
          .stat-value {
            font-size: 1rem;
          }
        }
      `}</style>
    </div>
  );
};

export default TypingStats;

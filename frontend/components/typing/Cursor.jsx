import React from 'react';

const Cursor = ({ 
  position, 
  isBlinking = true,
  color = '#007bff',
  height = '1.2em',
  width = '2px'
}) => {
  return (
    <span 
      className={`cursor ${isBlinking ? 'blinking' : ''}`}
      style={{
        position: 'absolute',
        left: `${position * 0.6}em`,
        top: 0,
        height,
        width,
        backgroundColor: color,
        display: 'inline-block'
      }}
    >
      <style jsx>{`
        .cursor {
          transition: left 0.1s ease;
          pointer-events: none;
        }
        
        .cursor.blinking {
          animation: blink 1s step-end infinite;
        }
        
        @keyframes blink {
          0%, 50% { opacity: 1; }
          50.1%, 100% { opacity: 0; }
        }
      `}</style>
    </span>
  );
};

export default Cursor;

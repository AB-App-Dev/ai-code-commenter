// This is a functional component for a button
export const Button = ({ label, onClick, disabled }) => {  // Define the Button Component as a function with props
  return (                                                  // Start of JSX to be returned
    <button onClick={onClick} disabled={disabled}>          // A button element that listens for click events and can be disabled
      {label}                                                // The inner text or label of the Button, received as a prop
    </button>                                                 // End of JSX to be returned
  );                                                         // Close the return statement
};                                                          // End of Function Component